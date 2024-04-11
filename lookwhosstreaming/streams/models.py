from django.db import models
from django.utils import timezone
from datetime import datetime
import json

class Platform(models.Model):
    name = models.CharField(max_length=52, null=True, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def color(self):
        if self.name == 'Instagram':
            return '#fbad50'
        elif self.name == 'YouTube':
            return '#ff0000'
        elif self.name == 'Twitch':
            return '#6441A4'

    @property
    def logo(self):
        return f'<i class="fab fa-{self.name.lower()}" style="color: {self.color}; font-size: 29px"></i>'


class Category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    class Meta: 
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Streamer(models.Model):
    name = models.CharField(max_length=50, null=True, help_text="What does this streamer call himself / herself?")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def profile_pic(self):
        if accounts := self.account_set.all():
            for platform in Platform.objects.all().order_by('name'):
                if profile_pic := accounts.get(platform=platform).profile_pic_url:
                    return profile_pic
                else:
                    return 'https://vignette.wikia.nocookie.net/kirby-fan-fiction/images/d/d0/IMG_0181.PNG/revision/latest?cb=20161213171018'
        else:
            return 'https://vignette.wikia.nocookie.net/kirby-fan-fiction/images/d/d0/IMG_0181.PNG/revision/latest?cb=20161213171018'


class Account(models.Model):
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True)
    name = models.CharField(verbose_name="Account Name", max_length=100)
    full_name = models.CharField(verbose_name="Full Name", max_length=100, null=True, blank=True)
    description = models.TextField("Account Description", null=True, blank=True)
    link = models.URLField(blank=True, null=True)
    live = models.BooleanField("Live", default=False)
    profile_pic_url = models.URLField("Profile Picture URL", max_length=512, null=True, blank=True)
    monitor = models.BooleanField(default=True)
    followers = models.IntegerField("Account Followers", null=True, blank=True)
    followers_data = models.TextField("Followers over time", null=True, blank=True)

    class Meta:
        ordering = ['streamer']
    
    def __str__(self):
        return self.full_name or self.name

    def save(self, *args, **kwargs):
        if not self.profile_pic_url:
            self.profile_pic_url = 'https://vignette.wikia.nocookie.net/kirby-fan-fiction/images/d/d0/IMG_0181.PNG/revision/latest?cb=20161213171018'

        return super().save(*args, **kwargs)

    @property
    def card_display_name(self):
        return self.streamer.name
    
    @property
    def account_name_with_host_name(self):
        return f"{self.streamer.name}: {self.name}"

    @property
    def name_with_platform(self):
        return f"{self.streamer.name} - {self.platform.name}"

    @property
    def url(self):
        if self.platform.name == "Instagram":
            return f'https://www.instagram.com/{self.name}/'
        elif self.platform.name == "Twitch":
            return f'https://www.twitch.tv/{self.name}'
        elif self.platform.name == "YouTube":
            return f'https://www.youtube.com/channel/{self.name}'


class APIAccount(models.Model):
    username = models.CharField("Username", max_length=128)
    email = models.EmailField("Email", blank=True, null=True)
    password = models.CharField("Password", max_length=128)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT, null=True, verbose_name="Platform")
    client_id = models.CharField("Client ID", max_length=256, blank=True, null=True)
    auth_token = models.CharField("Authentication/bearer Token", max_length=5120, blank=True, null=True)
    api_key = models.CharField("API Key", max_length=512, blank=True, null=True)
    blacklist = models.BooleanField("Blacklist Flag", default=False)
    
    class Meta:
        ordering = ['platform', 'email']
        verbose_name = 'API Account'
        verbose_name_plural = 'API Accounts'
        
    def __str__(self): 
        return self.username

class Stream(models.Model): 
    broadcast_id = models.CharField("Broadcast-ID", max_length=200, unique=True, null=True, blank=True)
    host = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name="Host")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True, verbose_name="Platform")
    title = models.CharField("Title", max_length=200, blank=True, null=True)
    description = models.TextField("Description", blank=True, null=True)
    url = models.URLField("URL", null=True, blank=True)
    live = models.BooleanField("Live", default=False)
    start_time = models.DateTimeField("Start Time", null=True, help_text="Use yyyy-mm-dd hh:mm:ss format with hyphens.")
    end_time = models.DateTimeField("End Time", null=True, blank=True)
    viewer_data = models.TextField("Viewer Data", blank=True, null=True)
    likes_data = models.TextField("Likes Data", null=True, blank=True)
    update_time = models.DateTimeField("Update Time", null=True, blank=True)
    peak_viewers = models.PositiveIntegerField("Peak Viewers", default=0)
    average_viewers = models.PositiveIntegerField("Average Viewers", default=0)
    current_viewers = models.PositiveIntegerField("Current Viewers", default=0)
    cumulative_viewers = models.PositiveIntegerField("Cumulative Viewers", default=0)
    cover_frame_url = models.CharField("Cover Frame", max_length=400, null=True, blank=True)
    cobroadcasters = models.TextField("Co-Broadcaster", null=True, blank=True)
    score = models.FloatField("Score", default=0)
    is_manual = models.BooleanField("Manual", default=False)
    
    
    def save(self, *args, **kwargs):
        def closest(lst, K): 
            return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))] 
        
        if "youtube.com" in str(self.broadcast_id).lower():
            self.broadcast_id = self.broadcast_id.split('v=')[1]
        
        if not self.is_manual:
            
            # Average & Peak
            if self.viewer_data:
                data = [int(x) for x in list(json.loads(self.viewer_data).values())]
                self.average_viewers = sum(data) / len(data)
                self.peak_viewers = max(data)

            # Set platform
            if self.host and self.host.platform:
                self.platform = self.host.platform

            # Set url
            if self.platform and self.platform.name and self.platform.name == "Instagram":
                self.url = f'{self.host.url}live/'
        
        # Set score
        if self.host and self.host.followers and self.peak_viewers: 
            followers_data = json.loads(self.host.followers_data)
            followers = followers_data[str(closest(list(map(float, followers_data.keys())), self.start_time.timestamp()))]
            
            score = (int(self.peak_viewers) / int(self.host.followers)) * 2
            score += self.peak_viewers * 0.00002
            self.score = score
        
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['start_time', 'host']

    def __str__(self):
        return self.host.__str__()

    @property
    def likes(self):
        if self.likes_data:
            return list(json.loads(self.likes_data).values())[-1]
        else:
            return 0

    @property
    def duration(self):
        if self.start_time:
            if self.end_time:
                end_time = self.end_time
            else:
                end_time = timezone.now()
            
            days = (end_time - self.start_time).days
            duration = (end_time - self.start_time).seconds
            hours = int(duration / 3600)
            minutes = round(((duration / 3600) % 1) * 60)
            return f"{days}D {hours}H" if days else f"{hours}H {minutes}M"
        else:
            return None
