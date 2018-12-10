'''
Created on Dec 7, 2018

@author: anil.reddy.kunduru
'''

from commonutils.config import _config,_logger,clear_loggerfile
from pandas import read_csv
from multiprocessing.pool import ThreadPool
from Scraping.UrlSelection import FindUrls
from collections import defaultdict
from Scraping.get_news_by_link import News
from pandas import DataFrame
from datetime import datetime
import os 

class NewsDataframe:
    def __init__(self):
        return
    
    def create_directory(self):
        file='output-'+str(datetime.now().date())
        out=_config.get('files','out')
        directory=os.path.join(out,file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
    
    def get_all_links_by_area(self,path,area):
        df=read_csv(path)
        urls=[]
        baseurls=df.hyderabad
        furls=FindUrls()
        _logger.warning("getting all the urls of Area : {} started".format(area))
        for burl in baseurls:
            _logger.warning("url {} started".format(burl))
            try:
                out=furls.getArealinks(burl, area)
            except Exception as e:
                error="URL:"+str(burl)+" Area:"+str(area)+" Exception:"+str(e)
                _logger.error(error)
                pass
            if out:
                urls.extend(out)
        _logger.warning("completed getting all the urls for the Area: {a} and length of urls: {b}".format_map({'a':str(area),'b':str(len(urls))}))
        return urls
    
    def get_dataframe(self,path,area):
        out_path=os.path.join(self.create_directory(),area+'.csv')
        urls=self.get_all_links_by_area(path, area)
        news=defaultdict(list)
        _logger.warning("get news to dataframe loop started for Area: {}".format(area))
        for i,url in enumerate(urls):
            if i%10==0:
                print(i)
            if url:
                n=News(url)
                if n.page:
                    date=n.get_date()
                    if date:
                        news['date'].append(date)
                    else:
                        news['date'].append(None)
                    title=n.get_title()
                    if title:
                        news['title'].append(title)
                    else:
                        news['title'].append(None)
                    news['url'].append(url)
                    news['area'].append(area)
                    artical=n.get_news()
                    if artical:
                        news['news'].append(artical)
                    else:
                        news['news'].append(None)
                    image=n.get_image()
                    if image:
                        news['image'].append(image)
                    else:
                        news['image'].append(None)
                    keywords=n.get_keywords()
                    if keywords:
                        news['keywords'].append(keywords)
                    else:
                        news['keywords'].append(None)
                    summy=n.get_summary()
                    if summy:
                        news['summy'].append(summy)
                    else:
                        news['summy'].append(None)
        if news:
            for k in news:
                print(str(k)+" "+str(len(news[k])),end=' ')
            DataFrame(news).to_csv(out_path)
        _logger.warning("dataframe for Area: {} completed".format(area))
                

if __name__ == '__main__':
    clear_loggerfile(True)
    path=_config.get("files",'news_links')
    area=_config.get("files",'area')
    new=NewsDataframe()
    new.get_dataframe(path,area)



    


