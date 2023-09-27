# 1 Elencare marca e modello di veicoli noleggio prelevati a Ponte Nova a luglio 2021; 

select brand, modello
from Veicolo_T, Veicolo_Noleggio_T, Noleggio_T, Concessionaria_T
where Veicolo_T.Id_Veicolo = Veicolo_Noleggio_T.N_Id_Veicolo and 
Veicolo_Noleggio_T.N_Id_Veicolo = Noleggio_T.N_Id_Veicolo and 
Veicolo_T.Id_Concessionaria = Concessionaria_T.Id_Concessionaria and 
Concessionaria_T.Città = "Ponte Nova" and 
Noleggio_T.Data_Consegna between "2021-07-01" and "2022-07-31"; 
     
     
# 2 Calcolare il numero totale di noleggi e acquisti di veicoli a due ruote; 

select *
from (select count(*) as Noleggi_Tipo1 
from Noleggio_T, Veicolo_Noleggio_T 
where Noleggio_T.N_Id_Veicolo=Veicolo_Noleggio_T.N_Id_Veicolo 
and Veicolo_Noleggio_T.Tipo = 1) as Noleggi, (select count(*) as Vendite_Tipo1
from Vendita_T, Veicolo_Vendita_T
where Vendita_T.V_Id_Veicolo=Veicolo_Vendita_T.V_Id_Veicolo
and Veicolo_Vendita_T.Tipo = 1) as Vendite;


# 3 Visualizzare nome, cognome e codice fiscale dei clienti che hanno noleggiato 3+ volte un’auto sportiva; 

select nome,cognome, codice_fiscale
from 
(select nome, cognome, codice_fiscale, count(Noleggio_T.N_Id_Veicolo) as NumNoleggiSportiva
from cliente_t, noleggio_t, N_Quattro_Ruote_T
where Noleggio_T.N_Codice_Fiscale = Cliente_T.Codice_Fiscale and
Noleggio_T.N_Id_Veicolo = N_Quattro_Ruote_T.Q_N_Id_Veicolo and
N_Quattro_Ruote_T.Categoria = "Sportiva" 
group by Cliente_T.Codice_Fiscale) as NolggiSportva
where NumNoleggiSportiva > 2;


# 4 Visualizzare la marca del veicolo con il maggior numero di noleggi da parte dei clienti che hanno più di 60 anni; 

create view Noleggi60 as
select brand, count(*) as Noleggi
from Veicolo_T, Noleggio_T, Cliente_T
where Veicolo_T.Id_Veicolo = Noleggio_T.N_Id_Veicolo and
Noleggio_T.N_Codice_Fiscale = Cliente_T.Codice_Fiscale and 
2022-year(cliente_t.data_nascita)>=60
group by brand;

select brand 
from Noleggi60
where Noleggi = (select max(Noleggi) from Noleggi60);


# 5 Id dei dipendenti che in un anno hanno più provvigioni; 

create view Provvigioni as
select dipendente_t.id_dipendente, 
sum((Ammontare_Senza_IVA+Aliquota_IVA/100*Ammontare_Senza_IVA)*Tasso_Commissione/100) 
as Provvigioni
from  Dipendente_T, Vendita_T, Pagamento_Vendita_T, Pagamento_T
where Dipendente_T.Id_Dipendente = Vendita_T.Id_Dipendente and
Vendita_T.Id_Vendita = Pagamento_Vendita_T.Id_Vendita  and 
Pagamento_Vendita_T.V_Id_Pagamento = Pagamento_T.Id_Pagamento and 
Pagamento_T.Data_Pagamento between "2022-01-01" and "2022-12-31"
group by dipendente_t.id_dipendente;

select *
from Provvigioni 
where Provvigioni = (select max(Provvigioni) from Provvigioni);


# 6 Verificare se ai clienti a cui sono state inviate le e-mail poi hanno effettivamente acquistato veicolo; 

select Promozione_T.Id_Promozione, Abituale_Promozione_T.A_V_Codice_Fiscale, 
Vendita_T.Id_Vendita
from Promozione_T, Abituale_Promozione_T, Vendita_T
where Promozione_T.Id_Promozione = Abituale_Promozione_T.Id_Promozione and 
Abituale_Promozione_T.A_V_Codice_Fiscale = Vendita_T.V_Codice_Fiscale and 
Data_Ordine between Promozione_T.Data_Inizio and Promozione_T.Data_Fine;


