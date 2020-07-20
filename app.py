from datetime import datetime
from flask import Flask
from flask import render_template
from flask import redirect, url_for
from flask import request
from elasticsearch import Elasticsearch
from Core.core import *

app = Flask(__name__)

analyzer = None
es_host = "127.0.0.1"
es_port = "9200"
es = Elasticsearch([{"host": es_host, "port": es_port}], timeout=30)

status = {
    Result.Success: "success",
    Result.Failure: "failure",
    Result.Duplication: "duplication"
}

@app.route("/")
@app.route("/index")
def index():
    global analyzer

    urlDict = {}
    urlList = []
    if es.indices.exists(index="wdsa"):
        res = es.search(index="wdsa", doc_type="doc", body={
            "size": 10000,
            "query": {
                "match_all": {}
            }
        })

        for doc in res["hits"]["hits"]:
            source = doc["_source"]
            urlDict[source["url"]] = source["document"]
            urlList.insert(0, [
                source["url"],
                source["date"],
                source["wordcount"],
                source["etime"],
                source["result"]
            ])
    
    analyzer = Analyzer(urlDict)
    return render_template("index.html", urlList=urlList)

@app.route("/add", methods=["GET", "POST"])
def add():
    global analyzer
    resp = {}

    if request.method == "POST":
        url = request.form["url"]
        result = analyzer.crawl(url)
        resp["url"] = url
        resp["status"] = status[result["status"]]

        if result["status"] == Result.Success:
            document = analyzer.crawler.crawled_documents[url]
            data = {
                "url": url,
                "document": document,
                "wordcount": len(document),
                "etime": result["time"],
                "result": status[result["status"]],
                "date": datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            }

            res = es.index(index="wdsa", doc_type='doc', id=len(analyzer.crawler.crawled_documents.keys()), body=data)

    return resp

@app.route("/add2", methods=["GET", "POST"])
def add2():
    global analyzer
    resp = {}

    if request.method == "POST":
        urls = request.form["url"].split("\r\n");
        resp["urls"] = []

        for url in urls:
            result = analyzer.crawl(url)
            resp["urls"].append([url, status[result["status"]]])

            if result["status"] == Result.Success:
                document = analyzer.crawler.crawled_documents[url]
                data = {
                    "url": url,
                    "document": document,
                    "wordcount": len(document),
                    "etime": result["time"],
                    "result": status[result["status"]],
                    "date": datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                }

                res = es.index(index="wdsa", doc_type='doc', id=len(analyzer.crawler.crawled_documents.keys()), body=data)

    return resp

@app.route("/tfidf", methods=["GET", "POST"])
def tfidf():
    global analyzer
    resp = {}

    if request.method == "POST":
        url = request.form["url"]
        result = analyzer.analyze_words(url)
        resp["url"] = url
        resp["status"] = status[result["status"]]

        if result["status"] == Result.Success:
            resp["tfidf"] = result["tfidf"]
            resp["time"] = result["time"]
    
    return resp

@app.route("/cs", methods=["GET", "POST"])
def cs():
    global analyzer
    resp = {}

    if request.method == "POST":
        url = request.form["url"]
        result = analyzer.analyze_similarity(url)
        resp["url"] = url
        resp["status"] = status[result["status"]]

        if result["status"] == Result.Success:
            resp["cos"] = result["cos"]
            resp["time"] = result["time"]
    
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0")