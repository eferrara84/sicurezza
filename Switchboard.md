Title:	Gestione Mail con Switchboard  
Author: Enrico Ferrara, Maura Pintor, Marco Uras
	
Date:	July 31, 2017  

# Switchboard

## Cos’è Switchboard

Switchboard è uno strumento per l’elaborazione di mail tramite un server  
Utilizza dei worker esterni che possono elaborare le mail tramite delle API

## Funzionamento

Switchboard si connette a un indirizzo di posta e consente a degli strumenti software, i Client e i Workers, di connettersi a esso tramite un'interfaccia bidirezionale.

I Client e i Workers possono rimanere in attesa dei messaggi in arrivo sull'indirizzo mail e catturare metadata e contenuto, consentendo di analizzare la posta in arrivo.

## Software necessario

* [Virtualbox](https://www.virtualbox.org/wiki/Downloads) Software per la virtualizzazione
* [Vagrant](https://docs.vagrantup.com/v2/installation/index.html) Gestore di macchine virtuali
* [Ansible](http://docs.ansible.com/intro_installation.html) Motore di automazione che permette di gestire i playbook

## Comandi iniziali switchboard

**vagrant@vagrant-ubuntu-trusty-64:~$service switchboard** 

>Usage: /etc/init.d/switchboard {start|stop|restart|reload|status}  

**vagrant@vagrant-ubuntu-trusty-64:~$ /etc/init.d/switchboard start**
  
>   ...done.  

**vagrant@vagrant-ubuntu-trusty-64:~$ /etc/init.d/switchboard status** 
 
>pong
  
**vagrant@vagrant-ubuntu-trusty-64:~$ /etc/init.d/switchboard stop**
  
>ok  
   ...done
   
## Workers e Clients

Switchboard si configura come un server standalone che si connette a worker e client esterni.

Le interfacce sono bidirezionali, e permettono a processi esterni di ricevere notifiche di nuove email, e di raccogliere maggiori informazioni dalle email stesse.

Switchboard gestisce richieste concorrenti a account IMAP.


I Worker e i Client di Switchboard differiscono per i permessi di accesso:

* I Worker possono elaborare email in tutti gli account in cui Switchboard è connesso. Essi possono far connettere Switchboard a diversi account, e la connessione permane anche alla morte di un worker (a meno che non sia esplicitamente terminata). I comandi sono simili a quelli del client, ma necessitano di un attributo chiave-valore indicante a quale account devono essere applicati.

* I Client possono solo connettersi e interagire con un unico account tramite Switchboard. La connessione dei client è unica e tutti i comandi vengono eseguiti sull’unico account connesso. Se il client possiede l’ultimo riferimento all’account quando questo muore, le connessioni con l’account IMAP vengono chiuse. Le credenziali non vengono mai salvate di default.


## POP e IMAP

POP e IMAP sono le modalità in cui si può configurare l’accesso alla Posta nel programma (client) di posta del computer o nell’app su smartphone e tablet.

Con IMAP (Internet Mail Access Control) i messaggi, sia della cartella Posta in arrivo che di tutte le altre Cartelle, rimangono sul server: sul computer/device mobile ne viene scaricata una copia.

Con la modalità POP (Post Office Protocol), i messaggi saranno prelevati dalla cartella Posta in arrivo del server e scaricati in locale sul PC: sulla Webmail quindi non ci saranno più, a meno che non scelga nel POP l’opzione che permette di conservare una copia dei messaggi sul server.

## SMTP

SMTP è un protocollo relativamente semplice, testuale, nel quale vengono specificati uno o più destinatari di un messaggio, verificata la loro esistenza il messaggio viene trasferito.


## JMAP - Json Meta Application Protocol

JMAP è pensato come nuovo standard per connettere i client email agli store. Il principale scopo è quello di sostituire IMAP + SMTP. JMAP è inoltre strutturato in modo più generico, in modo da poter essere esteso con contatti e calendario. Non rimpiazza le trasmissioni MTA-to-MTA SMTP.

[Link al sito](http://jmap.io/
)

I client di Switchboard hanno un’interfaccia JMAP, e i worker sono basati su questa ma con opportune modifiche.

JMAP definisce una struttura JSON che rappresenta tutte le informazioni necessarie a un client di posta in modo strutturato e consistente.


## Websocket

Un worker o client di Switchboard si connette al server tramite un websocket. Se si usa Switchboard in locale, l’indirizzo URL di default è [ws://192.168.50.2:8000/clients](ws://192.168.50.2:8000/clients).

I dati sono codificati in UTF8 JSON. I comandi del client hanno la sintassi:

[[${method \<string>}, ${args \<object>}, ${tag (optional)}], ...]

$

Il server esegue i comandi in ordine, e genera una lista di risposta per ogni comando, con la stessa forma del comando stesso. 


## Comandi Worker

* **connect**  
Accetta l'host e la porta del server IMAP, insieme a un oggetto di identificazione che è utilizzato per accedere dopo la connessione a un server.  
A connessione avvenuta si ottiene in risposta una conferma dell'accesso avvenuto con successo.

* **watchAll**  
Il comando watchAll configura il server oer inviare al Worker notifiche ogni volta che arriva una mail nella casella osservata.

* **watchMailboxes**  
Questo comando configura il server per creare connessioni IMAP per il set di nomi di caselle di posta elencati. Non fa parte delle specifiche JMAAP. Se il tentativo di connessione fallisce, la risposta sarà una lista di risposte, una per ogni nome di casella. Ogni chiamata di “watchMailboxes” rimpiazza la lista di mailbox monitorate.

* **getMailboxes**  
Restituisce una lista di tutte le mailbox monitorate, con i rispettivi permessi e ruoli.

* **getMessageList**  
Ottiene la lista di messaggi nelle mailbox.

* **getMessages**  
Ricava i messaggi corrispondenti ai messageID elencati in una lista.


## Comandi Client

Diversamente dai comandi Worker, non richiedono un argomento contenente le informazioni dell'account. Il client, invece, deve richiedere la connessione per un account, e da quel momento in poi tutti i comandi saranno applicati a questo.

* **connect**  
Il comando _connect_ del Client è identico a quello del Worker. A connessione avvenuta, non è possibile connettersi ad altri account, e sarà possibile inviare comandi solo per quello richiesto.

* **watchMailboxes**  
Questo comando è simile a quello del Worker, e comunica a Switchboard di inviare notifiche per tutte le mailbox indicate in una lista per l'account richiesto.


* **getMailboxes**  
Restituisce la lista di tutte le mailbox monitorate.

* **getMessageList**  
Analogo a quello del Worker, ottiene la lista di tutti i messaggi presenti nelle mailbox elencate, per l'account monitorato.

* **getMessages**  
Ottiene i messaggi contrassegnati dai messageID presenti nella lista presente nel comando.


## Switchboard + Python

[Repository GitHub] (https://github.com/jtmoulia/switchboard-python)

Installation
============

It's simplest to install this library from PyPi_:

.. code:: bash

    pip install switchboard-python

Dentro la cartella examples si trovano diversi file:

* apnsworker.py
* lamsonworker.py
* listener.py
* twilioworker.py

In particolare, il file [listener.py](https://github.com/jtmoulia/switchboard-python/blob/master/examples/listener.py) contiene il codice per creare un Worker:

>A basic Switchboard worker that will listen for new email notifications. When it receives a notification, it fetches the raw email from Switchboard and parses it using the email module.


Aprendo il file listener.py si possono inserire i dati della casella di posta da monitorare.  
In particolare è da modificare il dizionario CONN_SPEC inserendo i dati:

```python
ACCOUNT = 'tesinasicurezza@gmail.com'  
CONN_SPEC = {'host': 'imap.gmail.com',  
             'port': 993,  
             'auth': {  
                 'type': 'plain',  
                 'username': ACCOUNT,  
                 'password': 'computersecurity'}};  

```

## Creazione di un worker

Prima di creare un worker è necessario avviare il servizio switchboard tramite vagrant.
  
**cd '\<PATH>/switchboard'; vagrant up; vagrant ssh**

E una volta avviata la connessione ssh:

**vagrant@vagrant-ubuntu-trusty-64:~$ service switchboard start**  
>   ...done.

I passaggi appena fatti avviano il servizio Switchboard e attivano il websocket ["ws://192.168.50.2:8080/workers"](ws://192.168.50.2:8080/workers)

Adesso si può eseguire lo script Python:

**cd switchboard-python/examples/
python listener.py**

## Ricezione di una mail

Mandando una mail all'indirizzo "ascoltato", si ottiene sulla console Python il seguente messaggio:

>INFO:\_\_main\_\_:Setup complete, listening...  
INFO:\_\_main\_\_:Subject: Prova_listener, From: XXXX 
\<XXXX@gmail.com>, To: tesinasicurezza@gmail.com

## Modifica per leggere il payload


Per accedere al payload è sufficiente utilizzare la funzione _get\_payload()_ su msg nel metodo _received\_new_ della classe _ListenerWorker_

```python
def received_new(self, msg):
        """
        Called when a new message is received.
        """
        logger.info("Subject: %s, From: %s, To: %s, Payload: %s",
                    msg['subject'], msg['from'], msg['to'], msg.get_payload())
```

Si ottiene il seguente output:

>INFO:\_\_main\_\_:Subject: Messaggio, From: XXXX \<XXXX@gmail.com>, To: tesinasicurezza@gmail.com, Payload: Payload\_messaggio

## Salviamo le mail in un database

Allo scopo di analizzare payload e metadati è stata creata la seguente tabella:

```python

class Mail(Base):
    __tablename__ = "mail"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String)
    sender = Column(String)
    subject = Column(String)
    payload = Column(String)
    datetime = Column(String)
    to = Column(String)
    category = Column(String)

```

Questa tabella è salvata in un database che viene aggiornato ogni volta che si avvia lo script Python.


## Analisi del payload

Nel passaggio seguente sarà creato un sistema per classificare in modo automatico le mail ricevute. Dopo aver raccolto un dataset sufficiente, si può addestrare un sistema di Machine Learning a riconoscere lo spam. I passaggi per la realizzazione sono:

1. Preprocessing dei dati, per esempio eliminazione delle congiunzioni e desinenze delle parole.
2. Creazione di un dizionario per capire le parole "sensibili" per la classificazione.
3. Estrazione delle features, ovvero di vettori binari in cui sono messi a 1 i valori corrispondenti alle parole presenti nella mail.
4. Assegnazione delle etichette alle mail (spam/ham)
5. Addestramento del classificatore

In seguito si potrà utilizzare il modello creato per classificare in modo automatico le mail al momento della ricezione.

Nota: L'analisi del payload sarà fatta utilizzando un dizionario in **Inglese**, stessa lingua delle mail collezionate.

### Preprocessing

Il primo passaggio per l'analisi del testo è solitamente la "pulizia" del testo, in cui sono rimosse le parole che non contengono informazione per la classificazione.
Le mail contengono solitamente numerosi caratteri aggiuntivi come congiunzioni, punteggiatura, parole molto corte, cifre etc. 

Il preprocessing delle mail è stato eseguito nel seguente modo:

* Rimozione di articoli, congiunzioni e parole molto frequenti ma povere di informazione
* Lemmatization, ovvero riduzione delle parole alla radice, per rimuovere plurali, verbi al passato, etc. (esempio "includes", "included" possono essere rappresentate dalla parola "include" senza perdita di significato)
* Rimozione delle non-words come punteggiatura e caratteri speciali


### Creazione del Dizionario

Le mail hanno una lunghezza variabile, che risulta difficile da gestire per un classificatore. Per ottenere vettori di feature di uguale lunghezza per tutte le mail, si utilizza la costruzione di un "lexicon" o dizionario. Si sono analizzate tutte le parole (pre-elaborate) presenti nel dataset di train, e si è costruita una lista contenente tutte queste. La lista è poi stata tagliata ai soli 3000 elementi più frequenti.


```python
def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir,f) for f in os.listdir(train_dir)]    
    all_words = []       
    for mail in emails:    
        with open(mail) as m:
            for i,line in enumerate(m):
                if i == 2:  #Body of email is only 3rd line of text file
                    words = line.split()
                    all_words += words
    
    dictionary = Counter(all_words)
    # Paste code for non-word removal here(code snippet is given below) 
    return dictionary

list_to_remove = dictionary.keys()
for item in list_to_remove:
    if item.isalpha() == False: 
        del dictionary[item]
    elif len(item) == 1:
        del dictionary[item]
dictionary = dictionary.most_common(3000)

```


### Estrazione delle features

Il vettore di features è un contatore, inizialmente un vettore di 3000 zeri, con indici corrispondenti alla lista di parole nel lexicon.

L'estrazione delle features avviene confrontando la stringa di testo del payload della mail con il lexicon. Ogni parola viene esaminata, e se presente nel dizionario il suo contatore viene incrementato di uno.

Si otterrà per ogni mail un vettore lungo quanto il lexicon, che cattura l'informazione sulla presenza/assenza e frequenza di parole "chiave" per la classificazione.

```python
def extract_features(mail_dir): 
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),3000))
    docID = 0;
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID,wordID] = words.count(word)
        docID = docID + 1     
    return features_matrix
```

### Assegnazione delle label

Per utilizzare metodi di classificazione supervisionati, è necessario fornire al classificatore le etichette delle mail presenti nel dataset di train (e anche di test nel caso si voglia ottenere un indice delle prestazioni). Le etichette sono state così definite:

* 0 : email ham
* 1 : email di spam

### Addestramento del classificatore

Per l'addestramento e l'utilizzo del classificatore in Python è possibile utilizzare la libreria open source di machine learning **scikit-learn**. 

Sono stati addestrati due classificatori, rispettivamente un Multinomial Naive Bayes Classifier (MNB) e una Support Vector Machine (SVM). Il primo è molto utilizzato per la classificazione di documenti che assume indipendenza tra ogni coppia di features. L'SVM è invece più efficace quando si hanno molte features, e cerca di trovare un subset dei campioni che individuino degli iper-piani di separazione per la classificazione.


```python

import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.metrics import confusion_matrix 
# Create a dictionary of words with its frequency

train_dir = 'train-mails'
dictionary = make_Dictionary(train_dir)

# Prepare feature vectors per training mail and its labels

train_labels = np.zeros(702)
train_labels[351:701] = 1
train_matrix = extract_features(train_dir)

# Training SVM and Naive bayes classifier

model1 = MultinomialNB()
model2 = LinearSVC()
model1.fit(train_matrix,train_labels)
model2.fit(train_matrix,train_labels)

# Test the unseen mails for Spam
test_dir = 'test-mails'
test_matrix = extract_features(test_dir)
test_labels = np.zeros(260)
test_labels[130:260] = 1
result1 = model1.predict(test_matrix)
result2 = model2.predict(test_matrix)
print confusion_matrix(test_labels,result1)
print confusion_matrix(test_labels,result2)

```


### Test del sistema

Una volta che i classificatori sono stati addestrati, si può testare il sistema per capire la performance. Il test viene fatto in un subset di mail tenuto nascosto al classificatore, che prende il nome di test set. Si estrae il conteggio parole de ogni mail nel test-set e si predice la sua classe di appartenenza (ham/spam). Il risultato è poi confrontato con le etichette vere e viene estratta la matrice di confusione:

|            |  pSpam   |  pHpam  |
|------------|:--------:|:-------:|
| **tSpam**  |    TP    |    FN   |
|  **tHam**  |    FP    |    TN   |

* **TP**: Mail di spam classificate come spam (rifiutate)
* **FN**: Mail di spam classificate come ham (non individuate)
* **FP**: Mail di ham classificate come ham (falsi allarmi)
* **TN**: Mail di ham classificate come ham (accettate)

### Miglioramenti

Il sistema può essere migliorato per ottenere un classificatore più robusto. Tra i miglioramenti applicabili sono presenti:

* Incremento dei dati di train
* Incremento della dimensione del dizionario (più features per ogni mail)
* Utilizzo di altri classificatori
* Migliore scelta dei parametri del classificatore
* Analisi più fine del dizionario per individuare parole di poco significato







