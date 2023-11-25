from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import *


app_name = 'v1'


router = DefaultRouter()
router.register(r'carousel', CarouselViewSet, basename='carousel')
router.register(r'promo-section', PromoSectionViewSet, basename='promo_section')
router.register(r'page', PageViewSet, basename='page')
router.register(r'banner', BannerViewSet, basename='banner')
router.register(r'flyer', FlyerViewSet, basename='flyer')
router.register(r'nav-category', NavCategoryViewSet, basename='nav_category')
router.register(r'notice', NoticeViewSet, basename='notice')
router.register(r'event', EventViewSet, basename='event')
router.register(r'useful-link', UsefulLinksViewSet, basename='useful_link')

urlpatterns = [
    path('', include(router.urls)),

    path(
        'login-page-banners/',
        login_page_banners_list,
        name='login_page_banners_list'
    ),

    path('home-page/', include([
        path(
            'available-category-list/',
            AvailableCategoryList.as_view(),
            name='available_category_list'
        ),

        path(
            'products-based-on-category/',
            ProductsBasedOnCategory.as_view(),
            name='products_based_on_category'
        ),

        path(
            'related-random-products-based-on-category/',
            RelatedRandomProductsBasedOnCategory.as_view(),
            name='related_random_products_based_on_category'
        ),

        path(
            'latest-products/',
            LatestProducts.as_view(),
            name='latest_products'
        ),

        path(
            'brand-images/',
            BrandImageList.as_view(),
            name='brand_images'
        ),

        path(
            'admin-index/',
            AdminPanelIndexApiView.as_view(),
            name='admin_index'
        ),
    ])),
]
