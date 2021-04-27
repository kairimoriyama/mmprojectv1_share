from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager

# Create your models here.



# class CustomUserManager(UserManager):
#     """ユーザーマネージャー"""
#     use_in_migrations = True

#     def _create_user(self, email, password, **extra_fields):
#         if not email.split('@')[1] in ['@gmail.com']:
#             raise ValueError('許可されていないドメインです')


class CustomUser(AbstractUser):

    is_active = models.BooleanField("is_active", default=True) #個別にアカウントの許可を設定
    
    class Meta:
        verbose_name_plural = 'CustomUser'
    




