# web-data-similarity-analysis
Analyze web data based on TF-IDF, Cosine Similarity

![1](https://user-images.githubusercontent.com/60180255/87978112-d57be700-cb0a-11ea-9296-747335d9e1f4.PNG)

---

![2](https://user-images.githubusercontent.com/60180255/87978156-e88eb700-cb0a-11ea-8eb9-2e0fe936a7f5.PNG)

---

![3](https://user-images.githubusercontent.com/60180255/87978166-ef1d2e80-cb0a-11ea-9623-ee0b3912b53c.PNG)

#### Compatibility

This web application could run on the ```Ubuntu 20.04 LTS (WSL2)``` and is compatible with only ```Python 3```.

```Elasticsearch``` is used to store crawled data. Therefore, you need to run ```Elasticsearch``` before you run the web application.

#### Installation

Python requirements are as below:

```
validators
requests
flask
numpy
nltk
bs4
```

NLTK requirements are as below:

```
$ python -m nltk.downloader punkt
$ python -m nltk.downloader stopwords
```

#### Usage

```
$ python ./app.py
```

