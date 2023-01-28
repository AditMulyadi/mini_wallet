# Generated by Django 4.1.5 on 2023-01-28 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transaction_reference_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='reference_id',
            field=models.TextField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together={('type', 'reference_id')},
        ),
    ]
