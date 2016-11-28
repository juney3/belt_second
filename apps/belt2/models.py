from __future__ import unicode_literals

from django.db import models


# Create your models here.

import re, bcrypt, datetime


## Validation regexes
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z\s]*$')
PW_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')


# Create your models here.


############################  UserManager definition  ############################
##################################################################################  

class UserManager(models.Manager):

##################  Registration definition  ##################  
## Creates a new user and logs the user in

	def register(self, post):
		reg_errors=[]

	## First and last name validation
	## Check for name length and whether alpha only

		if len(post['name']) <= 2:
			reg_errors.append('Name must be longer than 2 characters')
		elif not NAME_REGEX.match(post['name']):
			reg_errors.append('Name must be alphabetical characters only')

		if len(post['alias']) <= 2:
			reg_errors.append('Alias must be longer than 2 characters')

	## Email validation
	## Check for empty email field, check whether email is in valid format
		
		if len(post['email']) == 0:
			reg_errors.append('Email field cannot be empty')
		elif not EMAIL_REGEX.match(post['email']):
			reg_errors.append('Email address is not valid')


	## Password validation
	## Check for password length and whether pw confirmation matches
		if len(post['password']) < 8:
			reg_errors.append('Password must be 8 characters or longer')
		elif post['password'] != post['confirm']:
			reg_errors.append('Passwords do not match')

	## Birth date validation -- Birth date must be before today
	## Convert form data to datetime.datetime.date() object and compare to current date
		if not post['birth_date']:
			reg_errors.append('Please enter a date of birth')
		elif datetime.datetime.strptime(post['birth_date'], '%Y-%m-%d').date() > datetime.datetime.now().date():
			reg_errors.append('Date of birth must be before today')


	## If validation errors, return error messages to view
		if len(reg_errors) != 0:
			return(False, reg_errors)


	## If success, hash pw, create user, and return user to view
		else: 
			pw_str = str(post['password'])
			hashed = bcrypt.hashpw(pw_str, bcrypt.gensalt())
			user = User.usrMgr.create(
				name=post['name'], 
				alias=post['alias'],
				email=post['email'],
				password=hashed,
				birth_date=post['birth_date']
				)
			users = User.usrMgr.filter(email=post['email'])
			user_id = users[0].id
			return (True, user_id)


##################  Login definition  ##################  
## Logs in an existing user

	def login(self, post):
		log_errors = []

		user = User.usrMgr.filter(email=post['email'])

	## Validate email 
		if len(post['email']) == 0:
			log_errors.append('Email field cannot be empty')
		elif not EMAIL_REGEX.match(post['email']):
			log_errors.append('Email address is not valid')
		

	## Validate password
		if len(post['password']) == 0:
			log_errors.append('Password field cannot be empty')
		elif bcrypt.hashpw(str(post['password']), str(user[0].password)) != user[0].password:
			log_errors.append('Password is not correct')

	## If validation errors, return error messages to view
		if len(log_errors) != 0:
			return(False, log_errors)


	## If user passes validation, log user in
		else: 
			user_id = user[0].id
			return (True, user_id)


##################  Add friend definition  ##################  
## Adds a friend to a user's friend list

	def addFriend(self, user, friend):
	## Get user and friend information
		user = user[0]
		friend = friend[0]

	## Add user to item
		added_friend = friend.friends.add(user)
		return added_friend		


##################  Remove friend definition  ##################
## Removes a friend from a user's friend list  

	def removeFriend(self, user, friend):
	## Get user and friend information
		user = user[0]
		friend = friend[0]

	## Remove friend from user
		removed_friend = friend.friends.remove(user)
		return removed_friend	


###############################  Model definitions  ##############################
################################################################################## 

## Database models

class User(models.Model):
	name = models.CharField(max_length=50)
	alias = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	friends = models.ManyToManyField('self', related_name='friends')
	password = models.CharField(max_length=50)
	birth_date = models.DateField(auto_now=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	usrMgr = UserManager()




