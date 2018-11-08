from django.contrib.auth.base_user import BaseUserManager

from livefield import LiveManager


class AccountManager(LiveManager):
    pass

class StoreManager(LiveManager):
    pass

class MemberManager(LiveManager, BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super Member must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super Member must have is_superuser=True.')
        if extra_fields.get('account') is None:
            raise ValueError('Super Member must have account.')

        return self._create_user(email, password, **extra_fields)
