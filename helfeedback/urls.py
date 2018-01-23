"""helfeedback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

# from feedback.api import APIRouter
from feedback.views import FeedbackView, FeedbackCreate

admin.autodiscover()

# router = APIRouter()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^v1/', include(router.urls)),
    url(r'^v1/', FeedbackView.as_view()),
    url(r'feedback/add', FeedbackCreate.as_view(), name='feedback-add'),
    url(r'^$', RedirectView.as_view(url='v1/')),
]
