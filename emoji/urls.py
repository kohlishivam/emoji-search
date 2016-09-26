from django.conf.urls import patterns, include, url
from django.contrib import admin
import chatbot.views as v


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'emoji.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index$',v.index),
    url(r'^facebook_auth/?$',v.MyChatBotView.as_view()),
)
