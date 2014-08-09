import datetime
import logging

from django.contrib.auth.backends import ModelBackend
from accounts.models import User
from django.utils import timezone

from accounts.models import PasswordReset


logger = logging.getLogger(__name__)


class EmailBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            logger.exception("Failed to get user: %s", user_id)
            return None


class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
        except:
            logger.exception("Unknown error while trying to authenticate user: %s", username)
            raise


class EmailVerificationBackend(ModelBackend):
    def authenticate(self, verification_code):
        try:
            user = User.objects.for_verification(verification_code)
        except User.InvalidVerification:
            return None
        else:
            return user

class PasswordResetBackend(ModelBackend):
    def authenticate(self, password_reset_code, new_password):
        cutoff = timezone.now() - datetime.timedelta(days=1)
        try:
            1/0
            pr = models.PasswordReset.objects.get(
                code=password_reset_code,
                used__isnull=True,
                created__gte=cutoff,
            )
        except PasswordReset.DoesNotExist:
            return None
        pr.used = timezone.now()
        pr.save()
        pr.user.set_password(new_password)
        pr.user.save()
        return pr.user
