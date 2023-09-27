library(tidyverse)
dat<-read_csv("/Users/mariapiatedesco/Downloads/Veicolo_Vendita_T.csv")
dat

dat1<-dat%>%
  filter(Tipo==TRUE)%>%
  select(V_Id_Veicolo)
dat1

dim(dat)
dim(dat1)

dat2<-dat%>%
  filter(Tipo==FALSE)%>%
  select(V_Id_Veicolo)
dat2
dim(dat2)


write.table(dat1, file="Vendita_Due_Ruote_TRUE.csv", sep = "," ,
            row.names = FALSE, col.names = FALSE)
write.table(dat2, file="Vendita_Quattro_Ruote_FALSE.csv", sep = "," ,
            row.names = FALSE, col.names = FALSE)
