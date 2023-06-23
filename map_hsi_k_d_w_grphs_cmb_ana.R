
setwd("F:/WORK/GSI_Project/reapeat2/final_final_try/fin_cmb")
met5_dat<-read.csv("classify_analyze_with_facc.txt")


my_custom_themes<-theme_bw()+
  theme(plot.margin = unit(c(0.5,0.5,0.6,0.5), "cm"),
        legend.position = c(1, 0.50),
        legend.direction = "vertical",
        legend.justification = c("right", "top"),
        legend.box.just = "right",
        legend.margin = margin(6, 6, 6, 6), 
        # legend.title = element_text(size = 12), 
        legend.title = element_blank(),
        legend.text = element_text(size = 12)
  )+
  # labs(title = paste("Erosion in relation to", factor[n1]))+xlab("Scenarios")+ 
  theme(axis.title.x = element_blank(), axis.title.y = element_text(size =16),
        axis.text.x.bottom = element_text(angle = 70, hjust = 1, size = 16),
        axis.text.y.left = element_text(size = 16),
        plot.margin = unit(c(0.3,0.3,0.6,0.3), "cm"),plot.title = element_text(hjust = 0.5, size = 22), panel.grid.major = element_blank(),
        strip.text = element_text(size = 15),
        panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))


m6<-met5_dat[,c(2,3)]


m7<-as.data.frame(m6[,1])
# m7<-as.data.frame(rep(m6$VALUE, m6$COUNT))
colnames(m7)<-c("VAL")

m7$HSI<-NA
m7$K<-NA
m7$D<-NA
m7$S<-NA
m7$A<-NA


############# Naming of the classes ######

# vec2<-c(1,2,3,4,3.5)
# ve<-vec2[-5]

# cls_d<-function(a){
#   
#   if(a==0){r<-"Shallow(<0.64)"}
#   else if(a==1){r<-"Shallow (0.64-0.68)"}
#   else if(a==2){r<-"Moderate (0.68-0.82)"}
#   else if(a==3){r<-"Deep (0.82-0.90)"}
#   else if(a==4){r<-"Very Deep (>0.9)"}
#   else { r<-"NO DATA"}
#   # else{r<-"Deep (>=0.64)"}
#   return(r)
# }
cls_d2<-function(a){
  
  if(a==0){r<-"<0.64"}
  # else if(a==1){r<-"0.64-0.68"}
  else if(a==1|a==2){r<-"0.64-0.82"}
  else if(a==3){r<-"0.82-0.90"}
  else if(a==4){r<-">0.9"}
  else { r<-"NO DATA"}
  # else{r<-"Deep (>=0.64)"}
  return(r)
}

dclass <-c("<0.64","0.64-0.82","0.82-0.90",">0.9")

# cls_k<-function(a){
#   
#   if(a==1){r<-"Least permeable (<0.2)"}
#   else if(a==2){r<-"Low permeable (0.2-2.2)"}
#   else if(a==3){r<-"Moderately permeable (2.2-5.5)"}
#   else if(a==4){r<-"Permeable (5.5-15.5)"}
#   else if(a==5){r<-"Very permeable (>15.5)"}
#   else { r<-"NO DATA"}
#   return(r)
# }

cls_k2<-function(a){
  
  if(a==1){r<-"<0.2"}
  else if(a==2){r<-"0.2-2.2"}
  # else if(a==3){r<-"2.2-5.5"}
  else if(a==3|a==4){r<-"2.2-15.5"}
  else if(a==5){r<-">15.5"}
  else { r<-"NO DATA"}
  return(r)
}

kclass <-c("<0.2","0.2-2.2","2.2-15.5",">15.5")

# 
# cls_s<-function(a){
#   
#   if(a==1){r<-"Flat (<12)"}
#   else if(a==2){r<-"Inclining (12-24)"}
#   else if(a==3){r<-"Slopy (24-36)"}
#   else if(a==4){r<-"Steep (36-48)"}
#   else if(a==5){r<-"Very Steep (>48)"}
#   else { r<-"NO DATA"}
#   return(r)
# }

cls_s2<-function(a){
  
  if(a==1){r<-"<12"}
  else if(a==2){r<-"12-24"}
  else if(a==3){r<-"24-36"}
  else if(a==4|a==5){r<-">36"}
  # else if(a==5){r<-">48"}
  else { r<-"NO DATA"}
  return(r)
}

slp_class <-c("<12","12-24","24-36",">36")

# 
# cls_a<-function(a){
#   
#   if(a==1){r<-"Least (<100) "}
#   else if(a==2){r<-"Low (100-10000)"}
#   else if(a==3){r<-"Moderate (10000-30000)"}
#   else if(a==4){r<-"Very High (30000-100000)"}
#   else if(a==5){r<-"Very Very High(>100000)"}
#   else { r<-"NO DATA"}
#   return(r)
# }


