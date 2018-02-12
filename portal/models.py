"""Declare models for portal app."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    """User model."""

    username = models.CharField(_('username'), max_length=150, unique=False)
    email = models.EmailField(
        _('email address'), 
        max_length=255,
        unique=True, 
        error_messages={
            'unique': _("A user with that email already exists."),
        },)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Team(models.Model):
    team_head = models.ForeignKey(MyUser, default=None, null=True)
    team_name = models.CharField(max_length=200, blank=False)
    team_info = models.TextField(default=None, blank=True)
    team_link = models.CharField(max_length=255, blank=True)
    number_of_players = models.IntegerField(default=0)
    game_on = models.IntegerField(default=0)
    team_lock = models.BooleanField(default=False)
    team_avatar = models.ImageField(upload_to="team_image", null=True, blank=True)

    def __str__(self):
        return self.team_name


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    steam_id = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, default='India', blank=True)
    avatar = models.ImageField(upload_to="profile_image", null=True, blank=True)
    status_CS = models.IntegerField(default=0)
    status_FIFA = models.IntegerField(default=0)
    team_cs = models.ForeignKey(Team, default=None, null=True, blank=True)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email

    @property
    def get_steam_id(self):
        if self.steam_id is not None and self.steam_id != "":
            return self.steam_id
        return None

@receiver(post_save, sender=MyUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class TeamNotification(models.Model):
    team = models.ForeignKey(Team,default=None,null=True)
    user = models.ForeignKey(MyUser,default=None,null=True)

    def __str__(self):
        return self.team
    
