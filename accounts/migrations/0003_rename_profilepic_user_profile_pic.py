# Generated by Django 4.1.3 on 2023-01-01 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_address_user_date_of_birth_user_telephone_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profilepic',
            new_name='profile_pic',
        ),
    ]
