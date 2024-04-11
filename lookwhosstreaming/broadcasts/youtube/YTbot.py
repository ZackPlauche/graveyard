import datetime
import json
import numpy as np
import pytz
import re
import requests
import sqlite3
import time
from matplotlib import pyplot as plt
from matplotlib import ticker

class YoutubeBroadcastBot():
    search_endpoint = "https://www.googleapis.com/youtube/v3/search/"
    video_endpoint = "https://www.googleapis.com/youtube/v3/videos"
    channels_endpoint = "https://www.googleapis.com/youtube/v3/channels/"
    # chat_endpoint = "https://www.googleapis.com/youtube/v3/liveChat/messages"
    chat_endpoint = "https://www.googleapis.com/youtube/v3/superChatEvents/"
    API_KEY = None
    web_session = None
    
    def __init__(self, API_KEY):        
        self.API_KEY = API_KEY        
        self.web_session = requests.session()
        self.web_session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
        
    def __del__(self):
        if self.web_session:
            self.web_session.close()
    
    def is_live(self, channel_id):
        base_url = "https://youtube.com/channel/"
        response = self.web_session.get(base_url + channel_id + '/live') 
        
        print(response.status_code)
        
        # live_html = "BADGE_STYLE_TYPE_LIVE_NOW"
        # live_html = 'overlay-style="LIVE"'
        live_html = 'yt_live_broadcast'
        
        if response.status_code == 200 and re.search(live_html, response.text, re.IGNORECASE):
            return True
        
        else:
            return False
    
    def monitor_video(self, videoId):
        BroadcastStatus = 1
        is_live = False
        print(f"Started to monitor video '{videoId}'")
        
        while BroadcastStatus != 'none':
            data = self.get_video_stats(videoId, is_live)
            BroadcastStatus = data['items'][0]['snippet']['liveBroadcastContent']
            
            if not is_live and BroadcastStatus == "live":
                print("Broadcast live!")
                data = self.get_video_stats(videoId, is_live)
                is_live = True

            if not is_live:
                time.sleep(300)
            else:
                self.store_broadcasts(data['items'][0])
                self.store_broadcasts_stats(data['items'][0])
                time.sleep(60)
        
        print("Livestream over!")
    
    @staticmethod
    def GETrequest(url, params):
        response = requests.get(url=url, params=params)
        
        if response.status_code == 200:
            return json.loads(response.text)
        
        elif response.status_code == 403:
            data = json.loads(response.text)
            if data['error']['errors'][0]['reason'] == "quotaExceeded":
                print(f"QUOTA_EXCEEDED {params['key']}")
        
        else:
            print("An error occured")
            print(response, response.text)
    
    def get_channel_info(self, channel_id):
        params = {"part": "snippet, id, statistics",                              
                  "id": channel_id,
                  "key": self.API_KEY}
        
        response = self.GETrequest(self.channels_endpoint, params)
        # print("Channel Info", json.dumps(response, indent=2))
        
        if (thumbnail_url := response['items'][0]['snippet']['thumbnails'].get('standard', None)) == None:
            thumbnail_url = response['items'][0]['snippet']['thumbnails'].get('default', None)
        
        try:
            return {
                "full_name": response['items'][0]['snippet']['title'],
                "description": response['items'][0]['snippet'].get('description', None),
                "thumbnail_url": thumbnail_url['url'],
                "subscribers" : response['items'][0]['statistics']['subscriberCount']
            }

        except (KeyError, IndexError):
            return None  

    def get_channel_id(self, username):
        params = {"part": "snippet, id",                              
                  "forUsername": username,
                  "key": self.API_KEY}
        
        response = self.GETrequest(self.channels_endpoint, params)
        
        try:
            return response['items'][0]["id"]
        except (KeyError, IndexError):
            return None
    
    def get_channel_broadcasts(self, channel_id):
        """ Watch out, search endpoint is very expensive with 100 points"""
        params = {"part": "id", 
                  "eventType": "live", 
                  "maxResults": 50, 
                  "type": "video", 
                  "key": self.API_KEY,
                  "channelId": channel_id}
        
        response = self.GETrequest(self.search_endpoint, params)
        # print(f"Broadcasts: {response}")
        
        try:
            return response['items'][0]['id']['videoId']
        except (KeyError, IndexError) :
            return None
    
    def get_chat_messages(self, chatID = "Cg0KC2dPUEk5RnJQXzkwKicKGFVDLWxISlpSM0dxeG0yNF9WZF9BSjVZdxILZ09QSTlGclBfOTA"):
        params = {"part": "id, snippet", 
                  "type": "video", 
                  "key": self.API_KEY,
                  "liveChatId": chatID}
        
        response = self.GETrequest(self.chat_endpoint, params)
        
        print(json.dumps(response, indent=4))
    
    def get_video_stats(self, video_id, is_live = True):
        # Quota cost is 9 per call
        if is_live:
            part = "snippet,contentDetails,statistics,liveStreamingDetails"
        else:
            part = "snippet,liveStreamingDetails"
        
        params = {"part": part, 
                  "maxResults": 50, 
                  "key": self.API_KEY, 
                  "id": video_id}
        
        # data['items'][0]['snippet']['liveBroadcastContent']
        response = self.GETrequest(self.video_endpoint, params)
        # print(f"Reponse:\n{json.dumps(response,indent=2)}")
        try:
            if isinstance(response, type(dict())) and len(data := response['items']) > 0:
                data = data[0]
                
                # can be used to check if vid is live, by setting param is_live = False
                if not is_live and data['snippet']['liveBroadcastContent'] == 'live':
                    return True
                
                elif not is_live and data['snippet']['liveBroadcastContent'] != 'live':
                    return False
                
                else:
                    if (thumbnail_url := data['snippet']['thumbnails'].get('standard', None)) == None:
                        thumbnail_url = data['snippet']['thumbnails'].get('default', None)
                    
                    start_time, end_time = None, None
                    live = True if data['snippet']['liveBroadcastContent'] != 'none' else False
                    
                    viewers = data['liveStreamingDetails'].get('concurrentViewers', None)
                    
                    start_time = data['liveStreamingDetails'].get('actualStartTime', 
                                                                 data['snippet']['publishedAt'])
                    end_time = data['liveStreamingDetails'].get('actualEndTime', None)                   
                    
                    return {
                        "startTime": start_time,
                        "endTime": end_time,
                        "full_name": data['snippet']['channelTitle'],
                        "title": data['snippet']['title'],
                        "description": data['snippet']['description'],
                        "thumbnail_url": thumbnail_url.get('url', None),        
                        "cumulative_viewers": data['statistics'].get('viewCount', None),
                        "viewers": viewers,
                        "live": live,
                        "likes": data['statistics']['likeCount']
                    }
                    
            return None
        except Exception as e:
            print(f"Failed to get youtube video stats, {video_id} {e} {json.dumps(data, indent = 2)}")
            raise e
    
