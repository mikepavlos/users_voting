# Generated by Django 4.2.4 on 2023-08-24 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_code', models.CharField(max_length=6, unique=True, verbose_name='Инвайт код')),
                ('activated_invite', models.CharField(default=None, max_length=6, null=True, verbose_name='Активированный код другого участника')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.AddConstraint(
            model_name='profile',
            constraint=models.CheckConstraint(check=models.Q(('activated_invite', models.F('invite_code')), _negated=True), name='self_invite'),
        ),
    ]