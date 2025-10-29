from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name, username,email,password=None): # this is for creating the user  User can create an account without password temporarily But later password must be set Django will not crash if password is not given initially summarizze this line

        if not email:
            raise ValueError('user must have an email address')
        
        if not username:
            raise ValueError('user must have an username')

        user=self.model(                     #points to your custom User model
            email=self.normalize_email(email),  # noremaile email converts email into proper format hello@gmail.com
            username=username,
            first_name=first_name,
            last_name=last_name,

        )

        user.set_password(password)     #This will convert password into hashed form (Password will NOT store as plain text — security!)
        user.save(using=self._db)         #After saving → return newly created user
        return user
    
# create the superuser
    def create_superuser(self,first_name,last_name,username,email,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
         )
        # permissions
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user


# we create the custom use model
# in this we login through the email not the user name 

class Account(AbstractBaseUser):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=50)
    
    
    
    #You are creating your own fields instead of Django’s default ones.

# required this fiedls are the mendatory when we createe the custom useer model

    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
# in this we login through the email not the user name 
    USERNAME_FIELD='email'         #Email will be used to log in (not username).
    REQUIRED_FIELDS=['username','first_name','last_name']    #Extra required info when creating superuser

    objects=MyAccountManager()           #Tells Django to use your create_user and create_superuser functions.
    

    def __str__(self):            #instead of showing this It will show this: someone@gmail.com
        return self.email
    #Allows admin panel access Django needs these functions to check permissions
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True