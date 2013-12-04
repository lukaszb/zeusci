from zeusci.zeus.api.urls import urlpatterns as api_urlpatterns
from zeusci.zeus import urls

urlpatterns = urls.urlpatterns + api_urlpatterns
