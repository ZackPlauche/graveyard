import numpy as np
import re
import io
from logging import getLogger
from base64 import b64decode

if __name__ != "__main__":
    from .models import * 
    from broadcasts.youtube.YTbot import YoutubeBroadcastBot  

from django import template
register = template.Library()

DEBUG = False

@register.filter
def format_large_number(value, num_decimals=2):
    """
    https://gist.github.com/dnmellen/bfc1b3005999aaff3ed4
    
    Django template filter to convert regular numbers to a
    cool format (ie: 2K, 434.4K, 33M...)
    :param value: number
    :param num_decimals: Number of decimal digits
    """

    int_value = int(value)
    formatted_number = '{{:.{}f}}'.format(num_decimals)
    if int_value < 1000:
        return str(int_value)
    elif int_value < 1000000:
        return formatted_number.format(int_value/1000.0).rstrip('0.') + 'K'
    else:
        return formatted_number.format(int_value/1000000.0).rstrip('0.') + 'M'

def strip_username(link : str) -> str:
    pattern_username = r'instagram\.com\/([^\/]*)|youtube.[\w]{2,4}\/channel\/([^\/]*)|twitch.[\w]{2,4}\/([^\/]*)'
    pattern_channel = r'youtube.[\w]{2,4}[userc\/]{1,6}([^\/]*)'
    
    # Extract username from urls
    if match := re.findall(pattern_username, link, re.IGNORECASE):
        username = [x for x in match[0] if x][0].strip('/').strip()
        return username
    
    # Extract channel name from youtube, and get channel_id
    elif channel := re.findall(pattern_channel, link, re.IGNORECASE):
        channel = channel[0].strip('/').strip()
        API_KEY = APIAccount.objects.filter(platform__name__iexact = "youtube")[0].api_key
        username = YoutubeBroadcastBot(API_KEY).get_channel_id(channel)

        return username
    
    # If no match, the username is no url, so return the username directly
    else:
        try: 
            b64decode(link)
            username = link
        except:
            API_KEY = APIAccount.objects.filter(platform__name__iexact = "youtube")[0].api_key
            username = YoutubeBroadcastBot(API_KEY).get_channel_id(link)
            
        return username

def search_list(phrase : str, list_ : list) -> int:        
        match = [np.where(list_ == x)[0][0] for x in list_ if re.findall(phrase, x, re.IGNORECASE)]
        
        return match[0] if match else None

def upload_api_accounts(text : str) -> bool:
    logger = getLogger('uploads')
    logger.info("Bulk uploading API accounts")
    
    # Load CSV file
    try:
        with open(str(text), 'r') as file:
            upload_data = np.loadtxt(file, delimiter=",", dtype=str)
        logger.debug(f"Opened csv from file path {text}")
    except Exception:
        upload_data = np.loadtxt(io.BytesIO(text), delimiter=",", dtype=str)
        logger.debug(f"Loaded in csv from text string")
        
    columns = ['username', 'email', 'password', 'platform', 'client_id', 'auth_token', 'api_key']
    column_indices = {column : index for column in columns if (index := search_list(column, upload_data[0])) != None}
        
    # Check if necessary columns are present
    if not column_indices.keys():
        logger.error("0 matching colums found !! sucker")
        return False
    
    elif 'username' not in column_indices.keys():
        logger.error("username column not found")
        return False
        
    elif 'password' not in column_indices.keys():
        logger.error("passwords column not found")
        return False

    elif 'platform' not in column_indices.keys():
        logger.error("platform column not found")
        return False
    
    # Process rows
    for row in upload_data[1:]:
        def get_field(column):
            return row[index] if (index := column_indices.get(column, None)) != None else None
        
        platform = Platform.objects.filter(name__iexact = row[column_indices['platform']])
        if not platform:
            logger.warning(f"Invalid platform provided: '{row[column_indices['platform']]}'")
            continue
        else:
            platform = platform[0]
            
        account, created = APIAccount.objects.get_or_create(username = row[column_indices['username']], platform = platform)
        account.email = get_field('email')
        account.password = get_field('password')
        account.client_id = get_field('client_id')
        account.auth_token = get_field('auth_token')
        account.api_key = get_field('api_key')
        account.save()
        logger.debug(f"Added/Updated {account.username}")
    
    return True
    
def process_watch_list_csv(file_path : str) -> None:
    logger = getLogger('uploads')
    logger.info("Bulk uploading accounts to monitor")
    
    # Load CSV file
    try:
        with open(str(file_path), 'r') as file:
            streamer_upload_data = np.loadtxt(file, delimiter=",", dtype=str)
        logger.debug(f"Opened csv from file path {file_path}")
    except Exception:
        streamer_upload_data = np.loadtxt(io.BytesIO(file_path), delimiter=",", dtype=str)
        logger.debug(f"Loaded in csv from text string")
    
    # Get streamer index
    if (index_streamer := search_list("name|artist|influencer|celebrity|celebrities", streamer_upload_data[0])) == None:
        logger.error("No name or artist column found in csv sheet")
        return None, "ERROR: Artist or Name not found"  # tweak this so it and returns an error
    
    # Get category index
    index_streamer_category = search_list("category", streamer_upload_data[0]) 

    platforms = Platform.objects.all()  # Create a list of each platform's object
    platform_indices = {}

    # Dynamically find each platforms index
    for platform in platforms:
        platform_index = search_list(platform.name, streamer_upload_data[0])
        platform_indices[platform_index] = platform

    errors = []
    success = []

    # Itterate over csv table
    for row in streamer_upload_data[1:]:
        try:
            # Create the streamer object
            streamer, created = Streamer.objects.get_or_create(name=row[index_streamer])
            
            if index_streamer_category:
                streamer.category, category_created = Category.objects.get_or_create(name=row[index_streamer_category])
            streamer.save()

            # Create accounts for the streamer
            for platform_index, platform in platform_indices.items():
                if account_name := strip_username(row[platform_index]):

                    # Needs to stay this way because the objects need to relate both to the platform and streamer. That's what makes them unique
                    account, account_created = Account.objects.get_or_create(platform=platform, streamer=streamer)
                    account.name = account_name
                    account.save()


            # Put this at the end
            logger.debug(f"Added to the database: {account}")
            success.append(row[index_streamer])
            
        except Exception as e:
            logger.error("Failed to add account, with error {e}")
            errors.append(e)
            # you can remove this at the end
            if DEBUG:
                raise e

    # Give this back to the user on the front-end somehow
    logger.info(f"Finished adding csv files, with {len(success)} successes, and {len(errors)} errors")
    return success, errors


if __name__ == "__main__":
    # process_watch_list_csv("/home/tyler/Launchpad/test/_LWS Artist & Influencers Site List - ARTIST.csv")
    # print(re.findall('name|artist|influencer|celebrity|celebrities', "Artist", re.IGNORECASE))
    
    test = "https://www.youtube.com/channel/UCC3zgQZssIUMPZEYZWaqvbg/about"
    test2 = "https://www.instagram.com/timbaland/"
    print(strip_username(test2))
