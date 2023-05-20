# Generated by Django 4.1.3 on 2022-12-31 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='Address',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='Date_of_Birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='Marital_Status',
            field=models.CharField(blank=True, choices=[('Single', 'Single'), ('Marriage', 'Marriage'), ('Disvorce', 'Disvorce'), ('Engaged', 'Engaged'), ('Window', 'Window')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='Profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
