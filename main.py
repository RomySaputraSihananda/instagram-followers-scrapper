import click
import os
import pandas

from json import dumps

from followers import Followers

@click.command()
@click.option('--cookie')
@click.option('--username', default='romys.12')
@click.option('--output', default='data')
def main(**kwargs) -> None:
    username: str = str(kwargs.get('username'))
    
    followers: Followers = Followers(kwargs.get('cookie'))
    
    data: dict | None = followers.get_followers_by_username(username) 
    if(not data): return None
        
    output: str = f'{kwargs.get("output")}/{username}'

    if(not os.path.exists(output)): 
        os.mkdir(output)

    with open(f'{output}/{username}.json', 'w') as file:
        file.write(dumps(data, indent=4, ensure_ascii=False))

    df = pandas.DataFrame(data=data['followers'])
    df.to_csv(f'{output}/{username}.csv', sep=',')
        

if __name__ == "__main__":
    main()
