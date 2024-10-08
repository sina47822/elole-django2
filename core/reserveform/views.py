from django.shortcuts import HttpResponse, get_object_or_404, redirect,render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.utils.dateformat import DateFormat

from accounts.models import User,UserType
from django.views.generic.edit import FormView
from stylist.models import Stylist,Services,ServiceCategoryModel,WorkHour,WorkDay
# from reserveform.utils import get_available_hours

from django.conf import settings
from kavenegarapp.sender import send_telegram_message  # This will be used for sending SMS notifications

from reserveform.models import ReserveFormModel
from reserveform.forms import ReservationForm,ReservationForm2,ReservationForm3,ReservationForm4,ReservationForm5,ReservationForm6

from kavenegar import *
from django.contrib import messages

from django.http import JsonResponse

class ReserveFormView(FormView):
    template_name = "formreserve/reserve-form.html"
    form_class = ReservationForm
    

    login_url = 'accounts:login'  # Update this to the correct login URL
    
    def get_context_data(self, **kwargs):
        context = super(ReserveFormView, self).get_context_data(**kwargs)
        
        # Get all service categories
        categories = ServiceCategoryModel.objects.all()
        context['categories'] = categories
        
        # Retrieve selected steps from session data if available
        session_data = self.request.session.get('reservation_data', {})

        return context
    
    def post(self, request, *args, **kwargs):
        # Handle AJAX requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            category_id = request.POST.get('category')
            service_id = request.POST.get('service')
            admin_id = request.POST.get('admin')
            workday = request.POST.get('workday')

            if category_id:
                services = Services.objects.filter(category__id=category_id)
                return JsonResponse({
                        'success': True,  # Set this based on your logic
                        'redirect_url': 'reserveform:services'  # The URL you want to redirect to
                    })

            if service_id:
                selected_service = Services.objects.get(id=service_id)
                admins = selected_service.stylist.filter(user__type=UserType.admin.value)
                admins_options = "".join([f'<option value="{a.id}">{a.user.user_profile.first_name}</option>' for a in admins])
                return JsonResponse({'admins': admins_options})

            if admin_id:
                workdays = WorkDay.objects.filter(stylist__id=admin_id)
                workdays_options = "".join([f'<option value="{wd.id}">{wd.day}</option>' for wd in workdays])
                return JsonResponse({'workdays': workdays_options})

            if workday:
                times = WorkDay.objects.get(day=workday).hour.all()
                times_options = "".join([f'<option value="{t.id}">{t}</option>' for t in times])
                return JsonResponse({'times': times_options})

        return super().post(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated before proceeding
        if not request.user.is_authenticated:
            # Redirect to the login page if the user is not logged in
            return redirect(f"{reverse('accounts:login')}?next={request.path}")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Handle form submission
        selected_service_id = self.request.POST.get('service')
        selected_admin_id = self.request.POST.get('admin')
        selected_workday = self.request.POST.get('workday')
        selected_time_id = self.request.POST.get('time')

        # Store all selections in the session
        reservation_data = {
            'category': self.request.POST.get('category'),
            'service': selected_service_id,
            'admin': selected_admin_id,
            'workday': selected_workday,
            'time': selected_time_id
        }
        self.request.session['reservation_data'] = reservation_data

        # Ensure session is saved by marking it as modified
        self.request.session.modified = True

        # Debug to see if session is being set
        print("Session Data:", self.request.session.get('reservation_data'))

        # Ensure session data is saved
        return redirect(reverse('reserveform:reservation_confirm'))
    
    def get(self, request, *args, **kwargs):
        # Check if the user was redirected from the login/signup page after session data was stored
        if request.user.is_authenticated and 'reservation_data' in request.session:
            return self.process_reservation()
        return super().get(request, *args, **kwargs)
    
    def process_reservation(self):
        # Retrieve the reservation data from the session
        reservation_data = self.request.session.get('reservation_data')

        # Create the reservation if the session data exists
        if reservation_data:
            try:
                form_instance = ReserveFormModel(
                    customer=self.request.user,
                    service_category=get_object_or_404(ServiceCategoryModel, id=reservation_data['category']),
                    service=get_object_or_404(Services, id=reservation_data['service']),
                    stylist=get_object_or_404(User, id=reservation_data['admin']),
                    day=get_object_or_404(WorkDay, id=reservation_data['workday']),
                    hour=get_object_or_404(WorkHour, id=reservation_data['time']),
                )
                form_instance.save()
                # Clear the session data after reservation is complete

                print(self.request.session.__dict__)
                print(self.request.session.get("reservation_data"))
                # Send SMS Notifications
                self.send_sms_notification(form_instance)
                
                # Prepare Telegram message
                message = f"New Reservation:\n" \
                          f"Category: {form_instance.service_category.name}\n" \
                          f"Service: {form_instance.service.name}\n" \
                          f"Stylist: {form_instance.stylist.username}\n" \
                          f"Day: {form_instance.day.name}\n" \
                          f"Time: {form_instance.hour.time}."
                
                # Send Telegram message
                send_telegram_message(message)

                # Redirect to success page
                messages.success(self.request, 'Your reservation was successful!')
                return redirect(reverse('reserveform:reservation_success'))

            except Exception as e:
                messages.error(self.request, f"An error occurred while processing your reservation: {str(e)}")
                return redirect(reverse('reserveform:reservation_failed'))

        # If no session data or other error occurs
        messages.error(self.request, 'There was an issue with your reservation. Please try again.')
        return redirect(reverse('reserveform:reservation_failed'))
    
class ReservationConfirmView(FormView):
    template_name = "formreserve/reserve-confirm.html"
    form_class = ReservationForm

    def get_context_data(self, **kwargs):
        context = super(ReservationConfirmView, self).get_context_data(**kwargs)
        reservation_data = self.request.session.get('reservation_data')

        if reservation_data:
            # Fetch the actual objects based on session data for preview
            context['category'] = get_object_or_404(ServiceCategoryModel, id=reservation_data['category'])
            context['service'] = get_object_or_404(Services, id=reservation_data['service'])
            context['stylist'] = get_object_or_404(User, id=reservation_data['admin'])
            context['workday'] = get_object_or_404(WorkDay, id=reservation_data['workday'])
            context['time'] = get_object_or_404(WorkHour, id=reservation_data['time'])
        
        return context

    def form_valid(self, form):
        # Process the reservation
        return self.process_reservation()

    def process_reservation(self):
        return ReserveFormView().process_reservation(self)

import logging

logger = logging.getLogger(__name__)

def reservation_form_category(request):
    if request.method == 'POST' and  request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            logger.info(f"Received data: {request.POST}")  # Log the received data
            form = ReservationForm3(request.POST)
            if form.is_valid():
                # Save form data to session
                category_instance = form.cleaned_data['service_category']
                request.session['service_category'] = category_instance.id  # Store just the ID
                logger.info(f"Category set in session: {request.session['service_category']}")


                # Return success response with redirect URL
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/reserveform/services/',  # Adjust the URL as needed
                    'session_data': request.session['service_category']
                })
                
            else:
                logger.error(f"Form errors: {form.errors}")  # Log the form errors
                # Return error response
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            logger.exception("An error occurred while processing the request.")
            return JsonResponse({'success': False, 'message': str(e)})

    # Handle GET request to render the form
    categories = ServiceCategoryModel.objects.all()
    form = ReservationForm3()  # Initialize the form
    category_id = request.session.get('service_category')
    return render(request, 'formreserve/forms/category.html', {'form': form, 'categories': categories, 'category_id':category_id})

