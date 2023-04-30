import requests
from dotenv import load_dotenv
import os
import whois
import pandas as pd
import json
import pywhois
from send_email import send_email
import datetime

#load env
load_dotenv()

#date
yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')


#url
url = 'https://reverse-whois.whoisxmlapi.com/api/v2'

#api key
api_key = os.getenv('API_KEY')

#body
data = {
    "apiKey": api_key,
    "mode": "purchase",
    "createdDateFrom": yesterday_str,
    "advancedSearchTerms": [{
        "field": "DomainName",
        "term": "*"
    }]    
}

#json list
json_list = []

try:
    response = requests.post(url, json=data)
    json_data = response.json()

    for domain in json_data['domainsList']:
        w = whois.whois(domain)
        print(w)
        element = {}
        if(w.name==None):
            continue 
        elif(type(w.name)==str):
            element["name"] = w.name
        elif(type(w.name)== list):
            element["name"] = w.name[0]
        
        if(w.domain_name==None):
            continue
        elif(type(w.domain_name)==str):
            element["domain_name"] = w.domain_name
        elif(type(w.domain_name)== list):
            element["domain_name"] = w.domain_name[0]
        
        if(w.emails==None):
            continue 
        elif(type(w.emails)==str):
            element["email"] = w.emails
        elif(type(w.emails)== list):
            element["email"] = w.emails[0]
        
        if(len(json_list)==3): break
        
        #append into list
        json_list.append(element)
        
        
        
except Exception as e:
    print("an error has occured %s", e)


df = pd.DataFrame(json_list)
df.to_csv('output.csv', index=False)


#sending email
send_email()


