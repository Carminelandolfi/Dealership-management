data = read.csv("/Users/mariapiatedesco/Downloads/Promozione_T_Mock.csv")
head(data)

data$data_fine=substr(data$data_fine,1,10)
head(data)
class(data)

setwd("/Users/mariapiatedesco/Downloads")
write.table(data,file="Promozione_T_R.csv", sep=",", row.names=FALSE, col.names=TRUE)

prova=read.csv("/Users/mariapiatedesco/Downloads/Promozione_T.csv")
head(prova)
