### This script merges all layers in an ArcGIS Pro aprx into a single table

import arcpy
import time
import os

# TODO Define the aprx path, map's name, and where you want to save the files
aprxpath = r'C:\Users\bfethe\Desktop\Temp\GIS\Temp.aprx'
mapname = 'Map'
workspacePath = r'C:\Users\bfethe\Desktop\Temp\GIS'

# connect to the map
aprx = arcpy.mp.ArcGISProject(aprxpath)
m = aprx.listMaps(mapname)[0]

# Set your workspace
today = time.strftime('%Y%m%d%H%M')
gdbName = 'Merger_' + today + '.gdb'
arcpy.CreateFileGDB_management(out_folder_path=workspacePath, out_name=gdbName)
arcpy.env.workspace = os.path.join(workspacePath, gdbName)

# Export the tables to a new geodatabase
for lyr in m.listLayers():
    #Export table
    print(lyr)
    arcpy.ExportTable_conversion(in_table=lyr,
                                    out_table=lyr.name)

# Add layer name for tracking
for table in arcpy.ListTables():
    trackerFieldName = 'LayerName'

    #Make a tracker field if not already there, skip otherwise
    try:
        arcpy.management.AddField(in_table=table,
                                field_name= trackerFieldName, 
                                field_type="TEXT", 
                                field_length= 50)
    except:
        pass

    # Add field name to tracker field
    arcpy.management.CalculateField(in_table=table,
                                    field=trackerFieldName,
                                    expression="'{}'.format(table)", 
                                    expression_type='PYTHON3')


# Merge all tables together with source field
arcpy.management.Merge(inputs=';'.join(arcpy.ListTables()), 
                        output='MergedTable')