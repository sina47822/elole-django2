from django.http import HttpResponse
# slug is required
import string, random 
from django.utils.text import slugify 
# blog neede
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
#newsletterform
from .forms import ContactForm, NewsLetterForm
from django.contrib import messages
from django.views.generic import CreateView
# models.fields
from website.models import SliderModel,CategorySEO, Post, Category , Tags ,PostSEO, TagsSEO

def index(request):
    posts = Post.objects.all().order_by('-id')
    categories = Category.objects.all()
    tags = Tags.objects.all()
    images = SliderModel.objects.all()

    context = {'posts': posts,
                'categories':categories,         
                'tags':tags,
                'images':images,
                }

    return render (request,'website/index.html', context)

def aboutus(request):
    return render (request,'website/about.html')

def contactus(request):
    return render (request,'website/contact.html')

def category(request):
    categories = Category.objects.filter(parent__isnull=True)  # top-level categories
    return render(request, 'website/blog.html', {'categories': categories})


def postcategory(request, slug):
    category = get_object_or_404(Category, slug=slug)  # Retrieve the category object based on the slug
    posts = Post.objects.filter(categories=category)  # Filter posts based on the category object

    seo = CategorySEO.objects.filter(Category_seo=category).first()

    paginator = Paginator(posts, 8)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    context = {'category': category, 'page_obj': page_obj, 'seo': seo, 'posts' : posts}

    return render(request, 'website/category.html', context)

def posttags(request, slug):
    tag = get_object_or_404(Tags, slug=slug)  # Retrieve the category object based on the slug
    posts = Post.objects.filter(tags=tag)  # Filter posts based on the category object
    seo = TagsSEO.objects.filter(tags_seo=tag).first()

    paginator = Paginator(posts, 8)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'tag': tag,'page_obj' :page_obj , 'posts': posts, 'seo' : seo}
    return render(request, 'website/tags.html', context)


def blog(request):
    posts = Post.objects.all().order_by('publish_date')
    categories = Category.objects.all()
    tags = Tags.objects.all()


    paginator = Paginator(posts, 4)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    latests = Post.objects.all().order_by('publish_date')[:5]  # Example: fetching the 1 latest posts
    context = {'posts': posts,
                'latests': latests,
                'categories':categories,         
                'tags':tags,
                'page_obj' :page_obj}
    return render(request, 'website/blog.html', context)

def blogposts(request, slug): 
    post = get_object_or_404(Post, slug =slug )
    seo = PostSEO.objects.filter(post=post).first()  # Retrieve the first PostSEO object associated with the post
    posts = Post.objects.all().order_by('-id')[:4]
    categories = Category.objects.all()
    tags = Tags.objects.all()

    context = {'slug': slug,
               'post' : post,
               'seo' : seo,
               'posts': posts,
               'categories':categories,
               'tags' : tags
               }

    return render(request, 'website/blog-detail.html', context) 

def TermsAndCondition(request):
    return render (request , 'website/termandcondition.html')

class SendContactView(CreateView):
    """
    a class based view to show index page
    """
    http_method_names = ['post']
    form_class = ContactForm

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, 'تیکت شما با موفقیت ثبت شد و در اسرع وقت با شما تماس حاصل خواهد شد')
        return super().form_valid(form)

    def form_invalid(self, form):
        # handle unsuccessful form submission
        messages.error(
            self.request, 'مشکلی در ارسال فرم شما پیش آمد لطفا ورودی ها رو بررسی کنین و مجدد ارسال نمایید')
        return redirect(self.request.META.get('HTTP_REFERER'))

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
    
class NewsletterView(CreateView):
    http_method_names = ['post']
    form_class = NewsLetterForm
    success_url = '/'

    def form_valid(self, form):
        # handle successful form submission
        messages.success(
            self.request, 'از ثبت نام شما ممنونم، اخبار جدید رو براتون ارسال می کنم 😊👍')
        return super().form_valid(form)

    def form_invalid(self, form):
        # handle unsuccessful form submission
        messages.error(
            self.request, 'مشکلی در ارسال فرم شما وجود داشت که می دونم برا چی بود!! چون ربات هستید!')
        return redirect('website:index')