library(tidyverse)
dat<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\Data_Pagamento_Vendita.csv")
dat2<-read_csv("C:\\Users\\Lenovo\\Dropbox\\Il mio PC (DESKTOP-KNLR9GQ)\\Desktop\\Data_Pagamento_Noleggio.csv")
dat
dat2
dat<-data.frame(dat,Vendita=TRUE)
dat2<-data.frame(dat2,Vendita=FALSE)
names(dat)<-c("Id_Noleggio","Data_Pagamento","Vendita")
names(dat)
dat3<-union(dat,dat2)
dat3

write.table(dat3,file="Pagamento_T.csv",sep=",",row.names=FALSE,col.names=TRUE)
