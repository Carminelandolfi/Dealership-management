library(tidyverse)
dat<-read_csv("/Users/mariapiatedesco/Downloads/Veicolo_Noleggio_T.csv")
dat

dat1<-dat%>%
  filter(Tipo==TRUE)%>%
  select(N_id_Veicolo)
dat1

dim(dat)
dim(dat1)

dat2<-dat%>%
  filter(Tipo==FALSE)%>%
  select(N_id_Veicolo)
dat2
dim(dat2)


write.table(dat1, file="Noleggio_Due_Ruote_TRUE.csv", sep = "," ,
            row.names = FALSE, col.names = FALSE)
write.table(dat2, file="Noleggio_Quattro_Ruote_FALSE.csv", sep = "," ,
            row.names = FALSE, col.names = FALSE)
