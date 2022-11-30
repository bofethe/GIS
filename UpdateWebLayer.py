import arcgis
import arcpy

### TODO Define the web layer to update ###
webLayerURL = 'https://services.arcgis.com/rD2ylXRs80UroD90/arcgis/rest/services/test5/FeatureServer/0'
newLayerPath = r'C:\Users\bfethe\Desktop\Temp\GIS\Test\e2357855-bace-4c36-95bb-b6d9039ada43.gdb\Test'

# Initiate the gis object
print('Authenticating using ArcGIS Pro')
gis = arcgis.GIS('Pro')

# Truncate the original web layer
print('Truncating layer...')
arcpy.management.TruncateTable(webLayerURL)

# Add missing fields from local layer to web layer, if applicable
print('Checking for new fields to add to web layer')
webFields = arcpy.ListFields(webLayerURL)
newFields = arcpy.ListFields(newLayerPath)
webFieldNames = []
newFieldNames = []

for f in webFields:
    webFieldNames.append(f.name)

for f in newFields:
    newFieldNames.append(f.name)
    if f.name not in webFieldNames and f.required == False:
        print('\tAdding field [{}: {}] to web layer'.format(f.name, f.type))
        arcpy.management.AddField(in_table=webLayerURL,
                                    field_name=f.name,
                                    field_type=f.type)

for f in webFields:
    if f.name not in newFieldNames and f.required == False:
        print('\tRemoving field {} from web layer'.format(f.name))
        arcpy.management.DeleteField(in_table=webLayerURL,
                                    drop_field=f.name)

# Append new data to original web layer
print('Appending new data to web layer...')
arcpy.management.Append(newLayerPath, webLayerURL, schema_type='NO_TEST')

print('\nDone!')