library("tidyverse")
library("plotly")
library("qqplotr")
library("questionr")
library("ggcorrplot")
library("forcats")
library("gapminder")
library("vcd")
library("DT")

d<-read_csv("C:\\Users\\Administrator\\Downloads\\Abituale_Brand_Preferito_T.csv")
d_2<-read_csv("C:\\Users\\Administrator\\Downloads\\Abituale_Brand_Preferito_T(1).csv")

d_3<-union(d,d_2)
dir()

setwd("C:\\Users\\Administrator\\Desktop")

write.table(d_3,file="Abituale_Brand_Preferito_T.csv",sep=",",row.names=FALSE,col.names=TRUE)
