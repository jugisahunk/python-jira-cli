# Introduction
This is a cli tool for querying Jira. It uses basic authentication. To use it, you'll need to use the username and password credentials for a user with read access to the Jira cloud instance you wish to query against.

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
The query script takes a single, positional argument called ```query``` and runs it against your cloud instance of Jira using the latest version of the api
