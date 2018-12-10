'''
Created on Oct 19, 2018

@author: anil.reddy.kunduru
'''
from urllib.parse import urlparse
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import re
from boilerpipe.extract import Extractor
from commonutils.config import _logger
from newspaper import Article

class News:
    def __init__(self,url):
        try:
            self.page=requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            self.soup=BeautifulSoup(self.page.text,'html.parser')
        except:
            _logger.error("request.get method failed from url: {}".format(str(url)))
            pass
        try:
            self.article = Article(url, language='en')
            self.article.download()
            self.article.parse()
            self.article.nlp()
        except:
            _logger.error("newpaper library failed for url: {}".format(str(url)))
            pass
        self.url=url
        return
    
    def get_image(self):
        image=self.article.top_image
        return image
    
    def get_keywords(self):
        keywords=self.article.keywords
        return keywords
        
    def get_summary(self):
        summary=self.article.summary
        return summary
        
    def get_date(self):
        date=self.article.publish_date
        if date:
            return date
        else:
            date=self._get_date()
            if date:
                return date
            else:
                return None
        
    
    def get_news(self):
        try:
            extractor = Extractor(extractor='ArticleExtractor', url=self.url)
            extracted_text=extractor.getText()
        except:
            pass
        if not extracted_text:
            news=''
            p=self.soup.findAll('p')
            for i,v in enumerate(p):
                if i ==0:
                    continue
                news+=v.text
            return news
        else:
            return extracted_text
        #p_length=len(news)
#         if "thehindu" in self.url:
#             return news
#         else:
#             div=self.soup.find_all('div')
#             for d in div:
#                 if len(d.text)>p_length:
#                     print(len(d.text))
#                     news=d.text.encode("utf-8")
#             return news
        
    def _get_date(self):
        regex="\d{1,4}(-|\\|\/|\s|,)\d{1,2}(-|\\|\/|\s|,)\d{1,4}(\s\s|,|,\s|\s|T)\d{1,2}[:]\d{1,2}|[a-zA-Z0-9]{2,8}(-|\\|\/|\s|,\s|,)[a-zA-Z0-9]{2,8}(-|\\|\/|\s|,\s|,|)\d{2,4}\d{2,4}(\s\s|,|,\s|\s)\d{1,2}[:]\d{1,2}|\d{1,2}\w{1,2}(-|\\|\/|\s|,|\s\s)[a-zA-z]{2,8}(-|\\|\/|\s|,|\s\s)\d{2,4}(\s\s|,|,\s|\s)\d{1,2}[:]\d{1,2}|[a-zA-Z]{3}\s{1,2}\d{1,2}[,]\s?\d{4}"
        d=self.soup.find_all('date')
        if d:
            for data in d:
                match=re.search(regex,data.text)
                if match:
                    return match.group()
        t=self.soup.find_all('time')
        if t:
            for data in t:
                match=re.search(regex,data.text)
                if match:
                    return match.group()
        span=self.soup.find_all('span')
        if span:
            for s in span:
                date=s.text
                r=re.search(regex, date)
                if r:
                    date=r.group()
                    #print(date)
                        #print(date)
                    return date
                elif "Updated" in date:
                    #date=date.replace('Updated','')
                    index=date.index('Updated')+7
                    date=date[index:]
                    if date and re.search('[0-9]',date):
                        return date.replace(':','').strip()
                    ne=s.find_next_sibling('span')
                    if ne:
                        r=re.search(regex, next.text)
                        if r:
                            return r.group()
                elif 'Published' in date:
                    index=date.index('Published')+9
                    date=date[index:]
                    if date and re.search('[0-9]',date):
                        return date.replace(':','').strip()
                    ne=s.find_next_sibling('span')
                    if ne:
                        r=re.search(regex, ne.text)
                        if r:
                            print(r)
                            return r.group()
                else:
                    continue
    
    def get_date_notfound(self):
        span=self.soup.find_all('span')
        if span:
            for s in span:
                date=s.text
                if "Today" in date or 'hour'  in date:
                    words=word_tokenize(date)
                    #print(words)
                    for word in words:
                        if word=='Today':
                            return date
                        elif word=='hour':
                            return word
                        else:
                            continue

    def get_span(self):
        span=self.soup.find_all('span')
        for s in span:
            print(s.text)
            
    def get_title(self):
        titile_dict=defaultdict(int)
        url=re.sub('\/$','',self.url)
        title_url=urlparse(url).path
        title_list=re.sub('[-/]'," ",title_url).split()
        title=[]
        regex=re.compile('(.*title.*|.*headline.*)')
        #print(self.soup.findAll(["span",'h1'], {"class" : regex,"itemprop":regex}))
        tag=self.soup.find_all(["span",'h1','div'], {"class" : regex})
        if not tag:
            tag=self.soup.findAll('h1')
        for EachPart in tag:
            title.append(EachPart.text.strip())
        if title:
            for i in title:
                for j in i.lower().split():
                    if j in title_list:
                        titile_dict[i]+=1
        if titile_dict:
            count=list(titile_dict.values())
            if len(count)>1:
                count=sorted(count)[-1]
            else:
                count=count[0]
            for k,v in titile_dict.items():
                if v==count:
                    return k
        
if __name__=="__main__":
    import time
    url='https://telanganatoday.com/live-updates-telangana-starts-voting'
    n=News(url)
    print(n.url)
    if n.page:
        #n.get_span()
        print(n.get_date())
        print("---date---")
        print(n.get_title())
        print("---title--")
        time.sleep(5)
        print(n.get_news())
        print("----image---")
        print(n.get_image())
        print("--keywords---")
        print(n.get_keywords())
        print('---summy--')
        print(n.get_summary())
        
    else:
        print("fail")
        