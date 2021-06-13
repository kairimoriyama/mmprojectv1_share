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

    is_active = models.BooleanField("Active", default=True) #個別にアカウントの許可を設定
    financial = models.BooleanField(default=False)
    outside = models.BooleanField(default=False)
    academy = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'CustomUser'
    
    def __str__(self):
        return self.username +' '+ self.email +' '+ str(self.is_active)



