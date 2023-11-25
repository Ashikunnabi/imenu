from django.db import models

from apps.rbac.models import BaseModel


class Carousel(BaseModel):
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=256, default='')
    discount = models.IntegerField(default=0)
    redirect_url = models.CharField(max_length=256, default='')
    image = models.CharField(max_length=256)
    order = models.FloatField(default=999, blank=True, null=True)

    def __str__(self):
        return self.title


class PromoSection(BaseModel):
    title = models.CharField(max_length=50)
    promo = models.CharField(max_length=256)
    redirect_url = models.CharField(max_length=256)
    image = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Page(BaseModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Banner(BaseModel):
    title = models.CharField(max_length=50)
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='banner_page'
    )
    redirect_url = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
    order = models.FloatField(default=999, blank=True, null=True)

    def __str__(self):
        return self.title


class Flyer(BaseModel):
    title = models.CharField(max_length=50)
    redirect_url = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
    image1 = models.CharField(max_length=256, blank=True, null=True)
    image2 = models.CharField(max_length=256, blank=True, null=True)
    image3 = models.CharField(max_length=256, blank=True, null=True)
    is_promotional = models.BooleanField(default=False)
    show_at_home_page = models.BooleanField(default=False)
    order = models.FloatField(default=999, blank=True, null=True)

    def __str__(self):
        return self.title


class NavCategory(BaseModel):
    title = models.CharField(max_length=50)
    order = models.FloatField(default=999)
    redirect_url = models.CharField(max_length=256)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.title


class Notice(BaseModel):
    title = models.CharField(max_length=50)
    redirect_url = models.CharField(max_length=256)
    target = models.CharField(max_length=50, default='_self')
    background_color = models.CharField(max_length=50, default='white')
    color = models.CharField(max_length=50, default='black')
    order = models.FloatField(default=999)

    def __str__(self):
        return self.title


class Event(BaseModel):
    title = models.CharField(max_length=50)
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='event_page', blank=True, null=True
    )
    button_text = models.CharField(max_length=256)
    redirect_url = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
    priority = models.FloatField(default=999, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class UsefulLinks(BaseModel):
    title = models.CharField(max_length=50)
    redirect_url = models.CharField(max_length=256)
    order = models.FloatField(default=999, blank=True, null=True)

    def __str__(self):
        return self.title
