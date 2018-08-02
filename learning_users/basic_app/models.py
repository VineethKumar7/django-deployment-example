from django.db import models
#imoporting basic user models in admin page
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model): # This is the model class for additional information, that the default user does't have.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #additional
    portfolio_site = models.URLField(blank = True)#blank = True means that there will be no error If we don't fill this field out.
    profile_pic = models.ImageField(upload_to='profile_pics',blank = True) # profile_pic is need to be the media subfolder. So make sure to create one.
    def __str__(self):
        return self.user.username #Where the username is the default attribute of the User we have imported. here we use user bez its OneToOneField of User.
#make sure the pillow is installed so $pip install pillow , in virenv
