from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.urls import reverse

from accounts.models import User,UserType
from django.views.generic.edit import FormView
from stylist.models import Services,ServiceCategoryModel,WorkHour,WorkDay

from django.conf import settings
from kavenegarapp.sender import send_telegram_message  # This will be used for sending SMS notifications

from reserveform.models import ReserveFormModel
from reserveform.forms import ReservationForm

from kavenegar import *
from django.contrib import messages

class ReserveFormView(FormView):
    template_name = "formreserve/reserve-form.html"
    form_class = ReservationForm

    def get_context_data(self, **kwargs):
        context = super(ReserveFormView, self).get_context_data(**kwargs)
        
        # Get all service categories
        categories = ServiceCategoryModel.objects.all()
        context['categories'] = categories
        
        # Retrieve selected steps from session data if available
        session_data = self.request.session.get('reservation_data', {})
        print(self.request.session.__dict__)
        # self.request.session['category'] = self.request.GET.get('category')
        # Step 1: Categories
        # Check if a category is selected in GET params
        selected_category_id = self.request.GET.get('category') or session_data.get('category')
        
        if selected_category_id:
            # Get services for the selected category
            context['selected_category_id'] = int(selected_category_id)
            services = Services.objects.filter(category__id=selected_category_id)
            context['services_with_images'] = services
        
            # Step 2: Services
            selected_service_id = self.request.GET.get('service') or session_data.get('service')
            if selected_service_id:
                context['selected_service_id'] = int(selected_service_id)
                selected_service = Services.objects.get(id=selected_service_id)
                admins = selected_service.stylist.filter(user__type=UserType.admin.value)
                context['admins'] = admins

                # Step 3: Admins
                selected_admin_id = self.request.GET.get('admin') or session_data.get('admin')
                if selected_admin_id:
                    context['selected_admin_id'] = int(selected_admin_id)
                    admin_workdays = WorkDay.objects.filter(stylist_id=selected_admin_id)
                    context['admin_workdays'] = admin_workdays
        

                    # Step 4: Workdays
                    selected_workday_id = self.request.GET.get('workday') or session_data.get('workday')
                    if selected_workday_id:
                        context['selected_workday_id'] = int(selected_workday_id)
                        available_times = WorkDay.objects.get(id=selected_workday_id).hour.all()
                        context['available_times'] = available_times
                    # else:
                    #     available_times = WorkHour.objects.all()
                    #     context['available_times'] = available_times
                # else:
                #     admin_workdays = WorkDay.objects.all()
                #     context['admin_workdays'] = admin_workdays
            # else:
            #     admins = User.objects.filter(type=UserType.admin.value).select_related('stylist_profile')
            #     context['admins'] = admins
        # else:
        #     services = Services.objects.all()
        #     context['services_with_images'] = services
        return context
    
    # def form_valid(self, form):

        # service = form.cleaned_data['service']
        # admin = form.cleaned_data['admin']  # The admin (selected after service)
    
        # if not form.cleaned_data.get('service'):
        #     form.add_error('service', "Service is required before selecting a stylist")
        #     return self.form_invalid(form)
        # This method is called when valid form data has been GETed.
        # It should return an HttpResponse.
        #form.send_email()
        #print "form is valid"
        # return super(ReserveFormView, self).form_valid(form)'
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
        print(self.request.session.__dict__)
        print(self.request.session.get("reservation_data"))

        # Redirect to login page if the user is not authenticated
        if not self.request.user.is_authenticated:
            return redirect(f"{reverse('accounts:login')}?next={reverse('reserveform:reservation_confirm')}")  # Adjust 'login' to the actual login URL

        # # Assign the selected data to the form instance
        # form.instance.customer = self.request.user  # Assuming the customer is the logged-in user
        # form.instance.service_category = get_object_or_404(ServiceCategoryModel, id=self.request.GET.get('category'))
        # form.instance.service = get_object_or_404(Services, id=selected_service_id)
        # form.instance.stylist = get_object_or_404(User, id=selected_admin_id)
        # form.instance.day = get_object_or_404(WorkDay, id=selected_workday_id)
        # form.instance.hour = get_object_or_404(WorkHour, id=selected_time_id)

        # # Save the reservation and handle success
        # return super().form_valid(form)

        # After login, proceed to create the reservation
        # return redirect('reservation_confirm')
    
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

                print(self.request.session.__dict__)
                print(self.request.session.get("reservation_data"))
                # Clear the session data after reservation is complete
                del self.request.session['reservation_data']

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
    
    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
        
    #     # Pre-fill form if necessary or customize field queryset if needed
    #     return form
    def get(self, request, *args, **kwargs):
        # Check if the user was redirected from the login/signup page after session data was stored
        if request.user.is_authenticated and 'reservation_data' in request.session:
            return self.process_reservation()
        return super().get(request, *args, **kwargs)
    
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
