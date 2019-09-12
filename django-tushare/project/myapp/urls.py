from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"hello/", views.hello, name="hello"),
    url(r"market/", views.market, name="market"),
    url(r"area/", views.area, name="area"),
    url(r"industry/", views.industry, name="industry"),
    url(r"", views.hello, ),
]