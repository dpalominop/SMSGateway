from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#from django.contrib.sites.models import Site
#from django.contrib.contenttypes.models import ContentType

admin.autodiscover()
#admin.site.unregister(Site)
#admin.contenttypes.unregister(ContentType)

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'sms_web.views.home', name='home'),
    # url(r'^sms_web/', include('sms_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^sms/', include(admin.site.urls)),
)

#import utils.admin_auth