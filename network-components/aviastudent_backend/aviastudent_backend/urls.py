from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aviastudent_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^$', 'aviastudent_backend.views.home', name='home'),
    url(r'^test_auth_required$', 'aviastudent_backend.views.test_auth_required', name='test_auth_required'),
    url(r'^admin/', include(admin.site.urls)),
)
