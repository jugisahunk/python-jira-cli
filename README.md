# Introduction
This is a cli tool for querying Jira. It uses basic authentication. To use it, you'll need to use the username and password credentials for a user with read access to the Jira cloud instance you wish to query against.

# Jira REST API
You need to refereance the [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/) when adding functionality to this tool. We will default to using the latest version whenever possible. Go here to jump right to the [search api](https://developer.atlassian.com/cloud/jira/platform/rest/#api-api-2-search-get).

# Using ```query.py```
To generate query results to csv, call ```query.py``` using the ```query``` and ```--csv``` arguments from your terminal. To retrieve all issues created in the last week, you could use the following example:

```python3 query.py --csv="results.csv" "created > -7d"```

# Configuration

## Script Config
1) Create a root directory named ```config```
2) Create a ```jira.yml``` file in the ```config``` directory
3) Add your Jira ```instance url``` and credentials to the ```jira.yml``` file:
```
host: https://myjira.atlassian.net

username: fthsteven
password: schfifteen
```
4) Run ```pip install -r requirements.txt```

## Field Config
```query.py``` is agnostic to your Jira instance. You therefore need to tell it how you want it to output your issue field data
1) Create a ```fields.json``` file in the ```config``` directory
2) Add a JSON object for each field in your Jira instance you want exported. 

***Note: csv column order is determined by the order of these field objects.***
### Structure
The ```fields.json``` contains a single array of all field objects. Each field object has a *name* and a *value* property.
-**name:** csv column name 
-**value:** array with 1 or 2 values. - The first value is a [JMESPath](http://jmespath.org/) expression identifying the field value in the JSON api response. The second is a simple format string which is used to output the value in more robust ways. If no formatting string is given, only the field value is output. 

Here's an example that outputs only the *key* and *summary* fields of issues returned by a query:

```
[
    { "name" : "key", "value" : ["key"] },
    { "name" : "summary", "value" : ["fields.summary"] }
]
```
***Outputs***
key | summary |
|---|---|
| ABC-15 | A jira issue summary value |
| ABC-16 | A second jira issue summary value |

### Formatting Examples

##### *Basic String format*
This utilizes the basic string formatting functionality in python; the ```{}``` is simply replaced by the value output by the JMESPath expression. The following is an example assuming a Jira issue with the key of 'ABC-15':
```
[
    { "name" : "Key Greeting", "value" : ["key", "Hello, my key is {}"] }
]
```
This mapping outputs the record: 
Key Greeting |
|---|
| Hello, my value is: ABC-15 |

##### *Config value options:*
The formatting knows to look for certain keywords and replace them with helpful data:
- ```[host]``` get's replaced by the ```host``` value specified in the ```jira.yml``` file

##### *Combined example*
The basic format may be combined with the config value keywords. For instance, you could output the instance url for browsing to an issue with the following field config:
```
[
    { "name" : "url", "value" : ["key","[host]/browse/{}"]
]
```
Assuming the configured host value is ```https://myjira.atlassian.net``` and the issue keys returned are XYZ-100 and XYZ-101, This mapping outputs the record: 
url |
|---|
| https://myjira.atlassian.net/browse/XYZ-100 |
| https://myjira.atlassian.net/browse/XYZ-101 |