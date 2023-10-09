# Logging Class Usage Guide

## About
This logging class has functions that can print logs in the terminal and/or in a file and/or upload logs to a Grafana Loki Server.
The following logging types are supported:
1. DEBUG
2. INFO
3. WARNING
4. ERROR
5. CRITICAL

## Getting Started
Please install all the required packages from the requirements.txt
```sh
pip install -r requirements.txt
```

### Importing The Class
```python
import sys
sys.path.insert(0, r"<Location of Repo>")
from Logging_Import import *
```

### Initializing The Class
```python
log = LogUpload('<ENTER LOG FILE NAME>', 'ENTER LOGGING LEVEL')
```
The first parameter is the name of which your log file will be saved. 
It will have the following naming convention: %d_%m_%Y-%H-%M-%S_<LOG FILE NAME>_<LOGGING LEVEL>_Log.log

The second parameter is the Logging Level, there are 3 options to choose from:
1. Silent: Nothing is printed in the Python Terminal, logs will be published in the log file and uploaded to Grafana Loki if it is initialized (below). **Level=logging.INFO**
   
2. Print: Logs will be printed in the Python Terminal, logs will be published in the log file and uploaded to Grafana Loki if it is initialized (below). **Level=logging.INFO**

    **_THIS IS THE DEFAULT SETTING_**
   
4. Debug: Logs will be printed in the Python Terminal, logs will be published in the log file and uploaded to Grafana Loki if it is initialized (below). **Level=logging.DEBUG**

### Enabling Loki Logging
After initializing the class run the following command:
```python
initialize_loki(url, system_name)
```
The first parameter is the Loki URL, it should be in the following format: "https://my-loki-instance/loki/api/v1/push"

The second parameter is the system name, this is added as a tag so that you can filter for this specific system in Grafana Loki. 


## Usage
```python

log.debug("This is a Debug Message")

log.info("This is Info Message")

log.warning("This is a Warning Message")

log.error("This is a Error Message")

log.critical("This is a Critical Message")

```

