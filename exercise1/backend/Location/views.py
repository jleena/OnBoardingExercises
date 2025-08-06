# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Country, State, City
from django.db import transaction

class BulkInsertView(APIView):
    def post(self, request):
        data = request.data

        if not isinstance(data, list):
            return Response({"error": "Expected a list of records"}, status=400)

        try:
            with transaction.atomic():
                created_countries = {}
                created_states = {}
                created_cities = {}

                for row in data:
                    # --- Country ---
                    country_key = row['country']['country_code']
                    if country_key not in created_countries:
                        country, _ = Country.objects.get_or_create(
                            country_code=country_key,
                            defaults={
                                "name": row['country']['country_name'],
                                "curr_symbol": row['country']['curr_symbol'],
                                "phone_code": row['country']['country_phone_code']
                            }
                        )
                        created_countries[country_key] = country
                    else:
                        country = created_countries[country_key]

                    # --- State ---
                    state_key = f"{country_key}-{row['state']['state_code']}"
                    if state_key not in created_states:
                        state, _ = State.objects.get_or_create(
                            state_code=row['state']['state_code'],
                            country=country,
                            defaults={
                                "name": row['state']['state_name'],
                                "gst_code": row['state']['gst_code']
                            }
                        )
                        created_states[state_key] = state
                    else:
                        state = created_states[state_key]

                    # --- City ---
                    if row['city']['city_code'] not in created_cities:
                        city_details = row['city']
                        city, _ = City.objects.get_or_create(
                            name=city_details['city_name'],
                            city_code=city_details['city_code'],
                            phone_code=city_details['city_phone_code'],
                            population=city_details['population'],
                            avg_age=city_details['avg_age'],
                            num_of_adult_males=city_details['num_of_adult_males'],
                            num_of_adult_females=city_details['num_of_adult_females'],
                            state=state
                        )
                        created_cities[city_details['city_code']] = city

            return Response({"message": "Bulk insert successful"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class InsertOne(APIView):
    def post(self, request):
        data = request.data
        try:
            with transaction.atomic():
                country, _ = Country.objects.get_or_create(
                    country_code=data['country']['country_code'],
                    defaults={
                        "name": data['country']['country_name'],
                        "curr_symbol": data['country']['curr_symbol'],
                        "phone_code": data['country']['country_phone_code']
                    }
                )

                state, _ = State.objects.get_or_create(
                    state_code=data['state']['state_code'],
                    country=country,
                    defaults={
                        "name": data['state']['state_name'],
                        "gst_code": data['state']['gst_code']
                    }
                )

                city, created = City.objects.get_or_create(
                    city_code=data['city']['city_code'],
                    state=state,
                    defaults={
                        "name": data['city']['city_name'],
                        "phone_code": data['city']['city_phone_code'],
                        "population": data['city']['population'],
                        "avg_age": data['city']['avg_age'],
                        "num_of_adult_males": data['city']['num_of_adult_males'],
                        "num_of_adult_females": data['city']['num_of_adult_females']
                    }
                )

                if created:
                    return Response({"message": "City created successfully"}, status=201)
                else:
                    return Response({"message": "City already exists"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
