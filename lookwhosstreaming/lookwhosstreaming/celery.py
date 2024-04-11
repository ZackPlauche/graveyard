import os
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
from celery.signals import celeryd_init


# To start the beat service: 
#   celery -A project beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
# To start the workers:
#   celery -A project worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
# To start a local redis server:
#   redis-server --port 9800

# Celery set-up
project_name = "lookwhosstreaming"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')

app = Celery(project_name)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Schedule
monitor_interval = 60 * 5
live_interval = 60 * 1
app.conf.beat_schedule = {
    # Default monitoring tasks
    'monitor-youtube-trigger': {
        'task': 'broadcasts.monitor.monitorYoutube',
        'schedule': monitor_interval,
    },
    
    'monitor-instagram-trigger': {
        'task': 'broadcasts.monitor.monitor_instagram',
        'schedule': monitor_interval,
    },
    
    'monitor-twitch-trigger': {
        'task': 'broadcasts.monitor.monitorTwitch',
        'schedule': monitor_interval,
    },
    
    # Monitor live streams
    'monitor-youtube-live': {
        'task': 'broadcasts.monitor.monitorYoutube',
        'schedule': live_interval,
        'kwargs': {
            'track_live': True
            }
    },
    
    'monitor-instagram-live': {
        'task': 'broadcasts.monitor.monitor_instagram',
        'schedule': live_interval,
        'kwargs': {
            'track_live': True
            }
    },
    
    'monitor-twitch-live': {
        'task': 'broadcasts.monitor.monitorTwitch',
        'schedule': live_interval,
        'kwargs': {
            'track_live': True
            }
    },
    'check-live': {
        'task': 'lookwhosstreaming.celery.check_live',
        'schedule': monitor_interval
    }
}


@celeryd_init.connect
def STARTUP(*args, **kwargs):
    print("RUNNING STARTUP")
    
    ### ADD STARTUP METHODS HERE
    concat_instagram_streams()
    check_live()
    save_all()
    # update_twitch_streams()
    
    print("DONE WITH STARTUP")

def save_all():
    from streams.models import Stream
    
    streams = Stream.objects.all()
    for stream in streams:
        stream.save()

@app.task(bind=True)
def check_live(self=None):
    from streams.models import Account, Stream
    
    streams = Stream.objects.filter(host__live=True, live=False)
    live_streams = Stream.objects.filter(live=True)
    
    not_live = [stream.host for stream in streams]
    live = [stream.host for stream in live_streams]
    hosts = [host for host in not_live if host not in live]
    
    for host in hosts:
        host.live = False
        host.save()
        print(f"Marked {host} as offline")


def concat_instagram_streams():
    from streams.models import Stream, Account, APIAccount
    from broadcasts.instagram.IGbot import InstagramBroadcastBot
    import time
    import random
    import json

    instagram_streams = Stream.objects.filter(platform__name__iexact = "instagram")
    insta_hosts = set([stream.host.name for stream in instagram_streams])

    for host in insta_hosts:
        host_streams = Stream.objects.filter(platform__name__iexact = "instagram", host__name = host).order_by('start_time')
        
        for index in range(len(host_streams)):
            _ = index
            next = True
            to_add = []
            chosen = []
            while next and _ + 1 < len(host_streams):
                if index in chosen or not (host_streams[_ + 1].start_time and host_streams[_].end_time):
                    break
                
                delta = host_streams[_ + 1].start_time - host_streams[_].end_time
                if delta.total_seconds() < 10 * 60:
                    if not to_add:
                        to_add.append(host_streams[_])
                    to_add.append(host_streams[_ + 1])
                    chosen.append(_ + 1)
                else:
                    next = False
                _ += 1
            
            if to_add:
                try:
                    first_stream = to_add[0]
                    viewer_data = json.loads(first_stream.viewer_data)
                    likes_data = json.loads(first_stream.likes_data)
                    
                    if first_stream.cobroadcasters:
                        try:
                            cobroadcasters = json.loads(first_stream.cobroadcasters)
                        except:
                            try:
                                cobroadcasters = eval(first_stream.cobroadcasters)
                            except:
                                cobroadcasters = []
                    else:
                        cobroadcasters = []
                    
                    end_time = first_stream.end_time
                    description = first_stream.description
                    update_time = first_stream.update_time
                    
                    for later_stream in to_add[1:]:
                        try:
                            viewer_data.update(json.loads(later_stream.viewer_data))
                            likes_data.update(json.loads(later_stream.likes_data))
                            
                            if later_stream.cobroadcasters:
                                try:
                                    new_cobroadcaster = json.loads(later_stream.cobroadcasters)
                                except:
                                    try:
                                        new_cobroadcaster = eval(later_stream.cobroadcasters)
                                    except:
                                        new_cobroadcaster = []
                        
                            if cobroadcasters and new_cobroadcaster not in cobroadcasters:
                                cobroadcasters = cobroadcasters.extend(new_cobroadcaster)
                            elif new_cobroadcaster:
                                cobroadcasters = new_cobroadcaster
                                                
                            if later_stream.end_time > end_time:
                                end_time = later_stream.end_time
                                
                            if later_stream.description:
                                description = later_stream.description
                                
                            if later_stream.update_time > update_time:
                                update_time = later_stream.update_time
                                
                            first_stream.viewer_data = viewer_data
                            first_stream.likes_data = likes_data
                            first_stream.cobroadcasters = cobroadcasters
                            first_stream.end_time = end_time
                            first_stream.description = description
                            first_stream.update_time = update_time
                            later_stream.delete()
                        except Exception as e:
                            print(f"ERROR   : Failed to add stream by {host} {later_stream.broadcast_id} with {e}")
                            # raise e
                
                    first_stream.save()
                except Exception as e:
                    print(f"ERROR   : Failed to process stream list for {host} with {e}")
                    # raise e
                
                
            print(f"STARTUP: {host} added: {to_add}")

def update_twitch_streams():
    from streams.models import Stream, Account, APIAccount
    import time
    import random
    from datetime import timedelta
        
    negative_duration_streams = [stream for stream in Stream.objects.all() if stream.duration and '-' in stream.duration]
    
    for stream in negative_duration_streams:
        stream.start_time -= timedelta(hours=7)
        stream.save()
        print(f"Updated stream {stream.host} {stream.platform}")

def update_youtube_times():
    from streams.models import Stream, Account, APIAccount
    from broadcasts.youtube.YTbot import YoutubeBroadcastBot
    import time
    import random
    
    api_accounts = APIAccount.objects.filter(platform__name__iexact = "youtube")
    youtube_streams = Stream.objects.filter(platform__name__iexact = "youtube")
    
    index = 0
    print(f"STARTUP: processing {len(youtube_streams)}")
    for stream in youtube_streams:
        api = YoutubeBroadcastBot(random.choice(api_accounts).api_key)

        try:
            if 'youtube.com' in stream.broadcast_id:
                stream.broadcast_id = stream.broadcast_id.split('v=')[1]
            videoStats = api.get_video_stats(stream.broadcast_id)
            
            stream.start_time = videoStats['startTime']
            
            if videoStats.get('endTime', None):
                stream.end_time = videoStats['endTime']
            
            stream.save()
            index += 1
            print(f"STARTING: {index} Updated stream {stream.host.name} {stream.broadcast_id}")
            
        except Exception as e:
            print(f"STARTING: Failed to update time for {stream.host.name} {stream.broadcast_id} with {e} ")    
            # raise e
        time.sleep(2)