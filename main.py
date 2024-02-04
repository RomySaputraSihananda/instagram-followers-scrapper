import requests
import os

from json import dumps
from dotenv import load_dotenv

load_dotenv()

headers = {
    'Cookie': os.getenv('COOKIE'),
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Ig-App-Id': '936619743392459',
}


response = requests.get('https://www.instagram.com/api/v1/friendships/1536133488/following/', headers=headers,
                        params={
                            'count': 200,
                            'max_id': 0
                        })
#response = requests.get('https://i.instagram.com/api/v1/users/web_profile_info/?username=romys.12', headers=headers)

followers: list = response.json()['users']

for i, follower in enumerate(followers):
    print(i + 1, follower['username'])
