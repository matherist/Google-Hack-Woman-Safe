from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import *
from django.contrib import messages
from django.views import generic
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User 
from youtubesearchpython import VideosSearch
default_user = User.objects.get(username='dinaiym')
from django.contrib.auth.decorators import login_required
import uuid
from django.http import JsonResponse
import cv2
import numpy as np

def logout_view(request):
    logout(request)
    return redirect("/")

def home(request):
    return render(request, 'dashboard/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!!")
            return redirect('login')
    else:
       form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, "dashboard/register.html", context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homeworks_done = True
    else:
        homeworks_done = False
  
    context = {
        'homeworks': homeworks,
        'homes_done': homeworks_done,
    }
    return render(request, 'dashboard/profile.html', context)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            
            # Generate a unique identifier for the image filename
            unique_filename = str(uuid.uuid4())
            
            # Get the file extension from the original filename
            file_extension = post.photo.name.split('.')[-1]
            
            # Combine the unique identifier and file extension to create the new filename
            new_filename = f"{unique_filename}.{file_extension}"
            
            # Save the image with the new filename
            post.photo.name = f'user_photos/{new_filename}'
            
            post.user = request.user
            post.save()
            return redirect('home')  
    else:
        form = UserPostForm()
    return render(request, 'dashboard/add_post.html', {'form': form})

@login_required
def face_recognition(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['uploaded_image']
        
        # Read the uploaded image
        nparr = np.fromstring(uploaded_image.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform face recognition here using dlib or OpenCV

        # Assuming you have found a similar face in your database
        # Fetch the user information associated with the found face
        similar_user_post = UserPost.objects.filter(user=request.user).first()

        if similar_user_post:
            response_data = {
                'found': True,
                'photo_url': similar_user_post.photo.url,
                'text': similar_user_post.text,
            }
        else:
            response_data = {'found': False}

        return JsonResponse(response_data)

    return render(request, 'dashboard/face_recognition.html')

@login_required
def face_recognition_view(request):
    if request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded photo from the form
            uploaded_photo = form.cleaned_data['photo']

            # Convert the uploaded photo to a NumPy array
            nparr = np.fromstring(uploaded_photo.read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Your face recognition logic goes here
            # Assume that you have a function recognize_face() for face recognition
            matching_post = face_recognition(img)

            if matching_post:
                return render(request, 'dashboard/face_recognition_result.html', {'matching_post': matching_post})
            else:
                # No matching post found
                return render(request, 'dashboard/face_recognition_result.html', {'no_match': True})
    else:
        form = UserPostForm()
    return render(request, 'dashboard/face_recognition.html', {'form': form})