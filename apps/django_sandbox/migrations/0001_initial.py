# Generated by Django 3.1a1 on 2020-06-19 14:27

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import common.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sandbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('url', models.CharField(max_length=2048, validators=[django.core.validators.URLValidator(schemes=['http', 'https'])])),
                ('enabled', models.BooleanField()),
                ('poll_usage_every', models.DurationField(default=60, validators=[
                    common.validators.MinDurationValidator(10)])),
                ('last_usage_poll', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SandboxUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('cpu_usage', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=4)),
                ('cpu_freq', models.FloatField()),
                ('memory_ram', models.BigIntegerField()),
                ('memory_swap', models.BigIntegerField()),
                ('memory_storage', models.JSONField()),
                ('writing_io', models.JSONField()),
                ('writing_bytes', models.JSONField()),
                ('reading_io', models.JSONField()),
                ('reading_bytes', models.JSONField()),
                ('sending_packets', models.BigIntegerField()),
                ('sending_bytes', models.BigIntegerField()),
                ('receiving_packets', models.BigIntegerField()),
                ('receiving_bytes', models.BigIntegerField()),
                ('process', models.PositiveSmallIntegerField()),
                ('container', models.PositiveSmallIntegerField()),
                ('sandbox', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usage', to='django_sandbox.sandbox')),
            ],
            options={
                'ordering': ['-date', 'sandbox'],
            },
        ),
        migrations.CreateModel(
            name='SandboxSpecs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polled', models.BooleanField(default=False)),
                ('sandbox_version', models.CharField(default=None, max_length=64, null=True)),
                ('docker_version', models.CharField(default=None, max_length=64, null=True)),
                ('cpu_core', models.PositiveSmallIntegerField(default=None, null=True)),
                ('cpu_logical', models.PositiveSmallIntegerField(default=None, null=True)),
                ('cpu_freq_min', models.FloatField(default=None, null=True)),
                ('cpu_freq_max', models.FloatField(default=None, null=True)),
                ('memory_ram', models.BigIntegerField(default=None, null=True)),
                ('memory_swap', models.BigIntegerField(default=None, null=True)),
                ('memory_storage', models.JSONField(default=None, null=True)),
                ('sandbox', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='server_specs', to='django_sandbox.sandbox')),
            ],
        ),
        migrations.CreateModel(
            name='ContainerSpecs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polled', models.BooleanField(default=False)),
                ('working_dir_device', models.CharField(default=None, max_length=128, null=True)),
                ('count', models.SmallIntegerField(default=None, null=True)),
                ('process', models.SmallIntegerField(default=None, null=True)),
                ('cpu_count', models.SmallIntegerField(default=None, null=True)),
                ('cpu_period', models.SmallIntegerField(default=None, null=True)),
                ('cpu_shares', models.SmallIntegerField(default=None, null=True)),
                ('cpu_quota', models.SmallIntegerField(default=None, null=True)),
                ('memory_ram', models.BigIntegerField(default=None, null=True)),
                ('memory_swap', models.BigIntegerField(default=None, null=True)),
                ('memory_storage', models.BigIntegerField(default=None, null=True)),
                ('writing_io', models.JSONField(default=None, null=True)),
                ('writing_bytes', models.JSONField(default=None, null=True)),
                ('reading_io', models.JSONField(default=None, null=True)),
                ('reading_bytes', models.JSONField(default=None, null=True)),
                ('libraries', models.JSONField(default=None, null=True)),
                ('bin', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), default=None, null=True, size=None)),
                ('sandbox', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='container_specs', to='django_sandbox.sandbox')),
            ],
        ),
        migrations.AddIndex(
            model_name='sandboxusage',
            index=models.Index(fields=['-date'], name='django_sand_date_20ccbc_idx'),
        ),
    ]
