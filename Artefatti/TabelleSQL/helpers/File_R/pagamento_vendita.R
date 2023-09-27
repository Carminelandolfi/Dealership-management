library(tidyverse)
d<-read_csv("C:\\Users\\Administrator\\Desktop\\Francesco\\csv\\Pagamento_10000.csv")
dat<-d%>%
  filter(Vendita==1)%>%
  select(Id_Pagamento)
dat

d2<-read_csv("C:\\Users\\Administrator\\Desktop\\Prezzo_Acquisto.csv")

completo<-data_frame(Id_Veicolo=d2$id_veicolo,Prezzo_Acquisto=d2$Prezzo_Acquisto
,Id_Venidita=d2$id_Vendita,Id_Pagamento=dat$Id_Pagamento)
write.table(completo, file="Tutto.csv", sep = "," ,
            row.names = FALSE, col.names = TRUE)