# 7_1 Visualizzare gli ID di singoli clienti, il numero degli acquisti effettuati; 

select codice_fiscale, count(Vendita_T.Id_Vendita) as Numero_Ordini
from cliente_t, vendita_t
where codice_fiscale = vendita_t.v_codice_fiscale  
group by codice_fiscale;


# 7_2 Visualizzare gli ID di singoli clienti, il numero dei noleggi effettuati; 

select codice_fiscale, count(Noleggio_T.Id_Noleggio) as Numero_Ordini
from cliente_t, Noleggio_T
where codice_fiscale = noleggio_t.n_codice_fiscale 
group by codice_fiscale;


# 8 Restituire le foto del primo veicolo venduto da una concessionaria;

select id_veicolo, foto
from Veicolo_T, Vendita_T
where Veicolo_T.Id_Veicolo = Vendita_T.V_Id_Veicolo and
Data_Ordine = (select min(Data_Ordine) from Vendita_T);
    

# 9 Visualizzare il preventivo del noleggio dei veicoli del brand **brand** per 5 giorni; 

select Id_Veicolo, Prezzo_Giorno*5 as Preventivo5Giorni
from Veicolo_T, Veicolo_Noleggio_T
where Veicolo_T.Id_Veicolo = Veicolo_Noleggio_T.N_Id_Veicolo and 
Brand = "Ford";


# 10 Restituire id dei dipendenti che hanno ricevuto il maggior numero di recensioni positive (Soddisfatto, Molto Soddisfatto); 

create view NumeroRecensioniPositive_Dip as 
select Dipendente_T.Id_Dipendente, count(Dipendente) as NumRecPos
from dipendente_t, recensione_t
where Dipendente_T.Id_Dipendente = Recensione_T.Id_Dipendente and
Dipendente in ("Soddisfatto", "Molto Soddisfatto")
group by Dipendente_T.Id_Dipendente;
 
select *
from NumeroRecensioniPositive_Dip 
where NumRecPos = (select max(NumRecPos) from NumeroRecensioniPositive_Dip);
    
    
# 11 Restituire id dei dipendenti che hanno ricevuto il maggior numero di recensioni negative (Insoddisfatto, Molto Insoddisfatto); 

create view NumeroRecensioniNegative_Dip as 
select Dipendente_T.Id_Dipendente, count(Dipendente) as NumRecNeg
from dipendente_t, recensione_t
where Dipendente_T.Id_Dipendente = Recensione_T.Id_Dipendente and
Dipendente in ("Insoddisfatto", "Molto Insoddisfatto")
group by Dipendente_T.Id_Dipendente;
 
select *
from NumeroRecensioniNegative_Dip 
where NumRecNeg = (select max(NumRecNeg) from NumeroRecensioniNegative_Dip);


# 12 Restituire id delle concessionarie i cui veicoli hanno ricevuto il maggior numero di recensioni positive (Soddisfatto, Molto Soddisfatto); 

create view NumeroRecensioniPositive_Conc as
select Concessionaria_T.Id_Concessionaria, count(Veicoli) as NumRecPos
from Concessionaria_T, Dipendente_T, Recensione_T
where Dipendente_T.Id_Concessionaria = Concessionaria_T.Id_Concessionaria  and
Recensione_T.Id_Dipendente = Dipendente_T.Id_Dipendente and 
Veicoli in ("Soddisfatto", "Molto Soddisfatto")
group by Concessionaria_T.Id_Concessionaria;

select *
from NumeroRecensioniPositive_Conc
where NumRecPos = (select max(NumRecPos) from NumeroRecensioniPositive_Conc);


# 13 Inviare gli auguri ai clienti che oggi compiono gli anni; 

select Nome, Cognome, email, telefono
from Cliente_T
where day(Data_Nascita) = day(current_date()) and month(Data_Nascita) = month(current_date());
    

# 14 Visualizzare la concessionaria che ha fatto più vendite nel periodo **periodo**, specificando id concessionaria e numero di vendite; 

