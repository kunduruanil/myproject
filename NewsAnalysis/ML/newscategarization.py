'''
Created on Nov 27, 2018

@author: anil.reddy.kunduru
'''
from ML.load_spacy import spacy_load_lg


class NewsCaegarization:
    def __init__(self,news_body,title):
        self.new_body=news_body
        self.title=title
        text=title+" "+news_body
        self.doc=spacy_load_lg(text)
        
    def prepare_data(self):
        for sent in self.doc:
            return
        

if __name__ == '__main__':
       