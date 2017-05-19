from django.conf.urls import include, url
from django.contrib import admin

from crawlermanage import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'geowind_crawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^crawlermanage/$',views.login, name='login'),
    url(r'^crawlermanage/login/$',views.login, name='login'),
    url(r'^crawlermanage/index/$',views.index, name='index'),
    url(r'^crawlermanage/tasks/$',views.tasks, name='tasks'),
    url(r'^crawlermanage/newsdata/$',views.newsdata, name='newsdata'),
    url(r'^crawlermanage/newsdetail/$',views.newsdetail, name='newsdetail'),
    url(r'^crawlermanage/ecommercedata/$',views.ecommercedata, name='ecommercedata'),
    url(r'^crawlermanage/layout/$',views.layout, name='layout'),

    # url(r'^crawlermanage/$','crawlermanage.views.login'),
    # url(r'^crawlermanage/login/$','crawlermanage.views.login'),
    # url(r'^crawlermanage/index/$','crawlermanage.views.index'),
    # url(r'^crawlermanage/tasks/$','crawlermanage.views.tasks'),
    # url(r'^crawlermanage/taskdata/$','crawlermanage.views.taskdata'),
    # url(r'^crawlermanage/layout/$','crawlermanage.views.layout'),

]
