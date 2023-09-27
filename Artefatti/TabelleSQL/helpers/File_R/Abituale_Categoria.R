library(tidyverse)
library("plotly")
library("qqplotr")
library("questionr")
library("ggcorrplot")
library("forcats")
library("gapminder")
library("vcd")
library("DT")
dat<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Downloads\\Abituale_Categoria.csv")
dat2<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Downloads\\Abituale_Categoria_T.csv")
dat
dim(dat)
dat2
dim(dat2)
dim(dat2)
datatable(dat)
dat3<-union(dat,dat2)

dat3
dim(dat3)
dir()
write.table(dat3,file="Abituale_Categoria_T.csv",sep=",",row.names=FALSE,col.names=TRUE)
