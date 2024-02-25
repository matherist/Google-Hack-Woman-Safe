from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('logout', logout_view),
    path('add_post/', add_post, name='add_post'),
    path('face_recognition/', face_recognition, name='face_recognition'),
    path('face_recognition_view/', face_recognition_view, name='face_recognition_view'),

]