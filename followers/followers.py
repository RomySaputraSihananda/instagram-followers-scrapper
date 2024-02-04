import os

from json import dumps
from requests import Session, Response
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ]\t:: %(message)s', datefmt="%Y-%m-%dT%H:%M:%S")

load_dotenv()

class Followers:
    def __init__(self) -> None: 
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'Cookie': str(os.getenv('COOKIE')),
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Ig-App-Id': '936619743392459',
        })

    def __get_user_detail(self, username: str) -> dict:
        response: Response = self.__requests.get('https://i.instagram.com/api/v1/users/web_profile_info/', params={
            'username': username
        })
        
        return response.json()['data']['user']
        
    def _get_followers_by_id(self, id: int) -> None:
        followers: list = []
        next_max_id: int = 0
        while(True):
            response: Response = self.__requests.get(f'https://www.instagram.com/api/v1/friendships/{id}/followers/',
                                            params={
                                                'count': 24,
                                                'max_id': next_max_id
                                            })
            data: dict = response.json()
            
            if(response.status_code != 200): return logging.error('failed to fetch this account')

            users: list = data['users']
            
            if(not users): return logging.error("this account private in your account, follow dlu..")

            for user in users:
                logging.info(f'{user["username"]} :: {user["full_name"]}')

            followers.extend(data['users'])
                
            if(not 'next_max_id' in data): break
            next_max_id += len(users) 

    def _get_followers_by_username(self, username: str) -> None:
        user: dict = self.__get_user_detail(username)
        
        logging.info(f'try fetch followers')
        logging.info(f'username: {user["username"]} [ {user["edge_owner_to_timeline_media"]["count"]} ]  [{user["edge_followed_by"]["count"]} ] [ {user["edge_follow"]["count"]} ] [ {"private" if user["is_private"] else "public"} ] {"[ verivied ]" if user["is_verified"] else ""}')
        
        self._get_followers_by_id(user['id'])

if __name__ == "__main__":
    followers: Followers = Followers()
    followers._get_followers_by_username('alyaassp')
    #followers._get_followers_by_username('ryyo.cs')
