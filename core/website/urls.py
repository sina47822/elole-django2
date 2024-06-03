from django.urls import path
from website.views import aboutus,contactus,index,blog,blogposts,TermsAndCondition, postcategory,posttags
app_name = 'website'

urlpatterns = [
    path('', index , name='home'),
    path('about-us/', aboutus, name='about'),
    path('contact-us/', contactus, name='contact'),
    path('blog/', blog , name='blog-list'),
    path('terms-and-conditions/', TermsAndCondition, name='Terms-and-conditions'),

    path('category/<slug:slug>/',postcategory , name='blog-category'),
    path('tags/<slug:slug>/',posttags , name='blog-tags'),

    path('<slug:slug>/',blogposts , name='blog-detail'),

]