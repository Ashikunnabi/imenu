import base64
import json
from django.db.models import Q
import pandas as pd
import random

from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.base.utils.basic import *
from apps.base.drf_custom_permisson import AuthenticatedStaffOrReadOnly
from apps.home.models import (
    Carousel,
    PromoSection,
    Page,
    Banner,
    Flyer,
    NavCategory,
    Notice,
    Event,
    UsefulLinks
)
from apps.inventory.models import (
    # ProductCategory,
    Product,
    # DealerBrand,
    Brand
)
from apps.home.api.v1.serializers import (
    CarouselSerializer,
    DashboardSummarySerializer,
    PromoSectionSerializer,
    PageSerializer,
    BannerSerializer,
    BrandImageOnlySerializer,
    FlyerSerializer,
    NavCategorySerializer,
    NoticeSerializer,
    EventSerializer,
    UsefulLinksSerializer
)



class CarouselViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Carousel: A new carousel '{request.data.get('title')}' added."
        )

    def perform_update(self, instance, serializer, request):
        """ Update an existing Branch and store activity log. """
        previous_data_before_update = self.queryset.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Carousel: An existing Carousel '{previous_data_before_update.title}' modified."
        )

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        store_user_activity(
            request,
            store_json=serializer,
            description=f"Carousel: An existing carousel '{serializer.get('title')}' deleted by {request.user.name}.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('order')
        if not request.user.is_staff:
            queryset = queryset.filter(is_active=True, is_soft_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.CAROUSEL_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.CAROUSEL_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        instance = self.get_object()
        if data.get('title') == '':
            instance.title = ''
        if data.get('description') == '':
            instance.description = ''
        if data.get('discount') == '':
            instance.discount = 0
        if data.get('redirect_url') == '':
            instance.redirect_url = ''
        instance.save()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Carousel deleted successfully"}, status=status.HTTP_200_OK)


class PromoSectionViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = PromoSection.objects.all()
    serializer_class = PromoSectionSerializer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"PromoSection: A new Promo '{request.data.get('title')}' added."
        )

    def perform_update(self, instance, serializer, request):
        """ Update an existing Branch and store activity log. """
        previous_data_before_update = self.queryset.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"PromoSection: An existing Promo '{previous_data_before_update.title}' modified."
        )

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        store_user_activity(
            request,
            store_json=serializer,
            description=f"PromoSection: An existing Promo '{serializer.get('title')}' deleted by {request.user.name}.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.user.is_staff:
            queryset = self.get_queryset().filter(is_active=True, is_soft_deleted=False)[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.PROMO_SECTION_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.PROMO_SECTION_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Promo deleted successfully"}, status=status.HTTP_200_OK)


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Page: A new Page '{request.data.get('title')}' added."
        )

    def perform_update(self, instance, serializer, request):
        """ Update an existing Page and store activity log. """
        previous_data_before_update = self.queryset.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Page: An existing Page '{previous_data_before_update.title}' modified."
        )

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        store_user_activity(
            request,
            store_json=serializer,
            description=f"Page: An existing Page '{serializer.get('title')}' deleted by {request.user.name}.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.user.is_staff:
            queryset = self.get_queryset().filter(is_active=True, is_soft_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Page deleted successfully"}, status=status.HTTP_200_OK)


class BannerViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Banner: A new Banner '{request.data.get('title')}' added."
        )

    def perform_update(self, instance, serializer, request):
        """ Update an existing Banner and store activity log. """
        previous_data_before_update = self.queryset.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Banner: An existing Banner '{previous_data_before_update.title}' modified."
        )

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        store_user_activity(
            request,
            store_json=serializer,
            description=f"Banner: An existing Banner '{serializer.get('title')}' deleted by {request.user.name}.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.user.is_staff:
            queryset = self.get_queryset().filter(is_active=True, is_soft_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.BANNER_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        # set page id
        data['page'] = Page.objects.get(hashed_id=data.get('page')).id

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # set to mutable
        data._mutable = True

        # store files in server
        for file in files:
            file_path = f'{settings.BANNER_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        # set page id
        data['page'] = Page.objects.get(hashed_id=data.get('page')).id

        # set to immutable
        data._mutable = False

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Banner deleted successfully"}, status=status.HTTP_200_OK)


class AvailableCategoryList(APIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]

    def get(self, request):
        """
        Return a list of all available product categories.
        """
        queryset = ProductCategory.objects.filter(
            show_at_home_page=True,
            is_soft_deleted=False,
            is_active=True
        )
        data = [{
            'name': category.name,
            'hashed_id': category.hashed_id,
            'html_id': ''.join(e for e in category.name.lower() if e.isalnum())
        } for category in queryset]
        return Response({'data': data})


class ProductsBasedOnCategory(APIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    requested_user = None

    def get_your_price(self, obj):
        # provide discounted price if available for dealer
        try:
            user = self.requested_user
            dealer_brand = DealerBrand.objects.filter(
                dealer=user,
                brand=obj.manufacturer
            )
            if dealer_brand.exists():
                queryset = dealer_brand[0]
                current_jobbar_price = float(obj.jobbar_price)
                discount_on_jobbar = float(queryset.discount)
                new_cost = current_jobbar_price - (current_jobbar_price * discount_on_jobbar) / 100
                return str(round(new_cost, 2))
            else:
                return obj.your_price
        except Exception as ex:
            return obj.your_price

    @staticmethod
    def get_image_url(obj):
        try:
            if obj.added_from_finale:
                return obj.image_url
            else:
                return '/media/' + obj.image
        except Exception as ex:
            return obj.image_url

    def get(self, request):
        """
        Return a list of available products.
        """
        category_hashed_id = request.GET.get('category_hashed_id')
        length = int(request.GET.get('length', 12))

        if request.user.is_authenticated:
            self.requested_user = request.user

        # inactive brand for dealer
        inactive_brands_id = DealerBrand.objects.filter(
            dealer=request.user,
            is_active=False
        ).values_list('brand_id', flat=True)

        queryset = Product.objects.filter(
            category__is_active=True,
            manufacturer__is_active=True,
            show_at_homepage_category=True,
            category__hashed_id=category_hashed_id,
            is_soft_deleted=False,
            is_active=True
        )

        # remove inactive brands product for dealer
        queryset = queryset.exclude(
            manufacturer_id__in=inactive_brands_id
        ).order_by('-updated_at')[:length]

        data = ProductSerializer(queryset, many=True).data
        for d in data:
            try:
                temp_queryset = Product.objects.get(id=d['id'])
                d['your_price'] = self.get_your_price(temp_queryset)
                d['image_url'] = self.get_image_url(temp_queryset)
            except Exception as ex:
                pass

        data = get_products_with_custom_column(data, request.user)
        return Response({'data': data})


class RelatedRandomProductsBasedOnCategory(APIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]

    def get(self, request):
        """
        Return a list of available products randomly based on category.
        """
        product_hashed_id = request.GET.get('product_hashed_id')
        category_hashed_id = request.GET.get(
            'category_hashed_id',
            Product.objects.get(hashed_id=product_hashed_id).category.hashed_id
        )
        length = int(request.GET.get('length', 12))

        queryset = Product.objects.filter(
            category__hashed_id=category_hashed_id,
            manufacturer__is_active=True,
            is_soft_deleted=False,
            is_active=True
        ).exclude(hashed_id=product_hashed_id)

        # randomize the queryset to get a random products for each request
        random_products = random.sample(list(queryset), length)

        data = ProductSerializer(random_products, many=True).data

        for d in data:
            try:
                if d['added_from_finale']:
                    d['image_url'] = d['image_url']
                else:
                    d['image_url'] = '/media/' + d['image']
            except Exception as e:
                pass

        data = get_products_with_custom_column(data, request.user)
        return Response({'data': data})


class LatestProducts(APIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]

    def get(self, request):
        """
        Return a list of available latest products.
        """
        length = int(request.GET.get('length', 12))

        # inactive brand for dealer
        inactive_brands_id = DealerBrand.objects.filter(
            dealer=request.user,
            is_active=False
        ).values_list('brand_id', flat=True)

        queryset = Product.objects.filter(
            category__is_active=True,
            manufacturer__is_active=True,
            is_soft_deleted=False,
            is_active=True
        ).order_by('-created_at')

        # remove inactive brands product for dealer
        queryset = queryset.exclude(manufacturer_id__in=inactive_brands_id)[:length]
        data = ProductSerializer(queryset, many=True).data

        for d in data:
            try:
                if d['added_from_finale']:
                    d['image_url'] = d['image_url']
                else:
                    d['image_url'] = '/media/' + d['image']
            except Exception as e:
                pass

        data = get_products_with_custom_column(data, request.user)
        return Response({'data': data})


class BrandImageList(APIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]

    def get(self, request):
        """
        Return a list of available/latest brands for a dealer.
        """
        show_latest = int(request.GET.get('show_latest', 0))
        length = int(request.GET.get('length', 0))

        # inactive brand for dealer
        inactive_brands_id = DealerBrand.objects.filter(
            dealer=request.user,
            is_active=False
        ).values_list('brand_id', flat=True)

        queryset = Brand.objects.filter(
            is_soft_deleted=False,
            is_active=True
        )

        # remove inactive brands product for dealer
        queryset = queryset.exclude(
            id__in=inactive_brands_id
        )

        if show_latest:
            queryset = queryset.order_by('-created_at')

        if length:
            queryset = queryset[:length]

        data = BrandImageOnlySerializer(queryset, many=True).data
        return Response({'data': data})


class FlyerViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = Flyer.objects.all()
    serializer_class = FlyerSerializer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Flyer: A new Flyer '{request.data.get('title')}' added."
        )

    def perform_update(self, instance, serializer, request):
        """ Update an existing Flyer and store activity log. """
        previous_data_before_update = self.queryset.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Flyer: An existing Flyer '{previous_data_before_update.title}' modified."
        )

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        store_user_activity(
            request,
            store_json=serializer,
            description=f"Flyer: An existing Flyer '{serializer.get('title')}' deleted by {request.user.name}.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        show_at_home_page = request.GET.get('sp', 0)
        show_promotional = int(request.GET.get('promotional', 0))

        queryset = self.get_queryset()
        if not request.user.is_staff:
            if show_at_home_page:
                queryset = self.get_queryset().filter(
                    show_at_home_page=True,
                    is_active=True,
                    is_soft_deleted=False
                )
            else:
                if show_promotional:
                    queryset = self.get_queryset().filter(
                        is_promotional=True,
                        is_active=True,
                        is_soft_deleted=False
                    )
                else:
                    queryset = self.get_queryset().filter(
                        is_promotional=False,
                        is_active=True,
                        is_soft_deleted=False
                    )
        serializer = self.get_serializer(queryset.order_by('order'), many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.FLYER_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # set to mutable
        data._mutable = True

        # store files in server
        for file in files:
            file_path = f'{settings.FLYER_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        # set to immutable
        data._mutable = False

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Flyer deleted successfully"}, status=status.HTTP_200_OK)


class NavCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = NavCategory.objects.all()
    serializer_class = NavCategorySerializer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"NavCategory: A new NavCategory '{request.data.get('title')}' added."
        )

    def perform_update(self, instance, serializer, request):
        """ Update an existing NavCategory and store activity log. """
        previous_data_before_update = self.queryset.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"NavCategory: An existing NavCategory '{previous_data_before_update.title}' modified."
        )

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        store_user_activity(
            request,
            store_json=serializer,
            description=f"NavCategory: An existing NavCategory '{serializer.get('title')}' deleted by {request.user.name}.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.user.is_staff:
            queryset = self.get_queryset().filter(
                is_active=True, is_soft_deleted=False
            ).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "NavCategory deleted successfully"}, status=status.HTTP_200_OK)


