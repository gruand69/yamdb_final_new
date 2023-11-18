from django.contrib.auth.models import AbstractUser
from django.db import models

# class MyEmailField(models.EmailField):
#     def __init__(self, *args, **kwargs):
#         super(MyEmailField, self).__init__(*args, **kwargs)

#     def get_prep_value(self, value):
#         return str(value).lower()


# class NameField(models.CharField):
#     def __init__(self, *args, **kwargs):
#         super(NameField, self).__init__(*args, **kwargs)

#     def get_prep_value(self, value):
#         return str(value).lower()


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user')
    )
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=150,
                                unique=True
                                )
    email = models.EmailField(verbose_name='Адрес электронной почты',
                              max_length=254,
                              unique=True)
    # username = NameField(verbose_name='Имя пользователя',
    #                      max_length=150,
    #                      unique=True
    #                      )
    # email = MyEmailField(verbose_name='Адрес электронной почты',
    #                      max_length=254,
    #                      unique=True)

    role = models.CharField(verbose_name='Роли пользователя',
                            default=USER,
                            choices=ROLE_CHOICES,
                            max_length=40)
    bio = models.TextField(verbose_name='Биография',
                           blank=True)
    confirmation_code = models.CharField(verbose_name='Проверочный код',
                                         max_length=150, )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
