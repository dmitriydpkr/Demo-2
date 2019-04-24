from django.db import models
from django.contrib.auth.models import User
from main_app.models import Good


class Comment(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='CommentUser')
    good = models.ForeignKey(Good, verbose_name='GoodComment', on_delete=models.CASCADE, related_name='GoodComment')
    date = models.DateTimeField(auto_now_add=True, verbose_name='DateComment')
    comment_overview = models.CharField(max_length=300, verbose_name='Comment', default='na')

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
