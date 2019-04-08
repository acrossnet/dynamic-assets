# Generated by Django 2.0.13 on 2019-04-08 09:10

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(50)])),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default={})),
            ],
        ),
        migrations.CreateModel(
            name='AssetClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(20)])),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(20)])),
                ('asset_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='assets.AssetClass')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(20)])),
            ],
        ),
        migrations.AddField(
            model_name='assetclass',
            name='domain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset_classes', to='assets.Domain'),
        ),
        migrations.AddField(
            model_name='asset',
            name='kls',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='assets.AssetClass'),
        ),
        migrations.AddField(
            model_name='asset',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='assets.Asset'),
        ),
    ]