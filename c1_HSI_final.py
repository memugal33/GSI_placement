# SCRIPT 1 OF 3

#SCRIPT ARE DIVIDED INTO WORKFLOW, INPUT/OUTPUT AND ANALYSIS PART
#WORKFLOW gives the detail of what the script does
#INPUT/OUTPUT part gives control over naming, chosing workspace and arguments
#ANALYSIS part just uses the arcgis function and perform analysis

############ WORKFLOW #####
#1. Fill the sinks in the elevation file
#2. Calculate flow direction, flow accumulation (can change the algorithm)
#3. Calculate slope
#4. Calculate TWI
#5. Calculate SWSC
#6. Calculate HSI



###### INPUT/OUTPUT ######

### For calculating HSI following data are needed
#  * All data should be clipped to the same area
# Elevation data
# Hydraulic conductivity data
# Soil depth to restrictive layer data
## Layer that shows impervious layer in the area


### This is with Dinf

### USe this line below to stop adding the object to map document everytime it is created
arcpy.env.addOutputsToMap = False

### Setup the workspace
wspc = r'F:\WORK\GSI_Project\reapeat2\try2'  ## save the workspace path in a variable
arcpy.env.workspace = wspc ##Setup the workspace
elv_area = 'ft_6_elv.tif' ## UNPROJECTED
flw_ac = "flw_acc" #This needs to be named carefully because this will be needed later to calculate contributing area
twi_nm = "finaltwi" ### This is the name of twi layer
dep_res = "d_meter_c_1.83.tif"  ## depth to rest. layer from ssurgo
imprv_lyr = "imperv_1_829.tif" ## impervious layer
kst = "k_mperd_ras_c_1.829.tif" ## hydraulic conductivity layer
flw_alg = "DINF"  ## It could be "D8" or "MFD"

mod_prj = "mod_prj_d"  ## modified layer that will be obtained after the analysis part
swsc = "swsc" ## name of the soil and water storage capacity layer

hsilyr = "hsi" ## This is the name of hsi layer computed


################# ANALYSIS ###########

### Project the data first
m = wspc +"\\"+elv_area  ## need to use a full path .. reason given here: https://support.esri.com/en/technical-article/000011874

arcpy.ProjectRaster_management(m, 'prjected', "PROJCS['NAD_1983_HARN_StatePlane_Washington_South_FIPS_4602_Feet',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1640416.666666667],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',45.83333333333334],PARAMETER['Standard_Parallel_2',47.33333333333334],PARAMETER['Latitude_Of_Origin',45.33333333333334],UNIT['Foot_US',0.3048006096012192]]", 'NEAREST', '6.00060889861806 5.99983879994011', 'NAD_1983_To_HARN_WA_OR', '#', "PROJCS['NAD_1983_StatePlane_Washington_North_FIPS_4601_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1640416.666666667],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.8333333333333],PARAMETER['Standard_Parallel_1',47.5],PARAMETER['Standard_Parallel_2',48.73333333333333],PARAMETER['Latitude_Of_Origin',47.0],UNIT['Foot_US',0.3048006096012192]]", 'NO_VERTICAL')
arcpy.gp.Fill_sa('prjected', "Filled", '#') ## Fill tool
arcpy.gp.FlowDirection_sa('Filled', "fd_elv", 'NORMAL', '#', flw_alg)  ## Flow direction tool
arcpy.gp.FlowAccumulation_sa("fd_elv", flw_ac, '#',"FLOAT",flw_alg) ## Flow accumulation
slp = arcpy.sa.Slope("Filled", "DEGREE", 1, "PLANAR", '#') ## Use slope tool
slp.save("slp")
slp_rad = (slp * 1.570796)/90   ## This is conversion to radian
slp_rad.save("slp_rad")
arcpy.gp.RasterCalculator_sa('Con("slp_rad" > 0, Tan("slp_rad"), 0.0001)', "tnslp") ### convert to tanslope

x = arcpy.GetRasterProperties_management(flw_ac, "CELLSIZEX") ## cellsize
fw = "'{}'".format(flw_ac)
aarg = '({}+1)*{}'.format(fw,x)
arcpy.gp.RasterCalculator_sa(aarg, "flw_acc_scld") ## scale the flow accumulation
arcpy.gp.RasterCalculator_sa('Ln("flw_acc_scld" / "tnslp")', twi_nm) ## calculate final twi

### Now this is the soil water storage capacity part

### Need to see if the hydraulic conductivity and depth layer are also in the
##Same resolution or not
## They need to be in same resolution for best results


### Setup the new workspace to store the file
## Only do this if necessary because best is to have same storage workspace
#arcpy.env.workspace = r'F:\WORK\GSI_Project\repeat same analysis\soilpart' 


### This takes the Hydraulic conductivity and depth to the restrictive layer data that has already been projected


arg_m0 = '("{}"*"{}")'.format(dep_res,imprv_lyr)
arcpy.gp.RasterCalculator_sa(arg_m0, mod_prj)

arg_m1 = 'Ln("{}"*"{}")'.format(kst,mod_prj)
arcpy.gp.RasterCalculator_sa(arg_m1, swsc)

### Now calculate HSI
#arcpy.env.workspace = r'F:\WORK\GSI_Project\reapeat2'
#arcpy.gp.RasterCalculator_sa('"finaltwi" - "soilpart\\swsc"', "hsi")
arg_m2 = '"{}"-"{}"'.format(twi_nm,swsc)
arcpy.gp.RasterCalculator_sa('"finaltwi" - "swsc"', hsilyr)
