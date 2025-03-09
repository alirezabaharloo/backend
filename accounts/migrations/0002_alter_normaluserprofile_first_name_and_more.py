# Generated by Django 5.1.5 on 2025-01-27 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normaluserprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='normaluserprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='normaluserprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='selleruserprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='selleruserprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='selleruserprofile',
            name='phone_number',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
