# from django.shortcuts import render
from rest_framework import viewsets, status
from api.models import Checkbox
from api.serializers import CheckboxSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework import generics

# class CheckboxViewSet(viewsets.ModelViewSet):
#     queryset = Checkbox.objects.all()
#     serializer_class = CheckboxSerializer

class CheckboxList(APIView):
    # authentication_classes = ['authentication.TokenAuthentication']
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        checboxes = Checkbox.objects.all()
        serializer = CheckboxSerializer(checboxes, many=True)
        return Response(serializer.data)

    def post(self, request, fomat=None):
        serializer = CheckboxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CheckboxDetailed(APIView):

    def delete(self, request, pk, format=None):
        checkbox = Checkbox.objects.get(id=pk)
        checkbox.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def checkbox_list(request):
    checboxes = Checkbox.objects.all()
    serializer = CheckboxSerializer(checboxes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def checkbox_detail(request, pk):
    try:
        checbox = Checkbox.objects.get(id=pk)
        serializer = CheckboxSerializer(checbox)
    except Checkbox.DoesNotExist:
        return Response({"error": f"Checkbox with id={pk} is not found"} ,status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)


@api_view(['POST'])
def checkbox_create(request):
    serializer = CheckboxSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def checkbox_update(request, pk):
    try:
        checkbox = Checkbox.objects.get(id=pk)
        serializer = CheckboxSerializer(checkbox, data=request.data)
        if serializer.is_valid():
            serializer.save()
    except Checkbox.DoesNotExist:
        return Response({"error": f"Checkbox with id={pk} is not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)


@api_view(['DELETE'])
def checkbox_delete(request, pk):
    checkbox = Checkbox.objects.get(id=pk)
    checkbox.delete()
    # serializer = CheckboxSerializer(checkbox, data=request.data)
    return Response(status=status.HTTP_204_NO_CONTENT)