import requests
import argparse
import yaml
import csv
import json

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

r = requests.get(url, auth=(jira['username'], jira['password']))
print("querying: " + args.query)
print(r.status_code)
print(r.text)

if(args.csv):
    json_data_parsed = json.loads(r.text)
    issue_data = json_data_parsed["issues"]

    print("issues returned: " + str(len(issue_data)))

    with open(args.csv + ".csv", 'w') as csvfile:

        csv_writer = csv.writer(csvfile)

        csv_writer.writerow(["key","url","summary"])
        for row in issue_data:
            issue_key = row["key"]
            url = jira["host"] + "/browse/" + issue_key
            summary = row["fields"]["summary"]
            
            csv_writer.writerow([issue_key, url, summary])