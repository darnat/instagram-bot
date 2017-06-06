import os
import random

from .component import Component
from ..models.comment import Comment as CommentModel


class Comment(Component):
    """
    Comment Component class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize Comment Component Object
        """
        super().__init__(*args, **kwargs)
        self._comments = self.get_comments()
        self._action_interval = (24 * 60 * 60) / int(os.environ.get('INSTA_COMMENT_PER_DAY', 200))

    def get_comments(self):
        """
        Get the comments stored in the DB
        """
        return CommentModel.query.all()

    def run(self, media=None):
        """
        Run the process
        """
        if media and self.able_to():
            comment = random.choice(self._comments)
            res = self._instana.comment(media, comment.content)
            print('Picture Commented : {}'.format(media._id))
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
