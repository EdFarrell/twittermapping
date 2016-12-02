import os
import arcpy

# ensure that your output is overwritten to avoid conflicts
arcpy.env.overwriteOutput = True

# set your workspace
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
