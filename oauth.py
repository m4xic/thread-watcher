# Reused from https://github.com/m4xic/twitter-bookmarks/blob/main/oauth.py
import tweepy
from dotenv import load_dotenv
from os import environ

load_dotenv()

auth = tweepy.OAuthHandler(environ.get(
    "THREADWATCH_TW_CONSUMER_KEY"), environ.get("THREADWATCH_TW_CONSUMER_SECRET"))
redirect_url = auth.get_authorization_url()
print(f"You need to login via Twitter: {redirect_url}")
verifier = input("Enter your verifier code:")
auth.get_access_token(verifier)

print("You've completed authentication. Add this to the bottom of your .env file:")
print(
    f"\nTHREADWATCH_TW_ACCESS_TOKEN={auth.access_token}\nTHREADWATCH_TW_ACCESS_TOKEN_SECRET={auth.access_token_secret}")
