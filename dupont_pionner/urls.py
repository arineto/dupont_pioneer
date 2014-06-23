from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^filter/(?P<filter_value>.+)/$', 'core.views.home', name='home'),
    url(r'^save_map/$', 'core.views.save_map', name='save_map'),
    url(r'^save_map/(?P<map_id>\d+)/$', 'core.views.save_map', name='save_map'),
    url(r'^delete_map/(?P<map_id>\d+)/$', 'core.views.delete_map', name='delete_map'),
    url(r'^edit_map/(?P<map_id>\d+)/$', 'core.views.edit_map', name='edit_map'),
    url(r'^add_info/(?P<map_id>\d+)/$', 'core.views.add_info', name='add_info'),
    url(r'^edit_info/(?P<farm_id>\d+)/$', 'core.views.edit_info', name='edit_info'),
    url(r'^remove_info/(?P<farm_id>\d+)/$', 'core.views.remove_info', name='remove_info'),
    url(r'^logout/$', 'core.views.logout_aux', name='logout_aux'),
    url(r'^login/$', 'core.views.login_aux', name='login_aux'),
    url(r'^access_info/$', 'core.views.access_info', name='access_info'),
    url(r'^access_info/(?P<username>.+)/$', 'core.views.access_info', name='access_info'),
    url(r'^forgot_password/$', 'core.views.forgot_password', name='forgot_password'),
    url(r'^change_password/$', 'core.views.change_password', name='change_password'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )