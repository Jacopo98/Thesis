from mongoengine import connect

import sec_tool.conference_manager as conference_manager
from sec_tool.models import Author

from sec_tool.config import DB_NAME

from sec_tool.models import Conference


def add_conferences(conferences):
    for conf in conferences:
        add_conference(conf)


def add_conference(Conferenza):
    connect(DB_NAME, host='localhost')
    conf_editions = conference_manager.search_conference(Conferenza)
    

    resultantList = []
    resultantListYear= []

    for element in conf_editions:
        if element.year not in resultantListYear:
            resultantList.append(element)
            resultantListYear.append(element.year)
    
    #### OLTREPASSARE IL PROBLEMA DI WIKICFP CHE NON FUNZIONA #####
    ## è possibile usare il tool anche in questo modo, l'elenco delle conferenze non vine trovato
    ## da codice su WikiCFP ma viene creato a mano. Fornisce anche un rilutato leggermente diverso in quanto
    ## alcune vecchie conferenze non vengono estratte su WikiCFP.
    
    """  raid2017=Conference(acronym='RAID', year=2017)
    raid2020=Conference(acronym='RAID', year=2020)
    raid2021=Conference(acronym='RAID', year=2021)
    raid2019=Conference(acronym='RAID', year=2019)
    raid2016=Conference(acronym='RAID', year=2016)
    raid2013=Conference(acronym='RAID', year=2013)
    raid2018=Conference(acronym='RAID', year=2018)
    raid2015=Conference(acronym='RAID', year=2015)
    raid2011=Conference(acronym='RAID', year=2011)
    raid2012=Conference(acronym='RAID', year=2012)
    #
    raid2010=Conference(acronym='RAID', year=2010)
    raid2009=Conference(acronym='RAID', year=2009)
    raid2008=Conference(acronym='RAID', year=2008)
    raid2007=Conference(acronym='RAID', year=2007)
    raid2006=Conference(acronym='RAID', year=2006)

    acsac2021=Conference(acronym='ACSAC', year=2021)
    acsac2016=Conference(acronym='ACSAC', year=2016)
    acsac2014=Conference(acronym='ACSAC', year=2014)
    acsac2019=Conference(acronym='ACSAC', year=2019)
    acsac2012=Conference(acronym='ACSAC', year=2012)
    acsac2017=Conference(acronym='ACSAC', year=2017)
    acsac2020=Conference(acronym='ACSAC', year=2020)
    acsac2018=Conference(acronym='ACSAC', year=2018)
    acsac2015=Conference(acronym='ACSAC', year=2015)
    acsac2011=Conference(acronym='ACSAC', year=2011)
    #
    acsac2010=Conference(acronym='ACSAC', year=2010)
    acsac2009=Conference(acronym='ACSAC', year=2009)
    acsac2008=Conference(acronym='ACSAC', year=2008)
    acsac2007=Conference(acronym='ACSAC', year=2007)
    acsac2006=Conference(acronym='ACSAC', year=2006)

    ccs2017=Conference(acronym='CCS', year=2017)
    ccs2021=Conference(acronym='CCS', year=2021)
    ccs2018=Conference(acronym='CCS', year=2018)
    ccs2020=Conference(acronym='CCS', year=2020)
    ccs2019=Conference(acronym='CCS', year=2019)
    ccs2013=Conference(acronym='CCS', year=2013)
    ccs2012=Conference(acronym='CCS', year=2012)
    ccs2015=Conference(acronym='CCS', year=2015)
    ccs2016=Conference(acronym='CCS', year=2016)
    ccs2014=Conference(acronym='CCS', year=2014)
    #
    ccs2010=Conference(acronym='CCS', year=2010)
    ccs2009=Conference(acronym='CCS', year=2009)
    ccs2008=Conference(acronym='CCS', year=2008)
    ccs2007=Conference(acronym='CCS', year=2007)
    ccs2006=Conference(acronym='CCS', year=2006)

    esorics2015=Conference(acronym='ESORICS', year=2015)
    esorics2019=Conference(acronym='ESORICS', year=2019)
    esorics2021=Conference(acronym='ESORICS', year=2021)
    esorics2017=Conference(acronym='ESORICS', year=2017)
    esorics2016=Conference(acronym='ESORICS', year=2016)
    esorics2018=Conference(acronym='ESORICS', year=2018)
    esorics2014=Conference(acronym='ESORICS', year=2014)
    esorics2013=Conference(acronym='ESORICS', year=2013)
    esorics2012=Conference(acronym='ESORICS', year=2012)
    esorics2011=Conference(acronym='ESORICS', year=2011)
    #
    esorics2010=Conference(acronym='ESORICS', year=2010)
    esorics2009=Conference(acronym='ESORICS', year=2009)
    esorics2008=Conference(acronym='ESORICS', year=2008)
    esorics2007=Conference(acronym='ESORICS', year=2007)
    esorics2006=Conference(acronym='ESORICS', year=2006)

    usenix2020=Conference(acronym='USENIX', year=2020)
    usenix2021=Conference(acronym='USENIX', year=2021)
    usenix2019=Conference(acronym='USENIX', year=2019)
    #
    usenix2010=Conference(acronym='USENIX', year=2010)
    usenix2009=Conference(acronym='USENIX', year=2009)
    usenix2008=Conference(acronym='USENIX', year=2008)
    usenix2007=Conference(acronym='USENIX', year=2007)
    usenix2006=Conference(acronym='USENIX', year=2006)

    asiaccs2020=Conference(acronym='ASIACCS', year=2020)
    asiaccs2017=Conference(acronym='ASIACCS', year=2017)
    asiaccs2021=Conference(acronym='ASIACCS', year=2021)
    asiaccs2016=Conference(acronym='ASIACCS', year=2016)
    asiaccs2019=Conference(acronym='ASIACCS', year=2019)
    asiaccs2018=Conference(acronym='ASIACCS', year=2018)
    asiaccs2015=Conference(acronym='ASIACCS', year=2015)
    asiaccs2013=Conference(acronym='ASIACCS', year=2013)
    asiaccs2011=Conference(acronym='ASIACCS', year=2011)
    asiaccs2014=Conference(acronym='ASIACCS', year=2014)
    asiaccs2012=Conference(acronym='ASIACCS', year=2012)
    #
    asiaccs2010=Conference(acronym='ASIACCS', year=2010)
    asiaccs2009=Conference(acronym='ASIACCS', year=2009)
    asiaccs2008=Conference(acronym='ASIACCS', year=2008)
    asiaccs2007=Conference(acronym='ASIACCS', year=2007)
    asiaccs2006=Conference(acronym='ASIACCS', year=2006)

    resultantList = [raid2017, raid2020, raid2021, raid2019, raid2016, raid2013, raid2018, raid2015, raid2011, raid2012, acsac2021, acsac2016, acsac2014, acsac2019, acsac2012, acsac2017, acsac2020, acsac2018, acsac2015, acsac2011, ccs2017, ccs2021, ccs2018, ccs2020, ccs2019, ccs2013, ccs2012, ccs2015, ccs2016, ccs2014, esorics2015, esorics2019, esorics2021, esorics2017, esorics2016, esorics2018, esorics2014, esorics2013, esorics2012, esorics2011, usenix2020, usenix2021, usenix2019, asiaccs2020, asiaccs2017, asiaccs2021, asiaccs2016, asiaccs2019, asiaccs2018, asiaccs2015, asiaccs2013, asiaccs2011, asiaccs2014, asiaccs2012, raid2010, raid2009, raid2008, raid2007, raid2006, acsac2010, acsac2009, acsac2008, acsac2007, acsac2006, ccs2010, ccs2009, ccs2008, ccs2007, ccs2006, esorics2010, esorics2009, esorics2008, esorics2007, esorics2006, usenix2010, usenix2009, usenix2008, usenix2007, usenix2006, asiaccs2010, asiaccs2009, asiaccs2008, asiaccs2007, asiaccs2006]
    prova=[raid2017, raid2020] """

    for edition in resultantList:
        print(f'\n### BEGIN conference: {edition.acronym} {edition.year} ###')
        conference_manager.add_conference(edition)


def add_authors_stats(authors=None):
    if authors is None:
        authors = Author.objects()
    for author in authors:
        stats = stats_manager.get_author_stats(author)
        author.modify(committee_mentions=stats.committee_ratio,
                      total_mentions=stats.not_committee_ratio)


def plot_refs():
    return stats_manager.plot_refs()


