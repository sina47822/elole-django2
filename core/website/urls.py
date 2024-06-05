from django.urls import path
from website.views import NewsletterView,aboutus,contactus, create_person,index,blog,blogposts,TermsAndCondition, postcategory,posttags,SendContactView


app_name = 'website'

urlpatterns = [
    path('', index , name='home'),
    path('about-us/', aboutus, name='about'),
    path('contact-us/', contactus, name='contact'),
    path('blog/', blog , name='blog-list'),
    path('terms-and-conditions/', TermsAndCondition, name='Terms-and-conditions'),
    path("newsletter/", NewsletterView.as_view(), name="newsletter"),
    path("submit/ticket/",SendContactView.as_view(), name="submit-ticket"),
    path('beauty/', create_person, name='beauty'),
    path('beautyform/', create_person, name='beautyformaction'),

    path('category/<slug:slug>/',postcategory , name='blog-category'),
    path('tags/<slug:slug>/',posttags , name='blog-tags'),

    path('<slug:slug>/',blogposts , name='blog-detail'),

]