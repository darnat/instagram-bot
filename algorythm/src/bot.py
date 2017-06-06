import instana
import time
import os

from .db import db
from .models import *
from .components.like import Like
from .components.comment import Comment
from .components.follow import Follow
from .components.unfollow import Unfollow
# from .components.comment import Comment
# from .components.follow import Follow
# from .components.unfollow import Unfollow


class Bot(object):
    """
    Instagram Bot
    """
    def __init__(self):
        """
        Initialize Instagram Bot
        """
        username = os.environ.get('INSTA_USERNAME', 'default')
        password = os.environ.get('INSTA_PASSWORD', 'default')
        self._instana = instana.Instana()
        self._instana.login(username, password)
        db.create_all()
        self._like = Like(self._instana)
        self._comment = Comment(self._instana)
        self._follow = Follow(self._instana)
        self._unfollow = Unfollow(self._instana)

    def run_auto_mod(self):
        """
        Auto Mod Loop : Like, Comment, Follow, Unfollow
        """
        while True:
            self._like.run()
            self._comment.run(self._like._last_media_liked)
            self._follow.run(self._like._last_media_liked)
            self._unfollow.run(self._like._last_media_liked)
            time.sleep(10)
