import requests
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("query", help="JQL query", type=str)
parser.parse_args()
args = parser.parse_args()

query_api = "/rest/api/latest/search?jql="

with open("config/jira.yml", 'r') as ymlfile:
    try:
        jira = yaml.load(ymlfile)
    except yaml.YAMLError as exception:
        print(exception)
        sys.exit(1)

url = jira["host"] + query_api + args.query

r = requests.get(url, auth=(jira['username'], jira['password']))
print(r.status_code)
print(r.text)