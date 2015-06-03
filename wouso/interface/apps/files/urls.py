from django.conf.urls import patterns, url


urlpatterns = patterns('wouso.interface.apps.files.views',
    url(r'^$', 'index', name='files_index_view'),
    url(r'^add_perm/$', 'get_file_list_permission', name='file_list_permission'),
)
