from rest_framework import serializers
from .models import Country, City, State
from accounts.models import MyUser

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'country_code', 'curr_symbol', 'phone_code']
        read_only_fields = ['id']
    def create(self, validated_data):
        # Add the user from context
        validated_data['my_user'] = self.context['request'].user
        return super().create(validated_data)
    
class CitySerializer(serializers.ModelSerializer):
    my_state__name = serializers.CharField(source='state.name', read_only=True)

    class Meta:
        model = City
        fields = [
            'id', 'name', 'city_code', 'phone_code',
            'population', 'avg_age',
            'num_of_adult_males', 'num_of_adult_females',
            'state', 'state__name'
        ]
        read_only_fields = ['id', 'state__name']

    def validate(self, data):
        males = data.get('num_of_adult_males', 0)
        females = data.get('num_of_adult_females', 0)
        population = data.get('population')

        if population is not None and population <= (males + females):
            raise serializers.ValidationError("Population must be greater than or equal to the number of adult males + females.")
        return data

class StateSerializer(serializers.ModelSerializer):
    my_country__name = serializers.CharField(source='country.name', read_only=True)
    my_country__my_user__name = serializers.CharField(source='country.my_user.name', read_only=True)

    class Meta:
        model = State
        fields = [
            'id', 'name', 'state_code', 'gst_code', 'country',
            'country__name', 'country__my_user__name'
        ]
        read_only_fields = ['id', 'country__name', 'country__my_user__name']

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'name']

