library(tidyverse)
dat<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\Concessionaria_T.csv")
dat2<-dat%>%
  select(Città)
dat2
setwd("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop")
write.table(dat2,file="Città_Concessionarie.csv",sep=",",row.names=FALSE,col.names=TRUE)
