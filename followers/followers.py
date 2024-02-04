import os

from json import dumps
from requests import Session, Response
from dotenv import load_dotenv

load_dotenv()

class Followers:
    def __init__(self) -> None: 
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'Cookie': str(os.getenv('COOKIE')),
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Ig-App-Id': '936619743392459',
        })

    def __get_user_id(self, username: str) -> int:
        response: Response = self.__requests.get('https://i.instagram.com/api/v1/users/web_profile_info/', params={
            'username': username
        })
        return int(response.json()['data']['user']['id'])
        
    def _get_followers_by_id(self, id: int) -> None:
        response: Response = self.__requests.get(f'https://www.instagram.com/api/v1/friendships/{id}/following/',
                                        params={
                                            'count': 200,
                                            'max_id': 0
                                        })
        
        print(response.json())
        #for i in response.json()['users']:
            #print(i)

    def _get_followers_by_username(self, username: str) -> None:
        user_id: int = self.__get_user_id(username)
        self._get_followers_by_id(user_id)

        

if __name__ == "__main__":
    followers: Followers = Followers()
    followers._get_followers_by_username('yukkirikoo')
