# Thesis
Tesi di laurea triennale in ingegneria informatica

## TITOLO: 
Tool per lo studio dell’attività di ricerca in ambito di sicurezza informatica in Italia

## ABSTRACT: 
La bibliometria usa tecniche matematiche e statistiche per analizzare la distribuzione 
delle pubblicazioni scientifiche e l’impatto sulla comunità scientifica fornendo indicatori che 
permettono di valutare il rendimento di un gruppo di ricerca. L’obiettivo di questa tesi è la 
costruzione di un tool per la raccolta di dati bibliometrici utili ad analisi volte all’identificazione dei 
centri di ricerca più attivi in Italia nel campo della sicurezza informatica. L’implementazione utilizza 
tecniche avanzate di Natural Language Processing (NLP) per l’estrapolazione delle informazioni 
dalle pubblicazioni scientifiche coinvolte.

# PROCEDURA PER L'ESECUZIONE:
## ESTRAPOLAZIONE DATI
1. Installare Python 3.7 
2. Intallare PIP e VirtualEnv
  ```
  # installing PIP
  py -m pip --version
  py -m pip install --upgrade pip

  # Installing virtualenv
  py -m pip install --user virtualenv
  
  # Creating a virtual environment
  py -m venv env
  ```
3. Spostarsi sulla cartella e attivare il virtual environment
```
cd C:\Users\Jacopo\Desktop\Sec_tool\sec_tool-master
.\env\Scripts\activate
```
4. Installare le librerie
```
pip install -r requirements.txt
```
5. Installare MongoDB
6. Configurare Scopus fornendo una API key valida
```
python
import pybliometrics
pybliometrics.scopus.utils.create_config()
```
5. Avvio lo script per scaricare i dati:
```
py Avvio.py
```

## ANALISI DATI
1. Installo le librerie necessarie:
```
pip install folium
pip install pandas
pip install seaborn
```
2. Avvio lo script per l'analisi dei dati:
```
py analisi.py
```

# RISULTATI
Lo script ottiene in output la creazione di un grafico con la traccia della serie storica delle pubblicazioni in ambito di sicurezza informatica in Italia, relativamente alle conferenze selzionate per l'analisi. Inoltre viene generato un file (map.html) il quale mostra una mappa dinamica che mostra i centri di ricerca più attivi d'Italia e ne evidenzia le collaborazioni.

