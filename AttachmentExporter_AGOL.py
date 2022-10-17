from arcgis.gis import GIS
import pandas as pd
import os
import time


### TODO Pass your credentials as strings.
### If using AGOL, leave portalURL as None; otherwise, update ###
username = 'Owen Wilson'
password = 'Wow'
portalURL = None

### TODO Define the web layer with attachments ###
featureName = 'eSTORM_Devices_New - D1'

### TODO Define the root outpath. Subfolders will be created
out_path = r'C:\Users\bfethe\Desktop\Temp\eStorm'

# Initiate the gis and map object
gis = GIS(portalURL, username, password)
mapp = gis.map('Florida')

# Access the layer and show it on a map
searchResults = gis.content.search(featureName, 'Feature Layer')
data = searchResults[0].layers[0]
mapp.add_layer(data)
mapp.zoom_to_layer(data)

# Get list of objectIDs with attachments
attachmentList = data.attachments\
                    .search(as_df=True)['PARENTOBJECTID']\
                    .drop_duplicates()\
                    .to_list()

# get attribute field names
fieldList = []
for field in data.properties.fields:
    fieldList.append(field['name'])

# Map OBJECTID to a unique and UNIX-ready site name based on the on/at street combo
df = data.query().sdf
df['uniqueID'] = df['On_Street_Name'] + ' at ' + df['At_Street_Name']
df['uniqueID'] = df['uniqueID'].str.replace(r'/', ' ')
dict_ids = df[df['OBJECTID'].isin(attachmentList)]\
            .set_index('OBJECTID')\
            .to_dict()['uniqueID']

# Download the attachments
now = time.strftime('%Y%m%d_%H%M')

tic = time.time()
for i in attachmentList:
    siteID = dict_ids[i]
    data.attachments.download(oid = i, save_path = out_path + r'/' + now + r'/' + siteID)
toc = time.time()

print('Finished. Total elapsed time is {} seconds \n'.format(toc - tic))
