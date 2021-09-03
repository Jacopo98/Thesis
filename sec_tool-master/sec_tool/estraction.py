from sec_tool.models import Author, Paper
from pymongo import MongoClient
from pybliometrics.scopus import AbstractRetrieval, ScopusSearch
from collections import namedtuple
from sec_tool.config import DB_NAME

#set up DB
client = MongoClient('localhost', 27017)
db = client[f'{DB_NAME}']


def save_paper(conf):
    testoquery = f"CONFNAME({conf.getattr('acronym')}) AND PUBYEAR = {conf.getattr('year')}"
    
    documents = ScopusSearch(testoquery, view="STANDARD")

    try:
        papers = [Paper(scopus_id=sid) for sid in documents.get_eids()]  
    except Exception:
        return[]

    pubb = Paper()

        

    #salvataggio pubblicazioni
    for k in range(len(papers)):
            
        pubb.scopus_id=papers[k].scopus_id
            
        collection0 = db.papers
        doc = {
            'paper_ID': f'{pubb.scopus_id}'  
        }
            
        result0 = collection0.insert_one(doc)

    return papers


def save_author(papers):
    
    ## AUTORI
    #recupero autori
    autori= list()
    autori_tot=[]
    for p in papers:
        try:
            autori_ext = AbstractRetrieval(p.scopus_id, view="FULL").authorgroup
            autori.append(autori_ext)
        except Exception:
            print("ERRORE")
    
    #tetativo di 'scomporre' la tupla autori con namedtuple
    pp = namedtuple("Author", "affiliation_id dptid organization city postalcode addresspart country auid indexed_name surname given_name")
    
    

    for x in autori:
        if x:
            for i in range(len(x)):
                if x[i].country=="Italy":
                    autori_tot.append(x[i])
                    print(".", end="")      
        else:
            print("x", end="")
    
    print(" --> fine estrazione autori.")


    author = Author()
    authors = []
    
    #salvataggio autori
    for k in range(len(autori_tot)):
        
        author.affiliation_id= autori_tot[k].affiliation_id
        author.eid_list=autori_tot[k].auid
        author.fullname=autori_tot[k].given_name
        author.lastname=autori_tot[k].surname
        author.affiliation=autori_tot[k].organization
        author.affiliation_country=autori_tot[k].country
        author.city = autori_tot[k].city

        collection = db.authors
        doc = {
            'fullname': f'{author.fullname}',
            'lastname': f'{author.lastname}',
            'affiliation': f'{author.affiliation}',
            'affiliation_country': f'{author.affiliation_country}',
            'affiliation_id': f'{author.affiliation_id}',
            'city':f'{author.city}',
            'eid_list': f'{author.eid_list}'
        }
        
        collection.insert_one(doc)

        authors.append(author)

    print('Author extraction: extracted {0}.'
          .format(len(authors)))

    return(autori)

def save_groups(autori):
    groups = []
    cities = []
    for k in autori:
        if k:
            group=[]
            city=[]
            for h in range(len(k)):
                if k[h].country == "Italy":
                    group.append(k[h].auid)
                    city.append(k[h].city)
            if group:
                cities.append(city)
                groups.append(group)
    
    print("")
    print("numero possibili gruppi: ", end="")
    print(len(groups))

    for t in range(len(groups)):
        collection = db.probable_groups
        doc1 = {
            'gruppo' : f'{groups[t]}'
            #'citta':f'{cities[t]}'
        }
        collection.insert_one(doc1)
    
    return(groups)


def save_DataTS(groups, conf):
    num_papers = len(groups)
    acronimo= conf.getattr('acronym')
    anno = conf.getattr('year')

    tab = db.num_papers
    docstorico = {
        'anno': f'{anno}',
        'acronimo': f'{acronimo}',
        'num_papers' : f'{num_papers}'
    }
    tab.insert_one(docstorico)