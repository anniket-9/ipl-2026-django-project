from django.urls import path
from . import views

urlpatterns = [
    # Match URLs
    path('', views.match_list, name='match_list'),
    path('matches/', views.match_list, name='match_list'),
    path('matches/<slug:slug>/', views.match_detail, name='match_detail'),
    path('matches/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('matches/<slug:slug>/share/', views.share_match, name='share_match'),

    # Team URLs
    path('teams/', views.team_list, name='team_list'),
    path('teams/<slug:slug>/', views.team_detail, name='team_detail'),

    # Player URLs
    path('players/', views.player_list, name='player_list'),
]