class YTLocalBot(YoutubeBroadcastBot):
    DB_Name = "youtube_broadcasts.db"
    conn = None
    
    def __init__(self, path=None):
        super().__init__(API_KEY=None)
        self.get_api_key(path)

        self.conn = sqlite3.connect(self.DB_Name)
    
    def __del__(self):
        if self.conn:
            self.conn.close()
        
        return super().__del__()
        
    def get_api_key(self, path=None):
        if not path:
            path = "creds.txt"
        with open(path, 'r') as file:
            self.API_KEY = file.readline().strip()
            print("Read API key from file")
            
    def store_broadcasts(self, data):
        existingBroadcasts = self.conn.execute("SELECT videoId FROM Broadcasts")
        existingBroadcasts = [x[0] for x in existingBroadcasts.fetchall()]
        
        videoId = data['id']
        channelId = data['snippet']['channelId']
        channelTitle = data['snippet']['channelTitle']
        title = data['snippet']['title']
        publishedAt = data['snippet']['publishedAt']
        
        if videoId in existingBroadcasts:
            return
        
        sql = f"""INSERT INTO Broadcasts (videoId, channelId, channelTitle, title, publishedAt) 
                            VALUES ('{videoId}', '{channelId}', "{channelTitle}", "{title}", '{publishedAt}')"""
        
        print(sql)  
        self.conn.execute(sql)
        self.conn.commit()
        print("Comitted Broadcast")
    
    def store_broadcasts_stats(self, data):
        stats = data['statistics']
        stats.update({'liveViewers': data['liveStreamingDetails'].get('concurrentViewers', None)})
        
        self.conn.execute(f"""INSERT INTO BroadcastStats (videoId, stats, updateTime) VALUES ("{data['id']}", "{stats}", "{datetime.datetime.now().strftime('%s')}")""")
        self.conn.commit()
        
        print("Comitted Stats")
    
    def plot_views(self, videoId):
        sql = f"""SELECT stats, updateTime FROM BroadcastStats WHERE videoId = '{videoId}'"""
        data = np.array(self.conn.execute(sql).fetchall())
        
        viewCount = []
        likeCount = []
        dislikeCount = []
        liveViewers = [] 
            
        for row in data:
            date = datetime.datetime.fromtimestamp(int(row[1]), pytz.timezone('US/Eastern')).time()
            row[1] = date
            
            stats = json.loads( row[0].replace("\'", "\"").replace("liveViewer\"", "liveViewers\"").replace("None", "0"))
            print(stats.keys())
            viewCount.append(int(stats['viewCount']))
            likeCount.append(int(stats['likeCount']))
            dislikeCount.append(int(stats['dislikeCount']))
            liveViewers.append(int(stats['liveViewers']))
            
        fig = plt.figure(figsize=(8, 6))
        ax = plt.subplot(1, 1, 1)
        ax2 = ax.twinx()
        
        # plt.xticks(rotation=45)
        ax.plot(data[:, 1], likeCount, label="Likes", color="green", alpha=.8)
        # ax.plot(data[:, 1], dislikeCount, label="Dislikes", color="red", alpha=.8)
        ax.plot(data[:, 1], liveViewers, label="Live Viewers", color="purple", alpha=.8)
        
        ax.xaxis.set_major_locator(plt.MaxNLocator(20))
        
        ax2.plot(viewCount, label="Total Viewers", color='red', alpha=.8)

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:,.0f}'.format(y/1000) + 'K'))
        ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:,.0f}'.format(y/1000) + 'K'))
        
        ax2.set_ylabel("total viewers")
        
        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h1+h2, l1+l2, loc=2)
        
        plt.grid(alpha=0.3)
        ax.tick_params(axis='x', rotation=35)
        plt.title("J Balvin")
        plt.tight_layout()
        plt.show()

        
