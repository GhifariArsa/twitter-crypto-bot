import tweepy
import requests
import os
from datetime import date
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Today
today = date.today().strftime("%B %d, %Y")

# Twitter API credentials from environment variables
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
client = tweepy.Client(consumer_key=API_KEY, consumer_secret=API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET,)

# Get API Data
def get_coin_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'price_change_percentage': '24h',
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    coins = response.json()
    return coins

def get_top_gainers(coin):
    sorted_coins = sorted(coin, key=lambda x: x['price_change_percentage_24h'], reverse=True)
    top_gainers = sorted_coins[:5] 
    return top_gainers

def get_top_losers(coin):
    sorted_coins = sorted(coin, key=lambda x: x['price_change_percentage_24h'], reverse=False)
    top_losers = sorted_coins[:5] 
    return top_losers

def create_tweet(top_gainers, top_losers):
    tweet = "Top 24hr Gainers and Losers - " + today + '\n'
    for coin in top_gainers:
        tweet += f"${coin['symbol'].upper()} ({coin['name']}): {coin['price_change_percentage_24h']:.2f}%\n"
    
    return tweet

def tweet_top_gainers():
    coin = get_coin_data()
    tweet = get_top_gainers_and_loss(coin)
    try:
        client.create_tweet(text=tweet)
        print("Tweeted successfully!")
    except Exception as e:
        print(f"Error tweeting: {e}")

# Call the function to tweet
if __name__ == "__main__":
    coin = get_coin_data()
    print(get_top_gainers(coin))
