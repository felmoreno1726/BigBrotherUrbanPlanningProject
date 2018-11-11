from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # re_path(r"(?P<coordination>-?\d+\.?\d*)", views.geturl, name='geturl')

    # path('<str:id1>/<str:id2>/<str:id3>/<str:id4>', views.geturl, name='geturl'),

    path('cal', views.geturl, name='geturl'),
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote')
]