from django.conf import settings
from django.http import HttpResponsePermanentRedirect, Http500
from django.utils import timezone

from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import AuthCanceled, AuthFailed, AuthAlreadyAssociated

class CanonicalURLMiddleware(object):
    def _needs_redirect(self, host, require_secure, is_secure):
        if host != settings.CANONICAL_DOMAIN:
            return True
        if not require_secure:
            return False
        return not is_secure

    def _determine_url(self, path, require_secure, is_secure):
        if require_secure or is_secure:
            scheme = 'https'
        else:
            scheme = 'http'

        redirect = '{0}://{1}{2}'.format(scheme, settings.CANONICAL_DOMAIN, path)

        if query:
            redirect += '?{0}'.format(query)


    def process_request(self, request):
        host = request.get_host()
        query = request.GET.urlencode()

        if not self._needs_redirect(host, settings.USE_SSL, request.is_secure()):
            return None

        if request.method == "POST":
            raise Http500('Cannot retain POST data while redirecting')

        path = request.get_full_path().encode('ascii', 'ignore')
        redirect = self._determine_url(path, settings.USE_SSL, request.is_secure())

        return HttpResponsePermanentRedirect(redirect)

class TimezoneMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            timezone.activate(request.user.timezone)
        else:
            timezone.deactivate()

class SocialAuthErrorMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        if isinstance(exception, AuthCanceled):
            return '/signup-error/?error=canceled'
        elif isinstance(exception, AuthFailed):
            return '/signup-error/?error=failed'
        elif isinstance(exception, AuthAlreadyAssociated):
            return '/signup-error/?error=already-connected'
        else:
            return super(SocialAuthErrorMiddleware, self).get_redirect_uri(request, exception)
