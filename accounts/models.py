from django.db import models
from django.conf import UserSettingsHolder, settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import MaxValueValidator, MinValueValidator
 


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, userID, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
 
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            username = username,
            userID = userID,
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email,username, userID, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            username=username,
            userID=userID,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
 
 
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=200,default='こすこす')
    userID = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)],unique=True,default=0)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
 
    objects = MyUserManager()
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth','username','userID']
 
    def __str__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
 
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
 
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class StudentImage(models.Model):
    userID = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)],default=0)
    username = models.CharField(max_length=200,default='こすこす')
    published_date = models.DateTimeField(default=timezone.now)
    image = models.TextField()
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.username

class StudentStudyLog(models.Model):
    userID = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)],default=0)
    username = models.CharField(max_length=200,default='こすこす')
    goal_start = models.CharField(max_length=200,default='0000/00/00')
    goal_end = models.CharField(max_length=200,default='0000/00/00')
    study_time = models.IntegerField(default=0)
    sum_study_time = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class ThisWeekStudyTime(models.Model):
    userID = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)],default=0)
    username = models.CharField(max_length=200,default='こすこす')
    published_date = models.DateTimeField(default=timezone.now)
    weekly_study_time = models.BigIntegerField(default=0)
    week_name = models.CharField(max_length=200,default='2021/5/31~2021/6/7')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.username + ' : ' + self.week_name

class StudentVideo(models.Model):
    userID = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)],default=0)
    username = models.CharField(max_length=200,default='こすこす')
    published_date = models.DateTimeField(default=timezone.now)
    videoPath = models.TextField(default='default')
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.username + str(self.userID)


