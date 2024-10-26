import tweepy
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials from environment variables
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
client = tweepy.Client(consumer_key=API_KEY, consumer_secret=API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET,)

# Get the top gainers from CoinGecko
def get_top_gainers():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'price_change_percentage': '24h',
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    coins = response.json()
    
    # Sort by top 24h gainers
    sorted_coins = sorted(coins, key=lambda x: x['price_change_percentage_24h'], reverse=True)
    top_gainers = sorted_coins[:5]  # Top 5 coins
    
    # Format the data for tweeting
    tweet = "Top 24h Gainers in Crypto:\n"
    for coin in top_gainers:
        tweet += f"{coin['name']} ({coin['symbol'].upper()}): {coin['price_change_percentage_24h']:.2f}%\n"
    
    return tweet

# Post a tweet
def tweet_top_gainers():
    tweet = get_top_gainers()
    try:
        client.create_tweet(text=tweet)
        print("Tweeted successfully!")
    except Exception as e:
        print(f"Error tweeting: {e}")

# Call the function to tweet
if __name__ == "__main__":
    tweet_top_gainers()
