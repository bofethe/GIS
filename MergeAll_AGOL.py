### This script merges all layers in an ArcGIS Online into a single table

import arcpy
import arcgis
import time
import os

### TODO Define the aprx path, map's name, and where you want to save the files
webLayerURL = 'https://services1.arcgis.com/O1JpcwDW8sjYuddV/arcgis/rest/services/MCSAW_Dashboard_View/FeatureServer'
workspacePath = r'C:\Users\bfethe\Desktop\Work From Home\MCSAW'

### connect to the map
gis = arcgis.GIS('Pro')

### Set your workspace
today = time.strftime('%Y%m%d%H%M')
gdbName = 'Merger_' + today + '.gdb'
arcpy.CreateFileGDB_management(out_folder_path=workspacePath, out_name=gdbName)
arcpy.env.workspace = os.path.join(workspacePath, gdbName)

### Export the tables to a new geodatabase
print('Exporting tables...')
for lyr in arcgis.L():
    print(lyr.name)
#     ### Export table without attachments and keep the GUIDs
#     with arcpy.EnvManager(maintainAttachments="NOT_MAINTAIN_ATTACHEMENTS", preserveGlobalIds=True):
#         arcpy.ExportTable_conversion(in_table=lyr,
#                                         out_table=arcpy.ValidateTableName(lyr.name))


# ### Add layer name for tracking
# print('Adding layer source info...')
# for table in arcpy.ListTables():
#     trackerFieldName = 'LayerName'

#     ### Make a tracker field if not already there, skip otherwise
#     try:
#         arcpy.management.AddField(in_table=table,
#                                 field_name= trackerFieldName, 
#                                 field_type="TEXT", 
#                                 field_length= 50)
#     except:
#         pass

#     ### Add field name to tracker field
#     arcpy.management.CalculateField(in_table=table,
#                                     field=trackerFieldName,
#                                     expression="'{}'.format(table)", 
#                                     expression_type='PYTHON3')

# print('Merging tables...')
# ### Merge all tables together with source field
# arcpy.management.Merge(inputs=';'.join(arcpy.ListTables()), 
#                         output='MergedTable')