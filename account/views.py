from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
User = CustomUser

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash


# Create your views here.


def Account(request):
    return HttpResponse("Account")


def Signup(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            phone_no = request.POST.get('phone')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if User.objects.filter(phone_no=phone_no).exists() or User.objects.filter(email=email).exists():
                messages.warning(request, "An account with this email or phone number already exists.")
                return redirect('/account/signup')

            if (password != confirm_password):
                messages.warning(request, "Passwords are not same")
                return redirect('/account/signup')
            
     
            user = User.objects.create_user(phone_no=phone_no, email=email, password=password)
            user.is_active = True
            user.is_verified= False
            user.save()
            user.generate_activation_token() 
            SendActivationMessage(request, user) #call the SendActivationMessage function
            messages.success(request, "Account created successfully. Please check your email to activate your account.")
            return redirect('/account/login')

    except Exception as e:
        # messages.error(request, "Something went wrong. Try again.")
                messages.error(request, f"Something went wrong. Try again. Error: {str(e)}")

    return render(request, 'account/signup.html')



#handel the user account activation process
def Activate(request, pk, key):
    user = CustomUser.objects.filter(pk=pk).first()
    try:
        if user and user.activation_token == key:
            # user.is_active = True
            user.is_verified  = True
            user.activation_token = ""
            user.save()
            login(request, user)
            messages.success(request, "Your account has been activated and you are now logged in.")
        else:
            messages.error(request, "Invalid activation link or account already activated.")
    except:
         messages.error(request, "Something went wrong. Try again.")
    return redirect('Index')



def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email = email, password = password)

        if user is not None:
            login(request, user)
            messages.success(request,"Login successful.")
            return redirect("/")
        else:
            messages.error(request, 'You does not have an account or incorrect passwrd.')
            return redirect('/account/login')
        
    return render(request, 'account/login.html')



#login the existing account
# def Login(request):
#     try:
#         if request.method == 'POST':
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             user = authenticate(email = email, password = password)

#             if user is not None:
#                 login(request, user)
#                 if user.is_verified:
#                     messages.success(request,"Login successful.")
#                     return redirect("/")
#                 else:
#                     messages.error(request, "Your account is not verified. Verify your account.")
#                     return redirect('/account/login')

#             else:
#                 messages.error(request, 'You does not have an account or incorrect.')
#                 return redirect('/account/login')

#     except Exception as e:
#         messages.error(request, "Something went wrong. Try again.")
#         return redirect('/account/signup')

#     return render(request, 'account/login.html')


#hendle user profile page
@login_required(login_url="/account/login")
def Profile(request):
    user_data = request.user
    params = {'user_data': user_data}
    return render(request, 'account/profile.html', params)


#logout route 
@login_required(login_url="/account/login")
def Logout(request):
    logout(request)
    return redirect("/")


#handle the foget password page and take the email as an input
def ForgetPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            SendPasswordResetEmail(request, user)
            messages.success(request, "Password reset link has been sent to your email.")

        else:
            messages.error(request, "No account found with this email.")

    return render(request, 'account/forget-password.html')




# handle teh Password Reset Confirm View. after clik on reset link this function will be hanle every thing like update the old assword with new password
def PasswordResetConfirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    
    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # Keeps the user logged in after password change
                messages.success(request, "Password has been reset successfully.")
                return redirect('/account/login')
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, 'account/reset-password.html')
    else:
        messages.error(request, "Invalid reset link.")
        return redirect('/account/forget-password')




#send activation link to the user. this is the notmal function. There is no connection with url. this function use when we wan to send email to the user. Thi is only responsible for creating the activation link. 
def SendActivationMessage(request, user):
    try:
        current_site = get_current_site(request) #get current site
        domain = current_site.domain 
        mail_subject = "Please activate your account"
        urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f'{domain}/account/activate/{user.pk}/{user.activation_token}'
        message= f" Click On This Link & Verify Your Account First For Get Full Accesss - {verification_url}"
        send_mail(mail_subject, message, 'arpanbera1212@gmail.com', [user.email], fail_silently=False)

    except Exception as e:
         messages.error(request, "Something went wrong. Try again.")
         return redirect('/account/signup')



# Send Password Reset Email.  this is the notmal function. There is no connection with url. this function use when we wan to send email to the user. This is only responsible for generate the Send Password Reset Email 
def SendPasswordResetEmail(request, user):
    try:
        current_site = get_current_site(request)
        domain = current_site.domain
        mail_subject = 'Reset your password'
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f'http://{domain}/account/reset-password/{uid}/{token}/'
        message = f"Click the link below to reset your password:\n\n{reset_link}"
        send_mail(mail_subject, message, 'no-reply@example.com', [user.email], fail_silently=False)
    except Exception as e:
        messages.error(request, "Something went wrong. Try again.")
        return redirect('/account/forget-password')
    


