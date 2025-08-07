from django.db import migrations
import random

def assign_random_users_to_countries(apps, schema_editor):
    Country = apps.get_model('Locations', 'Country')
    User = apps.get_model('Accounts', 'MyUser')

    users = list(User.objects.all())
    if not users:
        return

    for country in Country.objects.all():
        country.my_user = random.choice(users)
        country.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Locations', '0002_country_my_user'),
    ]

    operations = [
        migrations.RunPython(assign_random_users_to_countries),
    ]
