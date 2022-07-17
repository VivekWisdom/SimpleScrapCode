import contextlib
from bs4 import BeautifulSoup
from lxml import html
import requests
import json
import pandas as pd

# {
#     "url":"https://www.mercer.us/events/webcasts/transforming-your-digital-employee-experience.html",
#     "description":"Digital interactions are the primary way that employees communicate with your company. Creating a positive and frictionless experience",
#     "title":"Transforming your digital employee experience | Mercer US",
#     "lastModified":"2022-06-02T19:21:28Z",
#     "geography":["north-america/united-states"],
#     "source":"mercer"
# }

class UtilMethods():

    def __init__(self) -> None:
        pass

    def get_url(self, resultObject:dict) -> str:
        """ Scraps URL of result"""
        url = None
        with contextlib.suppress(Exception):
            url = resultObject["url"]
        return url

    def get_description(self,  resultObject:dict) -> str:
        """Scrape page description."""

        description = None
        with contextlib.suppress(Exception):
            description = resultObject["description"]
        return description


    def get_title(self,  resultObject:dict) -> str:
        """Scrape page title."""

        title = None
        with contextlib.suppress(Exception):
            title = resultObject["title"]
        return title

    def get_modified(self,  resultObject:dict) -> str:
        """Scrape date modified."""

        lastModified = None
        with contextlib.suppress(Exception):
            lastModified = resultObject["lastModified"]
        return lastModified

    def get_geography(self,  resultObject:dict) -> str:
        """Scrape geography"""
        geography = None
        with contextlib.suppress(Exception):
            geography = resultObject["geography"]
        return geography


if __name__ == "__main__":

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

    homeUrl = "https://www.mercer.com/"
    searchUrl = "https://brain.mercer.com/api/v1//search/search"
    data = {"query":"Employee Experience AND (source:mercer) AND (geography:united-states) AND (language:english)","from":0,"size":228,"fields":["title","heading","url","pageUrl","description","contentSource","tagsRefiner","modified","icon","browserPageTitle","source"],"sortBy":1,"years":1,"apiVersion":1}


    sess = requests.Session()
    home_page = sess.options(searchUrl, headers=headers)
    home_page = sess.post(searchUrl, json=data, headers=headers)
    soup = BeautifulSoup(home_page.content, "html.parser")


    jsonData = json.loads(soup.text)
    fields = ["Url","Description","Title","Modified","Geography"]


    dataResponse = []
    if jsonData['success']:
        data = jsonData["data"]
        for len in range(int(data['total'])):
            print("Current item is", len, "\n")
            resultObject = data['results'][len]

            utilMethods = UtilMethods()

            metadata = [
                utilMethods.get_url(resultObject),
                utilMethods.get_description(resultObject),
                utilMethods.get_title(resultObject),
                utilMethods.get_modified(resultObject),
                utilMethods.get_geography(resultObject)
            ]
            dataResponse.append(metadata)

    finalDf = pd.DataFrame(dataResponse, columns=fields)
    finalDf.to_csv("Mercer_Scrap_Data.csv")
    print(finalDf.head())
