from decimal import Decimal
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
        
# Create your views here.
@csrf_exempt
@api_view(['POST'])
def users(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        try:
            user = User.objects.create(
                username = data['username'],
                email = data['email'],
                password = make_password(data['password'])
            )

            profile = Profile.objects.create(
                user=user,
                position = data['position'],
                years_of_exp = data['years_of_exp'],
                description = data['description'],
            )
            user.save()
            profile.save()
        except Exception as e:
            print(e)

        print(User.objects.all())
        #return render(request, HttpResponse("<h1>ok</h1>"))
        return HttpResponse("User was created sucessfully")
    
        
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    
    data = json.loads(request.body)
    print(data)
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == "GET":
        #profile_json = serializers.serialize('json', [ profile, ])
        profile_obj = model_to_dict(profile)
        profile_obj['resume'] = str(profile_obj['resume'])
        profile_obj['user'] = model_to_dict(user)
        del profile_obj['user']["password"]
        profile_obj['id'] = profile.id
        
        return JsonResponse({'profile':profile_obj}, safe=False)
    if request.method == "PUT":

        profile.position = data['profile']['position']
        profile.years_of_exp = data['profile']['years_of_exp']
        profile.description = data['profile']['description']
        profile.save()

        profile_obj = model_to_dict(profile)
        profile_obj['resume'] = str(profile_obj['resume'])
        profile_obj['user'] = model_to_dict(user)
        del profile_obj['user']["password"]
        profile_obj['id'] = profile.id
        
        return JsonResponse({'profile':profile_obj}, safe=False)

    return HttpResponse("Profile Updated")