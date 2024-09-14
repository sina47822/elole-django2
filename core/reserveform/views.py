from django.shortcuts import HttpResponse, get_object_or_404
from formtools.preview import FormPreview
from accounts.models import User,UserType
from reserveform.models import ReserveFormModel
from formtools.wizard.views import SessionWizardView
from django.views.generic.edit import FormView
from stylist.models import Services,ServiceCategoryModel,WorkHour,WorkDay

from .forms import ReservationForm
# Create your views here.
# class ReserveFormWizardView(SessionWizardView,FormPreview):
#     form_list = (ReservationForm,ReservationForm2,ReservationForm3,ReservationForm4,ReservationForm5,ReservationForm6)
#     template_name = 'formreserve/formwizard.html'
#     preview_template = 'formreserve/preview.html'

#     def done(self, request, **kwargs):
#         return HttpResponse('success')
    
# class ReserveFormPreview(FormPreview):
#     preview_template = 'formreserve/preview.html'
#     form_template = 'formreserve/formwizard.html'

#     def done(self, request, cleaned_data):
#         ReserveFormModel.objects.create(**cleaned_data)
#         return HttpResponse('success')

class ReserveFormView(FormView):
    template_name = "formreserve/reserve-form.html"
    form_class = ReservationForm
    success_url = "/thanks/"

    def get_context_data(self, **kwargs):
        context = super(ReserveFormView, self).get_context_data(**kwargs)
        
        # Get all service categories
        categories = ServiceCategoryModel.objects.all()
        context['categories'] = categories

        # Step 1: Categories
        # Check if a category is selected in GET params
        selected_category_id = self.request.GET.get('category')
        if selected_category_id:
            # Get services for the selected category
            context['selected_category_id'] = int(selected_category_id)
            services = Services.objects.filter(category__id=selected_category_id)
            context['services_with_images'] = services
        
        
            # Step 2: Services
            selected_service_id = self.request.GET.get('service')
            if selected_service_id:
                context['selected_service_id'] = int(selected_service_id)
                selected_service = Services.objects.get(id=selected_service_id)
                admins = selected_service.stylist.filter(user__type=UserType.admin.value)
                context['admins'] = admins

                # Step 3: Admins
                selected_admin_id = self.request.GET.get('admin')
                if selected_admin_id:
                    context['selected_admin_id'] = int(selected_admin_id)
                    admin_workdays = WorkDay.objects.filter(stylist_id=selected_admin_id)
                    context['admin_workdays'] = admin_workdays
        

                    # Step 4: Workdays
                    selected_workday_id = self.request.GET.get('workday')
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
        selected_service_id = self.request.GET.get('service')
        selected_admin_id = self.request.GET.get('admin')
        selected_workday_id = self.request.GET.get('workday')
        selected_time_id = self.request.GET.get('time')

        # Assign the selected data to the form instance
        form.instance.customer = self.request.user  # Assuming the customer is the logged-in user
        form.instance.service_category = get_object_or_404(ServiceCategoryModel, id=self.request.GET.get('category'))
        form.instance.service = get_object_or_404(Services, id=selected_service_id)
        form.instance.stylist = get_object_or_404(User, id=selected_admin_id)
        form.instance.day = get_object_or_404(WorkDay, id=selected_workday_id)
        form.instance.hour = get_object_or_404(WorkHour, id=selected_time_id)

        # Save the reservation and handle success
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Pre-fill form if necessary or customize field queryset if needed
        return form