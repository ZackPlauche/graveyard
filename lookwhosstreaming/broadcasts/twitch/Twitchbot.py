import json
import requests

class TwitchAuthentication():
    client_id = None
    bearer = None
    
    def get_credentials(self, client_id, bearer, path):
        if path:
            self.read_file_credentials(path)
        elif client_id and bearer:
            self.client_id = client_id.strip()
            self.bearer = bearer.strip()
        else:
            print("ERROR: Please provide either client_id & bearer, or path")
            
    
    def read_file_credentials(self, path):
        with open(path, 'r') as file:
            line = file.readline().strip().split(':')
            self.client_id = line[0]
            self.bearer = line[1]

        print("Read authorization details")

class TwitchBroadcastBot(TwitchAuthentication):
    api_base = "https://api.twitch.tv/helix/"
    
    def __init__(self, client_id=None, bearer=None, path=None, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self.getCredentials(client_id, bearer, path)
    
    def store_broadcasts(self):
        pass
    
    def store_broadcasts_stats(self):
        pass
    
    def get_user_stream(self, username):
        endpoint = "streams"
        params = {"user_login": username}
        
        data = self.GETRequest(endpoint, params)
        
        # print(json.dumps(data, indent=4))
        
        if isinstance(data, type(dict())):
            data = data['data']
        
            if len(data) >= 1:
                data = data[0]
                    
                return {
                    "id": data.get('id', None),
                    "username": username,
                    "type": data.get("type", None),
                    "title": data.get("title", None),
                    "broadcast_viewers": data.get("viewer_count", None),
                    "started_at": data.get("started_at", None),
                    "url": f"https://twitch.tv/{username}/videos",
                    "thumbnail_url": data.get("thumbnail_url").format(width=640, height=360)    
                }
                
        return None
    
    def get_video_info(self, id):
        endpoint = "videos"
        params = {"id": id}
        
        response = self.GETRequest(endpoint, params)
        
        print(f"VIDEO INFO: {json.dumps(response, indent=4)}")
    
    def get_user_info(self, username):
        endpoint = "users"
        params = {"login": username}
        
        data = self.GETRequest(endpoint, params)      
        # print(data)  
        
        if isinstance(data, dict):
            data = data['data']
            if len(data) >= 1:
                data = data[0]
                followers = self.GETRequest('users/follows', {'to_id': data['id']})['total']
            
                return {
                    "username": data.get("login", None),
                    "display_name": data.get("display_name", None),
                    "description": data.get("description", None),
                    "profile_picture_url": data.get("profile_image_url"),
                    "total_views": data.get("view_count", None),
                    "url": f"https://twitch.tv/{username}",
                    "followers": followers,     
                }

        return None
        
    def GETRequest(self, endpoint, params):
        url = self.api_base + endpoint
        # print(f"making request {url}")
        
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"bearer {self.bearer}"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            # print(f"Raw response: {response.status_code} {response.url} {json.dumps(json.loads(response.text), indent=4)}")
            # print(response.text)


            if response.status_code == 200:
                return json.loads(response.text)
            
            elif response.status_code == 401:
                print(response.text)
            
            elif response.status_code == 404:
                print(response.text)
            
        except Exception as e:
            raise e
        
if __name__ == "__main__":
    bot = TwitchBroadcastBot(path="creds.txt")
    
    user = "logic"
    # print(json.dumps(bot.get_user_stream(user), indent=4))
    # print(json.dumps(bot.get_user_info(user), indent=4))
    print("User info:", bot.get_user_info(user))
    
    bot.get_video_info('645049440')