cls_a2<-function(a){
  
  if(a==1){r<-"<100"}
  else if(a==2){r<-"100-10000"}
  else if(a==3|a==4){r<-"10000-100000"}
  # else if(a==4){r<-"30000-100000"}
  else if(a==5){r<-">100000"}
  else { r<-"NO DATA"}
  return(r)
}


area_class <-c("<100","100-10000","10000-100000",">100000")

classifier<-function(ve){
  
  r1<-cls_d2(ve[1])
  r2<-cls_k2(ve[2])
  r3<-cls_s2(ve[3])  
  r4<-cls_a2(ve[4])  
  
  ve_r<-c(r1,r2,r3,r4,ve[5])
  return(ve_r)
}

################################################



library(tidyr)
# a=m7[1,1]
separater<-function (a){
  
  
b<-unlist(strsplit(as.character(a), ""))
c<-length(b)

D<-as.numeric(b[c])
K<-as.numeric(b[c-1])
S<-as.numeric(b[c-2])  
A<-as.numeric(b[c-3])
c_2<-c-4

HSI<-as.numeric(paste(b[1:c_2], collapse=''))
vec<-c(D,K,S,A,HSI)

vec2<-classifier(vec)
# f<-''
# for (i in 1:c_2){
#   e<-b[i]
#   f<-paste0(f,e)
# }
# HSI<-as.numeric(f)

return(vec2)

  }


for (k in 1:nrow(m7)){
#k=1
v<-separater(m7[k,1])
m7[k,2]<-v[5]
m7[k,3]<-v[2]
m7[k,4]<-v[1]
m7[k,5]<-v[3]
m7[k,6]<-v[4]
}

# separater(a)

# apply(m7, 1, function (x) separater(x))

m7$HSI<-as.numeric(m7$HSI)/100

median(m7$HSI, na.rm = T)
# m7$K<-as.factor(m7$K)
# m7$D<-as.factor(m7$D)
# m7$S<-as.factor(m7$S)
# m7$A<-as.factor(m7$A)
### 10% values 
quantile(m7$HSI,probs = seq(0,1,1/5), na.rm = T)

# quantile(m7$HSI,probs = seq(0,1,1/5), na.rm = T)
# 0%   20%   40%   60%   80%  100% 
#   -2.53  4.61  8.16 11.77 15.67 29.59 

### The class can be based on 10 %
## median class most suitable
## one step lower than median, suitable
## one step higher than median, moderately suitable
## least suitable


###Also maybe i dont have to classify as zones
## maybe a hot/cold map or something that shows which areas are relatively more suitable
## or both,
## first a zonification
## second hot cold pixels
#####################

library(ggplot2)
library(viridis)
# install.packages("rayshader")
library(rayshader)
# install.packages("plot_gg")
# library(plot_gg)

# write.csv(m7,"trywith_python.csv")

# p<-ggplot(m7, aes(K, HSI, color=D))+geom_violin(trim = F)  ## if wanting to add depth in same

m7$S<-as.factor(m7$S)
m7$K<-as.factor(m7$K)
m7$D<-as.factor(m7$D)
m7$A<-as.factor(m7$A)


m7$S<-factor(m7$S, levels = slp_class)
m7$K<-factor(m7$K, levels = kclass)
m7$D<-factor(m7$D, levels = dclass)
m7$A<-factor(m7$A, levels = area_class)
# d_class
# k_class
# area_class
#### CDF ploting for HSI 


hcis<-data.frame(group = unique(m7$K), low =5.9, high=10.4)

x<-c(min(as.numeric(m7$S))-0.5, max(as.numeric(m7$S))+0.5)
# hcis<-data.frame(group = unique(m7$K), low =5.9, high=10.4)

hcis<-merge(hcis,"x"=x)


hci2<-NULL
hci2<-as.data.frame(hcis$group)
colnames(hci2)<-"K"

hci2$y<-c(8,8,8,8,8)
hci2$S<-c(unique(m7$S)[4])

library(ggplot2)
histplt<-ggplot(m7, aes(x = HSI))+
  geom_histogram(
    # aes(y = ..density..),
    binwidth=2, color = "black", fill = "white")+
  # geom_density(alpha=0.6)+
  ylab("Count")+
  theme_classic()+
  theme(axis.text = element_text(size = 18),
        axis.title = element_text(size = 20))


edfplt<-ggplot(m7, aes(HSI)) +stat_ecdf(geom="point")+
  labs(
        # title = "Empirical cumulative density function for HSI",
       y="F(HSI value)",
       x="HSI value")+
  theme_classic()+
  theme(axis.text = element_text(size = 18),
        axis.title = element_text(size = 20))


cowplot::plot_grid(histplt, edfplt, ncol = 2, align = "hv")

### Inside fin cmb directory ######

ggsave("cdf HSI_hist.eps", height = 8, width = 12)

p<-ggplot(m7, aes(S, HSI))+geom_violin(trim = F, fill="lightblue", color="black")+
  theme(axis.text.x.bottom = element_text(angle = 70, hjust = 1, size =10))
  
 
