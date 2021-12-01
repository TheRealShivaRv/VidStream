# Generated by Django 3.0.8 on 2020-08-21 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256, unique=True)),
                ('email', models.CharField(max_length=256)),
                ('requestid', models.CharField(max_length=256)),
                ('purpose', models.CharField(max_length=256)),
            ],
        ),
    ]
