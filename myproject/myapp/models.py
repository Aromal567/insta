from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=15)
    password=models.CharField(max_length=15)
    user_type=models.CharField(max_length=15)

    def _str_(self):
        return self.username
    

class User(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=20)    
    lastname=models.CharField(max_length=20)    
    email=models.CharField(max_length=20)    
    phone=models.CharField(max_length=20)
    image=models.ImageField(upload_to="gallery")
    
    def __str__(self):
        return self.firstname 


class Post(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="gallery")
    date_time = models.DateTimeField(auto_now=True)
    description=models.CharField(max_length=20)
    like_count=models.IntegerField(default=0)

    def __str__(self):
        return self.description




class Reel(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    video = models.FileField(upload_to="reels")
    caption = models.CharField(max_length=100)
    like_count=models.IntegerField(default=0)


    def __str__(self):
        return self.caption
    



class Likes(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    POST=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.USER
    

class Rlike(models.Model):
    REEL=models.ForeignKey(Reel,on_delete=models.CASCADE)    
    USER=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.REEL
     
class Rcomment(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now=True)
    REEL=models.ForeignKey(Reel,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class Comments(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    comment=models.CharField(max_length=200)
    POST=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment



class Friends(models.Model):
    USER_1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user1')
    USER_2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user2')
    status=models.CharField(max_length=30)

    def __str__(self):
        return self.status
    

class Message(models.Model):
    Sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender',null=True)
    Reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciever',null=True)
    date_time = models.DateTimeField(auto_now=True)
    message=models.CharField(max_length=100)

    def __str__(self):
        return self.message




