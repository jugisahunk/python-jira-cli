import requests
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("query", help="JQL query", type=str)
parser.parse_args()
args = parser.parse_args()

with open("config/credentials.yml", 'r') as ymlfile:
    try:
        credentials = yaml.load(ymlfile)
    except yaml.YAMLError as exception:
        print(exception)
        sys.exit(1)

url = 'https://vitals.atlassian.net/rest/api/latest/search?jql=' + args.query

r = requests.get(url, auth=(credentials['username'], credentials['password']))
print(r.status_code)
print(r.text)