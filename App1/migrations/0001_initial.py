# Generated by Django 4.1.7 on 2023-04-06 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('qty', models.IntegerField()),
                ('price', models.FloatField()),
                ('author', models.CharField(max_length=250)),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'book',
            },
        ),
    ]
