from bs4 import BeautifulSoup
import requests
import pandas as pd
import html5lib
import json
from joblib import Parallel, delayed

def scrape_job(url):
    page = requests.get(url)
    json_data = page.json()
    return json_data

url = 'https://www.cermati.com/karir'
page = requests.get(url)
content = page.content
soup = BeautifulSoup(content, 'html.parser')
lists = soup.find_all("script", type="application/json")
script = lists[0].contents[0]
json_data = json.loads(str(script))
json_main = json_data['smartRecruiterResult']

job_list = []
countries = list(json_data['smartRecruiterResult'].keys())
for country in countries:
    no = len(json_main[country]['content'])
    for i in range(0, no):
        job_list.append(json_main[country]['content'][i]['ref'])

data = Parallel(n_jobs=5)(delayed(scrape_job)(url) for url in job_list)

df = pd.DataFrame(data)
df1 = pd.DataFrame()

df1['Department name'] = df['department'].apply(lambda x: x['label'] if isinstance(x, dict) else None)
df1['title'] = df['name']
df1['location'] = df['location'].apply(lambda x: x['city'] if isinstance(x, dict) else None).str.cat(
    df['customField'].apply(lambda x: x[len(x) - 1]['valueLabel'] if isinstance(x, list) else None), sep=", ")
df1['description'] = df['jobAd'].apply(lambda x: x['sections']['jobDescription']['text'] if isinstance(x, dict) else None)
df1['description'] = df1['description'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())
df1['description'] = df1['description'].apply(lambda x: x.split('.'))
df1['qualification'] = df['jobAd'].apply(lambda x: x['sections']['qualifications']['text'] if isinstance(x, dict) else None)
df1['qualification'] = df1['qualification'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())
df1['qualification'] = df1['qualification'].apply(lambda x: x.split('.'))
df1['job_type'] = df['typeOfEmployment'].apply(lambda x: x['label'] if isinstance(x, dict) else None)

df2 = df1.groupby('Department name')

final_data = df2.apply(lambda x: x.to_dict(orient='records')).to_dict()

for department, rows in final_data.items():
    for row in rows:
        row.pop("Department name")

# final_data
with open('solution.json', 'w') as f:
      json.dump(final_data, f, indent=2)
