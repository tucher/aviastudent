from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from online_viewer.views import UserListAPIView
from aviastudent_backend.views import FacebookView

admin.autodiscover()


urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^$', 'aviastudent_backend.views.home', name='home'),
    # url(r'login', 'aviastudent_backend.views.home', name='home'),
    url(r'^test_auth_required$', 'aviastudent_backend.views.test_auth_required', name='test_auth_required'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'api/v1/auth/login/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'api/v1/users/', UserListAPIView.as_view()),
    # url(r'^.*$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/v1/auth/facebook/', FacebookView.as_view()),
)
