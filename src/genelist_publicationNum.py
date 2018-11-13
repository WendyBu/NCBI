"""
give a gene list, return how many paper can be found in the pubmed.
"""


import pandas as pd
import urllib2
from bs4 import BeautifulSoup
pd.set_option("display.max_columns", 100)


def query_pubmed(gene, cancer = ""):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=" + gene + "+" + cancer + "&retmax=1000"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    num = 0
    for x in soup.find_all('id'):
        num +=1
    return num


def main():
    geneListFile = pd.read_csv("../geneList/FBL.txt", sep="\t")
    geneList = geneListFile.gene_id.tolist()
    with open("../results/NumRecord.txt", "w+") as f:
        for gene in geneList:
            publication_num = query_pubmed(gene, cancer="")   # parse the gene name and a cancer type or none
            line = gene + " " + str(publication_num) + "\n"
            f.writelines(line)
    pass


if __name__ == "__main__":
    main()
