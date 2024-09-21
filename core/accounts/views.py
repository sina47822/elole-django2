from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import AuthenticationForm,UserCreationForm_Phone
from accounts.models import User

from kavenegarapp.models import OTPRequest

from django.contrib import messages  # To display feedback messages

class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
    
class LogoutView(auth_views.LogoutView):
    pass

def RegisterView(request):
    if request.method == 'POST':
        form = UserCreationForm_Phone(request.POST)

        if  form.is_valid():
            # Save the form data without committing to trigger OTP verification
            request.session['user_data'] = form.cleaned_data
            
            # Generate and store the OTP request_id in the session
            otp_request = OTPRequest.objects.generate({'channel': 'phone', 'receiver': form.cleaned_data['phone_number']})
            request.session['otp_request_id'] = str(otp_request.request_id)
            
            return redirect('accounts:verify_otp')
    else:
        form = UserCreationForm_Phone()

    return render(request, "accounts/sign-up.html", {'form':form})

def VerifyOTPView(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        phone_number = request.session.get('user_data').get('phone_number')
        request_id = request.session.get('otp_request_id')  # Retrieve request_id from the form or session

        if OTPRequest.objects.is_valid(phone_number,request_id, otp):
            user_data = request.session.get('user_data')
            # Create the user now after OTP verification
            user = User.objects.create(
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                phone_number=user_data.get('phone_number'),
            )
            user.set_password(user_data.get('password'))
            user.save()
            

            # Clear session data
            del request.session['user_data']
            del request.session['otp_request_id']
            messages.success(request, 'User has been created and verified successfully!')
            return redirect('accounts:login')  # Redirect to login after success
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'accounts/verify_otp.html')