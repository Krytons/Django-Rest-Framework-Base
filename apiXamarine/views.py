from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from djongo.database import DatabaseError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from apiXamarine.serializers import RegistrationSerializer, ObservedProductSerializer
from rest_framework.authtoken.models import Token

@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return Response('This is a test', status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        new_user = serializer.save()
        data['response'] = "Registration was successful"
        data['email'] = new_user.email
        data['name'] = new_user.name
        data['surname'] = new_user.surname
        data['nickname'] = new_user.nickname
        token = Token.objects.get(user=new_user).key
        data['token'] = token
        return JsonResponse(data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_observation(request):
    serializer = ObservedProductSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['creator'] != request.user:
            return Response({'response': 'You have no permissions to create an observed product for somebody '
                                         'else!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except DatabaseError:
                return Response({'response': 'This element is already observed'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

