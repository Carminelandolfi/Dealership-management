library(tidyverse)
dat<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\Vendita_T_PerR.csv")

dat2<-dat%>%
  select(Data_Pagamento)
dat2$Data_Pagamento<-substr(dat2$Data_Pagamento,1,10)
dat2
dat3<-dat%>%
  select(-Data_Pagamento)
dat3$Data_Consegna<-substr(dat3$Data_Consegna,1,10)
dat3

setwd("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop")
write.table(dat3,file="Vendita_T.csv",sep=",",row.names=FALSE,col.names=TRUE)


dat4<-dat3%>%
  filter(Abituale==1)%>%
  select(V_Codice_Fiscale)
dat4
write.table(dat4,file="Codici_fiscali_Abituali.csv",sep=",",row.names=FALSE,col.names=TRUE)
dim(dat4)


dat6<-read.csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\tabelle csv create da me\\Vendita_T.csv")
dat6
dim(dat6)

dat7<-dat6%>%
  select(Id_Vendita)

dat8<-data.frame(dat7,dat2)
dat8


write.table(dat8,file="Data_Pagamento_Vendita.csv",sep=",",row.names=FALSE,col.names=TRUE)
