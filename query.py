import math
import requests
import asyncio
import aiohttp
import argparse
import yaml
import csv
import json
import time
import datetime

from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        t = '{0:%H:%M:%S}'.format(datetime.datetime.now())
        print('Done: {}, {} ({})'.format(t, response.url, response.status))        
        return await response.text()

async def run(r,url):
    tasks = []
    all_issues = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    auth = aiohttp.BasicAuth(login=jira['username'], password=jira['password'])
    async with ClientSession(auth=auth) as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url + "&startAt={}".format(i*50), session))
            tasks.append(task)

        response_texts = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable

        return get_response_issues(response_texts)

def get_response_issues(response_texts):
    all_issues = []
    for response_text in response_texts:
        issue_page = json.loads(response_text)["issues"]
        all_issues.extend(issue_page)
    
    return all_issues

parser = argparse.ArgumentParser()
parser.add_argument("query", help="JQL query", type=str)
parser.add_argument("--csv", help="CSV Output Filename", type=str)
parser.parse_args()
args = parser.parse_args()

search_api = "/rest/api/latest/search?jql="

with open("config/jira.yml", 'r') as ymlfile:
    try:
        jira = yaml.load(ymlfile)
    except yaml.YAMLError as exception:
        print(exception)
        sys.exit(1)

url = jira["host"] + search_api + args.query

print("querying: " + args.query)
r = requests.get(url, auth=(jira['username'], jira['password']))
print("Status: {}".format(r.status_code))

json_data_parsed = json.loads(r.text)
total_results = json_data_parsed["total"]
print("Found {} total results.".format(total_results))

if(total_results > 50):
    task_count = math.ceil((total_results) / 50)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(task_count, url))
    all_issues = loop.run_until_complete(future)
else:
    all_issues = json_data_parsed["issues"]

print("Found {} issues. Retrieved {}".format(total_results, len(all_issues)))

if(args.csv):

    print("issues returned: " + str(len(all_issues)))

    with open(args.csv + ".csv", 'w') as csvfile:

        csv_writer = csv.writer(csvfile)

        csv_writer.writerow(["key","url","summary"])
        for issue in all_issues:
            issue_key = issue["key"]
            url = jira["host"] + "/browse/" + issue_key
            summary = issue["fields"]["summary"]

            csv_writer.writerow([issue_key, url, summary])