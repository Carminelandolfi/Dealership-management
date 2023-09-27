library(tidyverse)
d<-read_csv("C:\\Users\\Administrator\\Downloads\\Pagamento_Vendita_T (2).csv")
d
dd<-d%>%
  select(-prezzo)
write.table(dd, file="Pagamento_Vendita_T.csv", sep = "," ,
            row.names = FALSE, col.names = TRUE)
dd$Id_Vendita
