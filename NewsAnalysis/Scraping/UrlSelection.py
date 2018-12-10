'''
Created on Oct 18, 2018

@author: anil.reddy.kunduru
'''
import re
import copy
import tldextract
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

class FindUrls:
    def __init__(self):
        return
    
    def getLinksWithAnchor(self,url):
        html=requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
        soup=BeautifulSoup(html.text,'html.parser')
        soupBody=copy.copy(soup)
        domain = tldextract.extract(url).domain
        suffix = tldextract.extract(url).suffix
        resultList = dict()

        if soupBody:
            innerlinks = soupBody.findAll('a')
            for link in innerlinks:
                urlink=link.get('href')
                nurl = urljoin(url,urlink)
                d2 = tldextract.extract(nurl).domain
                s2 = tldextract.extract(nurl).suffix
                
                if domain == d2 and suffix == s2 and 'http' in nurl:
                    atxt = link.text
                    atxt = atxt.replace("\n","").replace("\r","").replace("\t","").replace("\s+"," ").strip(" ")
                    if atxt is not None and atxt != "":
                        atxt = atxt.lower()
                        if nurl in resultList:
                            temp = resultList[nurl]
                        else:
                            temp = set()
                        temp.add(atxt)
                        resultList[nurl]=temp
                            
        return resultList
    
    def getArealinks(self,url,area):
        all_urls=self.getLinksWithAnchor(url)
        news_links=[]
        for k in all_urls:
            k=re.sub('\/$','',k)
            k=k.lower()
            if k.endswith(area):
                resultdict=self.getLinksWithAnchor(k)
                news_links.extend(self.getcleandUrls(resultdict))
#             elif k.endswith((state,state+'/')):
#                 resultdict=self.getLinksWithAnchor(k)
#                 state_urls=self.getcleandUrls(resultdict)
        return news_links
    
    def getcleandUrls(self,resultdict):
        news_list=[]
        for k in resultdict:
            if re.search("\/\w+[-]\w+[-]\w+",k):
                news_list.append(k)
        return news_list

if __name__=="__main__":
    f=FindUrls()
    site="https://telanganatoday.com"
    area='hyderabad'
    import time
    start=time.time()
    area_links=f.getArealinks(site, area)
    end=time.time()
    print(end-start)
    print(area_links)
    print(len(area_links))
    