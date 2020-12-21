# -*- coding: utf-8 -*-
import pymysql
from sqlalchemy import create_engine
import getpass
import requests as r
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pandas as pd


password=getpass.getpass()

eng=create_engine(f"mysql+pymysql://root:{password}@localhost/hof")

tot=pd.read_sql_table("students", eng)

headers="""Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Cache-Control: no-cache
Connection: keep-alive
Cookie: _octo=GH1.1.495336122.1588197818; tz=Europe%2FMadrid; _device_id=3e5d463bf0446012d65bdfa018b4e3dc; _ga=GA1.2.1805656397.1591012101; logged_in=yes; dotcom_user=Eldiias; user_session=pwPnB7WQA7eN6xXto4rtKNTdHQWjmWWK-xRJFtE035F1G0hr; __Host-user_session_same_site=pwPnB7WQA7eN6xXto4rtKNTdHQWjmWWK-xRJFtE035F1G0hr; has_recent_activity=1; _gid=GA1.2.1110359907.1596533794; _gh_sess=ypbomtc7%2FmSl5BG4LaEkQ8tA92Aob4tDCzdmZc62zDvSh4%2F8kVno7uz2kU3pP%2FR927jam05Lkrq7o5v5%2FJn%2Bfiy6ozZuv%2BXWghNbP3V7%2FxiR9pjBj4Hwctuhzg650q6TIJjRkXBg8aXJeX3Wx6oq9RIgfmP7lUrw6mytq1XvAVj9WA4oApdFVq%2Fbf8WxJXmyQwJVO15S%2F8rLy0t0M1ftrcOLDfrRmt2QEZchnUjtOQpv8q4l2Vd9k6cYbvaD%2FzxLvU6ipDegFEntYn9CgP01AW6W%2Ftdn6wIgR3GvYCyEcHhdkizOiIrr4Gsu3lGUTtw9rWPlc%2F%2B6Dh78nZKltb1wjX1nfyAiPPXm811ishlTbjcwKtUpPl4bwJGW15mRzsJJ1LJIvOqFzCJACzZMnKDIofD2pp4SGy8peK49Do1NHDTc8qMQi9pNs6VJgzHloQyQ%2FZNBVU9RfS3eGFnuK0uM4Aw0jGPyq9djVXgC2KoKgqHwxylYbhNlqXAtykh%2BHJbgWYRx1Uo5hKHG1J1St9lLnTwePXPi64RSwxfmg8wIrXkrarEV--DBQF11sU2ShY18T5--GAcCdFpN6qVHXbSHrnv2OQ%3D%3D
DNT: 1
Host: github.com
Pragma: no-cache
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 OPR/70.0.3728.71"""

headers=dict(i.split(': ') for i in headers.split('\n'))

def get_last_update(jj):
    for k, v in reversed(list(jj.items())):
        if int(v)>0:
            return k
            break
        if k==list(jj.keys())[0]:
            return None
        
def get_list_of_data(profile):
    j={i.get('data-date'):i.get('data-count') for i in BeautifulSoup(r.get(f'https://github.com/{profile}', headers=headers).content).select('svg>g rect')}
    return get_last_update(j)


tot['Last_Update']=tot.URL.map(lambda text: re.findall('https://github.com/(.*)', text)[0]).map(get_list_of_data)
tot.Last_Update=pd.to_datetime(tot.Last_Update)
tot['Difference']=(datetime.now()-tot.Last_Update).dt.days.apply(lambda x: None if x>180 else x)
newdf=tot.copy()
newdf.dropna().drop(["Last_Update","Difference"], axis=1).to_sql("six_months", eng, if_exists="replace", index=False)
newdf[newdf.Last_Update.isna()].drop(["Last_Update","Difference"], axis=1).to_sql("no_update", eng, if_exists="replace", index=False)


