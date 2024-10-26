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
client = tweepy.Client( consumer_key=API_KEY, 
                        consumer_secret=API_SECRET, 
                        access_token=ACCESS_TOKEN, 
                        access_token_secret=ACCESS_TOKEN_SECRET)

# Get API Data
def get_coin_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'aud',
        'order': 'market_cap_desc',
        'price_change_percentage': '24h',
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    coins = response.json()
    return coins

def get_coin_category_data():
    url = 'https://api.coingecko.com/api/v3/coins/categories'
    response = requests.get(url)
    categories = response.json()
    return categories

def get_top_gainers(coin):
    sorted_coins = sorted(coin, key=lambda x: x['price_change_percentage_24h'], reverse=True)
    top_gainers = sorted_coins[:5] 
    return top_gainers

def get_top_losers(coin):
    sorted_coins = sorted(coin, key=lambda x: x['price_change_percentage_24h'], reverse=False)
    top_losers = sorted_coins[:5] 
    return top_losers

def create_tweet(top_gainers, gainer=True):
    tweet = f"Top 5 24-Hour {'Gainers' if gainer else 'Losers'} - " + today + '\n\n'
    for coin in top_gainers:
        tweet += f"{'📈' if gainer else '📉'} ${coin['symbol'].upper()} ({coin['name']}): A${coin['current_price']} ({'+' if coin['price_change_percentage_24h'] >= 0 else ''}{coin['price_change_percentage_24h']:.2f}%)\n"
    tweet += '\n #emirbelievedinsomething'
    return tweet

if __name__ == "__main__":
    coin = get_coin_data()
    top_gainer = get_top_gainers(coin)
    top_losers = get_top_losers(coin)
    
    # Create tweets
    tweet_gainers = create_tweet(top_gainer, gainer=True)
    tweet_losers = create_tweet(top_losers, gainer=False)
    
    # Tweet the gainers
    try:
        response = client.create_tweet(text=tweet_gainers)
        gainers_tweet_id = response.data['id']  # Get the ID of the gainers tweet
        # Tweet the losers as a reply to the gainers tweet
        client.create_tweet(text=tweet_losers, in_reply_to_tweet_id=gainers_tweet_id)
        print("Tweeted successfully!")
    except Exception as e:
        print(f"Error tweeting: {e}")




