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
    latest = fetch_latest()
    # NOTE: GitHub Actions의 Cron 인터벌 최소 값은 5분이다.
    if tweeted_within_n_minutes(latest, 5):
        post_message(latest)


def fetch_latest():
    api = twitter.Api(consumer_key=TWITTER_API_KEY,
                      consumer_secret=TWITTER_API_KEY_SECRET,
                      access_token_key=TWITTER_ACCESS_TOKEN,
                      access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    return api.GetUserTimeline(screen_name='Kexplo', count=1)[0]


def tweeted_within_n_minutes(latest, n):
    now = time.time()
    return latest.created_at_in_seconds + n*60 > now


def post_message(latest):
    requests.post(DISCORD_WEBHOOK_URL, json={
        'embeds': [{
            'title': '찬웅이형 트위터 그만해',
            'description': f'> {latest.text}',
            'url': assemble_status_url(latest),
            'thumbnail': {
                'url': 'https://yeonghoey.github.io/stoptwitteringkexplo/index.jpg',
            },
        }],
    })


def assemble_status_url(latest):
    # NOTE: Status로 직접가는 URL을 python-twitter에서
    # 만들어주지 않는 것으로 보인다.
    user_id = latest.user.id
    status_id = latest.id
    return f'https://twitter.com/{user_id}/status/{status_id}'


if __name__ == '__main__':
    main()
