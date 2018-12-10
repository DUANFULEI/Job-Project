from django.conf.urls import url
from app import views



urlpatterns = [
    url(r'^$', views.zhilianzhaopin_show, name='zhilianzhaopin_show'),
    url(r'^jobs/(?P<p>[0-9]+)/$', views.ListView.as_view(), name='jobs'),
    url(r'^top/', views.top_show, name='top_show'),
    url(r'^left/', views.left_show, name='left_show'),
    url(r'^main/', views.mian, name='main'),
    url(r'^all/', views.index, name='index'),
    url(r'^all1/', views.index1, name='index1'),
    url(r'^all2/', views.index2, name='index2'),
    url(r'^work_detail/(?P<n>[0-9]+)/$', views.work_detail, name='work_detail'),
]








