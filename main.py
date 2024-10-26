import tweepy
import requests
import os
from datetime import date
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# Today
today = date.today().strftime("%B %d, %Y")

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

client = tweepy.Client(
    consumer_key=API_KEY, 
    consumer_secret=API_SECRET, 
    access_token=ACCESS_TOKEN, 
    access_token_secret=ACCESS_TOKEN_SECRET
)

def get_coin_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'aud',
        'order': 'market_cap_desc',
        'price_change_percentage': '24h',
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    return response.json()

def get_coin_category_data():
    url = 'https://api.coingecko.com/api/v3/coins/categories'
    response = requests.get(url)
    return response.json()


def get_top_movers(data, key, top_n=5, gainers=True):
    filtered_data = [item for item in data if item[key] is not None]
    sorted_data = sorted(filtered_data, key=lambda x: x[key], reverse=gainers)
    return sorted_data[:top_n]


def create_tweet(data, label, key, gainer=True):
    tweet_type = "Gainers" if gainer else "Losers"
    tweet = f"Top 5 24-Hour {tweet_type} in {label} - {today}\n\n"
    
    for item in data:
        if label == "Categories":
            tweet += f"{'📈' if gainer else '📉'} {item['name'].capitalize()}: {item[key]:.2f}%\n"
        else:  # For individual coins
            tweet += f"{'📈' if gainer else '📉'} ${item['symbol'].upper()} ({item['name']}): A${item['current_price']} ({'+' if item[key] >= 0 else ''}{item[key]:.2f}%)\n"
    
    tweet += '\n #emirbelievedinsomething'
    return tweet

if __name__ == "__main__":
    # Coins
    coin_data = get_coin_data()
    top_coin_gainers = get_top_movers(coin_data, 'price_change_percentage_24h', gainers=True)
    top_coin_losers = get_top_movers(coin_data, 'price_change_percentage_24h', gainers=False)
    
    # Categories
    category_data = get_coin_category_data()
    top_category_gainers = get_top_movers(category_data, 'market_cap_change_24h', gainers=True)
    top_category_losers = get_top_movers(category_data, 'market_cap_change_24h', gainers=False)
    
    # Create tweets for both coins and categories
    tweet_coin_gainers = create_tweet(top_coin_gainers, label="Coins", key="price_change_percentage_24h", gainer=True)
    tweet_coin_losers = create_tweet(top_coin_losers, label="Coins", key="price_change_percentage_24h", gainer=False)
    tweet_category_gainers = create_tweet(top_category_gainers, label="Categories", key="market_cap_change_24h", gainer=True)
    tweet_category_losers = create_tweet(top_category_losers, label="Categories", key="market_cap_change_24h", gainer=False)
    
    print("TWEETING: " + today)
    try:
        # Similarly tweet the categories
        response = client.create_tweet(text=tweet_category_gainers)
        category_gainers_tweet_id = response.data['id']
        client.create_tweet(text=tweet_category_losers, in_reply_to_tweet_id=category_gainers_tweet_id)
        
        # Tweet the gainers and reply with the losers
        response = client.create_tweet(text=tweet_coin_gainers)
        gainers_tweet_id = response.data['id']
        client.create_tweet(text=tweet_coin_losers, in_reply_to_tweet_id=gainers_tweet_id)
        
        print("\tTweeted successfully!")
    except Exception as e:
        print(f"\tError tweeting: {e}")
