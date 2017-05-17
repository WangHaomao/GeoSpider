from django.conf.urls import include, url
from django.contrib import admin
#from crawlermanage import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'geowind_crawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^crawlermanage/$','crawlermanage.views.login'),
    url(r'^crawlermanage/login/$','crawlermanage.views.login'),
    url(r'^crawlermanage/index/$','crawlermanage.views.index'),
    url(r'^crawlermanage/tasks/$','crawlermanage.views.tasks'),
    url(r'^crawlermanage/taskdata/$','crawlermanage.views.taskdata'),
    url(r'^crawlermanage/layout/$','crawlermanage.views.layout'),
    # url(r'^/crawlermanage/^', views.home, name='login'),
    # url(r'^crawlermanage/login/', views.login, name='login'),
    # url(r'^crawlermanage/index/', views.index, name='index')

]
