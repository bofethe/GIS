### This script merges all layers in an ArcGIS Pro aprx into a single table

import arcpy
import time
import os

tic = time.time()

### TODO Define the aprx path, map's name, and where you want to save the files
aprxpath = r"C:\Users\bfethe\Desktop\Work From Home\MCSAW\MCSAW_TEST.aprx"
mapname = 'Map'
workspacePath = r'C:\Users\bfethe\Desktop\Work From Home\MCSAW'

### connect to the map
aprx = arcpy.mp.ArcGISProject(aprxpath)
m = aprx.listMaps(mapname)[0]

### Set your workspace
today = time.strftime('%Y%m%d%H%M')
gdbName = 'Merger_' + today + '.gdb'
arcpy.CreateFileGDB_management(out_folder_path=workspacePath, out_name=gdbName)
arcpy.env.workspace = os.path.join(workspacePath, gdbName)

### Export the tables to a new geodatabase
print('Exporting tables...')
for lyr in m.listLayers():
    print('Found: {}'.format(lyr.name))

    ### Export table without attachments and keep the GUIDs
    with arcpy.EnvManager(maintainAttachments="NOT_MAINTAIN_ATTACHEMENTS", preserveGlobalIds=True):
        arcpy.ExportTable_conversion(in_table=lyr,
                                        out_table=arcpy.ValidateTableName(lyr.name))


### Add layer name for tracking
print('Adding layer source info...')
for table in arcpy.ListTables():
    trackerFieldName = 'LayerName'

    ### Make a tracker field if not already there, skip otherwise
    try:
        arcpy.management.AddField(in_table=table,
                                field_name= trackerFieldName, 
                                field_type="TEXT", 
                                field_length= 50)
    except:
        pass

    ### Add field name to tracker field
    arcpy.management.CalculateField(in_table=table,
                                    field=trackerFieldName,
                                    expression="'{}'.format(table)", 
                                    expression_type='PYTHON3')

print('Merging tables...')
### Merge all tables together with source field
arcpy.management.Merge(inputs=';'.join(arcpy.ListTables()), 
                        output='MergedTable_ALL')


print('Getting only relevant fields...')
arcpy.conversion.TableToTable(in_rows="MergedTable_ALL", 
                            out_path=arcpy.env.workspace, 
                            out_name="MergeTable_SELECT", 
                            field_mapping='StationName "Station Name" true true false 50 Text 0 0,First,#,MergedTable,StationName,0,50;\
                                        TravelDirection "Travel Direction" true true false 50 Text 0 0,First,#,MergedTable,TravelDirection,0,50;\
                                        Functionality "Functionality" true true false 50 Text 0 0,First,#,MergedTable,Functionality,0,50;\
                                        Comments "Comments" true true false 125 Text 0 0,First,#,MergedTable,Comments,0,125;\
                                        AssessmentScore "Assessment Score" true true false 8 Double 0 0,First,#,MergedTable,AssessmentScore,-1,-1;\
                                        AssessmentCondition "Assessment Condition" true true false 50 Text 0 0,First,#,MergedTable,AssessmentCondition,0,50;\
                                        LayerName "LayerName" true true false 50 Text 0 0,First,#,MergedTable,LayerName,0,50')


toc = time.time()

print('\nDone!\nTotal processing time in minutes: {}:{}'.format(int((toc-tic)//60), round((toc-tic)%60,2)))