p2<-ggplot(m7, aes(D, HSI))+geom_violin(trim = F, fill="lightblue", color="black")
p+stat_summary(fun.y=median, geom = "point", size=2, color="red")+
  stat_summary(fun.y=mean, geom = "point", size=2, shape=23, color="blue")+
facet_wrap(~S)


###### violin plot can help you identify double clusters

p3<-p+geom_boxplot(width=0.1)+
  facet_wrap(~K)+ggtitle("Combine effect of Slope and K (m/day)")

# p+geom_boxplot(width=0.1)+
#   facet_wrap(~A)
# 
# p2+geom_boxplot(width=0.1)+
#   facet_wrap(~S)

p4<-p3+geom_ribbon(data = merge(hcis, m7),
               aes(x=x,ymin=low, ymax=high, group=group, fill="Optimum HSI range"),
               alpha=0.2)+
  geom_point(data = hci2, aes(x=S, y=y, colour="Optimum HSI value" ), shape=16)+
   scale_color_manual(name="", values = c("Optimum HSI range"=NA, "Optimum HSI value"="red"))+
  scale_fill_manual(name="", values=c("Optimum HSI range"="light green", "Optimum HSI value"=NA))+
  theme(legend.position = c(0.90,0.15))+
  theme(legend.key.size=unit(0, "lines"))
  # scale_shape_manual("", values=c("HSI"=NA, "HSI2"=16))


p5<-p4+scale_color_manual(name="", values = c("HSI"="red"))+
  scale_fill_manual(name="", values=c("HSI"="light green"))+
  scale_shape_manual("", values=c("HSI2"=16))
  

# +
  # scale_fill_manual("", values = "light green")


# 
# ### 3d plotting 
# mtplot = ggplot(m7) +
#   geom_point(aes(x=K,y=HSI,color=D)) +
#   scale_color_continuous(limits=c(0,8))+facet_wrap(~K)
# 
# 
# plot_gg(mtplot, width=3.5, multicore = TRUE, windowsize = c(1400,866), sunangle=225,
#         zoom = 0.60, phi = 30, theta = 45)
# render_snapshot(clear = TRUE)
# 
# remotes::install_github("tylermorganwall/rayshader")
# library(rayshader)
# library(ggplot2)
# library(tidyverse)
# 
# 



# scale_fill_manual("", values=c("HSI for Optimum range of Rain garden parameters" = "light green"))+
#   scale_shape_manual(values = c("HSI for optimum rain garden parameter"=16))+


cols<-c("K"="green")

ggplot(m7, aes(K, HSI))+geom_point()+
  scale_fill_manual(values=cols)+
  scale_color_manual(values=cols)+
  scale_shape_manual(values = cols)+
theme_bw() +
  theme(legend.box.background = element_rect(colour = "grey", fill = "white"), # create a box around all legends
        legend.box.margin = margin(0.1, 0.1, 0.1, 0.1, "cm"),                  # specify the margin of that box
        legend.background = element_blank(),                                   # remove boxes around legends (redundant here, as theme_bw() seems to do that already)
        legend.spacing = unit(-0.5, "cm"),                                     # move legends closer together
        legend.margin = margin(0, 0.2, 0, 0.2, "cm")) 

########## Effect of Slope and Area 

ggplot(m7, aes(S, HSI))+geom_violin(trim = F, fill="lightblue", color="black")+
geom_boxplot(width=0.1)+
  facet_wrap(~A, ncol = 5)+
  xlab("Slope (%)")+
  # theme_bw()+
  my_custom_themes+
  theme(
        strip.text.x = element_text(size = 24),
        axis.text.x.bottom = element_text(size=24, color = "black"),
        axis.text.y.left = element_text(size=24, color = "black"),
        axis.text.x = element_text(size = 30, angle = 60, hjust = 1),
        axis.text.y = element_text(size = 30),
        axis.title.x = element_text(size = 30),
        axis.title.y = element_text(size = 30))
  # ggtitle("Combine effect of Slope and K (m/day)")

ggsave("slopex_carea_HSI.eps", height = 8, width = 12)


######### Effect of Depth and K

ggplot(m7, aes(D, HSI))+
  geom_violin(trim = F, fill="lightblue", color="black")+
    geom_boxplot(width=0.1)+
    facet_wrap(~K, ncol = 5)+
    # theme_bw()+
    xlab("Depth (m)")+
    my_custom_themes+
  theme(
    strip.text.x = element_text(size = 24),
    axis.text.x.bottom = element_text(size=24, color = "black"),
    axis.text.y.left = element_text(size=24, color = "black"),
    axis.text.x = element_text(size = 30, angle = 60, hjust = 1),
    axis.text.y = element_text(size = 30),
    axis.title.x = element_text(size = 30),
    axis.title.y = element_text(size = 30))
  # ggtitle("Combine effect of Slope and K (m/day)")

ggsave("depthx_k_HSI.eps", height = 8, width = 12)
