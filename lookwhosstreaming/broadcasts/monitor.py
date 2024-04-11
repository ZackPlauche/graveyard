import os
import django
import json
import random
from broadcasts.instagram.IGbot import InstagramBroadcastBot, to_json, from_json
from broadcasts.youtube.YTbot import YoutubeBroadcastBot
from broadcasts.twitch.Twitchbot import TwitchBroadcastBot
from broadcasts.alert import alert_twitter
from datetime import datetime, timedelta
from django.conf import settings
from django.db.utils import IntegrityError
from django.utils import timezone
from logging import getLogger
from time import sleep

from lookwhosstreaming.celery import app
from instagram_private_api import ClientChallengeRequiredError, ClientCheckpointRequiredError
from streams.models import APIAccount, Account, Stream, Platform

if __name__ == "__main__":  
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lookwhosstreaming.settings")
    django.setup()

@app.task(bind=True)
def monitor_instagram(self, track_live=False, error_sleep=5, round_sleep=3):
    logger = getLogger('broadcasts.instagram')
    logger.info(f"Started checking instagram users for broadcast activity, track_live = {track_live}")
    
    apis = {}  # list with apis of usernames to use
    platform = Platform.objects.filter(name__iexact="Instagram")[0]
    
    # Get usernames
    monitor_accounts = Account.objects.filter(platform__name__iexact = "instagram", monitor = True, live = track_live)
    # logger.debug(f"Obtained Instagram accounts")
    
    # Go over all usernames to scrape
    for monitor_account in monitor_accounts:
        import time
        round_start = time.time()
        validAPI = False
        
        # Try to obtain a working api instance
        while not validAPI and (api_accounts := APIAccount.objects.filter(platform__name__iexact = "instagram", blacklist = False)):
            try:
                api_account = random.choice(api_accounts)
                
                # If api instance already loaded for account, use that api
                if api_account.username in apis.keys():
                    api = apis[api_account.username]
                    logger.debug(f"Used old Instagram API instance for {api_account}")
                    
                # Otherwise create new API instance
                else:                    
                    cached_settings = None
                    if api_account.auth_token:
                        cached_settings = json.loads(api_account.auth_token, object_hook=from_json)
                        logger.debug(f"Loaded in cached settings for instagram user {api_account}")
                        
                    api = InstagramBroadcastBot(username=api_account.username, 
                                                password=api_account.password, 
                                                cached_settings=cached_settings,
                                                logger=logger)
                    
                    apis[api_account.username] = api
                    api_account.auth_token = json.dumps(api.api.settings, default=to_json)
                    api_account.save()
                    logger.debug(f"Created Instagram API instance for {api_account}")
                    
                validAPI = True
            
            except (ClientChallengeRequiredError, ClientCheckpointRequiredError):
                api_account.blacklist = True
                api_account.save()
                logger.warning(f"Blacklisted Insta API account while creating API instance '{api_account}'")
                sleep(error_sleep)
             
            except Exception as e:
                logger.error(f"Failed to create an instagram API instance for user {api_account.username} with password {api_account.password}, error raised: '{e}' \n API settings: {api.api.settings}")
                logger.exception(e)
                # raise e
                sleep(error_sleep)
        
        if not validAPI:
            logger.error("Unable to obtain a valid Instagram API, quitting...")
            raise Exception("Unable to obtain a valid Instagram API, quitting...")
        
        # Check if user has an active broadcast
        def monitor_instagram(monitor_account : Account.objects) -> None:
            data = None
            try:
                uname = monitor_account.name.strip()
                logger.debug(f"Monitoring: {uname}")
                data = api.get_broadcast_info(uname)
                
            except ClientChallengeRequiredError:
                api_account.blacklist = True
                api_account.save()
                logger.warning(f"Blacklisted Insta API account '{api_account}'")
                monitor_instagram(monitor_account)
                return
            
            except Exception as e:
                logger.error(f"Error obtaining data for user {monitor_account.name}, with api account {api_account.username} with error {e}")
                logger.exception(e)
            
            # Create live steam for user
            if data and not track_live: 
                # Create stream
                url = data['owner'].get("profile_pic_url", None)
                monitor_account.profile_pic_url = url
                monitor_account.full_name = data['owner']['full_name']
                monitor_account.live = True
                title = ''
                
                minus_ten = datetime.now() - timedelta(minutes=10)
                old_streams = Stream.objects.filter(platform__name = "Instagram", host = monitor_account, end_time__gte = minus_ten)
                
                if old_streams:
                    try:
                        stream = old_streams[0]
                        stream.broadcast_id = data['broadcast_id']
                        stream.live = True
                        stream.update_time = datetime.fromtimestamp(data['update_time'])
                        stream.end_time = None
                        stream.current_viewers = data['viewer_count']
                        
                        if stream.cobroadcasters:
                            cobroadcasters = json.loads(stream.cobroadcasters)
                            cobroadcasters.extend(data['cobroadcasters'])
                        else:
                            stream.cobroadcasters = json.dumps(data['cobroadcasters'])
                            
                        viewer_data = json.loads(broadcast.viewer_data)
                        likes_data = json.loads(broadcast.likes_data)
                    
                        viewer_data[data['update_time']] = data['viewer_count']
                        likes_data[data['update_time']] = data['likes']
                        
                        stream.viewer_data = json.dumps(viewer_data)
                        stream.likes_data = json.dumps(likes_data)
                        
                        stream.save()
                        logger.info(f"Resumed old live stream for {monitor_account}")
                        
                    except Exception as e:
                        logger.error(f"Failed to resume live stream for {monitor_account} with {e}")
                        logger.exception(e)
                
                else:                
                    try:
                        Stream(
                            broadcast_id = data['broadcast_id'],
                            host = monitor_account,
                            platform = platform,
                            live = True,
                            start_time = datetime.fromtimestamp(data['start_time']),
                            update_time = datetime.fromtimestamp(data['update_time']),
                            likes_data = json.dumps({data['update_time']: data['likes']}),
                            viewer_data = json.dumps({data['update_time']: data['viewer_count']}),
                            current_viewers = data['viewer_count'],
                            cover_frame_url = data['cover_frame_url'],
                            cobroadcasters = json.dumps(data['cobroadcasters'])
                        ).save()
                        logger.info(f"Created new stream object for {monitor_account}")
                    except IntegrityError as e:
                        logger.error(f"Failed to create new steam item for {monitor_account}, but might not be bad. {e}")
                        logger.exception(e)
                    
                
                monitor_account.save()
                alert_twitter.apply_async(
                    kwargs = {
                        'data' : {
                            'name' : monitor_account.full_name, 
                            'title' : title, 
                            'platform' : 'Instagram',
                            'url' : f"https://instagram.com/{monitor_account.name}/live"
                            }
                        }
                    )

                logger.info(f"Sucessfully detected {monitor_account.name} going live on Instagram")
            
            # Update the broadcast if user was already live  
            elif data and track_live:
                # Update Stream data
                broadcast, created = Stream.objects.get_or_create(host = monitor_account, broadcast_id = data['broadcast_id'])
                
                # If for some reason no Stream object exists yet for the stream
                if created:
                    broadcast = broadcast[0]
                    broadcast.live = True
                    broadcast.platform = platform
                    broadcast.start_time = datetime.fromtimestamp(data['start_time'], tz=pytz.timezone(settings.TIME_ZONE))
                    broadcast.cover_frame_url = data['cover_frame_url']
                    viewer_data = {}
                    likes_data = {}
                else:
                    viewer_data = json.loads(broadcast.viewer_data)
                    likes_data = json.loads(broadcast.likes_data)
                
                broadcast.update_time = datetime.fromtimestamp(data['update_time'])
                broadcast.current_viewers = data['viewer_count']
                broadcast.cobroadcasters = json.dumps(data['cobroadcasters'])
                viewer_data[data['update_time']] = data['viewer_count']
                broadcast.viewer_data = json.dumps(viewer_data)
                likes_data[data['update_time']] = data['likes']
                broadcast.likes_data = json.dumps(likes_data)
                
                broadcast.save()
                logger.info(f"Updated broadcast for {monitor_account.name}")
            
            # Update if user stopped streaming
            elif not data and track_live:
                # Stream has ended
                broadcast = Stream.objects.filter(host=monitor_account, live=True)
                if broadcast:
                    broadcast = broadcast[0]
                    broadcast.live = False
                    broadcast.end_time = timezone.now()
                    broadcast.save()
                    logger.info(f"Livestream by {monitor_account.name} has ended")
                else:
                    logger.debug(f"Track live, but no stream found for {monitor_account.name}")
                    
                monitor_account.live = False
                monitor_account.save()
                
            # Update account information if anything is missing
            try:
                account_info = api.api.username_info(monitor_account.name)
                if account_info:
                    monitor_account.full_name = account_info['user']['full_name']
                    monitor_account.profile_pic_url = account_info['user']['profile_pic_url']
                    monitor_account.description = account_info['user']['biography']
                    monitor_account.followers = int(account_info['user']['follower_count'])
                    
                    if follower_data := monitor_account.followers_data:
                        follower_data = json.loads(follower_data)
                        follower_data[datetime.now().timestamp()] = monitor_account.followers
                        monitor_account.followers_data = json.dumps(follower_data)
                    else:
                        monitor_account.followers_data = json.dumps({datetime.now().timestamp() : monitor_account.followers})
                    
                    monitor_account.save()
                    
                logger.info(f"Updated account details for {monitor_account.name}")
            
            except ClientChallengeRequiredError:
                api_account.blacklist = True
                api_account.save()
                logger.warning(f"WARNING: Blacklisted Insta API account '{api_account}'")
                monitor_instagram(monitor_account)
                return
            
            except Exception as e:
                logger.error(f"ERROR: Failed to collect account info for {monitor_account.name} with {e}")
                logger.exception(e)
            
            round_end = time.time()
            logger.info(f"Round time: {round_end - round_start}")
            sleep(round_sleep)
        
        monitor_instagram(monitor_account)

