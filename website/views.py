from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm,CustomEmailForm,MobileNumberForm
from .models import Record 


import calendar
from datetime import datetime


def home(request):
    records = Record.objects.all()  # Retrieve all records from the database
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    return render(request, 'home.html', {'records': records})



def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})



def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                if add_record:
                    messages.success(request, "Record Added Successfully.")
                    return redirect('home')
                else:
                    messages.error(request, "Failed to add the record.")
            else:
                # Print form errors for debugging
                print(form.errors.as_json())  # Print JSON format of errors
                messages.error(request, "There was an error adding the record. Please check the form.")
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "You Must Be Logged In.")
        return redirect('home')




def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
	

def email_view(request):
    if request.method == 'POST':
        form = CustomEmailForm(request.POST)
        if form.is_valid():
            # Process the data
            return  redirect("Valid email")
    else:
        form = CustomEmailForm()
    return render(request, 'add_record.html', {'form': form})


def mobile_number_view(request):
    if request.method == 'POST':
        form = MobileNumberForm(request.POST) 
        if form.is_valid():
            # Process the data
            return redirect("Valid mobile number")
    else:
        form = MobileNumberForm() 
    return render(request, 'add_record.html', {'form': form})




def calendar_view(request):
    # Get the current date
    current_date = datetime.now()
    
    # Get year and month from request parameters, or use current year and month
    year = request.GET.get('year', current_date.year)
    month = request.GET.get('month', current_date.month)
    
    # Ensure year and month are integers
    year = int(year)
    month = int(month)

    # Generate the calendar data
    cal = calendar.monthcalendar(year, month)

    # Pass the calendar data and current date to the template
    context = {
        'calendar': cal,
        'current_date': current_date.day if year == current_date.year and month == current_date.month else None,
        'year': year,
        'month': month,
        'range': range(1, 13)  # Range for months (1 to 12)
    }
    return render(request, 'calendar.html', context)












# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import random
# from twilio.rest import Client

# @csrf_exempt
# def generate_otp(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         phone = data.get('phone')
#         user_otp = data.get('otp')

#         if phone and user_otp:
#             # Get the OTP stored in the session
#             otp_in_session = request.session.get('otp')
#             if otp_in_session and str(user_otp) == str(otp_in_session):  # Convert to string for comparison
#                 # Clear OTP from session after successful verification
#                 del request.session['otp']
#                 return JsonResponse({'success': True, 'message': 'OTP verified successfully'})
#             else:
#                 return JsonResponse({'success': False, 'message': 'Invalid OTP'})
        
#         # Generate OTP if phone number provided
#         elif phone:
#             otp = random.randint(100000, 999999)
#             # Send OTP via SMS
#             account_sid = 'ACdd090fa24997a0da0ab9679eb548193a'
#             auth_token = '359c14279c3e054e95a119af95bb13ac'
#             client = Client(account_sid, auth_token)
#             message = client.messages.create(
#                 from_='+17083406167',
#                 body=f'Your OTP is {otp}',
#                 to=phone
#             )
#             # Store OTP in the session
#             request.session['otp'] = otp
#             return JsonResponse({'success': True, 'message': 'OTP sent successfully'})

#     return JsonResponse({'success': False, 'message': 'Invalid request'})






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from twilio.rest import Client

@csrf_exempt
def generate_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')
        user_otp = data.get('otp')

        if phone and user_otp:
            # Get the OTP stored in the session
            otp_in_session = request.session.get('otp')
            if otp_in_session and str(user_otp) == str(otp_in_session):  # Convert to string for comparison
                # Clear OTP from session after successful verification
                del request.session['otp']
                return JsonResponse({'success': True, 'message': 'OTP verified successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid OTP'})
        
        # Generate OTP if phone number provided
        elif phone:
            otp = random.randint(100000, 999999)
            # Send OTP via SMS
            account_sid = 'ACdd090fa24997a0da0ab9679eb548193a'
            auth_token = '359c14279c3e054e95a119af95bb13ac'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_='+17083406167',
                body=f'Your OTP is {otp}',
                to=phone
            )
            # Store OTP in the session
            request.session['otp'] = otp
            return JsonResponse({'success': True, 'message': 'OTP sent successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})







