OPERAZIONI TECNICHE PRELIMINARI:

1. Nel Terminale: pip install flask
2. Nel Terminale: pip install flask_session
3. aprire il file app.py nella cartella WebApp e inserire la propria password MySQL 
4. Nel Terminale: cambiare la directory inserendo il path della cartella WebApp
5. Nel Terminale: set FLASK_APP=app
6. Nel Terminale: set FLASK_ENV=development
7. Nel Terminale: flask run
8. In un motore di ricerca: http://127.0.0.1:5000

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

NAVIGARE SUL SITO: 

BOTTONE CLIENTE)

Il sito web SunnyMotors permette di concludere operazioni di vendita e noleggio selezionando nella Home iniziale il bottone Cliente in alto.

* In cliente  si richiede di inserire nome, cognome, codice fiscale e V o N che stanno rispettivamente per Vendita e Noleggio. 

In queste righe che seguiranno sarà preso ad esempio il processo di una vendita. 

* Nel caso in cui questo utente non è nel Database si richiede di inserire altre informazioni: via, numero civico, cap, provincia, data nascita, email, telefono. La pagina web avvisa il cliente che i suoi dati sono stati inseriti nel Database. Si avvisa il cliente se è il suo compleanno o meno.

* Successivamente si richiede di inserire il brand e il modello dell'auto che il cliente desidera e sarà visualizzata una tabella con tutti i veicoli disponibili tra cui sarà possibile scegliere il veicolo e concludere l'operazione oppure scegliere un'altra categoria (Per 4 ruote: suv, berlina, sportiva, utilitaria - Per 2 ruote: naked, motocross, sportiva, scooter). 

* Nel primo caso si chiede al cliente se è beneficiario della legge104 e in base alla risposta data (Si o No) sarà applicata una determinata aliquota iva (4% o 22%). 

* In seguito sarà visualizzato il prezzo effettivo del veicolo e sarà chiesto al cliente se vuole procedere all'acquisto oppure no. 
Se si sceglie no, il cliente viene salutato; se invece sceglie sì, sarà chiesto di inserire il metodo di pagamento (Carta di Credito, Contanti, Bonifico, Assegno). 
Una volta inserito il  metodo di pagamento, sarà visualizzato un messaggio che informa che l'operazione è andata a buon fine.

Ora descriviamo il processo di una noleggio. 

* Si richiede all’utente di inserire il brand, il modello del veicolo desiderato e il periodo nel quale vuole noleggiarlo tramite l'inserimento della data d’inizio prenotazione e dal numero di giorni di noleggio. 

* Sarà visualizzata una tabella con tutti i veicoli disponibili tra cui sarà possibile scegliere il veicolo e concludere l'operazione oppure scegliere un'altra categoria (Per 4 ruote: suv, berlina, sportiva, utilitaria - Per 2 ruote: naked, motocross, sportiva, scooter). 

* Nel primo caso saranno mostrate al cliente due tabelle: una contenente le informazioni dei veicolo e l’altra contenente il prezzo effettivo nel noleggio e sarà chiesto al cliente se vuole procedere all'acquisto oppure no. 

* Se si sceglie no, il cliente viene salutato; se invece sceglie sì, sarà chiesto di scegliere la città nella quale vuole riconsegnare l’auto. 

* Una volta scelta la città, sarà visualizzato un messaggio che informa che l'operazione è andata a buon fine.

Possiamo notare che il cliente vuole scegliere di vedere un’altra categoria di auto, e quindi ripetere ciò quante volte vuole.

Infine, si chiede all'utente se vuole inserire una recensione, se si, gli sarà chiesto di dare un voto da 1 a 5 per il dipendente e per i veicoli proposti nel loro complesso. 


Ps: si ricorda che dopo ogni inserimento o visualizzazione di un messaggio bisogna pigiare invia per procedere col passaggio successivo.



BOTTONE ANALITICHE)

Tramite il sito web è possibile  visualizzare gli output delle analitiche, pigiando sulla sezione analitiche in alto a destra. Qui ci sarà la possibilità di scegliere una determinata analitica e in seguito sarà visualizzato l'output della stessa. Se vengono dati in input valori che non sono in database, non viene restituito nessun output.



BOTTONE LA NOSTRA STORIA)

Per visualizzare la storia della concessionaria. 

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

