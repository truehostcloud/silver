# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-02 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ("silver", "0048_auto_20180816_0409"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="fail_code",
            field=models.CharField(
                blank=True,
                choices=[
                    (b"transaction_declined_by_bank", b"transaction_declined_by_bank"),
                    (b"transaction_hard_declined", b"transaction_hard_declined"),
                    (b"invalid_payment_method", b"invalid_payment_method"),
                    (b"expired_payment_method", b"expired_payment_method"),
                    (b"default", b"default"),
                    (b"invalid_card", b"invalid_card"),
                    (b"insufficient_funds", b"insufficient_funds"),
                    (b"transaction_declined", b"transaction_declined"),
                    (b"expired_card", b"expired_card"),
                    (
                        b"transaction_hard_declined_by_bank",
                        b"transaction_hard_declined_by_bank",
                    ),
                    (b"limit_exceeded", b"limit_exceeded"),
                ],
                max_length=32,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="state",
            field=django_fsm.FSMField(
                choices=[
                    ("canceled", "Canceled"),
                    ("refunded", "Refunded"),
                    ("initial", "Initial"),
                    ("failed", "Failed"),
                    ("settled", "Settled"),
                    ("pending", "Pending"),
                ],
                default="initial",
                max_length=8,
            ),
        ),
    ]
