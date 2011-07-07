from django.conf.urls.defaults import patterns, include, url
from views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^wiki/$',get_all_articles), 
    (r'^wiki/([^/]+)/edit/add/$',add_article_to_db),                  
    (r'^wiki/([^/]+)/edit/$',edit_article),    
    (r'^wiki/([^/]+)/$',get_article),
    (r'^tags/([^/]+)/$',article_by_tag),
    (r'^search-form/$',search_form),
    (r'^search/$',search),
    # Examples:
    # url(r'^$', 'djTest.views.home', name='home'),
    # url(r'^djTest/', include('djTest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
