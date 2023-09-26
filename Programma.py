import mysql.connector
import random
from datetime import timedelta, date

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="62662Tm!",
    database="Car_Dealership")
cursor=db.cursor(buffered=True)


# A seconda che il programma sia interrogato da un cliente, un dipendente o un manager, il programma ha funzioni diverse:
# cliente: seguire il processo di vendita o noleggio
# dipendente: fornire analitiche al manager
# manager: licenziare
opzione=int(input("Iserisci 1 se sei un cliente, 2 se sei un dipendente, 3 se sei un manager: "))


if opzione==1:

    # SELEZIONARE UN DIPENDENTE (RANDOMLY) CHE SEGUA IL CLIENTE NEL PROCESSO DI VENDITA O NOLEGGIO
    cursor.execute("select id_dipendente from dipendente_t")
    results = cursor.fetchall()
    dipendente = int(random.choice(list(results))[0])
    print(f"Salve, sono il dipente {dipendente} e La aiuterò nella ricerca del veicolo adatto a Lei.")


    print("Per proseguire dovrà fornire alcune informazioni.")
    nome = input("Inserisca il Suo nome: ")
    cognome = input("Inserisca il Suo cognome: ")
    CF = input("Inserisca il suo Codice Fiscale: ")


    # Chiedere al cliente se intende acquistare o noleggiare un veicolo
    vendita = input("Intendi acquistare o noleggiare un veicolo? Rispondi V se intenti acquistare o N se intendi noleggiare. ")
    tipo = int(input("Un veicolo a due o quattro ruote? Rispondi 2 o 4. "))
    if tipo == 2:
        tipo = 1
    else:
        tipo = 0


    # Q1) VERIFICARE SE IL CLIENTE E' NEL DATABASE
    query1 = f"select codice_fiscale from cliente_t where codice_fiscale = '{CF}'"
    cursor.execute(query1)
    cliente = cursor.fetchall()


    abituale = False
    cl_vend = []


    # SE IL CLIENTE NON E' NEL DATABASE, INSERIRLO
    if len(cliente) == 0:
        print("Ci servono altre informazioni per inserirLa nel DB.")
        via = input("Inserisca la via del Suo indirizzo: ")
        numero_civico = int(input("Inserisca il numero civico del Suo indirizzo: "))
        cap = input("Inserisca il CAP del Suo indirizzo: ")
        provincia = input("Inserisca la Provincia del Suo indirizzo: ")
        data_nascita = input("Inserisca la Sua data di nascita nel seguente formato aaaa-mm-gg: ")
        email = input("Inserisca il Suo indirizzo email: ")
        telefono = input("Inserisca il Suo numero di telefono: ")

        query2=f"insert into Cliente_T (Codice_Fiscale, Nome, Cognome, Via, Numero_Civico, CAP, Provincia, Data_Nascita, Email, Telefono, Vendita, Noleggio) \
        values ('{CF}', '{nome}', '{cognome}', '{via}', {numero_civico}, '{cap}', '{provincia}', '{data_nascita}', '{email}', '{telefono}', false, false)"
        cursor.execute(query2)
        db.commit()


    # INVIARE GLI AUGURI A COLORO CHE COMPIONO GLI ANNI OGGI
    query_extra_auguri = f"select email, telefono \
    from Cliente_T \
    where day(Data_Nascita) = day(current_date()) \
    and month(Data_Nascita) = month(current_date()) \
    and Codice_Fiscale = '{CF}'"
    cursor.execute(query_extra_auguri)
    compl = cursor.fetchall()

    if len(compl) != 0:
        print("Tantissimi auguri da Sunny Motors!")
   

    # !!! VENDITA !!!
    if vendita in ["V", "v"]:

        brand = input("A quale brand sei interessato? ")
        modello = input("A quale modello sei interessato? ")

        id_veicolo_scelto = False
        percentuale_sconto = 0


        # Q2) SE IL CLIENTE E' NEL DATABASE, VERIFICARE SE E' UN CLIENTE VENDITA
        if len(cliente) != 0:
            query2_2=f"select * \
            from cliente_vendita_t \
            where v_codice_fiscale='{CF}'"
            cursor.execute(query2_2)
            cl_vend = cursor.fetchall()


        # Q3) SE IL CLIENTE E' UN CLIENTE VENDITA, VERIFICARE SE E' UN CLIENTE ABITUALE
        if len(cl_vend) != 0:
            query3 = f"select a_v_codice_fiscale \
            from abituale_t \
            where a_v_codice_fiscale = '{CF}'"
            cursor.execute(query3)

                    
            if cursor.execute(query3) != None:
                print("Ottimo. Sei un cliente abituale!")
                abituale = True

        
        # Q4) VERIFICARE LA DISPONIBILITA' DEL VEICOLO RICHIESTO DAL CLIENTE
        query4 = f"select id_veicolo \
        from veicolo_t, veicolo_vendita_t \
        where Veicolo_T.Id_Veicolo = Veicolo_Vendita_T.V_Id_Veicolo and \
        disponibile = true \
        and modello = '{modello}' \
        and brand = '{brand}' \
        and tipo = {tipo} \
        and disponibile = True"
        cursor.execute(query4)
        veicoli = cursor.fetchall()
        #print(veicoli)
        #print(len(veicoli))

        
        # Q5) SE IL VEICOLO E' DISPONIBILE, MOSTRARE TUTTE LE INFORMAZIONI NECESSARIE
        if len(veicoli) != 0:

            query5 = f"select id_veicolo, prezzo_proposto, colore, anno, chilometri, cavalli, cilindrata, foto \
            from veicolo_t, veicolo_vendita_t \
            where Id_Veicolo = V_Id_Veicolo and \
            disponibile = true \
            and modello = '{modello}' \
            and brand = '{brand}' \
            and veicolo_vendita_t.tipo = {tipo}"
            cursor.execute(query5)
            veicoli_disponibili = cursor.fetchall()
            
            #print(veicoli_disponibili)

            for i in range(len(veicoli_disponibili)):
                print(i+1, veicoli_disponibili[i], "\n")
            vuole = input("C'è qualcuno di questi veicoli che desideri acquistare? Rispondere Sì o No. ")
            if vuole in ["Si", "Sì", "si", "sì"]:
                idx = int(input("Quale di questi veicoli desideri? Inserisci il numero. "))

                id_veicolo_scelto = veicoli_disponibili[idx-1][0] 
                print(f"Ottimo, hai scelto il veicolo {id_veicolo_scelto}")
                prezzo_proposto = veicoli_disponibili[idx-1][1]


                # Q6) SE IL CLIENTE E' ABITUALE, VERIFICARE SE CI SONO PROMOZIONI IN CORSO
                if abituale == True:
                    query6 = f"select percentuale_sconto \
                    from promozione_T \
                    where brand='{brand}' and \
                    modello='{modello}' and \
                    current_date() between data_inizio and data_fine \
                    limit 1"
                    cursor.execute(query6)
                    percentuale_sconto = cursor.fetchall()
                    print("Ottimo! C'è uno sconto del {percentiale_sconto}% per te!")


        # Q7) SE IL VEICOLO NON E' DISPONIBILE OPPURE NON NE VUOLE NESSUNO DI QUELLI CHE GLI HAI MOSTRATO, SUGGERIRNE ALTRI
        if len(veicoli) == 0 or vuole not in ["Si", "Sì", "si", "sì"]:
            print("Ci dispiace. Possiamo suggerirLe un altro veicolo?")
            categoria = input("A quale categoria è interessato/a? ")

            if tipo == 1: 
                query7 = f"select id_veicolo, prezzo_proposto, brand, modello, colore, anno, chilometri, cavalli, cilindrata, foto \
                from Veicolo_T, Veicolo_Vendita_T, V_due_ruote_T \
                where Id_Veicolo = V_Id_Veicolo and \
                V_Id_Veicolo = D_V_Id_Veicolo and \
                Disponibile = true and \
                categoria = '{categoria}' and \
                veicolo_vendita_t.tipo = {tipo}"
                cursor.execute(query7)
                veicoli_disponibili = cursor.fetchall()
            else:
                query7 = f"select id_veicolo, prezzo_proposto, brand, modello, colore, anno, chilometri, cavalli, cilindrata, foto \
                from Veicolo_T, Veicolo_Vendita_T, V_quattro_ruote_T \
                where Id_Veicolo = V_Id_Veicolo and \
                V_Id_Veicolo = Q_V_Id_Veicolo and \
                Disponibile = true and \
                categoria = '{categoria}' and \
                veicolo_vendita_t.tipo = {tipo}"
                cursor.execute(query7)
                veicoli_disponibili = cursor.fetchall()

            for i in range(len(veicoli_disponibili)):
                print(i+1, veicoli_disponibili[i], "\n")
            vuole = input("C'è qualcuno di questi veicoli che desideri acquistare? Rispondere Sì o No. ")
            if vuole in ["Si", "Sì", "si", "sì"]:
                idx = int(input("Quale di questi veicoli desideri? Inserisci il numero. "))

                id_veicolo_scelto = veicoli_disponibili[idx-1][0] 
                prezzo_proposto = veicoli_disponibili[idx-1][1]
                brand = veicoli_disponibili[idx-1][2]
                modello = veicoli_disponibili[idx-1][3]

                # Q6) SE IL CLIENTE E' ABITUALE, VERIFICARE SE CI SONO PROMOZIONI IN CORSO 
                if abituale == True:
                    query8 = f"select percentuale_sconto \
                    from promozione_T \
                    where brand='{brand}' and \
                    modello='{modello}' and \
                    current_date() between data_inizio and data_fine \
                    limit 1"
                    cursor.execute(query8)
                    percentuale_sconto = cursor.fetchall()
                    print("Ottimo! C'è uno sconto del {percentiale_sconto}% per te!")
            else:
                print("Ci dispiace non poterLa soddisfare.")


        # Se il cliente vuole uno degli articoli mostrati, chiedere se è beneficiario della legge 104; ...
        if id_veicolo_scelto != False:
            aliquota_iva = False
            iva = input("Sei beneficiario della legge 104? Rispondi Sì o No. ")

            if iva in ["Si", "Sì", "si", "sì"]:
                aliquota_iva = 4

            else:
                aliquota_iva = 22
                

            # ... mostrare il prezzo effettivo; ...
            ammontare_senza_iva = prezzo_proposto # potremmo immaginare anche una fase di contrattazione
            prezzo_effettivo = (float(ammontare_senza_iva)+float(ammontare_senza_iva)*aliquota_iva/100)*(1-percentuale_sconto/100)
            print(f"Il prezzo effettivo di questo veicolo sarebbe {prezzo_effettivo}.")


            # ...chiedere se vuole acquistare il veicolo.
            compra = input("Vuoi procedere all'acquisto? Rispondi Sì o No. ")


            # Se il cliente vuole procedere all'acquisto, chiedere come vuole pagare.
            if compra not in ["Si", "Sì", "si", "sì"]:
                print("Ci dispiace non essere riusciti a soddisfarLa.")

            else:
                metodo_pagamento = input("Perfetto! Come desideri pagare? Puoi scegliere tra: Carta di Credito, Contanti, Bonifico, Assegno. ")


                # AGGIORNARE I DATI NEL DATABASE E INSERIRE I NUOVI DATI
                query9_2=f"update cliente_t \
                set vendita = True \
                where Codice_Fiscale = '{CF}'"
                cursor.execute(query9_2)

                if len(cl_vend) == 0:
                    query9_3=f"insert into Cliente_Vendita_T (V_Codice_Fiscale, Abituale) \
                    values ('{CF}', {abituale})"
                    cursor.execute(query9_3)
                    db.commit()

                query10=f"insert into Vendita_T(Data_Consegna,Data_Ordine,V_Id_Veicolo,Id_Dipendente,V_Codice_Fiscale) values \
                ('{date.today()+timedelta(days=3)}', '{date.today()}','{id_veicolo_scelto}',{dipendente},'{CF}')"
                cursor.execute(query10)
                db.commit() 
                
                query11=f"insert into Pagamento_T (Data_Pagamento,Vendita) \
                values ('{date.today()}', TRUE)"
                cursor.execute(query11)
                db.commit() 

                query_extra=f"select Id_Pagamento \
                from Pagamento_T \
                order by Id_Pagamento DESC \
                limit 1"
                cursor.execute(query_extra)
                Id_Pagamento=cursor.fetchall()

                query_extra2=f"select Id_Vendita \
                from Vendita_T \
                order by Id_Vendita DESC \
                limit 1"
                cursor.execute(query_extra2)
                Id_Vendita=cursor.fetchall()

                query12=f"insert into Pagamento_Vendita_T(V_Id_Pagamento,Ammontare_Senza_Iva,Aliquota_Iva,Metodo_Pagamento,Id_Vendita) values \
                ('{Id_Pagamento[0][0]}', {ammontare_senza_iva}, {aliquota_iva},'{metodo_pagamento}','{Id_Vendita[0][0]}')"
                cursor.execute(query12)
                db.commit() 

                query13=f"update veicolo_t \
                set disponibile = False \
                where V_Id_Veicolo = '{id_veicolo_scelto}'"

                print("Ottimo! Operazione andata a buon fine!")
                


    # !!! NOLEGGIO !!!
    else:
        # Chiediamo informazioni ruguardante il noleggio
        
        data="2000-01-01"
        brand = input("A quale brand è interessato? ")
        modello = input("A quale modello è interessato? ") 
        data_consegna=input("Quando vuole noleggiralo? Inserica una data nel formato aaaa-mm-gg. ")
        numero_giorni= int(input("Per quanti giorni vuole noleggiarlo? "))
        data_ordine=date.today()

        # Q8) VERIFICA DELLA DISPONIBILITA' DEL VEICOLO NOLEGGIO RICHIESTO DAL CLIENTE
        # Utilizzo sia python che sql per farlo
        verifica=f"select DATEDIff('{data_consegna}','{data}') as giorni_in, DATEDIff('{data_consegna}','{data}')+'{numero_giorni}'"
        #Questa query prende il numero di giorni dal 1 gennaio del 2000 e poi un'altra colonna che a questa data aggiunge il numero di giorni di noleggio.
        cursor.execute(verifica)
        verifica_2=cursor.fetchall()

        # Questa query prende per il modello richiesto l'intervallo della data di consegna e data restituzione il numero di giorni
        # dal 1 gennaio 2000, In questo modo abbiamo in termini di numeri di giorni gli intervalli.
        query20 = f"select Veicolo_T.Id_Veicolo,DATEDIff(Data_Consegna,'{data}') as giorni_in, DATEDIff(Data_Consegna,'{data}')+Numero_giorni \
        from Veicolo_T,Veicolo_Noleggio_T,Noleggio_T \
        WHERE veicolo_T.Id_veicolo=Veicolo_Noleggio_T.N_Id_Veicolo and \
        Veicolo_Noleggio_T.N_Id_Veicolo=Noleggio_T.N_Id_Veicolo and \
        Modello='{modello}' \
        and tipo='{tipo}'"
        cursor.execute(query20)
        veicoli=cursor.fetchall()
        veicoli_disponibili=list()
        #print("lunghezza:",len(veicoli))
        y=list(range(int(verifica_2[0][0]),int(verifica_2[0][1])))
        #print(f"y:{y}")
        # Veicoli contiene quindi tutti gli intervalli di prenotazione in numero di giorni rispetto al 1 gennaio 2000
        for i in veicoli:
            if i[0] not in veicoli_disponibili:
              veicoli_disponibili.append(i[0])
        i=0
        # Tramite questo while andiamo a verificare quali veicoli sono disponibili con i relativi intervalli
        while i<len(veicoli): 
          h=False
          x=list(range(int(veicoli[i][1]),int(veicoli[i][2])+1))
          for j in x:
            if j in y: 
              v=veicoli[i]
              for q in range(len(veicoli_disponibili)):
                if v[0]==veicoli_disponibili[q]:
                    del(veicoli_disponibili[q])
                    break
          i+=1
        # Ora siccome ci potrebbe essere lo stesso veicolo prenotato più volte vado a prendere solo gli id_veicoli diversi
        # dalla lista veicoli e l'inserisco in veicoli_disponibili.
        # Se veicoli_disponibili contiene elementi allora vuol dire che abbiamo veicoli disponibili per quell'intervallo
        if len(veicoli_disponibili)!=0:
            print("Il veicolo è disponibile")
            
            # Q9) SE IL VEICOLO E' DISPONIBILE, MOSTRARE TUTTE LE INFORMAZIONI NECESSARIE

            # Con python ho un problema riguardo le tuple con un solo elemento, perchè python mette il valore
            # e aggiunge una virgola, e su sql questo ds errore, quindi mi sono separato i due casi.
            # Qui gestisco quando c'è un solo veicolo disponibile

            if len(veicoli_disponibili)==1:
                query21=f"select Prezzo_Giorno,Colore,Cavalli,cilindrata,foto,anno \
                from Veicolo_T,veicolo_Noleggio_T \
                Where Veicolo_T.Id_VEicolo=Veicolo_Noleggio_T.N_Id_VEicolo and \
                Veicolo_t.Id_veicolo = '{veicoli_disponibili[0]}'"
        
            else:
               # qui gestisco quando ho più veicoli disponibili
               veicoli_disponibili=tuple(veicoli_disponibili)
               # siccome sql vuole che diamo in input una tupla ho trasfromato la lista in una tupla
               
               query21="select Prezzo_Giorno,Colore,Cavalli,cilindrata,foto,anno \
               from Veicolo_T,veicolo_Noleggio_T \
               Where Veicolo_T.Id_VEicolo=Veicolo_Noleggio_T.N_Id_VEicolo and \
               Veicolo_t.Id_veicolo in {}".format(veicoli_disponibili)
            # la query 21 è la stessa e mi danno tutte le informazioini che servono al cliente per poter
            # effettuare una scelta nel modo migliore
            cursor.execute(query21)
            informazioni=cursor.fetchall()
            # Faccio l'uotput formattato
            Valori=["Prezzo_Giorno","Colore","Cavalli","Cilindrata","foto","anno"]
            for i in range(len(informazioni)):

                print(i+1,"\n")
                for j in range(len(informazioni[i])):
                    print(Valori[j],":",informazioni[i][j],"\n")
                print("\n")
            
            
            print("Quale vuole acquistare? ")
            # Chiedo di scegliere quale veicolo vuole, e digitare 0 se non vuole noleggiare il veicolo.
            auto=int(input(f"Inserisca un valore da 1 a {len(veicoli_disponibili)}(0 per non noleggiarlo): "))
            # Qui creo questa variabile caso perchè mi serve per gestire la conclusione della trattativa
            
            if auto==0:
              caso=0
            else:
                veicoli_disponibili=veicoli_disponibili[auto-1]
                caso=1

                
        # Q10) SE IL VEICOLO NON E' DISPONIBILE, SUGGERIRNE ALTRI
        else:
            print("Il veicolo non è disponibile.")
            # Creo caso e cont perchè caso serve per gestire la coclusione della trattativa,cont per
            caso=0
            cont=0
            veicoli_disponibili=[]
            categoria=input("Possiamo suggerirLe altri veicoli. Inserisca la categoria alla quale è interessato. ")
            if tipo==0:
              
              # Questa query prende tutti i veicoli di quella categoria richiesta e in base al tipo
              query22=f"select Brand, Modello,Id_Veicolo \
              from Veicolo_t,Veicolo_NOleggio_T,N_Quattro_Ruote_T \
              where veicolo_T.Id_Veicolo= Veicolo_Noleggio_T.N_Id_Veicolo and \
              Veicolo_Noleggio_T.N_Id_Veicolo=N_Quattro_Ruote_T.Q_N_Id_VEicolo and \
              categoria = '{categoria}' \
              and tipo='{tipo}'"
            
            else:  
                query22=f"select Brand, Modello,Id_Veicolo \
                from Veicolo_t,Veicolo_NOleggio_T,N_Due_Ruote_T \
                where veicolo_T.Id_Veicolo= Veicolo_Noleggio_T.N_Id_Veicolo and \
                Veicolo_Noleggio_T.N_Id_Veicolo=N_Due_Ruote_T.D_N_Id_VEicolo and \
                categoria = '{categoria}' \
                and tipo='{tipo}'"

            cursor.execute(query22)
            veicoli_stessa_categoria=cursor.fetchall()
            print("I veicoli disponibili sono: ")

            # Q11) VERIFICARE QUALI DI QUESTI VEICOLI SONO DISPONIBILI

            # Anche qui lo faccio tramite sql e python
            # Questo quesry nel for serve a prendere tutti gli intervalli in numero di giorni per quel
            # veicolo
            for brand,modello,Id_Veicolo in veicoli_stessa_categoria:
                query20 = f"select Veicolo_T.Id_Veicolo,DATEDIff(Data_Consegna,'{data}') as giorni_in, DATEDIff(Data_Consegna,'{data}')+Numero_giorni \
                from Veicolo_T,Veicolo_Noleggio_T,Noleggio_T \
                WHERE veicolo_T.Id_veicolo=Veicolo_Noleggio_T.N_Id_Veicolo and \
                Veicolo_Noleggio_T.N_Id_Veicolo=Noleggio_T.N_Id_Veicolo and \
                Veicolo_T.Id_Veicolo='{Id_Veicolo}'"
                cursor.execute(query20)
                veicoli_categoria=cursor.fetchall()
                disp=list()
                y=list(range(int(verifica_2[0][0]),int(verifica_2[0][1])))
                #print(f"y:{y}")
                # Veicoli contiene quindi tutti gli intervalli di prenotazione in numero di giorni rispetto al 1 gennaio 2000
                for i in veicoli_categoria:
                    if i[0] not in veicoli_disponibili:
                      veicoli_disponibili.append(i[0])
                i=0
                # Tramite questo while andiamo a verificare quali veicoli sono disponibili con i relativi intervalli
                while i<len(veicoli_categoria): 
                  h=False
                  x=list(range(int(veicoli_categoria[i][1]),int(veicoli_categoria[i][2])+1))
                  for j in x:
                    if j in y: 
                      v=veicoli_categoria[i]
                      for q in range(len(veicoli_disponibili)):
                        if v[0]==veicoli_disponibili[q]:
                            del(veicoli_disponibili[q])
                            break
                  i+=1    
               
                
                # Se in disp ci sono elementi vuol dire che quel veicolo è disponibile, perchè per ogni
                # iterazione del ciclo for ricreo disp come una lista vuota
            for i in veicoli_disponibili:
                    # Q9) SE IL VEICOLO E' DISPONIBILE, MOSTRARE TUTTE LE INFORMAZIONI NECESSARIE
                    
                    # Qui mostro per i veicoli disponibili le informormazioni per permettere al cliente di scegliere nel modo migliore il veicolo da noleggiare
                    query21=f"select Prezzo_Giorno,Colore,Cavalli,cilindrata,foto,anno \
                    from Veicolo_T,veicolo_Noleggio_T \
                    Where Veicolo_T.Id_VEicolo=Veicolo_Noleggio_T.N_Id_VEicolo and \
                    Veicolo_t.Id_veicolo = '{i}'"
                    cursor.execute(query21)
                    ris21=cursor.fetchall()
                    # Faccio l'uotput formattato
                    Valori=["Prezzo_Giorno","Colore","Cavalli","Cilindrata","foto","anno"]
                    cont+=1
                    print(cont,"\n")
                    print(i)
                    for i in range(len(ris21)):

                       for j in range(len(ris21[i])):
                         print(Valori[j],":",ris21[i][j],"\n")
                       print("\n")
        
            # se cont==0 allora non abbiamo veicoli disponibili e poi salutiamo il cliente perchè caso è uguale a 0
            if cont==0:
                    print(f"Purtroppo non abbiamo per la catgoria '{categoria}' non abbiamo veicoli disponibili. ")
            # altrimneti facciamo scegliere al cliente il veicolo
            else:
                    print("Quale veicolo intende scegliere? ")
                    auto=int(input(f"Inserisca un numero da 1 a {cont},(0 se non vuole noleggiarlo): "))
                    caso=1
                    # se digita 0 non acquista nessun veicolo
                    if auto==0:
                        print("E' stato un piacere, arrivederci")
                    else:
                        veicoli_disponibili=[veicoli_disponibili[auto-1]][0]
                        # se sceglie caso diventa =2 così completiamo il processo di noleggio
                        caso=2
                        
        if caso==0:
            print("E' stato un piacere, arrivederLa")
        else:
            caso=2
                      
                      
        #  Se il noleggio è per 7+ giorni c’è uno sconto del 5%, per 30+ giorni c’è uno sconto del 10%,
        #  restituire la stringa “C’è una promozione per te!
        if caso==2:
            if 7<=numero_giorni<29:
                print("Abbiamo una promozione per lei, ha uno sconto del 5%")
                sconto=0.05
            elif numero_giorni>=30:
                print("Abbiamo una promozione per lei, ha uno sconto del 10%")
                sconto=0.10
            else:
                sconto=0
                    
            # Q12) MOSTRARE IL PREZZO EFFETTIVO DEL VEICOLO.
            # Una volta scelto il veicolo mostriamo il prezzo effettivo del noleggio tramite una query
            query24=f"select distinct veicolo_Noleggio_T.N_id_veicolo,prezzo_giorno*'{numero_giorni}'-(prezzo_giorno*'{numero_giorni}'*'{sconto}')\
                from pagamento_noleggio_t,noleggio_T,veicolo_noleggio_T,cliente_noleggio_T \
                where pagamento_noleggio_t.id_noleggio = noleggio_T.id_noleggio and \
                noleggio_T.n_id_veicolo=veicolo_noleggio_T.n_id_veicolo and \
                noleggio_t.N_codice_fiscale=cliente_noleggio_T.n_codice_fiscale \
                and veicolo_noleggio_T.n_id_veicolo = '{veicoli_disponibili}'"

            cursor.execute(query24)
            prezzi=cursor.fetchall()
            # Qui formattiamo l'outuput con i prezzi dei veicoli
            cont=0
            print("Il prezzo del veicolo è: ""\n")
            print(prezzi[0][1],"\n")
            
            
            
            N_Id_Veicolo=veicoli_disponibili
            prezzo_noleggio=prezzi[0][1]
            # Chiediamo in qualke città vuole consegnare il veicolo successivamente
            print("In quale città vuole consegnare l'auto? ")
            città_2="select città \
            from Concessionaria_t"
            cursor.execute(città_2)
            città=cursor.fetchall()
            # mostro un elenco delle città  e le numero in modo tale da capire in  quale città vuole riconsegnare
            cont=0
            for i in città:
                cont+=1
                print(cont,"\n")
                for j in i:
                    print(j,"\n")
                print("\n")
                    
            numero_restituzione=int(input(f"Inserisca un numero da 1 a {cont}: "))
            Luogo_Restituzione=città[numero_restituzione-1][0]
                
                
               
                # INSERIRE O MODIFICARE I DATI
                # verifico se il cliente ha già effettuato un noleggio nel passato
                # altrimenti lo aggiu ngo nella tabella cliente_noleggio_T
            query36=f"select N_Codice_Fiscale \
            from Cliente_Noleggio_T \
            where N_Codice_Fiscale ='{CF}'"
            cursor.execute(query36)
            ris36=cursor.fetchall()
            if len(ris36) == 0:
                query37=f"insert into Cliente_Noleggio_T(N_Codice_Fiscale) \
                values ('{CF}')"
                cursor.execute(query37)
                db.commit()
                    
            # Inserisco i dati riguardanti il noleggio
            query25=f"insert into Noleggio_T(Data_Consegna,Data_ordine,Numero_Giorni,Luogo_Restituzione,Id_Dipendente,N_Id_Veicolo,N_Codice_Fiscale) \
            values ('{data_consegna}','{data_ordine}',{numero_giorni},'{Luogo_Restituzione}',{dipendente},'{N_Id_Veicolo}','{CF}')" 
            cursor.execute(query25)
            db.commit()
            
            # Aggiornare la concessionaria nella quale si trova il veicolo
            # qui prendo l'id della concessionaria
            query26=f"select Id_Concessionaria \
            from Concessionaria_T \
            where città= '{Luogo_Restituzione}'"
            cursor.execute(query26)
            ris26=cursor.fetchall()
          
            # Qui aggiorno il luogo di restituzione
            
            query27=f"update Veicolo_T \
            set Id_Concessionaria= {ris26[0][0]} \
            where Id_Veicolo= '{N_Id_Veicolo}'"
            cursor.execute(query27)
            db.commit()
            # prendo l'ultimo id_Noleggio del noleggio effettuato
            query28=f"select Id_noleggio \
            from Noleggio_T \
            order by Id_Noleggio DESC \
            limit 1 "
            cursor.execute(query28)
            Id_Noleggio=cursor.fetchall()
            
            # inserisco i dati sul pagamento
            query29=f"insert into Pagamento_T(Data_Pagamento,Vendita) \
            values('{data_ordine}',0)"
            cursor.execute(query29)
            db.commit()
            # Prendo l'id_pagamento 
            query30=f" select Id_Pagamento \
            from Pagamento_T \
            order by Id_Pagamento DESC \
            limit 1"
            cursor.execute(query30)
            Id_Pagamento=cursor.fetchall()
            # Inseirsco i valori relativi al pagamento
            query31=f"insert into Pagamento_Noleggio_T(N_Id_Pagamento,Id_Noleggio,Ammontare) \
            values('{Id_Pagamento[0][0]}','{Id_Noleggio[0][0]}','{prezzo_noleggio}')"
            cursor.execute(query31)
            db.commit()

    # Chiedere al cliente se vuole lasciare una recensione
    recensione=input("Vuole lasciare una recensione? Rispondi Sì o No: ")
    if recensione in ["Si", "Sì", "si", "sì"]:
        Dipendente= int(input("Dia un voto al servizio clienti offerto dal dipendente da 1 a 5: "))
        Veicoli= int(input("Dia un voto ai veicoli offerti dalla concessionaria da 1 a 5: "))

        if Dipendente==1:
            Dipendente="Molto Insoddisfatto"
        elif Dipendente==2:
            Dipendente="Insoddisfatto"
        elif Dipendente==3:
            Dipendente="Nè Soddisfatto Nè Insoddisfatto"
        elif Dipendente==4:
            Dipendente="Soddisfatto"
        else:
            Dipendente="Molto Soddisfatto"
        if Veicoli==1:
            Veicoli="Molto Insoddisfatto"
        elif Veicoli==2:
            Veicoli="Insoddisfatto"
        elif Veicoli==3:
            Veicoli="Nè Soddisfatto Nè Insoddisfatto"
        elif Veicoli==4:
            Veicoli="Soddisfatto"
        else:
            Veicoli="Molto Soddisfatto"


        # INSERIRE I DATI RELATIVI ALLA RECENSIONE
        query32=f"insert into Recensione_T(Data_Recensione,Dipendente,Veicoli,Codice_Fiscale,Id_Dipendente) \
        values('{data_ordine}','{Dipendente}','{Veicoli}','{CF}','{dipendente}')"
        cursor.execute(query32)
        db.commit()
        
        print("Grazie! La Sua opinione conta!")
    else:
        print("Arrivederci")
        
    

