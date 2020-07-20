import re
import sys
import time
import string
import requests
import validators
from enum import Enum
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords

class Result(Enum):
    Success = 0
    Failure = 1
    Duplication = 2

class Crawler:
    def __init__(self, documents):
        self.stopwords = stopwords.words("english")     # stop words
        self.crawled_documents = documents              # Key: url string, Value: words set
        self.targets = {                                # target tags to crawl
            "h1": {},
            "h2": {},
            "h3": {},
            "h4": {},
            "p": {},
            "li": {},
            "dt": {},
            "dd": {}
        }
    
    def crawl(self, url):
        result = {}
        if url in self.crawled_documents.keys():
            result["status"] = Result.Duplication
            return result

        if not validators.url(url):
            result["status"] = Result.Failure
            return result

        rtime = time.time()
        page = None
        try:
            page = requests.get(url)
        except:
            result["status"] = Result.Failure
            return result

        if page.status_code >= 400:
            result["status"] = Result.Failure
            return result
        soup = BeautifulSoup(page.content, "html.parser")

        words = []
        for tag, attr in self.targets.items():
            tags = soup.find_all(tag, attr)
            for t in tags:
                sentence = t.text.strip().lower()
                for word in word_tokenize(sentence):
                    # Check if a word is the stopword
                    if word not in self.stopwords:
                        # Replace special characters to space in a word
                        new_word = re.sub("[^a-z0-9]+", " ", word.strip())
                        for nword in word_tokenize(new_word):
                            # The length of a word must be greater than 1 at least
                            # A word has only numbers, it's not helpful
                            if len(nword) > 1 and not nword.isnumeric():
                                words.append(nword)
        rtime = time.time() - rtime
        result["time"] = rtime

        if not words:
            result["status"] = Result.Failure
            return result

        self.crawled_documents[url] = words
        
        result["status"] = Result.Success
        return result
    
    def get_documents(self):
        return self.crawled_documents