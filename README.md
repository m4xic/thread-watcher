# thread-watcher

A Twitter bot that will watch a thread for a reply from OP. Useful for keeping track of developing news or stories with update threads.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

---

> **⚠️ I made this for myself and it's likely to break if you use it.**
> 
> You'll need elevated Twitter API access (free), an Airtable base (free), somewhere to host it (free?) and a can-do attitude to fix the inevitable bugs (priceless)

---

## Configuration

**.env**
```sh
# Airtable settings
THREADWATCH_AT_BASE=                    # Get from Airtable API docs
THREADWATCH_AT_TABLE=                   # "
THREADWATCH_AT_API_KEY=                 # "

# Twitter settings
THREADWATCH_TW_CONSUMER_KEY=            # Get from the Twitter Developer Portal
THREADWATCH_TW_CONSUMER_SECRET=         # "
THREADWATCH_TW_ACCESS_TOKEN=            # Use oauth.py to obtain. Set your redirect URL to localhost and copy the verifier from the URL
THREADWATCH_TW_ACCESS_TOKEN_SECRET=     # "

# Configuration
THREADWATCH_DM_REFRESH=                 # Number of seconds between refreshes of the DM inbox (Twitter enforces a 15 per 15 min ratelimit)
THREADWATCH_THREAD_CHECK=               # Number of DM inbox refreshes between thread checks
```

---

## Running

Once it's configured, just leave `python3 threadwatch.py` running and watch it fly. Enjoy!
