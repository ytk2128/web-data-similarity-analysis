import re
import sys
import math
import time
import string
import requests
import numpy as np
from nltk.corpus import stopwords
from nltk import word_tokenize
from bs4 import BeautifulSoup
from .crawler import *

'''
< Terminology >
t - term (word)
d - document (set of words)
N - count of corpus
corpus - the total document set
'''

class Analyzer:
    def __init__(self, documents):
        self.stopwords = stopwords.words("english")
        self.crawler = Crawler(documents)
        self.documents = {}

    # tf(t,d) = count of t in d / number of words in d
    def get_tf(self, url):
        words = self.documents[url]
        word_count = {}

        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # number of unique words
        d = len(word_count)
        tf = {}
        for word, cnt in word_count.items():
            tf[word] = float(cnt) / d

        return tf
    
    # df(t) = occurrence of t in documents
    # idf(w) = log(N / df(t))
    def get_idf(self, url):
        N = len(self.documents.items())
        idf = {}
        for word in set(self.documents[url]):
            df = 0
            for url, words in self.documents.items():
                if word in words:
                    df += 1
            
            idf[word] = np.log(float(N) / df)

        return idf
    
    def get_tfidf(self, url):
        idf = self.get_idf(url)
        tf = self.get_tf(url)

        tfidf = {}
        for word, val in tf.items():
            tfidf[word] = val * idf[word]

        return tfidf
    
    def crawl(self, url):
        return self.crawler.crawl(url)

    # Analyze words and return top 10 words
    def analyze_words(self, url):
        result = {}
        self.documents = self.crawler.get_documents()

        if len(self.documents) < 2:
            result["status"] = Result.Failure
            return result

        rtime = time.time()
        tfidf = self.get_tfidf(url)
        sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
        result["tfidf"] = sorted_tfidf[:10]
        
        rtime = time.time() - rtime
        result["time"] = rtime
        result["status"] = Result.Success
        return result
    
    def analyze_similarity(self, url):
        result = {}
        self.documents = self.crawler.get_documents()

        # Due to TF-IDF analysis, N has to be greater than 1 at least
        if len(self.documents) < 2:
            result["status"] = Result.Failure
            return result

        rtime = time.time()
        slist = []
        for key, value in self.documents.items():
            if key == url:
                continue
                
            words = set(self.documents[url] + value)
            v1 = []
            v2 = []

            for word in words:
                val = 0
                for term in self.documents[url]:
                    if term == word:
                        val += 1
                v1.append(val)

                val = 0
                for term in value:
                    if term == word:
                        val += 1
                v2.append(val)
            
            dot = np.dot(v1, v2)
            cos = dot / (np.linalg.norm(v1) * np.linalg.norm(v2))
            
            slist.append([url, key, cos * 100])

        sorted_slist = sorted(slist, key=lambda x: x[2], reverse=True)
        result["cos"] = sorted_slist[:3]

        rtime = time.time() - rtime
        result["time"] = rtime
        result["status"] = Result.Success
        return result