import os
import time
import requests
import twitter

TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_KEY_SECRET = os.environ['TWITTER_API_KEY_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']


def main():
    if tweeted_within_5_minutes():
        post_message()


def tweeted_within_5_minutes():
    api = twitter.Api(consumer_key=TWITTER_API_KEY,
                      consumer_secret=TWITTER_API_KEY_SECRET,
                      access_token_key=TWITTER_ACCESS_TOKEN,
                      access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

    latest = api.GetUserTimeline(screen_name='Kexplo', count=1)[0]

    last_tweeted_at = latest.created_at_in_seconds
    now = time.time()
    return last_tweeted_at + 5*60 > now


def post_message():
    requests.post(DISCORD_WEBHOOK_URL, json={'content': '찬웅이형 트위터 그만해'})


if __name__ == '__main__':
    main()
