# SCRIPT 3 OF 3

# SCRIPT ARE DIVIDED INTO WORKFLOW, INPUT AND ANALYSIS PART
#WORKFLOW gives the detail of what the script does
#INPUT part gives control over naming, chosing workspace and argument
#ANALYSIS part just uses the arcgis function and perform analysis

########WORKFLOW ##########
## 1. Creates a fishnet of specified size to make a zone layer in the shape of study area
## 2. Classify the final HSI raster obtained from script2 to various levels of suitability for rain garden
## 3. Obtain the area of each classification in each fishnet zones
## 4. Based on maximum value of the area specify a label to the area
## 5. Join the obtained result to the final area.



#########INPUTS #############

### Use this line below to stop adding the object to map document everytime it is created
arcpy.env.addOutputsToMap = False

wspc = r'F:\WORK\GSI_Project\reapeat2\final_final_try'  ## save the workspace path in a variable
arcpy.env.workspace = wspc ##Setup the workspace
reclassify = 'reclssfied_z'  ## This will be the name of the file that you reclassify
summtab = 'summ_tab_z'  ### This will be the name of summary table
fc = "prj_py_h12"        ### This is the study area projected feature class that will be used for clipping
gdb = "mygdb_z.gdb"  ## This is the gdb that will be created
sens = "sensit_tab_z" ## This is the final sensitivity table that will be created

rast = arcpy.Raster(wspc+"\\"+'fin_hsi_ar') ## This is the HSI raster that have already filtered the relevant area (output from previous script)
mini = rast.minimum ##need this in the classification ## just so the code is as automated as possible
maxi = rast.maximum ##need this in classification

args = "{} 4.61 0;4.61 8.16 1;8.16 11.77 2;11.77 15.67 3; 15.67 {} 4".format(mini, maxi)  ## This is how the HSI raster will be classified

fish_nem = "fs_200_c2_zn.shp" ### What is the name of the fishnet file?
wd = "100" ## what should be the width of the fishnet
ht = "100" ### What should be the height of the fishnet
zones = 'pfsh_c200_clpzn.shp' ## This will be my zone layer ### This is also the layer obtained after cliping the fishnet output to the study area

desc = arcpy.Describe(fc) ## This is necessary to obtain the parameter like coordinates of the study area (this goes as argument in fishnet creation)

cmp_HSI = 'composite_HSI'  ### This is for composite HSI based on the mean
recls_cmp = "cmp_rcls_HSI"

######### ANALYSIS #######

## This will create the fishnet

arcpy.CreateFishnet_management(fish_nem,str(desc.extent.lowerLeft),str(desc.extent.XMin) + " " + str(desc.extent.YMax + 10),wd,ht,"0","0",str(desc.extent.upperRight),"NO_LABELS","#","POLYGON")
arcpy.DefineProjection_management(wspc+"\\"+fish_nem, "PROJCS['NAD_1983_HARN_StatePlane_Washington_South_FIPS_4602_Feet',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1640416.666666667],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',45.83333333333334],PARAMETER['Standard_Parallel_2',47.33333333333334],PARAMETER['Latitude_Of_Origin',45.33333333333334],UNIT['Foot_US',0.3048006096012192]]")

arcpy.Clip_analysis(wspc+"\\"+fish_nem, fc, zones, '#') ## Clip it to the size of study area


## First classify the raster into several groups

arcpy.gp.Reclassify_sa(rast, 'VALUE', args, reclassify, 'DATA')

## Tabulate area

myoid = arcpy.Describe(wspc+"\\"+zones).OIDFieldName
arcpy.gp.TabulateArea_sa(wspc+"\\"+zones, myoid, reclassify, 'Value', summtab, reclassify)

##### This section will calculate the composite HSI for a study area
### Basically a mean calculation and making a broader HSI

arcpy.gp.ZonalStatistics_sa(wspc+"\\"+zones, 'FID', rast, wspc+"\\"+cmp_HSI, 'MEAN', 'DATA')  ### if FID doesnt work you can use myoid from previos function.
arcpy.gp.Reclassify_sa(rast, 'VALUE', args, reclassify, 'DATA')
### Analyzing attribute table

import pandas as pd
import numpy as np
my = arcpy.da.TableToNumPyArray(wspc+"\\"+summtab, (myoid, "VALUE_0","VALUE_1","VALUE_2","VALUE_3","VALUE_4"))

ana = pd.DataFrame(my)

ana["tot"]=ana[["VALUE_0","VALUE_1","VALUE_2","VALUE_3","VALUE_4"]].sum(axis=1)

ana['p0']=(ana['VALUE_0']/ana['tot'])*100
ana['p1']=(ana['VALUE_1']/ana['tot'])*100
ana['p2']=(ana['VALUE_2']/ana['tot'])*100
ana['p3']=(ana['VALUE_3']/ana['tot'])*100
ana['p4']=(ana['VALUE_4']/ana['tot'])*100

def cont(lec):
...     a = np.argmax(lec)  ## find the argument with maximum value and assign a label to it
...     if a == "p0":
...         b = "Least Priority"
...     elif a == "p1":
...         b = "High Priority"
...     elif a == "p2":
...         b = "Highest Priority"
...     elif a == "p3":
...         b = "Moderate Priority"
...     else:
...         b = "Least Priority"
...     return b

ana['Sensitivity'] = ana[["p0","p1","p2","p3","p4"]].apply(cont, axis = 1)


#### note: i ran into a problem here
#### arcpy wouldnt let me change my dataframe to correct kind of numpy array to use arcpy.da.NumpyArrayToTable() to convert my data to table
#### The problem seems to be in the fact that the object type of the "Sensitivity" Colomn is stores as "object" and not as "string"
#### upon research this thread helped figure out the solution   https://community.esri.com/t5/python-questions/arcpy-da-numpyarraytotable-returns-quot-runtimeerror-create/td-p/756281

x = ana.reset_index()
z = np.rec.fromrecords(x.values, names = x.columns.tolist())
arcpy.CreateFileGDB_management(wspc, gdb)
arcpy.da.NumPyArrayToTable(z, wspc+"\\"+gdb+"\\"+sens)
### Now join this table
### When the joining layer and table is not in the arcmap window join is a little complicated
### follow this link for more detail >>>>>>> https://gis.stackexchange.com/questions/247259/using-addjoin-in-arcpy


inFeatures = wspc+"\\"+zones  ### layer you want to join from
lnm = "myfeat_zn" ### local layer name
arcpy.MakeFeatureLayer_management(inFeatures, lnm) ## make a feature layer from feature class
arcpy.AddJoin_management(lnm, "FID", wspc+"\\"+gdb+"\\"+sens, "FID", 'KEEP_ALL') ## join
output = "jnt_finale_zn" ## want new output from this
arcpy.CopyFeatures_management(lnm, output) ## copy features
arcpy.RemoveJoin_management (lnm) ## remove the join for finality










