import os
import random
import time
import datetime

from .component import Component
from ..models.follower import Follower
from ..db import db


class Unfollow(Component):
    """
    UnFollow Component class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize Unfollow Component Object
        """
        super().__init__(*args, **kwargs)
        self._action_interval = int(os.environ.get('INSTA_FOLLOW_TIME', 10800))

    def get_followed(self):
        """
        Get the Following supposed to be unfollowed stored in the DB
        """
        return Follower.query.filter((Follower.timestamp + datetime.timedelta(seconds=self._action_interval)) <= datetime.datetime.now(), Follower.unfollowed == False).order_by(Follower.timestamp.desc()).first()
        # return Follower.query.filter(Follower.timestamp <= datetime.datetime.now() + datetime.timedelta(seconds=self._action_interval)).first()

    def run(self, media=None):
        """
        Run the process
        """
        unfollow = self.get_followed()
        if unfollow:
            res = self._instana.unfollow_by_id(unfollow.pk)
            unfollow.unfollowed = True
            db.session.commit()
            print('Unfollow a User : {}'.format(unfollow.pk))
        #     comment = random.choice(self._comments)
        #     res = self._instana.comment(media, comment.content)
        #     print('Picture Commented : {}'.format(media._id))
            # hashtag = random.choice(self._hashtags)
            # medias = self._instana.get_tag_feed(hashtag.name)
            # self.pertinence_calculator(medias)
            # medias.sort(key=lambda x: x.rate, reverse=True)
            # media = medias[0]
            # res = self._instana.like_media(media)
            # self._last_media_liked = media
            # save = LikeModel(media._user._pk, media._id, datetime.now())
            # db.session.add(save)
            # db.session.commit()
            # print('Picture Liked : {}'.format(media._id))
