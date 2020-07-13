# Generated by Django 3.1b1 on 2020-07-13 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_sandbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sandboxexecution',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='executions', to=settings.AUTH_USER_MODEL),
        ),
    ]
