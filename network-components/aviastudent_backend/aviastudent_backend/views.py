from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from social.apps.django_app.utils import psa
from rest_framework.views import APIView
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings


def home(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
    return render_to_response('aviastudent_templates/home.html',
                              context_instance=context)


@login_required
def test_auth_required(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
    return render_to_response('aviastudent_templates/test_auth_required.html',
                              context_instance=context)


@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    user = request.backend.do_auth(request.GET.get('access_token'))
    if user:
        login(request, user)
        return 'OK'
    else:
        return 'ERROR'


@psa()
def auth_by_token(request, backend):
    """Decorator that creates/authenticates a user with an access_token"""
    # token = request.DATA.get('access_token')
    # user = request.user
    user = request.backend.do_auth(
            access_token=request.DATA.get('access_token')
        )
    if user:
        return user
    else:
        return None


class FacebookView(APIView):
    """View to authenticate users through Facebook."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        auth_token = request.DATA.get('access_token', None)
        backend = request.DATA.get('backend', None)
        if auth_token and backend:
            try:
                # Try to authenticate the user using python-social-auth
                user = auth_by_token(request, backend)
            except Exception as e:
                return Response({
                        'status': 'Bad request',
                        'message': 'Could not authenticate with the provided token.' + str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)
            if user:
                if not user.is_active:
                    return Response({
                        'status': 'Unauthorized',
                        'message': 'The user account is disabled.'
                    }, status=status.HTTP_401_UNAUTHORIZED)

                # This is the part that differs from the normal python-social-auth implementation.
                # Return the JWT instead.

                # Get the JWT payload for the user.
                payload = jwt_payload_handler(user)

                # Include original issued at time for a brand new token,
                # to allow token refresh
                if api_settings.JWT_ALLOW_REFRESH:
                    payload['orig_iat'] = timegm(
                        datetime.utcnow().utctimetuple()
                    )

                # Create the response object with the JWT payload.
                response_data = {
                    'token': jwt_encode_handler(payload)
                }

                return Response(response_data)
        else:
            return Response({
                    'status': 'Bad request',
                    'message': 'Authentication could not be performed with received data.'
            }, status=status.HTTP_400_BAD_REQUEST)