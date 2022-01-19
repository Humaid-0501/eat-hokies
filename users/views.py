from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from actions.models import Action
from django.contrib import messages
from django.contrib.auth import authenticate
from users.models import Details
# from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
# For rendering profile page
def profile(request, username):
    user1 = get_object_or_404(User, username=username)
    action = Action.objects.filter(user_id=user1.id).order_by('-created')
    return render(request,
                  "users/user/profile.html",
                  {"user": user1, "actions": action},
                  )

# For creating new users
def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('first-name')
        lastname = request.POST.get('last-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
        messages.add_message(request, messages.SUCCESS, "You successfully registered with username: %s" % user.username)
        if user is not None:
            request.session['username'] = user.username
            request.session['role'] = user.details.role
            messages.add_message(request, messages.SUCCESS, "You have logged in successfully")

        return redirect('eatHokies:dining_home')
    else:
        return render(request,
                      "users/user/register.html",
                      )

# For handling login and creating sessions.
def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        request.session['username'] = username
        request.session['role'] = user.details.role
        messages.add_message(request, messages.SUCCESS, "You have logged in successfully")
        return redirect('eatHokies:dining_home')
    else:
        messages.add_message(request, messages.ERROR, "Invalid username or password")
    return redirect('eatHokies:dining_home')

def login_page(request):
    return render(request, 'eatHokies/dining_list/logIn.html')

# For logging out and deleting associated session.
def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect('eatHokies:dining_home')

# controller to navigate to the edit item view
def profile_edit(request, username):
    all_users = User.objects.all()
    if "username" in request.session:
        for user in all_users:
            if user.username == username:
                break
        return render(request, "users/user/profile_edit.html", {"user_list": user})

    else:
        return redirect('eatHokies:profile', username)

# controller to edit detail of a user
def edit_detail(request, username):

    user = User.objects.get(username=username)
    admin = User.objects.get(username=request.session.get('username'))
    if request.method == 'POST':
        _firstname = request.POST.get("firstname")
        _lastname = request.POST.get("lastname")
        _email = request.POST.get("email")
        _gender = request.POST.get("gender")
        _password = request.POST.get("password")
        _profile_pic = request.POST.get("profile-picture")

        role = user.details.role

        if request.session['role'] == "admin":
            _role = request.POST.get("role")
            user.details.role = _role

        if _profile_pic != "":
            user.details.profile_pic = "img/" + _profile_pic
        if _password:
            user.set_password(_password)

        user.first_name = _firstname
        user.last_name = _lastname
        user.email = _email
        user.details.gender = _gender

        user.save()
        userID = User.objects.get(username=username).id
        userDetail = Details.objects.get(user_id=userID)
        if request.session['role'] == "admin" and role != _role:
            # log the edit action.
            action = Action(
                user=admin,
                verb="changed the user role to "+_role+" for ",
                target=userDetail
            )
            action.save()

        messages.add_message(request, messages.INFO,
                             "You have successfully edited your information")

        return redirect('users:profile', user.username)
    else:
        return redirect('users:profile', user.username)