create view PeriodoEstivo as
select Concessionaria_T.id_concessionaria, count(Data_Ordine) as NumeroVendite
from Vendita_T, Dipendente_T, Concessionaria_T
where Vendita_T.Id_Dipendente = Dipendente_T.Id_Dipendente and 
Dipendente_T.Id_Concessionaria = Concessionaria_T.Id_Concessionaria and
Data_Ordine between '2022-06-21' and '2022-09-23'
group by concessionaria_t.Id_Concessionaria;

create view PeriodoPrimaverile as
select Concessionaria_T.id_concessionaria, count(Data_Ordine) as NumeroVendite
from Vendita_T, Dipendente_T, Concessionaria_T
where Vendita_T.Id_Dipendente = Dipendente_T.Id_Dipendente and 
Dipendente_T.Id_Concessionaria = Concessionaria_T.Id_Concessionaria and
Data_Ordine between '2022-03-20' and '2022-06-21'
group by concessionaria_t.Id_Concessionaria;

create view PeriodoInvernale as
select Concessionaria_T.id_concessionaria, count(Data_Ordine) as NumeroVendite
from Vendita_T, Dipendente_T, Concessionaria_T
where Vendita_T.Id_Dipendente = Dipendente_T.Id_Dipendente and 
Dipendente_T.Id_Concessionaria = Concessionaria_T.Id_Concessionaria and
Data_Ordine between '2022-12-21' and '2022-03-20'
group by concessionaria_t.Id_Concessionaria;

create view PeriodoAutunnale as
select Concessionaria_T.id_concessionaria, count(Data_Ordine) as NumeroVendite
from Vendita_T, Dipendente_T, Concessionaria_T
where Vendita_T.Id_Dipendente = Dipendente_T.Id_Dipendente and 
Dipendente_T.Id_Concessionaria = Concessionaria_T.Id_Concessionaria and
Data_Ordine between '2022-09-23' and '2022-12-21'
group by concessionaria_t.Id_Concessionaria;

select * 
from  periodoEstivo
where NumeroVendite = (select max(NumeroVendite) from PeriodoEstivo);

select * 
from periodoautunnale
where NumeroVendite = (select max(NumeroVendite) from periodoautunnale);

select * 
from periodoinvernale
where NumeroVendite = (select max(NumeroVendite) from periodoinvernale);

select * 
from periodoprimaverile
where NumeroVendite = (select max(NumeroVendite) from periodoprimaverile);


# 15 Differenza tra la media del prezzo di vendita dei veicoli e la media del prezzo dei veicoli di un determinato brand; 

select avg(Ammontare_Senza_IVA+Ammontare_Senza_IVA*Aliquota_IVA/100)-
(select avg(Ammontare_Senza_IVA+Ammontare_Senza_IVA*Aliquota_IVA/100) as PrezzoMedioBrand
from Pagamento_Vendita_T, Veicolo_T, vendita_t
where Pagamento_Vendita_T.Id_Vendita = Vendita_t.Id_Vendita and 
Vendita_T.V_Id_Veicolo = Veicolo_t.Id_Veicolo and 
brand = "Toyota") as Differenza
from Pagamento_Vendita_T;


# 16 Differenza tra la somma dei prezzi di listino dei veicoli venduti e la somma dei prezzi di vendita dei rispettivi veicoli; 

select sum(prezzo_listino-(ammontare_senza_iva+ammontare_senza_iva*aliquota_iva/100)) 
as differenza 
from veicolo_t, Vendita_t, Pagamento_Vendita_T
where Veicolo_T.Id_Veicolo = Vendita_T.V_Id_Veicolo and 
Vendita_T.Id_Vendita = Pagamento_Vendita_T.Id_Vendita;


# 17 Quali veicoli sono in deposito da più tempo rispetto alla media. 

create view GiorniDeposito as 
select veicolo_t.id_veicolo, (vendita_t.data_consegna-veicolo_t.data_acquisto) as giorni
from veicolo_t, vendita_t
where veicolo_t.id_veicolo = vendita_t.v_id_veicolo;

select *
from GiorniDeposito
where giorni > (select avg(giorni) from GiorniDeposito);

