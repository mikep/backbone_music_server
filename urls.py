from views import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^api/login$', login),
    (r'^api/logout$', logout),
    (r'^api/pl/$', ajax_playlist_view),
    (r'^api/pl/(?P<pl_file>[^/]+?)$', ajax_playlist_view),
    (r'^api/list_dir/(?P<dir>[^/]+?)?$', ajax_file_view),
    (r'^api/song_info/(?P<song>[^/]+?)$', song_info),
)