def reservation_form_service(request):
    if request.method == 'POST' and  request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            logger.info(f"Received data: {request.POST}")  # Log the received data
            form = ReservationForm4(request.POST)
            if form.is_valid():
                # Save form data to session
                service_instance = form.cleaned_data['service']
                request.session['service'] = service_instance.id  # Store just the ID
                logger.info(f"Service set in session: {request.session['service']}")


                # Return success response with redirect URL
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/reserveform/stylist/',  # Adjust the URL as needed
                    'session_data': request.session['service']
                })
                
            else:
                logger.error(f"Form errors: {form.errors}")  # Log the form errors
                # Return error response
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            logger.exception("An error occurred while processing the request.")
            return JsonResponse({'success': False, 'message': str(e)})

    # Handle GET request to render the form
    category_id = request.session.get('service_category')
    services = Services.objects.filter(category__id=category_id)
    service_id = request.session.get('service')
    form = ReservationForm4()  # Initialize the form
    return render(request, 'formreserve/forms/service.html', {'form': form, 'services': services, 'service_id':service_id})

def reservation_form_stylist(request):
    if request.method == 'POST' and  request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            logger.info(f"Received data: {request.POST}")  # Log the received data
            form = ReservationForm2(request.POST)
            if form.is_valid():
                # Save form data to session
                admin_instance = form.cleaned_data['stylist']
                request.session['stylist'] = admin_instance.id  # Store just the ID
                logger.info(f"stylist set in session: {request.session['stylist']}")


                # Return success response with redirect URL
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/reserveform/workday/',  # Adjust the URL as needed
                    'session_data': request.session['stylist']
                })
                
            else:
                logger.error(f"Form errors: {form.errors}")  # Log the form errors
                # Return error response
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            logger.exception("An error occurred while processing the request.")
            return JsonResponse({'success': False, 'message': str(e)})

    # Handle GET request to render the form
    service_id = request.session.get('service')  # Get service ID from session
    if not service_id:  # Check if service_id is None or not set
        service_id = 1  # Default value if not present
    selected_service = Services.objects.get(id=service_id)
    if not selected_service:  # Check if service_id is None or not set
        selected_service = 1  # Default value if not present
    admins = selected_service.stylist.filter(user__type=UserType.admin.value) 
    selected_admin_id = request.session.get('stylist')
    form = ReservationForm2()  # Initialize the form
    return render(request, 'formreserve/forms/stylist.html', {'form': form, 'admins': admins, 'selected_admin_id':selected_admin_id})

