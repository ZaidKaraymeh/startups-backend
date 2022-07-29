from decimal import Decimal
import re
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.core import serializers
from .models import *

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def posts(request):
    data = json.loads(request.body)
    user = request.user
    if request.method == "GET" and type(data['id']) == str:

        post = Post.objects.filter(user=user, id=data['id']).first()

        if not post:
            return HttpResponseBadRequest("Not found or not authorized")

        post_obj = model_to_dict(post)
        post_obj['status'] = "200"
        post_obj['id'] = post.id
        return JsonResponse({'post':post_obj}, safe=False)
        
    if request.method == "GET" and type(data['id']) == int:
        posts = Post.objects.filter(user=user)
        #posts_obj = serializers.serialize('json', list(posts))
        #return HttpResponse(posts_obj)
        posts_obj = json.loads(serializers.serialize('json', posts))
        return JsonResponse({'posts':posts_obj}, safe=False)

    if request.method == "POST":
        try:
            post = Post.objects.create(
                user=user,
                title = data['title'],
                description = data['description']
            )
            post.save()
            post_obj = model_to_dict(post)
            post_obj['message'] = "Post created Successfully"
            post_obj['id'] = post.id
            return JsonResponse({'post':post_obj}, safe=False)
        except Exception:
            return HttpResponseBadRequest(Exception)
    
    if request.method == "PUT" and data['post']['id']:
        post = Post.objects.filter(user=user, id=data['post']['id']).first()

        if not post:
            return HttpResponseBadRequest("Unauthorized")

        post.title = data['post']['title']
        post.description = data['post']['description']
        post.save()

        post_obj = model_to_dict(post)
        post_obj['message'] = "Post Updated Successfully"
        post_obj['status'] = "200"
        post_obj['id'] = post.id
        return JsonResponse({'post':post_obj}, safe=False)

    if request.method == "DELETE" and data['id']:
        post = Post.objects.filter(user=user, id=data['id']).first()

        if not post:
            return HttpResponseBadRequest("Unauthorized")

        post.delete()
        return JsonResponse({'message':'Post has been deleted'}, safe=False)