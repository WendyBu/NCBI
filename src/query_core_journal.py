"""
given a gene name, and a publication list (core.txt)
return the journal name, year, abstract and article title.
pubmed query
"""


import pandas as pd
import sys
import urllib2
from bs4 import BeautifulSoup
import requests
from xml.etree import ElementTree
pd.set_option("display.max_columns", 100)


def query_pubmed(gene, journal = ""):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=" + gene + "[TIAB]+" + journal + "[journal]" + "&retmax=1000"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    num = 0
    pubmedIDList = []
    for id in soup.find_all('id'):
        num +=1
        pubmed_ID = id.string
        pubmedIDList.append(pubmed_ID)
    return num,pubmedIDList


def getContents(pubmedID):
    absUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=" + pubmedID + "&retmode=xml"
    # https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=30217816&retmode=xml
    response_xml = requests.get(absUrl)
    root = ElementTree.fromstring(response_xml.content)
    Abstract = ""
    year = ""
    for child in root.iter('*'):
        if child.tag == "Title":
            JournalTitle = child.text
        if child.tag == "ArticleTitle":
            ArticleTitle = child.text
        if child.tag == "AbstractText":
            Abstract = child.text
        if child.tag == "Year":
            year = child.text
    return JournalTitle.encode('utf-8'), ArticleTitle.encode('utf-8'), Abstract.encode('utf-8'), year.encode('utf-8')


def main():
    gene = sys.argv[1]
    journals = pd.read_csv("../data/core.txt", sep="\t", index_col=0)
    journalList = journals.index.tolist()
    publicationList = []
    with open("../results/Abstracts.txt", "w+") as f:
        for journal in journalList[1:8]:
            journalName = journal.replace(" ", "+")
            publication_num, pubIDList = query_pubmed(gene, journalName)
            publicationList.extend(pubIDList)
        print "total number of articles:", len(publicationList)
        for id in publicationList:
            f.writelines(id + "\n")
            journalTitle, articleTitle, abstract, year = getContents(id)
            f.write(journalTitle + " " + year + " \n")
            f.write("Title: " + articleTitle + "\n")
            f.write("Abstract: " + abstract + "\n")
            f.writelines("\n")
    pass


if __name__ == "__main__":
    main()



# python query_core_journal.py ezh2