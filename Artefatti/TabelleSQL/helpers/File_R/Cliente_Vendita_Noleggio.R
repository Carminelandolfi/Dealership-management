library(tidyverse)
dat<-read_csv("/Users/mariapiatedesco/Downloads/Cliente_T.csv")
head(dat)

dat1<-dat%>%
  filter(Vendita==TRUE)%>%
  select(Codice_Fiscale)
dat1
dim(dat1)

dat2<-dat%>%
  filter(Noleggio==TRUE)%>%
  select(Codice_Fiscale)
dat2
dim(dat2)

setwd("/Users/mariapiatedesco/Downloads")
write.table(dat1, file="Vendita_TRUE.csv", sep = "," ,
            row.names = FALSE, col.names = FALSE)
write.table(dat2, file="Noleggio_TRUE.csv", sep = "," ,
            row.names = FALSE, col.names = FALSE)