def reservation_form_workday(request):
    if request.method == 'POST' and  request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Get 'day' value directly from request.POST
            day = request.POST.get('day')
            
            if day:
                # Store 'day' in the session
                request.session['day'] = day

                # Retrieve and work with the stylist and workdays
                admin_id = request.session.get('stylist')
                selected_stylist = Stylist.objects.get(id=admin_id)

                # Retrieve available workdays for the selected stylist
                available_workdays = WorkDay.objects.filter(stylist=selected_stylist)
                available_workdays_list = [DateFormat(workday.day).format('Y-m-d') for workday in available_workdays]
                # Check if the selected day is in the available workdays
                if day not in available_workdays_list:
                    return JsonResponse({'success': False, 'message': "این روز قابل انتخاب نیست. لطفاً یک روز دیگر را انتخاب کنید."})

                # Return success response with redirect URL
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/reserveform/workhour/',  # Adjust the URL as needed
                    'session_data': request.session['day']
                })
                
            else:
                logger.error(f"Form errors: {form.errors}")  # Log the form errors
                # Return error response
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            logger.exception("An error occurred while processing the request.")
            return JsonResponse({'success': False, 'message': str(e)})

    # Handle GET request to render the form
    admin_id = request.session.get('stylist')
    selected_stylist = Stylist.objects.get(id=admin_id)

    available_workdays = WorkDay.objects.filter(stylist=selected_stylist)
    workdays_formatted = [
        DateFormat(workday.day).format('Y-m-d')  # Format the date as 'YYYY-MM-DD'
        for workday in available_workdays
    ]
    form = ReservationForm5()  # Initialize the form
    return render(request, 'formreserve/forms/workday.html', {
        'form': form,
        'workdays_formatted': workdays_formatted,        
        'selected_workday': request.session.get('day')
    })

def reservation_form_workhour(request):
    service_id = request.session.get('service')
    stylist_id = request.session.get('stylist')
    workday = request.session.get('day')

    service = Services.objects.get(id=service_id)
    service_duration = service.duration
    stylist = Stylist.objects.get(id=stylist_id)
    workday = WorkDay.objects.get(day=workday)
    available_times = []

    workhours = WorkHour.objects.filter(workday=workday)
    
    for wh in workhours:
        start = wh.from_hour
        end = wh.to_hour
        time_slot = start
        
        # Convert start and end to strings and format them to "HH" format (e.g., "09", "11")
        start_str = f"{start:02d}"  # Converts integer 9 to string "09"
        end_str = f"{end:02d}"  # Converts integer 11 to string "11"


        # Convert start and end to datetime objects
        start_time = datetime.combine(datetime.today(), datetime.strptime(start_str, "%H").time())
        end_time = datetime.combine(datetime.today(), datetime.strptime(end_str, "%H").time())

        # Initialize the time_slot with the start time
        time_slot = start_time
        while time_slot + timedelta(minutes=service_duration) <= end_time:
            is_available = True

            if is_available:
                available_times.append(time_slot)

            # محاسبه بازه زمانی بعدی بر اساس مدت زمان سرویس
            time_slot += timedelta(minutes=service_duration)

    if request.method == 'POST' and  request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            logger.info(f"Received data: {request.POST}")  # Log the received data
            form = ReservationForm6(request.POST)
            hour = request.POST.get('hour')
            request.session['hour'] = hour

            if form.is_valid():
                # Get 'hour' value directly from request.POST


                if hour:
                    # Store 'day' in the session
                    print(f"Day stored in session: {hour}")

                return JsonResponse({
                    'success': True,
                    'redirect_url': '/reserveform/review/',
                    'session_data': request.session['hour']
                })
                
        except Exception as e:
            logger.exception("An error occurred while processing the request.")
            return JsonResponse({'success': False, 'message': str(e)})
    
    form = ReservationForm6()  # Initialize the form
    return render(request, 'formreserve/forms/workhour.html', {'form': form, 'times': available_times,'service_duration':service_duration})