@app.task(bind=True)
def monitorYoutube(self, track_live=False, round_pause=1):
    
    def update_youtube_profile(monitor_account):
        # If account fields are not populated, get the releavant account info
        try:
            account_info = api.get_channel_info(monitor_account.name)
            monitor_account.full_name = account_info['full_name']
            monitor_account.description = account_info['description']
            monitor_account.profile_pic_url = account_info['thumbnail_url']
            monitor_account.followers = account_info['subscribers']
            
            if follower_data := monitor_account.followers_data:
                    follower_data = json.loads(follower_data)
                    follower_data[datetime.now().timestamp()] = monitor_account.followers
                    monitor_account.followers_data = json.dumps(follower_data)
            else:
                monitor_account.followers_data = json.dumps({datetime.now().timestamp() : monitor_account.followers})
            
            monitor_account.save()
            
            logger.info(f"Updated YouTube account details for {monitor_account.full_name}, {monitor_account.name}")
                
        except Exception as e:
            logger.info(f"Failed to get YouTube account info for {monitor_account.full_name}, {monitor_account.name}. With error {e}")
            logger.exception(e)
            # raise e

    
    logger = getLogger('broadcasts.youtube')
    logger.info(f"Started monitoring YouTube accounts, track_live = {track_live}")
    
    # Get usernames
    api_accounts = APIAccount.objects.filter(platform__name__iexact = "youtube")
    monitor_accounts = Account.objects.filter(platform__name__iexact = "youtube", monitor = True, live = track_live)
    broadcasts = Stream.objects.filter(platform__name__iexact = "youtube", live = True)
    logger.debug(f"Obtained YouTube accounts {monitor_accounts}, {broadcasts}")
    
    if not api_accounts:
        logger.error("No YouTube API keys found")
        return
    
    api = YoutubeBroadcastBot(random.choice(api_accounts).api_key)
    
    # If monitor the accounts that are currently not live
    if not track_live:
        for monitor_account in monitor_accounts:
            logger.debug(f"Monitor: {monitor_account}, {monitor_account.name}")
            video_id = None
            
            # Check if user has active stream
            try:
                if api.is_live(monitor_account.name):
                    video_id = api.get_channel_broadcasts(monitor_account.name)
                    logger.debug(f"YouTube Account {monitor_account}, appears to be live, gathering more data")
                
            except Exception as e:
                logger.error(f"Failed to get YouTube channel broadcast info for {monitor_account} {monitor_account.name}, with error: '{e}'")
                logger.exception(e)
            
            # If account is live, create new broadcast
            if video_id:                
                try:
                    videoData = api.get_video_stats(video_id)
                    
                    monitor_account.full_name = videoData['full_name']
                    monitor_account.live = True
                    monitor_account.save()
                    
                    try:
                        start_time = datetime.strptime(videoData['startTime'], "%Y-%m-%dT%H:%M:%SZ")
                    except:
                        start_time = datetime.strptime(videoData['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    
                    update_time = timezone.now()
                    new_broadcast = Stream(
                                        broadcast_id = video_id,                                            
                                        host = monitor_account,
                                        platform = Platform.objects.filter(name__iexact="YouTube")[0],
                                        live = True,
                                        start_time = start_time,
                                        update_time = update_time,
                                        likes_data = json.dumps({update_time.timestamp(): videoData['likes']}),
                                        viewer_data = json.dumps({update_time.timestamp(): videoData['viewers']}),
                                        current_viewers = videoData['viewers'],
                                        cover_frame_url = videoData['thumbnail_url'],
                                        cumulative_viewers = videoData['cumulative_viewers'],
                                        title = videoData['title'],
                                        description = videoData['description'],
                                        url = f"https://www.youtube.com/watch?v={video_id}"
                                    ).save()
                    
                    alert_twitter.apply_async(
                        kwargs = {
                            'data' : {
                                'name' : monitor_account.full_name, 
                                'title' : videoData['title'],
                                'platform' : 'YouTube',
                                'url' : f"https://www.youtube.com/watch?v={video_id}"
                                }
                            }
                        )
                        
                    logger.info(f"YouTube live stream started by {monitor_account.full_name} {monitor_account.name}")
                    
                except Exception as e:
                    logger.error(f"Failed to get YouTube video data for live broadcast, {monitor_account.full_name} {monitor_account.name} With error {e}")
                    logger.exception(e)
            else:
                logger.info(f"YouTube user {monitor_account.full_name} {monitor_account.name} is not live")
                
            update_youtube_profile(monitor_account)
            sleep(round_pause)            
    
    # Monitor the accounts that are currently live
    else:
        for broadcast in broadcasts:
            try:
                videoData = api.get_video_stats(broadcast.broadcast_id)
                
                monitor_account = broadcast.host
                update_youtube_profile(monitor_account)
                update_time = timezone.now()
                broadcast.update_time = update_time
                likes_data = json.loads(broadcast.likes_data)
                likes_data[update_time.timestamp()] = videoData['likes']
                broadcast.likes_data = json.dumps(likes_data)
                
                viewer_data = json.loads(broadcast.viewer_data)
                
                if videoData['live']:
                    viewer_data[update_time.timestamp()] = videoData['viewers']
                    broadcast.viewer_data = json.dumps(viewer_data)
                    broadcast.current_viewers = videoData['viewers']
                else:
                    broadcast.current_viewers = 0
                    broadcast.live = False
                    monitor_account.live = False
                    monitor_account.save()
                    
                    try:
                        end_time = datetime.strptime(videoData['endTime'], "%Y-%m-%dT%H:%M:%SZ")
                    except:
                        end_time = datetime.strptime(videoData['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    
                    broadcast.end_time = end_time
                    logger.debug(f"YouTube live stream by {monitor_account} has ended")
                
                if videoData['cumulative_viewers']:
                    broadcast.cumulative_viewers = videoData['cumulative_viewers']
                
                broadcast.title = videoData['title']
                broadcast.description = videoData['description']
                
                broadcast.save()
                
                logger.info(f"Updated live stream data for {broadcast.host}, {broadcast.broadcast_id}")
                
            except Exception as e:
                logger.error(f"Failed to update broadcast for, {broadcast.host} id = {broadcast.broadcast_id}. With error {e}")
                logger.exception(e)
                # raise e

        sleep(round_pause)

@app.task(bind=True)
def monitorTwitch(self, track_live=False, round_pause=0.3):
    logger = getLogger('broadcasts.twitch')
    logger.info(f"Started montoring Twicth, track_live = {track_live}")
    
    # Get usernames
    api_accounts = APIAccount.objects.filter(platform__name__iexact = "twitch")
    monitor_accounts = Account.objects.filter(platform__name__iexact = "twitch", monitor = True, live = track_live)
    logger.debug(f"Obtained Twitch accounts {monitor_accounts}")
    
    if not api_accounts:
        logger.error("No Twitch API accounts found")
        return
    
    api = TwitchBroadcastBot(api_accounts[0].client_id, api_accounts[0].auth_token)
    
    # If monitor the accounts that are currently not live
    for monitor_account in monitor_accounts:
        logger.debug(f"Monitoring: {monitor_account}")
        
        platform = Platform.objects.filter(name__iexact="Twitch")[0]
        
        # Check if user has active stream
        try:
            stream_data = api.get_user_stream(monitor_account.name)
            
            # Create new stream
            if stream_data and not track_live:
                monitor_account.live = True
                monitor_account.save()
                update_time = timezone.now()
                
                try:
                    start_time = datetime.strptime(stream_data['started_at'], "%Y-%m-%dT%H:%M:%SZ")
                except:
                    start_time = datetime.strptime(stream_data['started_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
                   
                
                Stream(
                    broadcast_id = stream_data['id'],
                    host = monitor_account,
                    platform = platform,
                    live = True, 
                    start_time = start_time,
                    update_time = update_time,
                    viewer_data = json.dumps({update_time.timestamp() : stream_data['broadcast_viewers']}),
                    current_viewers = stream_data['broadcast_viewers'],
                    cover_frame_url = stream_data['thumbnail_url'],
                    url = stream_data['url'],
                    title = stream_data['title']
                ).save()
                
                alert_twitter.apply_async(
                    kwargs = {
                        'data' : {
                            'name' : monitor_account.full_name, 
                            'title' : stream_data['title'], 
                            'platform' : 'Twitch',
                            'url' : stream_data['url']
                            }
                        }
                    )
                
                logger.info(f"Added new stream for {monitor_account}")
            
            # Update live stream 
            elif stream_data and track_live:
                stream, created = Stream.objects.get_or_create(broadcast_id = stream_data['id'])
                update_time = timezone.now()
                
                # In the rare case that an account is marked as live, but no Stream has been created
                if created:
                    stream.live = True
                    
                    try:
                        start_time = datetime.strptime(stream_data['started_at'], "%Y-%m-%dT%H:%M:%SZ")
                    except:
                        start_time = datetime.strptime(stream_data['started_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    
                    stream.start_time = start_time
                    stream.cover_frame_url = stream_data['thumbnail_url']
                    stream.host = monitor_account
                    stream.platform = platform
                    stream.url = stream_data['url']
                    viewer_data = {}
                else:
                    viewer_data = json.loads(stream.viewer_data)    
                
                viewer_data[update_time.timestamp()] = stream_data['broadcast_viewers']
                stream.viewer_data = json.dumps(viewer_data)
                stream.current_viewers = stream_data['broadcast_viewers']
                stream.title = stream_data['title']

                stream.save()
                logger.info(f"Updated stream data for {monitor_account}")
            
            # Live stream has ended
            elif not stream_data and track_live:
                streams = Stream.objects.filter(host = monitor_account, platform = platform, live = True)
                
                for stream in streams:
                    stream.end_time = timezone.now()
                    stream.live = False
                    stream.save()
                    logger.info(f"Stream by {monitor_account} has ended")
                    
                monitor_account.live = False
                monitor_account.save()              
                
            # Account attributes not filled
            account_data = api.get_user_info(monitor_account.name)
            
            if account_data:
                monitor_account.full_name = account_data['display_name']
                monitor_account.description = account_data['description']
                monitor_account.profile_pic_url = account_data['profile_picture_url']
                monitor_account.followers = account_data['followers']
                
                if follower_data := monitor_account.followers_data:
                        follower_data = json.loads(follower_data)
                        follower_data[datetime.now().timestamp()] = monitor_account.followers
                        monitor_account.followers_data = json.dumps(follower_data)
                else:
                    monitor_account.followers_data = json.dumps({datetime.now().timestamp() : monitor_account.followers})
                
                monitor_account.save()
            else:
                logger.error(f"Failed to get account data for {monitor_account}")
            
            logger.info(f"Updated user data for {monitor_account}")
            
        except Exception as e:
            logger.error(f"Failed to get Twitch channel broadcast info for {monitor_account}, with error: '{e}''")
            logger.exception(e)
            # raise e
            
        sleep(round_pause)

def upload_auth_settings(auth_file_path):
    with open(auth_file_path, 'r') as file:
        auth_settings = json.load(file, object_hook=from_json)
        
    for user in auth_settings:
        print(f"Processing {user}")
        password = ""
        api_account, created = APIAccount.objects.get_or_create(
                                                        username = user,
                                                        platform = Platform.objects.get(name__iexact="Instagram")[0],
                                                        defaults = dict(password=password,
                                                                        auth_token=json.dumps(auth_settings[user], default=to_json))
                                                       )
        if created:
            print(f"Created object for username {user}\n")
        else:
            print(f"Skipped object for username {user}\n")


if __name__ == "__main__":
    monitor_instagram(None)
    # upload_auth_settings("broadcasts/instagram/auth_storage.txt")