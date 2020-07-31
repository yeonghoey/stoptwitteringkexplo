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
    # NOTE: GitHub Actions의 Cron 최소 인터벌 설정은 5분이지만,
    # 실제 실행되는 패턴을 보니 7~10분 정도 걸리기 때문에, 중복되더라도 놓치는 것이 없도록
    # 대략 10분으로 잡는다.
    if tweeted_within_n_minutes(latest, 10):
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
            'image': {'url': 'https://yeonghoey.github.io/stoptwitteringkexplo/main.jpg'},
        }],
    })


if __name__ == '__main__':
    main()
