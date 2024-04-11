import argparse
import codecs
import datetime
import json
import logging
import os.path
import matplotlib.ticker as ticker
import numpy as np
import pytz
import requests
import sqlite3
import time
import pytz
from http.client import IncompleteRead
from random import randrange
from matplotlib import pyplot as plt

from instagram_private_api import (
    Client, ClientError, ClientLoginError,
    ClientCookieExpiredError, ClientLoginRequiredError, ClientCompatPatch, ClientConnectionError,
    __version__ as client_version)
from instagram_web_api import Client as webClient

#  TODO:
# Implement Django database auth mechanism
# Catch LoginRequiredError if performing for a long time
# check out likes and ohter methods on a real life stream


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object

class InstagramAuthentication():
    """Class implementing the authenticantion and cookie storage"""

    api = None
    web_api = None
    session_data = {}
    username = None
    password = None
    accounts = {}
    cached_settings = None
    logger = None

    def __init__(self, accounts={}, cached_settings=None, credentials_file_path=None, username=None, password=None, settings_file_path=None, logger=None, force=False):
        if logger:
            self.logger = logger
        else:
            import logging
            self.logger = logging.getLogger('IGbot')

        self.check_connection()

        self.cached_settings = cached_settings

        if(username and password) or (username and settings_file_path) and isinstance(username, type(str())):
            self.username = username.lower()
            self.password = password
        elif credentials_file_path and isinstance(credentials_file_path, type(str())):
            self.get_credentials(credentials_file_path)  # what I mainly use
        else:
            raise Exception(
                "Error: please give either both a valid username and password or a valid file path for the credentials")

        self.settings_file_path = settings_file_path

        #  connect to the api
        try:
            self.connect(force_new_login=force)
            self.logger.debug(f"Logged in successfully as {self.api.authenticated_user_name}")
        except ClientConnectionError:
            raise Exception("\nNo internet connection")

    def check_connection(self):
        """ Check if there is a working internet connection """
        try:
            a = requests.get("https://google.com")
        except:
            raise Exception("Error: no network connection")

    def get_credentials(self, credentials_file_path):
        """ Obtain credentials from a file """
        if os.path.isfile(credentials_file_path):
            with open(credentials_file_path, 'r', encoding='utf-8') as credentials_file:
                first_line = credentials_file.readline().strip()
                if '//' in first_line or '#' in first_line:
                    first_line = credentials_file.readline().strip()

                if ':' in first_line:
                    first_line = first_line.split(':')
                    self.username = first_line[0].lower()
                    self.password = first_line[1]
                else:
                    self.username = credentials_file.readline().strip().lower()
                    self.password = credentials_file.readline().strip()
        else:
            raise Exception(
                "Error: please give either both a valid username and password or a valid file path for the credentials")

    def on_login_callback(self, api_, new_settings_file, like_amount=None):
        """ Store cookie in file"""
        if not new_settings_file and self.settings_file_path:
            new_settings_file = self.settings_file_path
        else:
            return

        cache_settings = api_.settings
        if not os.path.isfile(new_settings_file):
            auth_storage_data = {api_.authenticated_user_name: cache_settings}
        else:
            with open(new_settings_file, 'r') as infile:
                auth_storage_data = json.load(infile)

            auth_storage_data[api_.authenticated_user_name] = cache_settings

        with open(new_settings_file, 'w') as outfile:
            json.dump(auth_storage_data, outfile, default=to_json, indent=4)
            self.logger.debug('SAVED: {0!s}'.format(new_settings_file))

    @staticmethod
    def test_accounts(file_path):

        with open(file_path, 'r') as file:
            users = file.read()

        failed = []
        success = []
        for line in users.split('\n'):
            if line.strip():
                uname = line.split(':')[0]
                pword = line.split(':')[1]
                results, error = [], None
                print(f"Testing username {uname}")

                try:
                    bot = InstagramBroadcastBot(username=uname, password=pword)
                    results = bot._get_user_feed(username, num_posts=3)
                except Exception as e:
                    error = e

                if len(results) >= 1:
                    print("SUCCESS\n\n")
                    success.append(uname)
                else:
                    print(f"FAILED, {error}\n\n")
                    failed.append((uname, error))

                time.sleep(2)

        print(f"A total of {len(success)} successes, and {len(failed)} fails")

    def bad_password(self, *args):  # place holder
        pass

    def connect(self, force_new_login=False, webAPI=False):
        """ Establish a connection to the api with the given username and password """
        device_id = None
        self.logger.debug('Client version: {0!s}'.format(client_version))

        if webAPI:
            # connect Web API
            self.web_api = webClient(auto_patch=True, drop_incompat_keys=False)

        # connect App API
        def login(settings=None):
            # reuse auth settings
            try:
                api_ = Client(self.username, self.password, settings=settings, on_login=lambda x: self.on_login_callback(x, self.settings_file_path))
            except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
                self.logger.debug('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

                # Login expired, try without settings
                api_ = Client(self.username, self.password, on_login=lambda x: self.on_login_callback(x, self.settings_file_path))

            return api_

        try:
            # check if cached settings have been provided
            cached_settings = self.cached_settings
            if cached_settings:
                if isinstance(cached_settings, type(dir)):
                    settings = cached_settings.get(self.username, None)
                else:
                    settings = cached_settings

                self.api = login(settings=settings)

            # settings file does not exist, no cookie present
            elif not self.settings_file_path or (self.settings_file_path and not os.path.isfile(self.settings_file_path)) or force_new_login:
                if force_new_login:
                    self.logger.debug("Forcing new-login")
                elif not self.settings_file_path:
                    self.logger.debug("Creating new login")
                else:
                    self.logger.debug('Unable to find settings file: {0!s}, creating new login'.format(self.settings_file_path))

                # create new login and cookie
                self.api = login()

            # settings file does exist, open settings file and retrieve data
            else:
                self.logger.debug("Found storage file")
                with open(self.settings_file_path) as file_data:
                    auth_storage_data = json.load(file_data, object_hook=from_json)

                try:
                    # check if the setings file contains the settings for given username
                    cached_settings = auth_storage_data[self.username]
                    self.logger.debug('Reusing settings: {0!s}'.format(self.settings_file_path))

                    # reuse auth settings
                    try:
                        self.api = login(settings=cached_settings)
                    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
                        self.logger.debug('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

                        # Login expired
                        self.api = login()

                except KeyError as e:
                    # if not then create a new login
                    self.logger.debug("user {} not stored in the settings file, adding new entry".format(self.username))
                    self.connect(force_new_login=True)

            # to test if the login was succesfull, will raise LoginRequiredError if unsuccessful
            test_feed = self.api.self_feed()
            time.sleep(0.5)

        except ClientLoginError as e:
            self.logger.debug('ClientLoginError {0!s}'.format(e))
            if e.msg == "bad_password":
                self.bad_password(e)
                raise(e)

            raise e

        except ClientError as e:
            self.logger.debug('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
            raise(e)

        # Show when login expires
        cookie_expiry = self.api.cookie_jar.expires_earliest
        self.logger.debug('Cookie Expiry: {0!s}'.format(
            datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))

        self.logger.debug('connection established')

class InstagramBotBase(InstagramAuthentication):
    """Class with universal bot methods"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_user_id(self, username):
        """method to get user private key from username if not already pk"""
        if isinstance(username, type(str())):
            # get the private key of the given username
            # self.logger.debug(f"retrieving user info for {username}")
            try:
                user_info = self.api.username_info(username)
            except ClientError:
                raise Exception(f"Error: Unable to fetch instagram profile info, username not found: {username}")
            json.dumps(user_info, indent=2)

            user_id = user_info['user']['pk']
            # self.logger.debug("the private key for user {} is: {}".format(username, user_id))
        else:
            # if the username is not a string, it is the private key. Retrieve the matching username
            try:
                user_info = self.api.user_info(username)
                user_id = username
            except ClientError as e:
                if e.msg == "Not Found":
                    self.logger.debug(f"Username '{username}' not found")

                raise e

        return user_id

    def _get_user_feed(self, username, num_posts=100, sleep_time=0.5):
        user_id = self._get_user_id(username)

        post_ids = []
        self.logger.debug("retrieving {} pictures of {}".format(num_posts, username))

        # get the feed of the user
        feed = self.api.user_feed(user_id)

        # save the post private keys from the feed
        for item in feed['items']:
            post_ids.append(item['pk'])

        # collect more of the feed if availible
        while feed['more_available']:
            # if enough of the feed has been collected, stop retrieving more of the feed
            if num_posts != 0 and len(post_ids) >= num_posts:
                break

            time.sleep(sleep_time)
            feed = self.api.user_feed(user_id, max_id=feed['next_max_id'])

            for item in feed['items']:
                post_ids.append(item['pk'])

        return post_ids


class InstagramBroadcastBot(InstagramBotBase):
    
    def get_broadcast_info(self, username=None, user_id=None):
        # replay_broadcast_comments(broadcast_id, starting_offset=0, encoding_tag='instagram_dash_remuxed')
        # replay_broadcast_likes(broadcast_id, starting_offset=0, encoding_tag='instagram_dash_remuxed')
        # broadcast_like_count(broadcast_id, like_ts=0)

        # discover_top_live()
        # suggested_broadcasts()
        # top_live_status(broadcast_ids) -- Get status for a list of broadcast_ids
        # broadcast_heartbeat_and_viewercount(broadcast_id)

        if username:
            user_id = self._get_user_id(username)
            time.sleep(randrange(1, 3))

        user_broadcast = self.api.user_broadcast(user_id)

        if not user_broadcast:
            return None

        broadcast_id = user_broadcast['id']
        viewer_count = user_broadcast['viewer_count']
        cover_frame_url = user_broadcast['cover_frame_url']
        cobroadcasters = user_broadcast['cobroadcasters']
        owner = user_broadcast['broadcast_owner']
        start_time = user_broadcast['published_time']
        broadcast_like_count = self.api.broadcast_like_count(broadcast_id)
        likes = broadcast_like_count['likes']
        update_time = broadcast_like_count['like_ts']

        return {"broadcast_id": broadcast_id,
                "viewer_count": viewer_count,
                "cover_frame_url": cover_frame_url,
                "cobroadcasters": cobroadcasters,
                "owner": owner,
                "start_time": start_time,
                "update_time": update_time,
                "likes": likes}
    
    def get_broadcast_data(self, broadcast_id):
        viewer_data = self.api.broadcast_heartbeat_and_viewercount(broadcast_id)
        likes_data = self.api.broadcast_like_count(broadcast_id)

        return {
            "viewer_count": viewer_data['viewer_count'],
            "likes": likes_data['likes'],
            "cobroadcasters": viewer_data['cobroadcaster_ids'],
            "user_pay_max_amount_reached": viewer_data['user_pay_max_amount_reached']
        }
        
    def get_broadcast_likes(self, broadcast_id):
        broadcast_like_count = self.api.broadcast_like_count(broadcast_id)
        likes = broadcast_like_count['likes']
        update_time = broadcast_like_count['like_ts']

        return {"broadcast_id": broadcast_id,
                "update_time": update_time,
                "likes": likes}


class InstaLocalBot(InstagramBroadcastBot):

    DB_Name = "instagram_broadcast.db"
    conn = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.conn = sqlite3.connect(self.DB_Name)

    def __del__(self):
        if self.conn:
            self.conn.close()

    def track_broadcast(self, username):
        user_id = self._get_user_id(username)
        started = False
        stop_count = 0

        while True:
            broadcast_data = self.get_broadcast_info(user_id)
            
            if broadcast_data:
                if not started:
                    self.logger.debug("Broadcast is live!")
                    self.store_broadcast(broadcast_data)

                started = True
                self.store_likes(broadcast_data)

                time.sleep(60)
            else:
                if started:
                    stop_count += 1
                self.get_broadcast_info(user_id)
                self.logger.debug("long sleep")
                time.sleep(180)

            if started and stop_count >= 5:
                self.logger.debug("Stopping, broadcast seemed to have ended")
                break

    def plot_views(self, broadcast_id):
        sql = f"""SELECT views, likes, update_time FROM broadcast_likes WHERE broadcast_id = '{broadcast_id}'"""
        data = np.array(self.conn.execute(sql).fetchall())

        for row in data:
            row[0] = row[0].split('.')[0]

            date = datetime.datetime.fromtimestamp(int(row[2]), pytz.timezone('US/Eastern')).time()
            row[2] = date
        data[:, 0] = data[:, 0].astype(int)
        data[:, 1] = data[:, 1].astype(int)
        self.logger.debug(data)

        fig = plt.figure(figsize=(8, 6))
        ax = plt.subplot(1, 1, 1)
        ax2 = ax.twinx()

        # plt.xticks(rotation=45)
        ax.plot(data[:, 2], data[:, 0].astype(int), label="views")
        # self.logger.debug("ADSFASDF", np.min(data[:, 2]), np.max(data[:, 2]))

        ax.xaxis.set_major_locator(plt.MaxNLocator(20))

        ax2.plot(data[:, 1].astype(int), label="likes", color='red')

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:,.0f}'.format(y/1000) + 'K'))
        ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:,.0f}'.format(y/1000000) + 'M'))

        ax.set_ylabel("views")
        ax2.set_ylabel("likes")


        plt.grid(alpha=0.3)
        ax.tick_params(axis='x', rotation=35)
        plt.title("VerzuzTV: Alicia Keys vs. John Legend")
        plt.tight_layout()


        plt.show()
        # plt.plot(data[:, 2], data[:, 1], label="likes")


    def store_broadcast(self, data):
        existing_broadcasts = self.conn.execute("SELECT broadcast_id FROM broadcasts")
        existing_broadcasts = existing_broadcasts.fetchall()
        existing_broadcasts = [x[0] for x in existing_broadcasts]

        if data['broadcast_id'] in existing_broadcasts:
            return

        sql = f"""INSERT INTO broadcasts(broadcast_id, cover_frame_url, cobroadcaster, owner, start_time, username)
                          VALUES({data['broadcast_id']}, '{data['cover_frame_url']}', '{data['cobroadcaster']}', "{data['owner']}", '{data['start_time']}', '{username}')"""
        # self.logger.debug("executing:", sql)

        self.conn.execute(sql)
        self.conn.commit()
        self.logger.debug("Commited broadcast")

    def store_likes(self, data):
        self.conn.execute(f"INSERT INTO broadcast_likes (broadcast_id, likes, update_time, views) \
                                    VALUES ({data['broadcast_id']}, {data['likes']}, '{data['update_time']}', '{data['viewer_count']}')")
        self.conn.commit()

        self.logger.debug("Commited likes")


if __name__ == "__main__":

    username = "laughfactoryhw"
    username = "doroart_"

    # create a file called creds_01.txt with your username on first line and password on second line
    bot = InstagramBroadcastBot(username="davincible_", password="!&6xLDQ@ecZisD", settings_file_path="auth_storage.txt")
    # InstagramBroadcastBot.test_accounts("creds_insta_batch.txt")

    # print(json.dumps(bot.api.username_info(username), indent=4))
    import random

    broadcast_info = bot.get_broadcast_info('biancadata')
    broadcast_id = broadcast_info['broadcast_id']
    while True:
        info = bot.get_broadcast_data(broadcast_id)
        print(info)
        time.sleep(random.randrange(285, 315)/100)
    # print(f"Broadcast info for {username}:\n{json.dumps(broadcast_info, indent=4)}")

    # conn = sqlite3.connect("instagram_broadcast.db")
    # rows = conn.execute("SELECT * FROM sqlite_master")
    # self.logger.debug("", rows)


    # self.logger.debug(f"Starting to track broadcast for {username}")
    # bot.track_broadcast(username)

    # bot.plot_views('17892666328529515')
