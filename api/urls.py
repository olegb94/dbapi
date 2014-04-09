from django.conf.urls import patterns, include, url

from user_views import *
from forum_views import *
from thread_views import *
from post_views import *


urlpatterns = patterns('',

    url(r'^user/create', user_create),
    url(r'^user/details', user_details),
    url(r'^user/follow', user_follow),
    url(r'^user/unfollow', user_unfollow),
    url(r'^user/updateProfile', user_update),
    url(r'^user/listFollowers', user_listFollowers),
    url(r'^user/listFollowing', user_listFollowing),
    url(r'^user/listPosts', user_listPosts),

    url(r'^forum/create', forum_create),
    url(r'^forum/details', forum_details),
    url(r'^forum/listUsers', forum_listUsers),
    url(r'^forum/listPosts', forum_listPosts),
    url(r'^forum/listThreads', forum_listThreads),


    url(r'^post/create', post_create),
    url(r'^post/details', post_details),
    url(r'^post/remove', post_remove),
    url(r'^post/restore', post_restore),
    url(r'^post/update', post_update),
    url(r'^post/vote', post_vote),
    url(r'^post/list', post_List),

    url(r'^thread/create', thread_create),
    url(r'^thread/details', thread_details),
    url(r'^thread/close', thread_close),
    url(r'^thread/open', thread_open),
    url(r'^thread/remove', thread_remove),
    url(r'^thread/restore', thread_restore),
    url(r'^thread/update', thread_update),
    url(r'^thread/vote', thread_vote),
    url(r'^thread/subscribe', thread_subscribe),
    url(r'^thread/unsubscribe', thread_unsubscribe),
    url(r'^thread/listPosts', thread_listPosts),
    url(r'^thread/list', thread_List),
    url(r'^.*', other_pages)
)