elif opzione==2:
    ## QUERY ANALITICHE

    print("1.	Elencare marca e modello di auto prelevate nella **città**, nel periodo **periodo** ")
    print("2.	Calcolare il numero totale di noleggi e acquisti di veicoli a **tipo** ruote ")
    print("3.	Visualizzare nome, cognome e id dei clienti che hanno noleggiato più di 3+ un’auto **categoria** ")
    print("4.	Visualizzare la marca di automobile con il maggior numero di noleggi da parte dei clienti che hanno più di 60 anni ")
    print("5.	Id dei dipendenti che nel 2022 hanno ricevuto più provvigioni ")
    print("6.	Verificare se ai clienti a cui sono state inviate le e-mail (promozionale) poi hanno effettivamente acquistato veicolo ")
    print("7.	Visualizzare gli ID di singoli clienti, il numero degli ordini effettuati per vendita o noleggio ")
    print("8.	Restituire le foto del primo veicolo acquistato da un cliente **cliente** ")
    print("9.	Visualizzare il preventivo del noleggio dei veicoli del **brand** per 5 giorni ")
    print("10.	Restituire ID dei dipendenti che hanno ricevuto il maggior numero di recensioni positive (Soddisfatto, Molto Soddisfatto) ")
    print("11.	Restituire ID dei dipendenti che hanno ricevuto il maggior numero di recensioni negative (Insoddisfatto, Molto Insoddisfatto) ")
    print("12.	Restituire ID delle concessionarie i cui veicoli hanno ricevuto il maggior numero di recensioni positive (Soddisfatto, Molto Soddisfatto) ")
    print("13.  Inviare gli auguri ai clienti che oggi compiono gli anni")
    print("14.  Visualizzare la concessionaria che ha fatto più vendite nel periodo **periodo**, specificando ID concessionaria e numero di vendite")
    print("15.	Differenza tra la media del prezzo di vendita dei veicoli e la media del prezzo dei veicoli del brand **brand**")
    print("16.	Differenza tra la somma dei prezzi di listino dei veicoli venduti e la somma dei prezzi di vendita dei rispettivi veicoli ")
    print("17.	Quali veicoli sono in deposito da più tempo rispetto alla media ")

    print("Quale query vuoi eseguire? ")
    numero=int(input("Inserisci un numero da 1 a 17: "))

    if numero==1:
        città=input("Dare città: ")
        data_inizio=input("Inserire data di inizio periodo (es. aaaa-mm-gg): ")
        data_fine=input("Inserire data di fine periodo (es. aaaa-mm-gg): ")
        query40=f"select brand,modello \
        From Veicolo_Noleggio_T,Noleggio_T,Veicolo_T,Concessionaria_T \
        WHERE Veicolo_Noleggio_T.N_Id_veicolo= Noleggio_T.N_Id_Veicolo and \
        Veicolo_T.Id_Concessionaria=Concessionaria_T.Id_Concessionaria and \
        Veicolo_T.Id_Veicolo =Veicolo_Noleggio_T.N_Id_Veicolo and \
        Città='{città}' and \
        Data_Consegna Between '{data_inizio}' and '{data_fine}' "
        cursor.execute(query40)
        ris40=cursor.fetchall()
        c=0
        for i in ris40:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==2:
        tipo=int(input("Inserire 2 per veicoli a due ruote, 4 per veicoli a quattro ruote: "))
        if tipo==2:
            tipo=1
        else:
            tipo=0
        query41=f"select * \
        from (Select count(vendita_t.V_Id_Veicolo) as Vendita_Tipo_1 \
              from vendita_T,veicolo_vendita_t \
        where (vendita_T.V_Id_Veicolo = veicolo_vendita_t.V_Id_Veicolo) and \
        veicolo_vendita_t.tipo='{tipo}') as t ,(Select count(noleggio_t.N_id_veicolo) as Noleggio_Tipo_1 \
        from noleggio_T,veicolo_noleggio_T \
        where  (noleggio_t.N_Id_Veicolo = veicolo_noleggio_t.N_Id_Veicolo) and veicolo_noleggio_t.tipo='{tipo}' \
        ) as t_2 "
        cursor.execute(query41)
        ris41=cursor.fetchall()
        c=0
        for i in ris41:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==3:
        categoria=input("Inserire categoria auto (suv,berlina,sportiva,utilitaria) : ")
        query42=f"select nome,cognome, codice_fiscale \
        from (select nome, cognome, codice_fiscale, count(Noleggio_T.N_Id_Veicolo) as NumNoleggi \
              from cliente_t, noleggio_t, N_Quattro_Ruote_T \
              where Noleggio_T.N_Codice_Fiscale = Cliente_T.Codice_Fiscale and \
              Noleggio_T.N_Id_Veicolo = N_Quattro_Ruote_T.Q_N_Id_Veicolo and \
              N_Quattro_Ruote_T.Categoria = '{categoria}' \
              group by Cliente_T.Codice_Fiscale) as Noleggi \
        where NumNoleggi > 2"
        cursor.execute(query42)
        ris42=cursor.fetchall()
        c=0
        for i in ris42:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==4:

        query43="Select * \
        FROM Query4 \
        WHERE Num_Noleggi=(select Max(Num_Noleggi) FROM Query4) "
        cursor.execute(query43)
        ris43=cursor.fetchall()
        c=0
        for i in ris43:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
            
    elif numero==5:
        query44=f"select * \
        from Provvigioni \
        where Provvigioni = (select max(Provvigioni) from Provvigioni) "
        cursor.execute(query44)
        ris44=cursor.fetchall()
        c=0
        for i in ris44:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==6:
        query45=f"select Promozione_T.Id_Promozione, Abituale_Promozione_T.A_V_Codice_Fiscale, Vendita_T.Id_Vendita \
        from Promozione_T, Abituale_Promozione_T, Vendita_T \
        where Promozione_T.Id_Promozione = Abituale_Promozione_T.Id_Promozione and  \
        Abituale_Promozione_T.A_V_Codice_Fiscale = Vendita_T.V_Codice_Fiscale and \
        Data_Ordine between Promozione_T.Data_Inizio and Promozione_T.Data_Fine "
        cursor.execute(query45)
        ris45=cursor.fetchall()
        c=0
        for i in ris45:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==7:
        tipo=input("Inserisci Vendita o Noleggio: ")
        if tipo in ["Vendita","vendita"]:
            query46=f"select codice_fiscale, count(Vendita_T.Id_Vendita) as Numero_Ordini \
            from cliente_t, vendita_t \
            where codice_fiscale = vendita_t.v_codice_fiscale  \
            group by codice_fiscale"
        
        elif tipo in ["Noleggio", "noleggio"]:
            query46=f"select codice_fiscale, count(Noleggio_T.Id_Noleggio) as Numero_Ordini \
            from cliente_t, Noleggio_T \
            where codice_fiscale = noleggio_t.n_codice_fiscale \
            group by codice_fiscale "
        cursor.execute(query46)
        ris46=cursor.fetchall()
        c=0
        for i in ris46:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==8:
        Codice_Fiscale=input("Inserisci codice Fiscale: ")
        query47=f"select id_veicolo, foto \
        from Veicolo_T, Vendita_T, Cliente_VEndita_T \
        where Veicolo_T.Id_Veicolo = Vendita_T.V_Id_Veicolo and \
        Cliente_Vendita_T.V_Codice_Fiscale= '{Codice_Fiscale}' and \
        Data_Ordine = (select min(Data_Ordine) from Vendita_T,Cliente_Vendita_T \
                       where Cliente_VEndita_T.V_Codice_Fiscale=Vendita_T.V_Codice_Fiscale and \
                       Cliente_Vendita_T.V_Codice_Fiscale='{Codice_Fiscale}') "
        cursor.execute(query47)
        ris47=cursor.fetchall()
        c=0
        for i in ris47:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==9:
        brand=input("Scegliere il brand: ")
        numero_giorni=int(input("Inserire numero giorni: "))
        query48=f"select Id_Veicolo, Prezzo_Giorno*'{numero_giorni}' as PReventivo \
        from Veicolo_T, Veicolo_Noleggio_T \
        where Veicolo_T.Id_Veicolo = Veicolo_Noleggio_T.N_Id_Veicolo and \
        Brand = '{brand}'"
        cursor.execute(query48)
        ris48=cursor.fetchall()
        c=0
        for i in ris48:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==10:
        query49=f"select * \
        from NumeroRecensioniPositive_Dip \
        where NumRecPos = (select max(NumRecPos) from NumeroRecensioniPositive_Dip) "
        cursor.execute(query49)
        ris49=cursor.fetchall()
        c=0
        for i in ris49:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==11:
        query50=f"select * \
        from NumeroRecensioniNegative_Dip \
        where NumRecNeg = (select max(NumRecNeg) from NumeroRecensioniNegative_Dip) "
        cursor.execute(query50)
        ris50=cursor.fetchall()
        c=0
        for i in ris50:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==12:
        query51=f"select Id_Concessionaria \
        from NumeroRecensioniPositive_Conc \
        where NumRecPos = (select max(NumRecPos) from NumeroRecensioniPositive_Conc) "
        cursor.execute(query51)
        ris51=cursor.fetchall()
        c=0
        for i in ris51:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==13:
        query56=f"select Nome, Cognome, email, telefono \
        from Cliente_T \
        where day(Data_Nascita) = day(current_date()) and month(Data_Nascita) = month(current_date())"
        cursor.execute(query56)
        ris52=cursor.fetchall()
        c=0
        for i in ris56:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==14:
        periodo=input("Inserire stagione: ")
        periodo=periodo.capitalize()
        if periodo=="Estate":
            Query_54=f"select * \
            from PeriodoEstivo \
            where NumeroVendite = (select max(NumeroVendite) from PeriodoEstivo) "
        elif periodo=="Inverno":
            Query_54=f"select * \
                from PeriodoInvernale \
                where NumeroVendite = (select max(NumeroVendite) from PeriodoInvernale) "
        elif periodo=='Autunno':
           Query_54=f"select * \
                from PeriodoAutunnale \
                where NumeroVendite = (select max(NumeroVendite) from PeriodoAutunnale) "
        elif periodo=="Primavera":
            Query_54="select * \
                from PeriodoPrimaverile \
                where NumeroVendite = (select max(NumeroVendite) from PeriodoPrimaverile) "
        cursor.execute(Query_54)
        ris54=cursor.fetchall()
        c=0
        for i in ris54:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==15:
        brand=input("Inserire il brand desiderato: ")
        query53=f"select avg(Ammontare_Senza_IVA+Ammontare_Senza_IVA*Aliquota_IVA/100)-(select avg(Ammontare_Senza_IVA+Ammontare_Senza_IVA*Aliquota_IVA/100) as PrezzoMedioBrand \
        from Pagamento_Vendita_T, Veicolo_T, vendita_t \
        where Pagamento_Vendita_T.Id_Vendita = Vendita_t.Id_Vendita and \
        Vendita_T.V_Id_Veicolo = Veicolo_t.Id_Veicolo and \
        brand = '{brand}') as Differenza \
        from Pagamento_Vendita_T "
        cursor.execute(query53)
        ris53=cursor.fetchall()
        c=0
        for i in ris53:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")
    elif numero==16:
        query54=f"select sum(prezzo_listino-(ammontare_senza_iva+ammontare_senza_iva*aliquota_iva/100)) \
        as differenza \
        from veicolo_t, Vendita_t, Pagamento_Vendita_T \
        where Veicolo_T.Id_Veicolo = Vendita_T.V_Id_Veicolo and \
        Vendita_T.Id_Vendita = Pagamento_Vendita_T.Id_Vendita"
        cursor.execute(query54)
        ris54=cursor.fetchall()
        c=0
        for i in ris54:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")

            

    elif numero==17:
        query55=f"select * \
        from GiorniDeposito \
        where giorni > (select avg(giorni) from GiorniDeposito) "
        cursor.execute(query55)
        ris55=cursor.fetchall()
        c=0
        for i in ris55:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")

            
elif opzione==3:
    
    
#### DIPENDENTE

# RESTITUIRE L'ID DEL DIPENDENTE CHE HA RICEVUTO LE RECENSIONI PEGGIORI.

    query15 = f"select id_dipendente \
    from numrecneg_dip  \
    where numrecneg = (select max(numrecneg) from numrecneg_dip)"
    cursor.execute(query15)
    ris15=cursor.fetchall()
    c=0
    for i in ris15:
            c+=1
            print(c)
            for j in i:
                print(j,"\n")
            print("\n")


#fatto da Carmine, Mariapia, Francescoantonio
