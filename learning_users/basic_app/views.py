from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
#If you ever want a view to require a user to be logged in you can decorate it with login_required
from django.contrib.auth.decorators import login_required
#To make it more simple we use HttpResponce in place of render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')
@login_required
def user_logout(request):
    #we are going to use the built in logout function
    #We want to make sure that the user logged in is logged out. For specificity only the code inside this function is not enough.
    #The present code inside the function is that it doesn't require a user to be logged in inoder to logout, this causes issues with page.
    #All you do is decorate it with login_requred before the function and after @. This ensures any view that requires user to login to see it.
    logout(request)
    return HttpResponseRedirect(reverse('index'))
@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")
def register(request):
    # We are going to depend on this variable to say some one is registered or not
    registered =False
    if request.method == 'POST':
        # We are going to get information from both of the forms.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # This is generally hashing the password. This goes into the settings.py file and sets it as the hash
            user.set_password(user.password)
            user.save()# We save the hash pasword to the database.
            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)
            # If we commit it may show collition which overrides the user
            profile.user = user # That setup's the one to one relations ship, Just compare the views.py models.py and forms.py files to know the relationship.
            # Then we are checking that if they actually providing the profile picture.
            if 'profile_pic' in request.FILES:
                #This is bascially the dictiony of all the files they have uploaded
                profile.profile_pic = request.FILES['profile_pics']#This is basically the dictionary of all the files they uploaded in the request.
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})
def user_login(request):
    if request.method == 'POST':
        #the  reason we used .get('username') bez over in login.html file we named username input as name = "username"
        username = request.POST.get('username')
        password = request.POST.get('password')
        #Then  we are going to use django build in authentication function.
        user = authenticate(username = username, password=password)# Type in parameters are equal to in this case . It's the standard way of doing.i.e username =
        if user:
            if user.is_active:#To check the account is active or blocked
                #To use the build in django functions.
                login(request,user)
                #After login we return it may be profile page or home page etc.
                #Is going to redirect they login and successful and their account is active then reverse them redirect back to homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request, 'basic_app/login.html',{})
