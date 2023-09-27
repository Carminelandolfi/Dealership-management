library(tidyverse)
dat<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Downloads\\Veicolo_T.csv")
dat

dat1<-dat%>%
  filter(Vendita==TRUE)%>%
  select(Id_Veicolo)
dat1
dim(dat)
dim(dat1)
dat2<-dat%>%
  filter(Vendita==FALSE)%>%
  select(Id_Veicolo)
dat2
dim(dat2)


write.table(dat1, file="Vendita_TRUE.csv", sep = "," ,
            row.names = FALSE, col.names = FALSE)
write.table(dat2, file="Vendita_FALSE.csv", sep = "," ,
            row.names = FALSE, col.names = FALSE)
