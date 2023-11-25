from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest) -> render:
    """
    Customers can see this page after login to the system. It calls Index/home
    page.

    Attribute:
        request (HttpRequest): A http request object of current request

    Return:
        Render html page with all environment variable
    """
    return render(request, 'home/index.html')


def product_details(request: HttpRequest, hashed_id: str) -> render:
    """
    Show product details by it's hashed ID

    Attribute:
        request (HttpRequest): A http request object of current request
        hashed_id (str): A product's hashed_id that will help to identify
        specific product

    Return:
        Render html page with all environment variable and context variable
    """
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'home/product_details/product_details.html', context)


def product_list(request: HttpRequest) -> render:
    """
    Show lis to products

    Attribute:
        request (HttpRequest): A http request object of current request

    Return:
        Render html page with all environment variable
    """
    return render(request, 'home/product_list/product_list.html')


def about_us(request: HttpRequest) -> render:
    """
    About us page
    """
    return render(request, 'home/custom_page/about_us.html')


def brand_list(request: HttpRequest) -> render:
    """
    Brand list page
    """
    return render(request, 'home/brand/list.html')


def news_and_updates(request: HttpRequest) -> render:
    """
    News and updates page
    """
    return render(request, 'home/custom_page/news_and_updates.html')


def contact_us(request: HttpRequest) -> render:
    """
    Contact Us page
    """
    return render(request, 'home/custom_page/contact_us.html')


def advocacy(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/advocacy.html')


def brand_partner(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/brand_partner.html')


def brand_page_list(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/brand_page_list.html')


def brand_page(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/brand_page.html')


def why_buy_from_us(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/why_buy_from_us.html')


def shipping_policy(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/shipping_policy.html')


def faq(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/faq.html')


def return_policy(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/return_policy.html')

def marketting(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/marketting.html')


def promotion(request: HttpRequest) -> render:
    return render(request, 'home/custom_page/promotion.html')
