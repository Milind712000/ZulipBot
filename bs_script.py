import re
import datetime
import json
import requests as rs
from bs4 import BeautifulSoup

# helpers
regex = re.compile(r'\d+\s\w+')

def create_contest_obj(row):
    cells = row.select("td")
    contest_obj = {}
    contest_obj['ID']=row.get("data-contestid")
    contest_obj['Name']=cells[0].get_text().strip()
    contest_obj['StartTime']= cells[2].get_text().strip()
    contest_obj['duration']= cells[3].get_text().strip()
    contest_obj['Time_left_Start']=regex.search(cells[4].get_text()).group()
    contest_obj['Time_left_Registration']=regex.search(cells[5].get_text()).group()
    return contest_obj

# fetch contest page from codeforce
cfContestUrl = 'https://codeforces.com/contests'
try:
    res = rs.get(cfContestUrl)
    res.raise_for_status()
except:
    print("failed to get the page at ",cfContestUrl)

soup = BeautifulSoup(res.text,"html.parser")

# extract contest details

#array with current and upcoming contests
contests = []
contestSoup = soup.select_one(".datatable table").select("tr")[1:]
for tr in contestSoup:
    obj = create_contest_obj(tr)
    contests.append(obj)

# save to a file
time = datetime.datetime.now()
scraping_time = time.strftime('%m-%d-%Y_%I:%M%p')
name = 'contests_%s_.json'%scraping_time
fh = open(name,'w')
fh.write(json.dumps(contests))
fh.close()