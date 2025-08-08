from rest_framework import serializers
from .models import Country, City, State
from accounts.models import MyUser

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'country_code', 'curr_symbol', 'phone_code']
    
class CitySerializer(serializers.ModelSerializer):
    my_state__name = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = [
            'id', 'name', 'city_code', 'phone_code',
            'population', 'avg_age', 'num_of_adult_males', 'num_of_adult_females',
            'state', 'my_state__name'
        ]

    def get_my_state__name(self, obj):
        return obj.state.name

class StateSerializer(serializers.ModelSerializer):
    my_country__name = serializers.SerializerMethodField()
    my_country__my_user__name = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ['id', 'name', 'state_code', 'gst_code', 'country', 'my_country__name', 'my_country__my_user__name']

    def get_my_country__name(self, obj):
        return obj.country.name

    def get_my_country__my_user__name(self, obj):
        return obj.country.my_user.name

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'name']

