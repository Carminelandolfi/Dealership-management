library(tidyverse)
dat<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\noleggi\\Noleggio_1.csv")
dat2<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\noleggi\\Noleggio_2.csv")
dat3<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\noleggi\\Noleggio_3.csv")
dat4<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\noleggi\\Noleggio_4.csv")

dat6<-union(dat,dat2)

dat6
dat7<-union(dat3,dat4)
dat8<-union(dat6,dat7)
dim(dat8)
dat8$Data_Consegna<-substr(dat8$Data_Consegna,1,10)
dat8$Data_Pagamento<-substr(dat8$Data_Pagamento,1,10)
dat8

dat8<-dat8%>%
  filter(N_Codice_Fiscale!="N_Codice_Fiscale")
dim(dat8)

dat9<-dat8%>%
  select(-Data_Pagamento)

setwd("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop")
write.table(dat9,file="Noleggio_T.csv",sep=",",row.names=FALSE,col.names = TRUE)

dat10<-dat8%>%
  select(Data_Pagamento)

dat12<-read.csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\tabelle csv create da me\\Noleggio_T.csv")

dat13<-dat12%>%
  select(Id_Noleggio)

dat14<-data.frame(dat10,dat13)
dat14

write.table(dat14,file="Data_Pagamento_Noleggio.csv",sep=",",row.names=FALSE,col.names=TRUE)


