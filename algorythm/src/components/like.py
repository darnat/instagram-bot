import random
import time
import re
import os
import datetime

from .component import Component
from ..models.hashtag import Hashtag
from ..models.location import Location
from ..models.blacklist import Blacklist
from ..models.like import Like as LikeModel
from ..db import db


class Like(Component):
    """
    Like Component class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize Like Component Object
        """
        super().__init__(*args, **kwargs)
        self._locations = self.get_locations()
        self._hashtags = self.get_hashtags()
        self._blacklisted_hashtags = self.get_hashtags(True)
        self._blacklisted_user = self.get_blacklisted_user()
        self._blacklisted_user_pattern = self.get_blacklisted_user(True)
        self._last_media_liked = None
        self._action_interval = (24 * 60 * 60) / int(os.environ.get('INSTA_LIKE_PER_DAY', 1000))

    def get_locations(self):
        """
        Get the locations stored in the DB
        """
        return Location.query.all()

    def get_hashtags(self, blacklisted: bool = False):
        """
        Get the hashtags stored in the DB
        """
        return Hashtag.query.filter_by(blacklisted=blacklisted).all()

    def get_blacklisted_user(self, pattern: bool = False):
        """
        Get the blacklisted users stored in the DB
        """
        return Blacklist.query.filter_by(pattern_only=pattern).all()

    def run(self):
        """
        Run the process
        """
        if self.able_to():
            # if len(self._locations) > 0 and bool(random.getrandbits(1)):
            #     location = random.choice(self._locations)
            #     medias = self._instana.get_location_feed(location.pk)
            # else:
            hashtag = random.choice(self._hashtags)
            # last_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
            # max_id = last_hour.strftime("%s") + "000000"
            medias = self._instana.get_tag_feed(hashtag.name)
            self.pertinence_calculator(medias)
            medias.sort(key=lambda x: x.rate, reverse=True)
            media = medias[0]
            res = self._instana.like_media(media)
            self._last_media_liked = media
            save = LikeModel(media._user._pk, media._id, datetime.datetime.now())
            db.session.add(save)
            db.session.commit()
            print('Picture Liked : {} - {}'.format(media._id, media.rate))

    def pertinence_calculator(self, medias: list):
        """
        Algorythm to check the pertinence of each media
        """
        current = time.time()
        time_ago_last = (current - medias[-1]._taken_at)
        for media in medias:
            # Set the origin media rate to 1
            media.rate = 1.0
            # Calculate when the media was published and increase the ratio depends on
            time_ago = (current - media._taken_at)
            media.rate += (time_ago / time_ago_last) / 4.0 if time_ago <= 7200 else 0
            # Find All Hashtag in the Caption
            hashtags = re.findall('#((?:\[[^\]]+\]|\S+))',
                                  media._caption._text if media._caption._text else '')
            # Search for how many common hashtags are in and increase the rate
            sms = set([o.name for o in self._hashtags]).intersection(hashtags)
            media.rate += sms.__len__() / 10.0
            # Search for how many common blacklisted hashtags are in and empty the rate
            smsb = set([o.name for o in self._blacklisted_hashtags]).intersection(hashtags)
            if smsb.__len__() >= 1:
                media.rate *= 0
            # Increase the rate if the media is an image
            if media._media_type and media._media_type == 2:
                media.rate *= 0.1
            # Increase the rate depends on the Like count
            if media._like_count:
                media.rate += ((-1.0/1000) * media._like_count + 1.0/2.0) if media._like_count <= 500 else 0
            # Increase the rate depends on the Comment count
            if media._comment_count:
                media.rate += ((-3.0/100) * media._comment_count + 3.0/5.0) if media._comment_count <= 20 else 0
            # Check if the user is blacklisted
            if media._user._username in [o.name for o in self._blacklisted_user]:
                media.rate *= 0.0
            # Check if the user pattern is blacklisted
            if any(media._user._username in s for s in [o.name for o in self._blacklisted_user_pattern]):
                media.rate *= 0
            # Condition to not like the media
            if media._has_liked or media._user._is_verified or media._user._following:
                media.rate *= 0.0
