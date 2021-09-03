import re
from datetime import datetime
from multiprocessing import Pool, Lock

from fuzzywuzzy import fuzz
from pybliometrics.scopus import AbstractRetrieval

from sec_tool.config import WIKICFP_BASE_URL, DB_NAME, CONF_EDITIONS_LOWER_BOUNDARY, CONF_EXCLUDE_CURR_YEAR

import sec_tool.util.webutil as webutil
from sec_tool.models import Conference, Author, Paper, AuthorIndex
from sec_tool.util.helpers import printl

from pymongo import MongoClient

from pybliometrics.scopus import AbstractRetrieval
from sec_tool.models import Paper

import sec_tool.estraction as estraction

base_url = WIKICFP_BASE_URL
dbname = DB_NAME

def search_conference(conf, lower_boundary=CONF_EDITIONS_LOWER_BOUNDARY, exclude_current_year=CONF_EXCLUDE_CURR_YEAR):
    # Gets the conference editions from wikicfp.

    url = f'{base_url}/cfp/servlet/tool.search?q={conf.acronym}&year=a'
    html = webutil.get_page(url)['html']
    if not html.text:
        return None

    rows = html.select('.contsec table table tr')
    events = [[i, k] for i, k in zip(rows[1::2], rows[2::2])]

    conferences = list()
    for event in events:
        first_row = event[0]
        second_row = event[1]
        w_acr_year = re.split(r'(\d+)(?!.)', first_row.select('a')[0].text)
        w_year = int(w_acr_year[1])

        # if the conference has not taken place yet, there can't be references
        # to its papers, therefore there's no point in having it in db.
        current_year = datetime.now().year
        if (w_year > current_year - exclude_current_year or
           w_year < current_year - lower_boundary):
            continue

        w_url = base_url + first_row.select('a')[0]['href']
        w_name = first_row.select('td')[1].text
        w_acronym = w_acr_year[0]
        w_location = second_row.select('td')[1].text

        # use levenshtein to check if it's the right conference, based on the
        # acronym OR the name
        if (fuzz.partial_ratio(conf.name.lower(), w_name.lower()) < 70 and
           fuzz.token_set_ratio(conf.acronym.lower(), w_acronym.lower()) < 70):
            continue

        conferences.append(Conference(
            fullname=conf.name, name=conf.name, acronym=conf.acronym,
            location=w_location, year=w_year, wikicfp_url=w_url))

    return conferences


def get_subject_areas(conference):
    subject_areas = []
    printl("Getting conference subject areas")
    for paper in conference.papers:
        paper = AbstractRetrieval(paper.scopus_id, view="FULL")
        subject_areas += [s.code for s in paper.subject_areas]
        printl(".")

    printl(" Done")
    return list(set(subject_areas))


def add_conference(conf):
    
    #controllo se le conferenze sono già nel DB
    if Conference.objects(wikicfp_id=conf.wikicfp_id):
        print("Conference already in database. Skipping conference.")
        return

    #set up DB
    client = MongoClient('localhost', 27017)
    db = client[f'{DB_NAME}']


    ## PUBBLICAZIONI (recupero pubblicazioni)
    papers = estraction.save_paper(conf)

    ## AUTORI (recupero autori)
    autori = estraction.save_author(papers)
    
    ## IDIVIDUO I GRUPPI DI OGNI PUBBLICAZIONE (gruppi author_id per ogni paper ---> individuo i gruppi di ricerca)
    groups=estraction.save_groups(autori)
    
    ## DATI PER SERIE STORICA (recupero il numero di pubblicazioni per la conferenza in questione ed edizione in questione)
    estraction.save_DataTS(groups, conf)
    

    conf.save()

    print(f'Papers extraction: extracted {len(papers)} papers. ')

    print("")
    conf.processing_status = 'complete'
    conf.save()

index_lock = Lock()


 