if __name__ == "__main__":
    # channelId = bot.get_channel_id("jewishnationalfund")['items'][0]['id']
    # print("ID", channelId)
    # broadcasts = bot.get_channel_broadcasts(channelId)['items'][0]['id']['videoId']
    # video_stats = bot.get_video_stats(broadcasts)
    
    # bot = YTLocalBot()
    bot = YoutubeBroadcastBot("AIzaSyDjQRcIoNa1h92iNQH2Ubo-Q3eJXofPo8o")
    print("beast", bot.get_channel_id('MrBeast6000'))
    # print(bot.getChannelInfo("UCoaQyWkyU2juENnwone6uuQ"))
    # channelID = bot.getChannelId("ClayMixer")
    channelID = "UCX6OQ3DkcsbYNE6H8uQQuVA"  # mr beast first channel
    # channelID = "UCV0qA-eDDICsRR9rPcnG7tw"
    
    print("is_live", bot.is_live(channelID))
    print(bot.get_channel_info(channelID))
    # print(bot.getChannelBroadcasts(channelID))
    # print(bot.isLive(channelID))
    # print(bot.isLive("UCaC8IE_uJ9h8s6dIs4ITOwQ"))
    # # videoID = "gOPI9FrP_90"
    
    if not channel_id:
        print("ChannelID not found")
    else:
        # bot.get_video_stats(False)
        
        # video_id = bot.get_channel_broadcasts(channel_id)
        video_id = "dHhiD6t_bW4"
        
        if video_id:
            print(f"For {video_id}")
            channel_broadcast = bot.get_video_stats(video_id)
            print("Channel broadcast:", json.dumps(channel_broadcast, indent=2))
        else:
            print("No live broadcast going on")
        
    #     # GEZhD3J89ZE
        
