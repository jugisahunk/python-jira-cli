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
import jmespath
import sys

from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        t = '{0:%H:%M:%S}'.format(datetime.datetime.now())
        if(response.status == 200):
            print('Done: {}, {} ({})'.format(t, response.url, response.status))      
        else:
            print("############FAILURE############")
            print('Done: {}, {} ({})'.format(t, response.url, response.status))      

        return await response.text()

async def run(r,url):
    tasks = []
    all_issues = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    auth = aiohttp.BasicAuth(login=jira['username'], password=jira['password'])
    conn = aiohttp.TCPConnector(limit=30)
    async with ClientSession(auth=auth, connector=conn) as session:
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

def get_cycle_data(issue):
    return ["cycle_start_datetime", "cycle_end_datetime", "cycle_duration"]

parser = argparse.ArgumentParser()
parser.add_argument("query", help="JQL query", type=str)
parser.add_argument("--csv", help="CSV Output Filename", type=str, default="results")
parser.add_argument("-c", 
        help="Include Cycle Time Data. Assumes cycle begins with \"In Progress\" and ends with \"Resolved.\" Ignores issues which never entered \"In Progress\"", 
        action='store_true')
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
print("hitting url: " + url)
r = requests.get(url, auth=(jira['username'], jira['password']))
print("Status: {}".format(r.status_code))

json_data_parsed = json.loads(r.text)

if(r.status_code != 200):
    print("request returned with error code: {}".format(r.status_code))

    for error in json_data_parsed["errorMessages"]:
        print("Error: {}".format(error))

    for warning in json_data_parsed["warningMessages"]:
        print("Warning: {}".format(warning))

    sys.exit(1)


total_results = json_data_parsed["total"]
print("Found {} total results.".format(total_results))

if(total_results > 50):
    task_count = math.ceil((total_results) / 50)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(task_count, url))
    all_issues = loop.run_until_complete(future)
    loop.close()
else:
    all_issues = json_data_parsed["issues"]

print("Found {} issues. Retrieved {}".format(total_results, len(all_issues)))

with open('config/fields.json') as json_file:
    fields = json.load(json_file)

csv_columns = jmespath.compile('[*].name').search(fields)

if(args.c):
    csv_columns.extend(["cycle_start", "cycle_end", "cycle_time"])

csv_value_paths = jmespath.compile('[*].value').search(fields)

print("Writing results to {file_name}.csv".format(file_name=args.csv))

with open(args.csv + ".csv", 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(csv_columns)
    for issue in all_issues:
        issue_values = []
        for path in csv_value_paths:
            expression = jmespath.compile(path[0]) #jmespath expression
            field_value = expression.search(issue)
            
            if(len(path) == 2):
                value_format = path[1] #value output format
                output_value = value_format.replace('[host]', jira['host']).format(field_value)
            else:
                output_value = field_value

            issue_values.append(output_value)

        if(args.c):
            issue_values.extend(get_cycle_data(issue))
        
        csv_writer.writerow(issue_values)
