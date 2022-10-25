# Purpose

This is a single page trading application built for Coinbase Prime using Dash, an open source framework for building Python data apps.  

All scripts are written in Python and tested with version 3.8.9.

## Installation

Simply clone the repo from your terminal window with the below command.

```bash
git clone https://github.com/jc-cb/insto-trading-app-py
```

In order to run this, you will need to be running at least Python 3.8 so that you can install some key dependencies. To install dependencies, run the following: 
```
pip install -r requirements.txt
```
You will also need API key credentials from a valid Coinbase Prime portfolio in order to use this application.

Add your credentials to ``example.env``, then run this command to rename that file:
```
cp example.env .env
```

You can now run the program with the below command, which will open the application in your default browser window: 

```
python app.py
```

For information around Dash, please visit their [documentation](https://dash.plotly.com/introduction). 