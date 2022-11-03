import arcgis
import arcpy

### TODO Define the web layer to update ###
webLayerURL = 'https://services1.arcgis.com/O1JpcwDW8sjYuddV/arcgis/rest/services/Test5/FeatureServer/0'
newLayerPath = r'C:\Users\bfethe\Desktop\Temp\GIS\Test\e2357855-bace-4c36-95bb-b6d9039ada43.gdb\Test'

# Initiate the gis object
print('Authenticating using ArcGIS Pro')
gis = arcgis.GIS('Pro')

# Truncate the original web layer
print('Truncating layer...')
arcpy.management.TruncateTable(webLayerURL)

# Append new data to original web layer
print('Appending new data to web layer...')
arcpy.management.Append(newLayerPath, webLayerURL, schema_type='TEST')