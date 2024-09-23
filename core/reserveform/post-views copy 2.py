from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User,UserType
from django.views.generic.edit import FormView
from stylist.models import Services,ServiceCategoryModel,WorkHour,WorkDay

from django.conf import settings
from kavenegarapp.sender import send_telegram_message  # This will be used for sending SMS notifications

from reserveform.models import ReserveFormModel
from reserveform.forms import ReservationForm

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
            workday_id = request.POST.get('workday')

            if category_id:
                services = Services.objects.filter(category__id=category_id)
                services_options = "".join([f'<option value="{s.id}">{s.name}</option>' for s in services])
                return JsonResponse({'services': services_options})

            if service_id:
                selected_service = Services.objects.get(id=service_id)
                admins = selected_service.stylist.filter(user__type=UserType.admin.value)
                admins_options = "".join([f'<option value="{a.id}">{a.user.user_profile.first_name}</option>' for a in admins])
                return JsonResponse({'admins': admins_options})

            if admin_id:
                workdays = WorkDay.objects.filter(stylist__id=admin_id)
                workdays_options = "".join([f'<option value="{wd.id}">{wd.day}</option>' for wd in workdays])
                return JsonResponse({'workdays': workdays_options})

            if workday_id:
                times = WorkDay.objects.get(id=workday_id).hour.all()
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
        selected_workday_id = self.request.POST.get('workday')
        selected_time_id = self.request.POST.get('time')

        # Store all selections in the session
        reservation_data = {
            'category': self.request.POST.get('category'),
            'service': selected_service_id,
            'admin': selected_admin_id,
            'workday': selected_workday_id,
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
