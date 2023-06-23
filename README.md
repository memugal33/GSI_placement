# GSI_placement
Placement of Green Stormwater Infrastructure using Hydrological Sensitivity Index (HSI).. Pre and Post processing

## ```.py``` files are written to be used via ArcPy from ArcGIS

```C1_HSI_final.py``` can be used to compute the Hydrological Sensitivity Index.

```C2_raingarden_final.py``` can be used to filter unsuitable areas for the placement of rain garden and extract suitable areas.

```C3_classify2.py``` can be used to classify the suitable areas for the placement of rain garden using fishnet.

```C3_classify2_zonify.py``` uses alternative method for zonification where composite HSI is computed using the fishnet to classify the suitable areas.

```map_hsi_k_d_w_grphs_cmb_ana.R```HSI and its dependent Slope, Contr. Area, Soil Depth, and K are reclassified and based on raster calculation a unique number was created for each pixel. This r code, redistributes that number to calculate the HSI vs Slope, Cont. Area, S Depth and K. This code also analyze the distribution of HSI with different factors using violin plot.

```studywat_balance_best_wb_3ofe_all_repres.rmd``` WEPP simulation was conducted in for 122 scenarios of representative hillslopes for the Lower Puyallup River Watershed. This code extracts the water balance and other outputs for each of the scenarios and analyse the change in water balance in various scenarios. It also compute the HSI values for each hillslope and map it with runoff. 

This code also analyze the difference in runoff generation in No treatment Vs Pavement Vs Rain Garden scenarios.
