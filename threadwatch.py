import tweepy
from dotenv import load_dotenv
from os import environ
from time import sleep
from airtable import airtable
import re
from dateutil.parser import isoparse
from datetime import datetime
from random import choice

load_dotenv()
auth = tweepy.OAuthHandler(environ.get(
    "THREADWATCH_TW_CONSUMER_KEY"), environ.get("THREADWATCH_TW_CONSUMER_SECRET"))
auth.set_access_token(environ.get(
    "THREADWATCH_TW_ACCESS_TOKEN"), environ.get("THREADWATCH_TW_ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth)
at = airtable.Airtable(environ.get("THREADWATCH_AT_BASE"),
                       environ.get("THREADWATCH_AT_API_KEY"))

greetings = ["Howdy!", "Hi!", "Hello!", "Hiya!", "Bonjour!", "Hola!"]
success_emojis = ["🔮", "✨", "🌈", "😁", "🎉", "🍾", "🥳", "🎁"]
failure_emojis = ["🔭", "🔎", "🔍", "😓", "🤕", "🤷", "👀", "💩"]

while True:
    try:
        for i in range(0, int(environ.get("THREADWATCH_THREAD_CHECK"))):
            # Run DM check routine
            new_dms = api.get_direct_messages(count=50)
            for dm in new_dms:
                if 'urls' not in dm.message_create['message_data']['entities'].keys():
                    message = "Sorry, there was no URL found in that message."
                elif len(dm.message_create['message_data']['entities']['urls']) > 1:
                    message = "Sorry, I can only process one URL at once."
                else:
                    tweet_id = re.findall(
                        '(?<=\/status\/)\d+', dm.message_create['message_data']['entities']['urls'][0]['expanded_url'])
                    if not tweet_id:
                        print('no tweet ids found')
                        message = "Sorry, there was no Tweet in that URL."
                    elif len(tweet_id) > 1:
                        print('too many tweet ids found')
                        message = "Sorry, I need a URL with just one Tweet ID."
                    else:
                        tweet = api.get_status(tweet_id[0])
                        at.create(environ.get("THREADWATCH_AT_TABLE"), {
                                  'tweet_id': tweet_id[0], 'requester': dm.message_create['sender_id'], 'author': tweet.user.screen_name})
                        message = f"{choice(greetings)} I'm keeping an eye on @{tweet.user.screen_name}'s thread for you {choice(success_emojis)}"
                sent_dm = api.send_direct_message(
                    dm.message_create['sender_id'], message)
                api.delete_direct_message(sent_dm.id)
                api.delete_direct_message(dm.id)
            sleep(int(environ.get("THREADWATCH_DM_REFRESH")))
        # Run thread check routine
        for record in at.iterate(environ.get("THREADWATCH_AT_TABLE")):
            reply_id = ''
            for self_reply_tweet in tweepy.Cursor(api.search_tweets, f"to:{record['fields']['author']} from:{record['fields']['author']}", result_type='latest', since_id=record['fields']['tweet_id']).items(1000):
                if (self_reply_tweet.in_reply_to_status_id_str == record['fields']['tweet_id']):
                    reply_id = self_reply_tweet.id
            if reply_id:
                print('reply was found!')
                message = f"{choice(greetings)} It looks like @{record['fields']['author']} replied to the thread you asked me to watch {choice(success_emojis)} https://twitter.com/{record['fields']['author']}/status/{reply_id}"
            elif (datetime.now().astimezone() - isoparse(record['fields']['requested_at'])).days > 9:
                print('tweet expired!')
                message = f"{choice(greetings)} I've been keeping an eye on @{record['fields']['author']}'s thread for the past few days but looks like they haven't updated it. Send me it again if you want me to carry on watching {choice(failure_emojis)} https://twitter.com/{record['fields']['author']}/status/{record['fields']['tweet_id']}"
            else:
                print(
                    f"[~] Found no OP reply for Tweet {record['fields']['tweet_id']}")
                continue
            sent_dm = api.send_direct_message(
                record['fields']['requester'], message)
            api.delete_direct_message(sent_dm.id)
            at.delete(environ.get("THREADWATCH_AT_TABLE"), record['id'])
    except tweepy.TooManyRequests:
        print("Rate limited! Stopping for 15 minutes.")
        sleep(900)
    except tweepy.TweepyException as te:
        print("Problem with the Twitter API!")
        print(f"{te.with_traceback}")
        exit(1)
    except Exception as e:
        print(e)
        print(e.with_traceback)
        sleep(900)
