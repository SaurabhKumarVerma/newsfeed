# Generated by Django 2.2.16 on 2020-10-11 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short_txt', models.TextField()),
                ('body_txt', models.TextField()),
                ('date', models.CharField(max_length=12)),
                ('time', models.CharField(default='00:00', max_length=12)),
                ('pic', models.TextField()),
                ('picurl', models.TextField(default='-')),
                ('writer', models.CharField(max_length=50)),
                ('catname', models.CharField(default='-', max_length=50)),
                ('catid', models.IntegerField(default=0)),
                ('ocatid', models.IntegerField(default=0)),
                ('show', models.IntegerField(default=0)),
                ('tag', models.TextField(default='-')),
                ('act', models.IntegerField(default=0)),
            ],
        ),
    ]
