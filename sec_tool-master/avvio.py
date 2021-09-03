### SCRIPT DI AVVIO ###

import sec_tool
from sec_tool.models import Conference

import pandas as pd

lista = pd.read_csv('data/lista.csv', delimiter = ';', header = 0, index_col = 0)

for t in range(1,(len(lista['acronimo'])+1)):
    acronimo=lista['acronimo'][t]
    nome=lista['nome'][t]
    
    if __name__ == "__main__":
        conf = Conference(name=nome, acronym=acronimo)
        sec_tool.add_conference(conf)
 


"""
if __name__ == "__main__":
    conf = Conference(name="Conference on Computer and Communications Security", acronym="CCS")
    sec_tool.add_conference(conf)



if __name__ == "__main__":
    conf = Conference(name="European Symposium on Research in Computer Security", acronym="ESORICS")
    sec_tool.add_conference(conf)



if __name__ == "__main__":
    conf = Conference(name="USENIX Security Symposium", acronym="USENIX")
    sec_tool.add_conference(conf)



if __name__ == "__main__":
    conf = Conference(name="International Symposium on Recent Advances in Intrusion Detection", acronym="RAID")
    sec_tool.add_conference(conf)



if __name__ == "__main__":
    conf = Conference(name="ACM Symposium on Information, Computer and Communications Security", acronym="ASIACCS")
    sec_tool.add_conference(conf)



if __name__ == "__main__":
    conf = Conference(name="ISOC Network and Distributed System Security Symposium", acronym="NDSS")
    sec_tool.add_conference(conf)

    # nessuna estrazione 


if __name__ == "__main__":
    conf = Conference(name="IEEE Symposium on Security and Privacy", acronym="S%26P")
    sec_tool.add_conference(conf)
    
    # nessuna estrazione 

## utilizzo %26 al posto di & per problemi con url, vedi https://stackoverflow.com/questions/16622504/escaping-ampersand-in-url
"""