library(tidyverse)
dat<-read_csv("C:\\Users\\Administrator\\Desktop\\Francesco\\Pagamento_10000.csv")
dat
setwd("C:\\Users\\Administrator\\Desktop\\Francesco")
dat<-dat%>%
  filter(Vendita==0)%>%
  select(Id_Pagamento)
  
dat2<-read_csv("C:\\Users\\Administrator\\Downloads\\Noleggio_T (1).csv")
datt<-data_frame(N_Id_Noleggio=dat$Id_Pagamento,Id_Noleggio=dat2$Id_Noleggio)
write.table(datt, file="Pagamento_Noleggio10000.csv", sep = "," ,
            row.names = FALSE, col.names = TRUE)
