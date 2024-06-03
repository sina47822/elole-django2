from django.shortcuts import get_object_or_404, render
from stylist.models import Stylist,Services,WorkHour,WorkDay,Skills
from django.core.paginator import Paginator

def StylistListView(request):
    stylists = Stylist.objects.all().order_by('publish_date')
    services = Services.objects.all().order_by('publish_date')[:5]

    paginator = Paginator(stylists, 8)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'stylists': stylists,
                'services':services
               }
    return render(request, 'stylist/stylist-list.html', context)

def StylistView(request, slug): 
    stylist = get_object_or_404(Stylist, slug =slug )
    # seo = StylistSEO.objects.filter(post=post).first()  # Retrieve the first PostSEO object associated with the post
    stylists = Stylist.objects.all().order_by('-id')[:4]
    services = Services.objects.all()
    skills = Skills.objects.all()
    workday = WorkDay.objects.all()
    workhour = WorkHour.objects.all()

    context = {'slug': slug,
               'stylist' : stylist,
               'stylists': stylists,
               'services':services,
               'skills':skills,
               'workday':workday,
               'workhour':workhour,

               }

    return render(request, 'stylist/stylist-detail.html', context) 

def ServicesListView(request):
    stylists = Stylist.objects.all().order_by('publish_date')[:5]
    services = Services.objects.all().order_by('publish_date')

    paginator = Paginator(services, 4)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'stylists': stylists,
                'services':services
               }
    return render(request, 'stylist/services-list.html', context)

def ServicesView(request, slug): 
    service = get_object_or_404(Services, slug =slug )
    # seo = StylistSEO.objects.filter(post=post).first()  # Retrieve the first PostSEO object associated with the post
    stylists = Stylist.objects.all().order_by('-id')[:4]
    services = Services.objects.all()

    context = {'slug': slug,
               'service' : service,
               'stylists': stylists,
               'services':services,
               }

    return render(request, 'stylist/service-detail.html', context) 
