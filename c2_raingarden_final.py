# SCRIPT 2 OF 3

# SCRIPT ARE DIVIDED INTO WORKFLOW, INPUT AND ANALYSIS PART
#WORKFLOW gives the detail of what the script does
#INPUT part gives control over naming, chosing workspace and argument
#ANALYSIS part just uses the arcgis function and perform analysis


########### WORKFLOW #######

### Now This script will take in all the necessary shape files
### 1. perform a union of unsuitable areas
### 2. Remove it from the HSI LAYER
### 3. Reclassify the ksat, modified depth and contributing area into suitable for rain garden or unsuitable for raingarden
### 4. Uses Raster calculator to extract the suitable area
### 5. Than extract only these suitable area to obtain a new HSI layer




############INPUTS ##################
## First Get the HSI LAYER ready in the same workspace

## Also Get the watershed area projected and ready in the same workspace


##Unsuitable areas:
    #Erosion Hazard areas --- "er_hz"
    #Landslide Hazard areas --- "lnd_hz"
    #Forested Land --- "frst"
    #Flood Plains --- "fld_pln"
    #areas with building and roads --- "ar_rd"   ###dont need this because this is already eliminated
    #All WETLANDS --- "wtlnd"
    #Land within 30 meters of stream --- "str_bf30"
    # Recreational areas and parks --- "prk"


## All these areas should be already clipped to the shape of study area
##before coming to this analysis
## These areas file should already be in the workspace with the name specified above

## Setup a workspace
wspc = r'F:\WORK\GSI_Project\reapeat2\final_final_try'
arcpy.env.workspace = wspc
Inp_feat = ["er_hz","fld_pln", "lnd_hz", "prk", "str_bf30", "wtlnd"]  ## can add other shapefiles too
fc = "prj_py_h12.shp"        ### This is the study area projected feature class
hsi = "hsi" ### What is the name of hsi layer in the workspace that is being used to filter out irrelavant areas?
un_unsuit = "un_unsuit.shp" ### What do you want to name the unionof all the unsuitable areas?
eras1 = "aft_er_msk.shp" ### what do you want to name the first erased layer
hsi1 = "suit_hsi.tif" ### what do you want to name the hsi layer which has filtered out the first label of unsuitable area


## Constraints for suitability:

#Ksat = should be greater than 0.3 in/hr (0.18288 m/day or 7.62 mm/hr) and less than 9 in/hr (5.4864 m/day or 228.6 mm/hr). 
#Depth = Should be greater than or equal to 5 feet (1.524 m).
#Area = should be less than or equal to 1500 square feet. Which means contributing area should be less than 30000 square feet
kst = "k_mperd_ras_c_1.829.tif" ## hydraulic conductivity layer
ksat_hyd = arcpy.Raster(kst) ### This is the hydraulic conductivity layer that is in m per day in 6ft res
mini1 = ksat_hyd.minimum
maxi1 = ksat_hyd.maximum
args1 = '{} 0.182880 1;0.182880 5.486400 2;5.486400 {} 3'.format(mini1, maxi1)  ##This is how the ksat will be classified
recls_k = "recls_ksat"  ### what should be the name of the reclassed k layer

mod_prj = "mod_prj_d"  
sd = arcpy.Raster(mod_prj) ###This is the modified depth to restrictive layer
mini2 = sd.minimum
maxi2 = sd.maximum
args2 = '{} 1.524 10;1.524 {} 20'.format(mini2, maxi2)  ##This is how the depth will be classified
recls_d = "recls_sd"  ### what should be the name of the reclassed depth layer
  
f = "flw_acc"
flw_ac = arcpy.Raster(f) ### This is the flow accumulation raster
x = arcpy.GetRasterProperties_management(flw_ac, "CELLSIZEX")  ##extracting cell size
y = arcpy.GetRasterProperties_management(flw_ac, "CELLSIZEY")

cellarea = float(x[0])*float(y[0])

args3_0='"{}"*{}'.format(flw_ac, cellarea)
mini3 = flw_ac.minimum
maxi3 = flw_ac.maximum
d_arr = "drn_arr" ## name of drainage area
args3 = 'Con("{}" < 30000, 100,200)'.format(d_arr) ##This is how the contributing area will be classified
recls_a = "recls_ca"  ### what should be the name of the reclassed contributing area layer
  
args4 = '"{}"+"{}"+"{}"'.format(recls_k,recls_d,recls_a)
fin_suit = "cmb_sut" ## This is the name for all suitable layers combinations

#### We need 100 + 20 + 2 = 122
v_n = 122
args5 = 'Value = {}'.format(v_n)
extrct_lyr = "extrct_sut"


###Final layer name
fin_hsi_arr = "fin_hsi_ar"


############### ANALYSIS ##################

##### Buffering ###

##using already buffered stream in this case but following code can be used to buffer as well

##### arcpy.Buffer_analysis('flowline_std_area_prj2', r'F:\WORK\GSI_Project\GIS_work\datasets\Hydrography\HU8_17110014_Watershed\buff_prj30.shp', '98.42 Feet', 'FULL', 'ROUND', 'NONE', '#', 'PLANAR')

a = len(Inp_feat)
list2 = []
for i in Inp_feat:
...     a = wspc + "\\"+ i + ".shp" ### This is done because the arcpy ask for full path 
...     list2.append(a)     

arcpy.Union_analysis(list2, un_unsuit, "ALL", "#", "GAPS")
#### Erase unsuitable layer from the watershed
m3 = wspc + "\\"+fc
m4 = wspc + "\\" + un_unsuit  ## Again did this because we need full path

arcpy.Erase_analysis(m3, m4, eras1)


## Use this erased layer as a mask to extract by mask the HSI layer which doesnot fall in the unsuitable area

m5 = wspc + "\\"+hsi
m6 = wspc + "\\" + eras1 ## Again did this because we need full path

suit_hsi = arcpy.sa.ExtractByMask(m5, m6) ## Now these are the first layer of suitable place where hsi can be placed
suit_hsi.save(hsi1)
## Now second step is to find the area suitable for rain garden


##use raster classification to classify suitable and unsuitable areas based on these three constraints.

##Dont need to setup new workspace
## arcpy.env.workspace = r'F:\WORK\GSI_Project\reapeat2\soilpart'

arcpy.gp.Reclassify_sa(ksat_hyd, 'VALUE', args1, recls_k, 'DATA')
arcpy.gp.Reclassify_sa(sd, 'VALUE', args2, recls_d, 'DATA')
#### use raster calculator to convert the flow accumulation to drainage area.. Multiply using cell size.
####make sure the flow accumulation raster is in the workspace

arcpy.gp.RasterCalculator_sa(args3_0, d_arr)
arcpy.gp.RasterCalculator_sa(args3, recls_a)
arcpy.gp.RasterCalculator_sa(args4, fin_suit)  ### combine drainage area + reclassified k and reclassified d


#### We need 100 + 20 + 2 = 122
## Now use extract by attribute

arcpy.gp.ExtractByAttributes_sa(fin_suit, args5, extrct_lyr)

## Now use this extracted area as a mask to select even more suitable HSI
fin_hsi_ar = arcpy.sa.ExtractByMask(suit_hsi,extrct_lyr)
fin_hsi_ar.save(fin_hsi_arr)   ### Save this as the final suitability map that was created based on the constraints




































