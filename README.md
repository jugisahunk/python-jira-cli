# Introduction
This is a cli tool for querying Jira. It uses basic authentication. To use it, you'll need to use the username and password credentials for a user with read access to the Jira cloud instance you wish to query against.

# Setup
This CLI tool is tested to work using python 3.7.1. It will _not_ work on python 2.7.*. If you're on a mac, head to [python.org](https://www.python.org/downloads/) to download and install it or use brew. Here's a good guide to [using brew](https://docs.python-guide.org/starting/install3/osx/) as your installer.

Once you have python ready to go, run `pip install -r requirements.txt`. That's it! Refer to the **Using** section below for helping using your shiny, new cli :).

# Jira REST API
You need to referance the [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/) when adding functionality to this tool. We will default to using the latest version whenever possible. Go here to jump right to the [search api](https://developer.atlassian.com/cloud/jira/platform/rest/#api-api-2-search-get).

# Using ```query.py```
```
usage: query.py [-h] [--csv CSV] [-c] [-l] query

positional arguments:
  query       JQL query

optional arguments:
  -h, --help  show this help message and exit
  --csv CSV   CSV Output Filename
  -c          Include Cycle Time Data. Assumes cycle begins with "In Progress"
              and ends with "Resolved." Ignores issues which never entered "In
              Progress"
  -l          Include Lead Time Data. Assumes lead begins with "Open" and ends
              with "Resolved."
```
## Examples:
To retrieve all issues created in the last week and store them in a csv file named "last_week.csv" you would run:

```python3 query.py --csv="last_week" "created > -7d"```

If I wanted to add in cycle time data for those issues, I'd modify the line like so:

```python3 query.py -c --csv="last_week" "created > -7d"```

If I didn't care to name the file anything special:

```python3 query.py -c "created > -7d"```

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
    { 
        "name" : "key", 
        "value" : ["key"] 
    },
    { 
        "name" : "summary", 
        "value" : ["fields.summary"] 
    }
]
```
***Outputs***

|key | summary |
|---|---|
| ABC-15 | A jira issue summary value |
| ABC-16 | A second jira issue summary value |

### Formatting Examples

#### *Basic String format*
This utilizes the basic string formatting functionality in python; the ```{}``` is simply replaced by the value output by the JMESPath expression. The following is an example assuming a Jira issue with the key of 'ABC-15':
```
[
    { 
        "name" : "Key Greeting", 
        "value" : ["key", "Hello, my key is {}"] 
    }
]
```
This mapping outputs the record:

|Key Greeting|
|---|
| Hello, my value is: ABC-15 |

#### *Config value options:*
The formatting knows to look for certain keywords and replace them with helpful data:
- ```[host]``` get's replaced by the ```host``` value specified in the ```jira.yml``` file

#### *Combined example*
The basic format may be combined with the config value keywords. For instance, you could output the instance url for browsing to an issue with the following field config:
```
[
    { 
        "name" : "url", 
        "value" : ["key","[host]/browse/{}"]
    }
]
```
Assuming the configured host value is ```https://myjira.atlassian.net``` and the issue keys returned are XYZ-100 and XYZ-101, This mapping outputs the record: 

|url |
|---|
| https://myjira.atlassian.net/browse/XYZ-100 |
| https://myjira.atlassian.net/browse/XYZ-101 |

### Field Treatments
Though most fields can be easily output as single values, some may require *special treatment*. In those cases, refer to [JMESPath specifications](http://jmespath.readthedocs.io/en/latest/specification.html) for help. As a quick example, you could join together all values in a multi-value field with the ```|``` character with the following JMESPath expression where ```@``` represents the path to the multi-value field:
```
join(`|`, @)
```

