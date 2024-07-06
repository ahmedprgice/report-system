from django.db import migrations

def generate_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.create_superuser(email='admin@example.com', username='admin', password='admin')
    print('Superuser created!')

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_superuser),
    ]