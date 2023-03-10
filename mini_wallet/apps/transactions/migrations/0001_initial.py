# Generated by Django 4.1.5 on 2023-01-28 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wallets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'deposit'), (2, 'withdrawal')])),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'success'), (2, 'fail')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('reference_id', models.TextField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='wallets.wallet')),
            ],
            options={
                'unique_together': {('type', 'reference_id')},
            },
        ),
    ]