def reservation_form_review(request):
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            # Directly fetch form data from cleaned_data instead of session for these fields
            customer = form.cleaned_data.get('customer')
            stylist = form.cleaned_data.get('stylist')  # Assuming this is the selected stylist
            service = form.cleaned_data.get('service')
            service_category = form.cleaned_data.get('service_category')
            day = form.cleaned_data.get('day')
            hour = form.cleaned_data.get('hour')
            form.save()
            # Add a success message
            messages.success(request, 'Reservation submitted successfully!')

            # Prepare the message for Telegram or logging
            message = (
                f"New Reservation:\n"
                f"Category: {service_category.title}\n"
                f"Service: {service.name}\n"
                f"Stylist: {stylist.user.phone_number}\n"
                f"Day: {day}\n"
                f"Time: {hour}."
            )
            print(message)
            # Send Telegram message (if required)
            # send_telegram_message(message)  
            # Clear session data after the reservation is submitted successfully
            for key in ['service_category', 'service', 'stylist', 'day', 'hour']:
                if key in request.session:
                    del request.session[key]

            # Redirect to a confirmation page or home
            return redirect('website:home')
                # Send SMS Notifications (if required)
                # send_sms_notification(reservation)  # Assuming `send_sms_notification` is defined elsewhere
                
                # # Prepare Telegram message
                # Send Telegram message (if required)
                # send_telegram_message(message)  # Assuming `send_telegram_message` is defined elsewhere
            #     # Send success response
            #     messages.success(request, 'Your reservation was successful!')
                        
            #     return JsonResponse({
            #         'success': True,
            #         'redirect_url': '/reserveform/reserve-success/',  # Adjust the URL as needed
            #     })
            # else:
            #     return JsonResponse({'success': False, 'message': 'Missing reservation data.'})
        # Handle form errors for AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        else:
            # Return to the form with error messages for non-AJAX requests
            return render(request, 'formreserve/forms/review.html', {'form': form})
    else:
        # Prepare data for the review page (GET request)
        category_id = request.session.get('service_category')
        service_id = request.session.get('service')
        admin_id = request.session.get('stylist')
        workday = request.session.get('day')
        hour = request.session.get('hour')

        # Fetch the related objects
        if not category_id:
            selected_category = 'یک کتگوری انتخاب کنید'
        else:
            selected_category = ServiceCategoryModel.objects.get(id=category_id)
        if not service_id:
            selected_service = 'یک سرویس انتخاب کنید'
            service_duration = 10  # Default to zero in case no service is found
        else:
            selected_service = Services.objects.get(id=service_id)
            service_duration = selected_service.duration
        if not admin_id:
            selected_admin = 'یک استایلیست انتخاب کنید'
        else:
            if isinstance(selected_service, Services):
                selected_admin = selected_service.stylist.get(id=admin_id)
            else:
                selected_service = Services.objects.get(id=1)  # Fallback to a default service
                selected_admin = 'یک استایلیست انتخاب کنید'
        selected_workday = WorkDay.objects.get(day=workday) if workday else None
        selected_hour = hour if hour else None

        # Prepare the form for review
        customer = request.user
        form = ReservationForm(request.POST)

        # Ensure service_duration is passed to the template
        context = {
            'customer': customer,
            'category': selected_category,
            'service': selected_service,
            'admin': selected_admin,
            'day': selected_workday,
            'hour': selected_hour,
            'form': form,
            'service_duration': service_duration
        }

        return render(request, 'formreserve/forms/review.html', context)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, message, to_email):
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = 'sinaa.afshar@gmail.com'  # Replace with your email
    from_password = 'Sa8521301666'  # Replace with your password or app password

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(from_email, from_password)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)
    finally:
        server.quit()


def send_sms_notification(reservation):
    try:
        # Replace this with your Kavenegar API key from settings or hardcode it
        api_key = settings.KAVENEGAR_API_KEY
        api = KavenegarAPI(api_key)

        # Compose the SMS message
        message = (
            f"Dear {reservation.customer.phone_number},\n"
            f"Your reservation is confirmed!\n"
            f"Category: {reservation.service_category.name}\n"
            f"Service: {reservation.service.name}\n"
            f"Stylist: {reservation.stylist.username}\n"
            f"Date: {reservation.day.name}\n"
            f"Time: {reservation.hour.time}.\n"
            f"Thank you!"
        )

        # Use the customer's phone number for sending the SMS
        params = {
            'receptor': reservation.customer.phone_number,  # Assumes you have a phone_number field
            'message': message
        }

        # Send the SMS
        response = api.sms_send(params)
        print("SMS sent successfully:", response)

    except APIException as e:
        # Handle errors related to Kavenegar API
        print(f"APIException: {e}")
    except HTTPException as e:
        # Handle network or connection errors
        print(f"HTTPException: {e}")