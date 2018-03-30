# Introduction
This is a cli tool for querying Jira. It uses basic authentication. To use it, you'll need to use the username and password credentials for a user with read access to the Jira cloud instance you wish to query against.

# Jira REST API
You need to reference the [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/) when adding functionality to this tool. We will default to using the latest version whenever possible. Go here to jump right to the [search api](https://developer.atlassian.com/cloud/jira/platform/rest/#api-api-2-search-get).

# Configuration
1) Create a root directory named ```config```
2) Create a ```jira.yml``` file in the ```config``` directory
3) Add your Jira ```instance url``` and credentials to the ```jira.yml``` file:
```
host: https://myjira.atlassian.net

username: fthsteven
password: schfifteen
```
4) Run ```pip install -r requirements.txt```

# Using ```query.py```
To generate query results to csv, call ```query.py``` using the ```query``` and ```--csv``` arguments from your terminal. To retrieve all issues created in the last week, you could use the following example:

```python3 query.py --csv="results.csv" "created > -7d"```

