# Generated by Django 4.2 on 2023-05-16 07:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("silver", "0057_alter_billingdocumentbase_id_alter_billinglog_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="refund_code",
            field=models.CharField(
                blank=True,
                choices=[
                    ("default", "default"),
                    ("duplicate", "duplicate"),
                    ("fraudulent", "fraudulent"),
                    ("requested_by_customer", "requested_by_customer"),
                ],
                max_length=32,
                null=True,
            ),
        ),
    ]
