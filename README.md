# 24hr Top Gainers and Losers Crypto Bot
## Introduction 
This is a simple implementation of a twitter bot that reports the 24hr top crypto gainers and losers fetched from CoinGecko's API.
## Running the Twitter Bot
### Add your twitter API key and Access Token to the .env
```
API_KEY= <API_KEY>
API_SECRET= <API_SECRET>
ACCESS_TOKEN= <ACCESS_TOKEN>
ACCESS_TOKEN_SECRET= <ACCESS_TOKEN_SECRET>
```
### Setting up the program
Create a virtual environment:
```
python -m venv venv
```
Run that virtual environment:
```
source venv/bin/activate
```
Install all the required dependencies:
```
pip install -r /path/to/requirements.txt
```
### Running the program
```
python main.py
```