import os
import random
import time
import datetime

from .component import Component
from ..models.follower import Follower
from ..db import db


class Follow(Component):
    """
    Follow Component class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize Follow Component Object
        """
        super().__init__(*args, **kwargs)
        lastFollow = self.get_following()
        self._last_action = time.mktime(lastFollow.timestamp.timetuple()) if lastFollow else 0
        self._action_interval = (24 * 60 * 60) / int(os.environ.get('INSTA_FOLLOW_PER_DAY', 100))

    def get_following(self):
        """
        Get the last Following stored in the DB
        """
        return Follower.query.order_by(Follower.timestamp.desc()).first()
        # return Follower.query.filter(Follower.timestamp <= datetime.datetime.now() + datetime.timedelta(seconds=self._action_interval)).first()

    def run(self, media=None):
        """
        Run the process
        """
        if media and self.able_to():
            res = self._instana.follow(media._user)
            save = Follower(media._user._pk, media._user._username, datetime.datetime.now())
            db.session.add(save)
            db.session.commit()
            print('Follow a User : {}'.format(media._user._pk))
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
