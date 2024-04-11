import tweepy
from logging import getLogger
from lookwhosstreaming.celery import app
from streams.models import *


@app.task(bind = True)
def alert_twitter(self, data, *args, **kwargs):
    logger = getLogger('broadcasts')
    
    try:
        api_account = APIAccount.objects.filter(platform__name = "Twitter")
        
        if api_account and (api_account := api_account[0]):
            auth = tweepy.OAuthHandler(api_account['client_id'], api_account['auth_token'])
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth)
            
            text = f"{data['name']} has gone live on {data['platform']}! {data['title']} \n{data['url']}"
            api.update_status(status=text)
            
            logger.info(f"Tweeted for live stream by {data['name']}")
            
    except Exception as e:
        logger.error(f"Failed to tweet for {data['name']} with {e}")