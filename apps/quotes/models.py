
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Managers
class UserManager(models.Manager):

    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 or len(postData['alias']) < 2:
            errors['name_error'] = "Name and Alias must be 2 or more characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
            errors['pass_length'] = "Password must be 8 or more characters"
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Passwords must match"
        if User.objects.filter(email=postData['email']):
            errors['exists'] = "Email already taken"
        return errors

    def login(self, postData):
        errors = {}
        user_to_check = User.objects.filter(email=postData['email'])
        if len(user_to_check) > 0:
            user_to_check = user_to_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_to_check.password.encode()):
                user = {"user" : user_to_check}
                return user
            else:
                errors = { "error": "Login Invalid" }
                return errors
        else:
            errors = { "error": "Login Invalid" }
            return errors

class QuoteManager(models.Manager):

    def quote_validator(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 4:
            errors['quoted_by_error'] = "Quoted by must be more than 3 characters"
        if len(postData['desc']) < 11:
            errors['message_error'] = "Message must be more than 10 characters"
        return errors

    def create_quote(self, postData, user_id):
        new_quote = Quote.objects.create(quoted_by=postData['quoted_by'],desc=postData['desc'],posted_by=User.objects.get(id=user_id))
        return new_quote



# Models
class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "User object: Name = {}, alias = {}, email = {}".format(self.name,self.alias,self.email)

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="posted_quotes")
    favorites = models.ForeignKey(User, related_name="favorite_quotes", null=True)

    objects = QuoteManager()

    def __repr__(self):
            return "User object: quoted_by = {}, desc = {}".format(self.quoted_by,self.desc)
