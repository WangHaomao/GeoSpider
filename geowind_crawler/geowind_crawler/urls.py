from django.conf.urls import include, url
from django.contrib import admin
from crawlermanage import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'geowind_crawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='login'),
    url(r'^login/', views.login, name='index')
]
