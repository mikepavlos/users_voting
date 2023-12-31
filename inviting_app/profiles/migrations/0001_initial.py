# Generated by Django 4.2.4 on 2023-08-29 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_code', models.CharField(max_length=6, unique=True, verbose_name='Инвайт код')),
                ('activated_invite', models.CharField(default=None, max_length=6, null=True, verbose_name='Активированный код другого участника')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
