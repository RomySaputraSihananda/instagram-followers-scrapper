import os

from requests import Session, Response
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ]\t:: %(message)s', datefmt="%Y-%m-%dT%H:%M:%S")

load_dotenv()

class Followers:
    def __init__(self, cookie: str | None) -> None:
        self.__cookie: str| None = cookie 
        
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'Cookie': "" if not self.__cookie else self.__cookie,
            'User-Agent': 'Instagram 126.0.0.25.121 Android (23/6.0.1; 320dpi; 720x1280; samsung; SM-A310F; a3xelte; samsungexynos7580; en_GB; 110937453)',
            'X-Ig-App-Id': '936619743392459',
        })

        self.__result: dict = {}
        self.__result["user_detail"] = {}
        self.__result["followers"] = []

    def __get_user_detail(self, username: str) -> dict:
        response: Response = self.__requests.get('https://i.instagram.com/api/v1/users/web_profile_info/', params={
            'username': username
        })

        user_detail: dict = response.json()['data']['user']

        self.__result["user_detail"] = user_detail 
        
        return user_detail
        
    def _get_followers_by_id(self, id: int) -> None:
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

            self.__result["followers"].extend(data['users'])
                
            if(not 'next_max_id' in data): break
            next_max_id += len(users) 

    def get_followers_by_username(self, username: str) -> dict | None:
        if(not self.__cookie): return logging.error("cookie required")

        user: dict = self.__get_user_detail(username)
        
        logging.info(f'try fetch followers')
        logging.info(f'username: {user["username"]} [ {user["edge_owner_to_timeline_media"]["count"]} ] [{user["edge_followed_by"]["count"]} ] [ {user["edge_follow"]["count"]} ] [ {"private" if user["is_private"] else "public"} ] {"[ verivied ]" if user["is_verified"] else ""}')
        
        self._get_followers_by_id(user['id'])

        return self.__result

if __name__ == "__main__":
    followers: Followers = Followers(os.getenv('COOKIE'))
    followers.get_followers_by_username('alyaassp')
    #followers.get_followers_by_username('ryyo.cs')
