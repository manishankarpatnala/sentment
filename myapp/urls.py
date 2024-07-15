# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('output/', views.output, name='output'),
    path('login/', views.login, name='login'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('postlogin/', views.postlogin, name='postlogin'),
    path('analyze_sentiment/', views.analyze_sentiment_view, name='analyze_sentiment'),
]
