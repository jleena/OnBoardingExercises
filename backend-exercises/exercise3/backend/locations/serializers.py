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
    

class StateSerializer(serializers.ModelSerializer):
    country__name = serializers.CharField(source='country.name', read_only=True)
    country__my_user__name = serializers.CharField(source='country.my_user.name', read_only=True)

    class Meta:
        model = State
        fields = [
            'id', 'name', 'state_code', 'gst_code', 'country',
            'country__name', 'country__my_user__name'
        ]
        read_only_fields = ['id', 'country__name', 'country__my_user__name']

class CitySerializer(serializers.ModelSerializer):
    state__name = serializers.CharField(source='state.name', read_only=True)

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
    
# for CRUD operations with nested serializers on Country-State-City
class CityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ['id', 'state']

class StateCreateSerializer(serializers.ModelSerializer):
    cities = CityCreateSerializer(many=True)

    class Meta:
        model = State
        exclude = ['id', 'country']

class CountryNestedCreateSerializer(serializers.ModelSerializer):
    states = StateCreateSerializer(many=True)

    class Meta:
        model = Country
        exclude = ['id', 'my_user']

    def create(self, validated_data):
        states_data = validated_data.pop('states')
        validated_data['my_user'] = self.context['request'].user
        country, _ = Country.objects.get_or_create(**validated_data)

        for state_data in states_data:
            cities_data = state_data.pop('cities')
            state, _ = State.objects.get_or_create(country=country, **state_data)
            for city_data in cities_data:
                City.objects.get_or_create(state=state, **city_data)

        return country

    def create(self, validated_data):
        countries_data = validated_data.pop('countries')
        for country_data in countries_data:
            serializer = CountryNestedCreateSerializer(data=country_data, context=self.context)
            if serializer.is_valid():
                serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)
        return {'message': 'Locations created successfully'}

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'name']

