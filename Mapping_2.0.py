

########### Idea is to first reclassify the rasters



## Than map it vs the HSI

#a = list["d_meter_c_1.83","k_mperd_ras_c_1_829","slp"]

arcpy.env.workspace = r'F:\WORK\GSI_Project\reapeat2\final_final_try'


rast1 = arcpy.Raster("d_meter_c_1.83.tif")
mini1 = rast1.minimum
maxi2 = rast1.maximum

args = "{} 0.64 0;0.64 0.68 1;0.68 0.82 2;0.82 0.90 3; 0.90 {} 4".format(mini1, maxi2)
arcpy.gp.Reclassify_sa(rast1, 'VALUE', args, 'recls_rst1', 'DATA')

rast2 = arcpy.Raster("k_mperd_ras_c_1_829.tif")
mini3 = rast2.minimum
maxi4 = rast2.maximum

args = "{} 0.20 10;0.20 2.20 20;2.20 5.50 30;5.50 15.50 40; 15.50 {} 50".format(mini3, maxi4)
arcpy.gp.Reclassify_sa(rast2, 'VALUE', args, 'recls_rst2', 'DATA')

rast3 = arcpy.Raster("slp")
mini5 = rast3.minimum
maxi6 = rast3.maximum

args = "{} 12 100;12 24 200;24 36 300;36 48 400; 48 {} 500".format(mini5, maxi6)
arcpy.gp.Reclassify_sa(rast3, 'VALUE', args, 'recls_rst3', 'DATA')

rast4 = arcpy.Raster("flw_acc_scld")
mini7 = rast4.minimum
maxi8 = rast4.maximum

args = "{} 100 1000;100 10000 2000;10000 30000 3000;30000 100000 4000; 100000 {} 5000".format(mini7, maxi8)
arcpy.gp.Reclassify_sa(rast4, 'VALUE', args, 'recls_rst4', 'DATA')


############# Reclassify than use raster calculator..
## more info in "document.xlsx" which is inside the fin_cmb folder of final_final_try folder
