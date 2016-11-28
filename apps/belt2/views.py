from django.shortcuts import render, redirect

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.

###############################  Index definition  ###############################
##################################################################################

def index(request):
	return render(request, 'belt2/index.html')


###############################  Login definition  ###############################
##################################################################################
def login(request):
	if request.method == 'POST':

	# Check whether user is in database
		users = User.usrMgr.filter(email=request.POST['email'])

	# If user is not in database, show message to register
		if not users and len(request.POST['email']) != 0:
			messages.add_message(request, messages.ERROR, 'User is not in database -- Please register', extra_tags='login')
			return redirect('/')
	
	# If user is in database, proceed to login
		else:
			log_in = User.usrMgr.login(request.POST)

		# Passed validation:
			if log_in[0] == True:
				request.session['id'] = log_in[1]
				request.session['status'] = 'logged_in'
				return redirect('/friends')

		## Failed validation:
			else:
				error_login = log_in[1]
				for i in range (len(error_login)):
					messages.add_message(request, messages.ERROR, 
						error_login[i], extra_tags='login')
				return redirect('/')
	else:
		return redirect('/')		


#############################  Register definition  ##############################
##################################################################################

def register(request):
	if request.method == 'POST':

	# Check to see if the user already exists
		users = User.usrMgr.filter(email=request.POST['email'])
		if users:
			messages.add_message(request, messages.ERROR, 'User already exists -- Please log in', extra_tags='registration')
			return redirect('/')

	# Passed non-existence check
		else:
			reg = User.usrMgr.register(request.POST)

		# Passed validation:
			if reg[0] == True:
				request.session['id'] = reg[1]
				request.session['status'] = 'registered'
				return redirect('/friends')

		# Failed validation:
			else:
				error_reg = reg[1]
				for i in range (len(error_reg)):
					messages.add_message(request, messages.ERROR, 
						error_reg[i], extra_tags='registration')
				return redirect('/')
	else:
		return redirect('/')


#############################  Dashboard definition  #############################
##################################################################################

def friends(request):
# Get user and item information
	user = User.usrMgr.filter(id=request.session['id'])
	this_user = user[0]
	user_friends = User.usrMgr.filter(friends=this_user)
	all_users = User.usrMgr.exclude(friends=this_user).exclude(name=this_user.name)

	print user[0].name
	print all_users
	print user_friends

# Define context
	context = {
		'user': user[0], 
		'user_friends': user_friends,
		'all_users': all_users
		}
	return render(request, 'belt2/friends.html', context)


####################  Add existing user to friends definition  ###################
##################################################################################

def addFriend(request, id):

# Get user and friend information
	user = User.usrMgr.filter(id=request.session['id'])
	friend = User.usrMgr.filter(id=id)

# Add friend to user
	added_friend = User.usrMgr.addFriend(user, friend)	
	return redirect('/friends')


##############################  View user definition  ############################
##################################################################################

def user(request, id):
## Get user information
	user = User.usrMgr.filter(id=id)
	this_user = user[0]

## Define the context
	context = {'this_user': this_user}
	return render(request, 'belt2/user.html', context)


#############################  Remove friend definition  ###########################
##################################################################################

def remove(request, id):

# Get item and user information
	user = User.usrMgr.filter(id=request.session['id'])
	friend = User.usrMgr.filter(id=id)

# Remove user from item
	removed_friend = User.usrMgr.removeFriend(user, friend)
	return redirect('/friends')


###############################  Logout definition  ##############################
##################################################################################

def logout(request):
	request.session.pop('id')
	return redirect('/')

