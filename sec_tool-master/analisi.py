#### ANALISI Sec_toolDB (MongoDB) ####
import grafici
import pymongo
from sec_tool.config import DB_NAME, MIN_COMBO_NUM, MIN_AUTHORS_GROUP, CONF_EDITIONS_LOWER_BOUNDARY

# connect to the mongoclient
client = pymongo.MongoClient('mongodb://localhost:27017')

# get the database
database = client[f'{DB_NAME}']

# get collection Autori
Autori = database.get_collection("authors")
x=Autori.count_documents({}, {})
print("Numero autori: ", end="")
print(x)
print("")

# get collection Possibili gruppi
poss_group = database.get_collection("probable_groups")
g = list(poss_group.find({},{"_id": 0}))
groups = []
elemento=[]
for p in g:
    elemento = p.get('gruppo')
    val = eval(elemento)
    groups.append(val)


### ALGORITMO per determinare i gruppi di ricerca ###
# L'analisi avviene su groups che contiene vettori di possibili gruppi (autori per ogni paper)

autor = []    
prob_group = [autor]
n=0
elem = 1
elenco= []

for gr in groups:
    comboaut=[]
    count = 0                               #MIN_COMBO_NUM: [3] numero di volte che si devono presentare in combinazione degli autori per essere considerato un gruppo
    for i in range (elem, len(groups)):     #cambio riga su cui verifico di nuovo la presenza della stessa coppia
        comboaut_m = []
        comb = False
        rip = 0                             #MIN_AUTHORS_GROUP: [2] contatore numero di autori nella combinazione ripetuta
        for au in gr:
            for y in range(len(groups[i])):
                if au == groups[i][y]:
                    if au not in comboaut_m:
                        count+=1
                        rip+=1
                        comboaut_m.append(au)
                        elenco.append(au)
                    if rip>(MIN_AUTHORS_GROUP-1) and count>MIN_COMBO_NUM:
                        comboaut = comboaut_m
                        comb = True
        if comb == True:
            if comboaut not in prob_group and len(comboaut)!=1:
                prob_group.append(comboaut)
                n+=1
    elem += 1

#fusione di gruppi identificati composti da quasi gli stessi autori
k=1
gruppi = []

for gr in prob_group:
    gruppox=[]
    for a in gr:
        presente = False
        for x in range(len(gruppi)):
            if a in gruppi[x]:
                presente = True
        if presente == False:
            gruppox.append(a)
    if len(gruppox)>1:
        gruppi.append(gruppox)
        
print("Ho individuato ", end="") 
print(len(gruppi),end="")
print (" possibili gruppi")

#CONTEGGIO PUBBLICAZIONI SUDDIVISE PER GRUPPO
#Conto le pubblicazioni dove tra gli autori vi è o tutto il gruppo o almeno uno dei membri
num_paper = []

for g in gruppi:
    contatore = 0
    for i in groups:
        t = 0
        for x1 in g:
            for x2 in i:
                if x1 == x2:
                    t+=1
        if t > 1:               #almeno due presenze PER L'ALTERNATIVA SOSTITUIRE LA T CON PRESENZA = F/T
            contatore+=1
    num_paper.append(contatore)

print("")

#DETERMINO I NOMI ASSOCIATI AGLI ID
elenco_gruppi = []
n= 0
for gruppo in gruppi:
    elenco_nomigruppo = []
    n+=1
    for id_autore in gruppo:
        nomeautore = list(Autori.find({"eid_list" : f'{id_autore}'},{"_id": 0}))
        el=[]
        for p in nomeautore: #uso il ciclo per convertire il tipo Cursor in Dictionary ---> TODO altro modo (?)
            el = p.get('lastname')
            citta=p.get('city')
            nome = el
        elenco_nomigruppo.append(nome)
    stringa = ""
    for a in elenco_nomigruppo:
        if stringa=="":
            stringa = stringa+a
        else:
            stringa = stringa+"-"+a
    stringa_fin="Gr"+f"{n}("+stringa+")"
    elenco_gruppi.append(stringa_fin + citta)

print ("{:<50} {:<35}".format('Gruppi identificati:','Numero di paper:'))
print("")
for j in range(len(elenco_gruppi)):
    print ("{:<50} {:<35}".format(elenco_gruppi[j],num_paper[j]))
    
### INDIVIDUO EVENTUALI COLLABORAZIONI ###
# Variabili su cui lavoro
#   groups ---> elenco di autori (ID) per ogni pubblicazione
#   gruppi ---> elenco di gruppi (ID autori) identificati

collaborazioni = []
i=0
for team in groups:
    collab = ""
    distinct = []
    n_gruppi_coinvolti = 0
    for membro_team in team:
        for n in range(1,len(gruppi)+1):
            if membro_team in gruppi[n-1]:
                if n not in distinct:
                    n_gruppi_coinvolti +=1
                    distinct.append(n)
                    n_gruppo = str(n)
                    if collab == "":
                        collab = collab+"Gr"+n_gruppo
                    else:
                        collab = collab+"-"+"Gr"+n_gruppo
    if collab != "" and n_gruppi_coinvolti>1:
        i+=1
        collaborazioni.append("Collaborazione"+str(i)+"("+ collab +")")            

print("")
print("COLLABORAZIONI:" + f"{len(collaborazioni)}")

for z in collaborazioni:
    print(z)

## ANALISI STORICO
# get collection Storico
sto = database.get_collection("num_papers")

print("")
print("Storico numero di pubblicazioni:")

storico_papers = []
k=0
for anno in range((2021-CONF_EDITIONS_LOWER_BOUNDARY), 2021):              #analizzo gli anni dal 2008 al 2020 compresi, non considero il 2021 perché in corso
    annata = list(sto.find({"anno" : f'{anno}'},{"_id": 0}))
    tot=0
    for confer in annata:
        x = confer.get('num_papers')
        tot=tot+int(x)
    storico_papers.append(tot)

    print(f" Pubblicazioni {anno}: "+ f"{storico_papers[k]}")
    k+=1


grafici.create_output(storico_papers)

## OPZIONI ALTERNATIVE
#opzione 1 grafici
""" # import all the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
  
# create a dataframe
Sports = {
    "medals": [100, 98, 102, 56, 78, 56,
               78, 96],
    
    "Time_Period": [2010, 2011, 2012, 2013,
                    2014, 2015, 2016, 2017]
}
df = pd.DataFrame(Sports)
#print(df)
  
  
# to plot the graph
# subplot (rowno,columno,position) is used
# to plot in a single frame.
# to plot the scatter graph ,write kind= scatter
df.plot(x="Time_Period", y="medals", kind="bar")
plt.title("scatter chart")
plt.subplot(1, 1, 1)
  
  
# to Plot the graph in Bar chart
df.plot(x="Time_Period", y="medals", kind="bar")
plt.title("bar")
plt.subplot(1, 1, 1)
  
plt.show() """

#opzione 2 grafici
""" import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter


def myplot(x, y, s, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent


fig, axs = plt.subplots(2, 2)

# Generate some test data
x = np.random.randn(1000)
y = np.random.randn(1000)

sigmas = [0, 16, 32, 64]

for ax, s in zip(axs.flatten(), sigmas):
    if s == 0:
        ax.plot(x, y, 'k.', markersize=5)
        ax.set_title("Scatter plot")
    else:
        img, extent = myplot(x, y, s)
        ax.imshow(img, extent=extent, origin='lower', cmap=cm.jet)
        ax.set_title("Smoothing with  $\sigma$ = %d" % s)

plt.show() """

## fine algoritmo ##