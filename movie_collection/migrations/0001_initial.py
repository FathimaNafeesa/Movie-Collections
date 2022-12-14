# Generated by Django 4.1.4 on 2022-12-25 07:05

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=200)),
                ('description', models.CharField(default=None, max_length=200)),
                ('genres', models.CharField(default=None, max_length=20000)),
                ('uuid', models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RequestsCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hits', models.IntegerField()),
                ('count', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calls', to='movie_collection.requestscounter')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_name', models.CharField(max_length=200)),
                ('collection_description', models.CharField(default='-', max_length=20000)),
                ('title', models.CharField(default=None, max_length=200)),
                ('description', models.CharField(default=None, max_length=200000)),
                ('genres', models.CharField(default=None, max_length=20000)),
                ('uuid', models.UUIDField()),
                ('collection_uuid', models.UUIDField()),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='movie_collection.user')),
            ],
        ),
    ]
