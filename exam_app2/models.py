from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) < 2:
            errors['name'] = "Name should be at least 2 characters."
        if len(postData['email']) < 1:
            errors["email"] = "Email required for registration."
        existingUsers = User.objects.filter(email = postData['email'])
        if len(existingUsers) != 0:
            errors["try_again"] = "Email already registered.  Please login."
        if not EMAIL_REGEX.match(postData['email']):
            errors['format'] = "Please enter valid email address."
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confpw']:
            errors["confpw"] = "Password must match"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['email'] = "Email is required for login."
        else:
            userArray = User.objects.filter(email = postData['email'])
        if len(userArray) == 0:
            errors['email'] = "Email not found.  Please register."
        else:
            thisUser = userArray[0]
            if not bcrypt.checkpw(postData['password'].encode(), thisUser.password.encode()):
                errors['password'] = "Password not valid.  Please try again."
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) < 2:
            errors['author'] = "Quote author should consist of at least 2 characters."
        if len(postData['content']) < 10:
            errors['content'] = "Quote should consist of at least 10 characters."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    contributor = models.ForeignKey(User, related_name="contributions", on_delete=models.PROTECT)
    author = models.CharField(max_length = 255)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()