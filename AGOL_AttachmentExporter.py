import arcpy
from arcpy import da
import os

# gdb attachment table path
gdbpath = input('Enter the path to the geodatabase containing the attachments: ')
fcname = input('Enter the name of the feature class with the attachments: ')
fcPath = gdbpath + '\\' + fcname
inTable = gdbpath + '__ATTACH'

# output folder path
outputFolder = input('Enter the folder path to save the attachments in: ')


# Names of fields you want the attachment to be
field1 = input('Enter the attribute field name containing the desired filenames: ')

with da.SearchCursor(fcPath, ['OBJECTID', field1]) as fc:
    nameDic = {}
    for entry in fc:
        nameDic[entry[0]] = str(entry[1])

with da.SearchCursor(inTable, ['DATA', 'REL_OBJECTID']) as cursor:
    outputList = []
    for item in cursor:
        attachment = item[0]
        filename = nameDic[item[1]]
        while filename in outputList:
            filename = filename + '_'

        open(outputFolder + os.sep + filename + '.jpg', 'wb').write(attachment.tobytes())
        outputList.append(filename)
        print('Exported: ', filename)