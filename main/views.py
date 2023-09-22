from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'name': user.first_name + ' ' + user.last_name,
            'email': user.email
        })


def CheckSessionExist(request):
    if request.method == 'GET':
        list_data = []
        for key, value in request.session.items():
            list_data.append(key + '=>' + value)
        # key = request.session['id']
        return JsonResponse({'key': list_data})
    else:
        return JsonResponse({'key': 'qweq'})
