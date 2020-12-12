from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DatabaseError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from apiXamarine.models import ObservedProduct, AppUser
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
@permission_classes([IsAuthenticated])
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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_observation(request):
    try:
        observations = ObservedProduct.objects.all()
        serializer = ObservedProductSerializer(observations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'response': 'There are no observations at the moment'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_observation(request):
    try:
        observations = ObservedProduct.objects.filter(creator=request.user.id)
        serializer = ObservedProductSerializer(observations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'response': 'There are no observations for this user at the moment'},
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_observation(request, pk):
    try:
        observation = ObservedProduct.objects.get(id=pk)
        if observation.creator.email == request.user.email:
            serializer = ObservedProductSerializer(instance=observation, data=request.data)
            if serializer.is_valid():
                if request.user == serializer.validated_data['creator']:
                    try:
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except DatabaseError:
                        return Response({'response':'Duplicate observation'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'response':'You are not authorized to modify your request with somebody else '
                                                'email'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': 'You have no permissions to update this observation'},
                            status=status.HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
        return Response({'response':'This observation does not exist'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_observation(request, pk):
    try:
        observation = ObservedProduct.objects.get(id=pk)
        if observation.creator.email == request.user.email:
            observation.delete()
            return Response({'response':'Observation successfully deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'You have no permissions to delete this observation'}, status=status.HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
        return Response({'response':'This observation does not exist'}, status=status.HTTP_400_BAD_REQUEST)
