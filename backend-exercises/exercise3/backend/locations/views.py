from django.shortcuts import render
from django.conf import settings
from .serializers import CountrySerializer, StateSerializer, CitySerializer, CountryNestedCreateSerializer
from .models import Country, State, City
from rest_framework import generics, permissions
import rest_framework.status as status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class CountryListCreateView(generics.ListCreateAPIView):
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Country.objects.filter(my_user=self.request.user).select_related('my_user')
    def perform_create(self, serializer):
        serializer.save(my_user=self.request.user)

class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Country.objects.filter(my_user=self.request.user).select_related('my_user')

class StateListCreateView(generics.ListCreateAPIView):
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return State.objects.filter(
            country__my_user=self.request.user
        ).select_related('country', 'country__my_user')

class StateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return State.objects.filter(
            country__my_user=self.request.user
        ).select_related("country", "country__my_user")

class CityListCreateView(generics.ListCreateAPIView):
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return City.objects.filter(
            state__country__my_user=self.request.user
        ).select_related("state", "state__country", "state__country__my_user")

class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return City.objects.filter(
            state__country__my_user=self.request.user
        ).select_related("state", "state__country", "state__country__my_user")

class LocationCreateView(APIView):
    def post(self, request):
        serializer = CountryNestedCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            country = serializer.save()
            return Response({'message': 'Location created successfully', 'country_id': str(country.id)})
        return Response(serializer.errors, status=400)
