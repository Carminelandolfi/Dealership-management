# 1 Verificare se il cliente è nel database

select codice_fiscale
from cliente_t
where codice_fiscale = "DFFNHO36V42C587H"; # presente

select codice_fiscale
from cliente_t
where codice_fiscale = "DFFNHO36V42C597H"; # assente


# 2 Se il cliente è nel database, verificare se è un cliente vendita

select v_codice_fiscale
from cliente_vendita_t 
where v_codice_fiscale = "AYYGFF86S30M223A";


# 3 Se il cliente è un cliente vendita, verificare se è un cliente abituale

select a_v_codice_fiscale
from abituale_t 
where a_v_codice_fiscale = "AYYGFF86S30M223A";


# 4 Verificare la disponibilità del veicolo vendita richiesto dal cliente

select id_veicolo 
from veicolo_t, veicolo_vendita_t 
where Veicolo_T.Id_Veicolo = Veicolo_Vendita_T.V_Id_Veicolo and 
disponibile = true and
modello = 'RS 4' and 
brand = 'Audi' and 
tipo = 0 and 
disponibile = True;


# 5 Se il veicolo è disponibile, mostrare tutte le informazioni necessarie

select id_veicolo, prezzo_proposto, colore, anno, chilometri, cavalli, cilindrata, foto 
from veicolo_t, veicolo_vendita_t 
where Id_Veicolo = V_Id_Veicolo and 
disponibile = true 
and modello = 'rs 4' 
and brand = 'audi' 
and veicolo_vendita_t.tipo = 0;


# 6 Se il cliente è abituale, verificare se ci sono promozioni in corso
# NB qui non c’è una verifica sul fatto che il cliente sia abituale o meno poichè nel programmino
# viene mandato in esecuzione solo previa verifica tramite una precedente query

select percentuale_sconto 
from promozione_T 
where brand='audi' and 
modello='rs 4' and 
current_date() between data_inizio and data_fine 
limit 1;


# 7 Se il veicolo non è disponibile oppure non ne vuole nessuno di quelli che gli hai mostrato,
# suggerirne altri dopo aver chiesto se ne vuole uno a due o quattro ruote e a quale categoria è interessato 

# se il veicolo è a due ruote
select id_veicolo, prezzo_proposto, brand, modello, colore, anno, chilometri, cavalli, 
cilindrata, foto 
from Veicolo_T, Veicolo_Vendita_T, V_due_ruote_T 
where Id_Veicolo = V_Id_Veicolo and 
V_Id_Veicolo = D_V_Id_Veicolo and 
Disponibile = true and 
categoria = 'naked' and 
veicolo_vendita_t.tipo = 1;

# se il veicolo è a quattro ruote
select id_veicolo, prezzo_proposto, brand, modello, colore, anno, chilometri, cavalli, 
cilindrata, foto 
from Veicolo_T, Veicolo_Vendita_T, V_quattro_ruote_T 
where Id_Veicolo = V_Id_Veicolo and 
V_Id_Veicolo = Q_V_Id_Veicolo and 
Disponibile = true and 
categoria = 'utilitaria' and 
veicolo_vendita_t.tipo = 0;


# 8 Verificare la disponibilità del veicolo noleggio richiesto dal cliente per determinato periodo 
# NB: vista così potrebbe non avere senso, ma fa parte di un processo più ampio sul programmino

select Veicolo_T.Id_Veicolo,DATEDIff(Data_Consegna,'2000-01-01') as giorni_in, 
DATEDIff(Data_Consegna,'2000-01-01')+Numero_giorni 
from Veicolo_T,Veicolo_Noleggio_T,Noleggio_T 
WHERE veicolo_T.Id_veicolo=Veicolo_Noleggio_T.N_Id_Veicolo and 
Veicolo_Noleggio_T.N_Id_Veicolo=Noleggio_T.N_Id_Veicolo and 
Modello='Edge' 
and tipo=1;


# 9 Se il veicolo è disponibile, mostrare tutte le informazioni necessarie

select Prezzo_Giorno,Colore,Cavalli,cilindrata,foto,anno 
from Veicolo_T,veicolo_Noleggio_T 
Where Veicolo_T.Id_VEicolo=Veicolo_Noleggio_T.N_Id_VEicolo and 
Veicolo_t.Id_veicolo = '19UUA8F22CA833658';


# 10 Se il veicolo non è disponibile, suggerirne altri

# se quattro ruote
select Brand, Modello,Id_Veicolo 
from Veicolo_t,Veicolo_NOleggio_T,N_Quattro_Ruote_T 
where veicolo_T.Id_Veicolo= Veicolo_Noleggio_T.N_Id_Veicolo and 
Veicolo_Noleggio_T.N_Id_Veicolo=N_Quattro_Ruote_T.Q_N_Id_VEicolo and 
categoria = 'sportiva';

# se due ruote
select Brand, Modello,Id_Veicolo 
from Veicolo_t,Veicolo_NOleggio_T,N_Due_Ruote_T 
where veicolo_T.Id_Veicolo= Veicolo_Noleggio_T.N_Id_Veicolo and 
Veicolo_Noleggio_T.N_Id_Veicolo=N_Due_Ruote_T.D_N_Id_VEicolo and 
categoria = 'Motocross';


# 11 Verificare quali dei veicoli suggeriti sono disponibili 
# NB: vista così potrebbe non avere senso, ma fa parte di un processo più ampio sul programmino

select Veicolo_T.Id_Veicolo,DATEDIff(Data_Consegna,'2000-01-01') 
as giorni_in, DATEDIff(Data_Consegna,'2000-01-01')+Numero_giorni 
from Veicolo_T,Veicolo_Noleggio_T,Noleggio_T 
WHERE veicolo_T.Id_veicolo=Veicolo_Noleggio_T.N_Id_Veicolo and 
Veicolo_Noleggio_T.N_Id_Veicolo=Noleggio_T.N_Id_Veicolo 
and tipo=1
and Veicolo_T.Id_Veicolo='WBAXH5C56DD552450';


# 12 Mostrare il prezzo effettivo 

select distinct veicolo_Noleggio_T.N_id_veicolo,prezzo_giorno*10-(prezzo_giorno*9*0.05) as Prezzo
from pagamento_noleggio_t,noleggio_T,veicolo_noleggio_T,cliente_noleggio_T 
where pagamento_noleggio_t.id_noleggio = noleggio_T.id_noleggio and 
noleggio_T.n_id_veicolo=veicolo_noleggio_T.n_id_veicolo and 
noleggio_t.N_codice_fiscale=cliente_noleggio_T.n_codice_fiscale 
and veicolo_noleggio_T.n_id_veicolo = 'WBAXH5C56DD552450';


# 13 Selezionare la concessionaria in cui si trova il veicolo

 select Id_Concessionaria 
 from Concessionaria_T 
 where città= 'Floda';
 
 
# 14 Restituire l'id del dipendente che ha ricevuto le recensioni peggiori
 
create view numrecneg_dip as 
select Dipendente_T.Id_Dipendente, count(Dipendente) as NumRecNeg
from dipendente_t, recensione_t
where Dipendente_T.Id_Dipendente = Recensione_T.Id_Dipendente and
Dipendente in ("Insoddisfatto", "Molto Insoddisfatto")
group by Dipendente_T.Id_Dipendente;
 
select id_dipendente 
from numrecneg_dip  
where numrecneg = (select max(numrecneg) from numrecneg_dip);