class AdminPanelIndexApiView(APIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]

    def get(self, request):
        """
        Return a object of data.
        """

        # active products
        active_product_count = Product.objects.filter(
            manufacturer__is_soft_deleted=False,
            manufacturer__is_active=True,
            is_active=True,
            is_soft_deleted=False
        ).count()

        # active dealers
        active_dealer_count = get_user_model().objects.filter(
            is_staff=False,
            is_active=True
        ).count()

        # inactive dealers
        inactive_dealer_count = get_user_model().objects.filter(
            is_staff=False,
            is_active=False
        ).count()

        # active brands
        active_brand_count = Brand.objects.filter(
            is_active=True,
            is_soft_deleted=False
        ).count()

        pending_order_count = Order.objects.filter(
            in_processing=False,
            is_delivered=False,
            is_cancelled=False,
            is_ordered=True,
            is_active=True,
            is_soft_deleted=False
        ).count()

        in_processing_order_count = Order.objects.filter(
            in_processing=True,
            is_delivered=False,
            is_cancelled=False,
            is_ordered=True,
            is_active=True,
            is_soft_deleted=False
        ).count()

        data = {
            "product": {"count": active_product_count},
            "dealer": {
                "active_dealer_count": active_dealer_count,
                "inactive_dealer_count": inactive_dealer_count,
            },
            "brand": {"count": active_brand_count},
            "order": {
                "pending_order_count": pending_order_count,
                "in_processing_order_count": in_processing_order_count
            }
        }
        return Response({'data': data})


class NoticeViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Notice: A new Notice '{request.data.get('title')}' added."
        )

    def perform_update(self, instance, serializer, request):
        """ Update an existing Notice and store activity log. """
        previous_data_before_update = self.queryset.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Notice: An existing Notice '{previous_data_before_update.title}' modified."
        )

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        store_user_activity(
            request,
            store_json=serializer,
            description=f"Notice: An existing Notice '{serializer.get('title')}' deleted by {request.user.name}.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.user.is_staff:
            queryset = self.get_queryset().filter(
                is_active=True, is_soft_deleted=False
            ).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Notice deleted successfully"}, status=status.HTTP_200_OK)


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Event: A new Event '{request.data.get('title')}' added."
        )

    def perform_update(self, instance, serializer, request):
        """ Update an existing Event and store activity log. """
        previous_data_before_update = self.queryset.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"Event: An existing Event '{previous_data_before_update.title}' modified."
        )

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        store_user_activity(
            request,
            store_json=serializer,
            description=f"Event: An existing Event '{serializer.get('title')}' deleted by {request.user.name}.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-updated_at')
        serializer = self.get_serializer(queryset, many=True)
        if not request.user.is_staff:
            queryset = self.get_queryset().filter(
                ~Q(end_date__lt=datetime.today()),
                start_date__lte=datetime.today(),
                is_active=True, is_soft_deleted=False
            ).order_by('-priority')
            if queryset.exists():
                serializer = self.get_serializer(queryset.first())
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'data': []}, status=status.HTTP_200_OK)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.EVENT_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        # set page id
        # data['page'] = Page.objects.get(hashed_id=data.get('page')).id

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # set to mutable
        data._mutable = True

        # store files in server
        for file in files:
            file_path = f'{settings.EVENT_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        # set page id
        # data['page'] = Page.objects.get(hashed_id=data.get('page')).id

        # set to immutable
        data._mutable = False

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Event deleted successfully"}, status=status.HTTP_200_OK)


class UsefulLinksViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = UsefulLinks.objects.all()
    serializer_class = UsefulLinksSerializer
    lookup_field = 'hashed_id'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"UsefulLink: A new UsefulLink '{request.data.get('title')}' added."
        )

    def perform_update(self, instance, serializer, request):
        """ Update an existing UsefulLinks and store activity log. """
        previous_data_before_update = self.queryset.get(hashed_id=instance.hashed_id)
        serializer.save()
        store_user_activity(
            request,
            store_json=serializer.data,
            description=f"UsefulLink: An existing UsefulLink '{previous_data_before_update.title}' modified."
        )

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        store_user_activity(
            request,
            store_json=serializer,
            description=f"UsefulLink: An existing UsefulLink '{serializer.get('title')}' deleted by {request.user.name}.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('order')
        if not request.user.is_staff:
            queryset = self.get_queryset().filter(
                is_active=True, is_soft_deleted=False
            ).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response({"detail": "Notice deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def login_page_banners_list(request):
    queryset = Banner.objects.filter(
        page__title__icontains='Login page',
        is_active=True
    )

    # randomize the queryset to get a random products for each request
    random_banners = random.sample(list(queryset), queryset.count())

    data = []
    for banner in random_banners:
        with open(default_storage.path(banner.image), "rb") as image_file:
            image_data = base64.b64encode(image_file.read())
        data.append({
            'title': banner.title,
            'human_readable_page': banner.page.title,
            'redirect_url': banner.redirect_url,
            'image': image_data
        })
        break

    return Response({'data': data})


class DashboardSummaryViewSet(APIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    serializer_class = DashboardSummarySerializer

    def get(self, request, *args, **kwargs):
        data = [
            {
                "code": "total_products",
                "title": "Total Products",
                "count": 100
            },
            {
                "code": "total_orders",
                "title": "Total Orders",
                "count": 1000
            }
        ]
        serializer = self.serializer_class(data, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
