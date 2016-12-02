import os
import urllib
import arcpy
import tweepy
from tweepy import OAuthHandler

make_spatial = False

##########################################################################
##########################################################################
##########################################################################
##########################################################################
## Part 1 - Make Twitter request and process

# tweepy settings
consumer_key = 'xxxx'
consumer_secret = 'xxxx'
access_token = 'xxxxx'
access_secret = 'xxxxx'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# build and make our queries
queries = [urllib.quote_plus("#appgis"),]
page_count = 0
tweet_count = 0
max_tweets = 1000
tweet_recorder = []  # A list to hold the all of the tweets

for query in queries:
    for tweets in tweepy.Cursor(api.search, q=query, count=100,result_type="recent", include_entities=True).pages():
        for tweet in tweets:
            tweet_count += 1
            tweet_rec = {}  #empty dictionary. This will hold the tweet components
            tweet_rec['Date'] = tweet.created_at
            tweet_rec['Search'] = urllib.unquote_plus(query)
            tweet_rec['Username'] = tweet.user.name
            tweet_rec['Screenname'] = tweet.user.screen_name
            tweet_rec['Tweet'] = tweet.text
            tweet_rec['TweetURL'] = 'https://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id_str

            if tweet.geo:
                print('geo: ', tweet.geo)
                tweet_rec['X'] = tweet.geo['coordinates'][1]
                tweet_rec['Y'] = tweet.geo['coordinates'][0]
                tweet_rec['LocType'] = 'geo'
                tweet_recorder.append(tweet_rec)
            elif tweet.place:
                print('place coords: ', tweet.place.bounding_box.coordinates)
                lencoords = len(tweet.place.bounding_box.coordinates[0])
                sumX = 0; sumY = 0
                for val in tweet.place.bounding_box.coordinates[0]:
                    sumX = sumX + val[1]
                    sumY = sumY + val[0]
                tweet_rec['X'] = sumX/lencoords
                tweet_rec['Y'] = sumY/lencoords
                tweet_rec['LocType'] = 'place'
                tweet_recorder.append(tweet_rec)

        page_count += 1
        if tweet_count > max_tweets:
            break

print('tweet recorder: ', tweet_recorder)

##########################################################################
##########################################################################
##########################################################################
##########################################################################
## Part 2 - Make your fgdb and feature class

if make_spatial:
    arcpy.env.overwriteOutput = True
    # arcpy.env.workspace = r'C:\Users\Edward\Google Drive\AppsGIS_Spring2016\Labs\TwitterMapping\Data'
    arcpy.env.workspace = r'C:\Users\Edward\Desktop\Data'
    # your file geodatabase path
    fgdb_name = 'Twitter.gdb'
    fgdb = os.path.join(arcpy.env.workspace, fgdb_name) # this function concatenates the paths together
    print('FGDB path: ', fgdb)
    # your feature class path
    fc_name = 'tweets'
    fc = os.path.join(fgdb, fc_name)
    geometry_type = "POINT"
    spatial_reference = arcpy.SpatialReference(3857) # 4326 is the EPSG code for WGS 1984 Web Mercator
    # The fields for your feature class
    fields = [
        ['Date', 'TEXT'],
        ['Search', 'TEXT'],
        ['Username', 'TEXT'],
        ['Screenname', 'TEXT'],
        ['Tweet', 'TEXT'],
        ['TweetURL','TEXT'],
        ['X', 'DOUBLE'],
        ['Y', 'DOUBLE'],
        ['LocType', 'TEXT'],
    ]

    # Create the file geodatabase
    if arcpy.Exists(fgdb):
        # delete the existing geodadatabse if it exists
        arcpy.Delete_management(fgdb)
    arcpy.CreateFileGDB_management(arcpy.env.workspace, fgdb_name)
    # Create the feature class
    arcpy.CreateFeatureclass_management(fgdb, fc_name, geometry_type, "", "DISABLED", "DISABLED", spatial_reference)

    # Iterate through the field to create the fields in the feature class
    for field in fields:
        arcpy.AddField_management(fc, field[0], field[1])

    # Add your data

    # Open an InsertCursor
    cursor = arcpy.da.InsertCursor(fc, ['Date', 'Search', 'Username', 'Screenname',
                                        'Tweet', 'TweetURL', 'X', 'Y', 'LocType',
                                        'SHAPE@XY'])

    for twt in tweet_recorder:
        row = (twt['Date'], twt['Search'], twt['Username'], twt['Screenname'], twt['Tweet'],
             twt['TweetURL'], twt['X'], twt['Y'], twt['LocType'], (twt['X'], twt['Y']),)
        cursor.insertRow(row)

    # Delete cursor object
    del cursor