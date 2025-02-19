# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-08 13:01
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import OuterRef, Subquery


def populate_billing_log_invoice_from_proforma(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    BillingLog = apps.get_model("silver", "BillingLog")
    Proforma = apps.get_model("silver", "Proforma")

    BillingLog.objects.using(db_alias).filter(invoice=None).update(
        invoice_id=Subquery(
            Proforma.objects.using(db_alias)
            .filter(id=OuterRef("proforma_id"))
            .values("related_document_id")[:1]
        )
    )


class Migration(migrations.Migration):
    dependencies = [
        ("silver", "0049_auto_20181102_1303"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billinglog",
            name="billing_date",
            field=models.DateField(
                help_text="The date when the invoice/proforma was generated."
            ),
        ),
        migrations.RunPython(
            populate_billing_log_invoice_from_proforma, migrations.RunPython.noop
        ),
    ]
