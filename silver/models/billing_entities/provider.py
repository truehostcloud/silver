# Copyright (c) 2016 Presslabs SRL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from model_utils import Choices

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _

from silver.models.billing_entities.base import BaseBillingEntity


PAYMENT_DUE_DAYS = getattr(settings, "SILVER_DEFAULT_DUE_DAYS", 5)


class Provider(BaseBillingEntity):
    class FLOWS(object):
        PROFORMA = "proforma"
        INVOICE = "invoice"

    FLOW_CHOICES = Choices(
        (FLOWS.PROFORMA, _("Proforma")),
        (FLOWS.INVOICE, _("Invoice")),
    )

    class DEFAULT_DOC_STATE(object):
        DRAFT = "draft"
        ISSUED = "issued"

    DOCUMENT_DEFAULT_STATE = Choices(
        (DEFAULT_DOC_STATE.DRAFT, _("Draft")), (DEFAULT_DOC_STATE.ISSUED, _("Issued"))
    )

    class Meta:
        index_together = (("name", "company"),)
        ordering = ["name", "company"]

    name = models.CharField(
        max_length=128, help_text="The name to be used for billing purposes."
    )
    flow = models.CharField(
        max_length=10,
        choices=FLOW_CHOICES,
        default=FLOWS.PROFORMA,
        help_text="One of the available workflows for generating proformas "
        "and invoices (see the documentation for more details).",
    )
    invoice_series = models.CharField(
        max_length=20,
        help_text="The series that will be used on every invoice generated by "
        "this provider.",
    )
    invoice_starting_number = models.PositiveIntegerField()
    proforma_series = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="The series that will be used on every proforma generated by "
        "this provider.",
    )
    proforma_starting_number = models.PositiveIntegerField(blank=True, null=True)
    default_document_state = models.CharField(
        max_length=10,
        choices=DOCUMENT_DEFAULT_STATE,
        default=DOCUMENT_DEFAULT_STATE.draft,
        help_text="The default state of the auto-generated documents.",
    )
    generate_documents_on_trial_end = models.BooleanField(
        default=True,
        help_text="If this is set to True, then billing documents will be generated when the "
        "subscription trial ends, instead of waiting for the end of the billing cycle.",
    )
    separate_cycles_during_trial = models.BooleanField(
        default=False,
        help_text="If this is set to True, then the trial period cycle will be split if it spans "
        "across multiple billing intervals.",
    )
    prebill_plan = models.BooleanField(
        default=True,
        help_text="If this is set to True, then the plan base amount will be billed at the"
        "beginning of the billing cycle rather than after the end.",
    )
    cycle_billing_duration = models.DurationField(
        null=True,
        blank=True,
        help_text="This can be used to ensure that the billing date doesn't pass a certain date.\n"
        "For example if this field is set to 2 days, for a monthly subscription, the "
        "billing date will never surpass the 2nd day of the month. Billing documents can "
        "still be generated after that day during the billing cycle, but their billing "
        "date will appear to be the end of the cycle billing duration.",
    )

    def __init__(self, *args, **kwargs):
        super(Provider, self).__init__(*args, **kwargs)
        company_field = self._meta.get_field("company")
        company_field.help_text = "The provider issuing the invoice."

    def clean(self):
        if self.flow == self.FLOWS.PROFORMA:
            if not self.proforma_starting_number and not self.proforma_series:
                errors = {
                    "proforma_series": "This field is required as the "
                    "chosen flow is proforma.",
                    "proforma_starting_number": "This field is required "
                    "as the chosen flow is "
                    "proforma.",
                }
                raise ValidationError(errors)
            if not self.proforma_series:
                errors = {
                    "proforma_series": "This field is required as the "
                    "chosen flow is proforma."
                }
                raise ValidationError(errors)
            if not self.proforma_starting_number:
                errors = {
                    "proforma_starting_number": "This field is required "
                    "as the chosen flow is "
                    "proforma."
                }
                raise ValidationError(errors)

    def get_archivable_field_values(self):
        base_fields = super(Provider, self).get_archivable_field_values()
        provider_fields = ["name", "invoice_series", "proforma_series"]
        fields_dict = {field: getattr(self, field, "") for field in provider_fields}
        base_fields.update(fields_dict)
        return base_fields

    @property
    def admin_change_url(self):
        display = escape(self.name)
        if self.company and self.name != self.company:
            display += "<hr> " + escape(self.company)

        link = reverse("admin:silver_provider_change", args=[self.pk])
        return '<a href="%s">%s</a>' % (link, display)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Provider)
def update_draft_billing_documents(sender, instance, **kwargs):
    Invoice = apps.get_model("silver", "Invoice")
    Proforma = apps.get_model("silver", "Proforma")

    if instance.pk and not kwargs.get("raw", False):
        provider = Provider.objects.get(pk=instance.pk)
        old_invoice_series = provider.invoice_series
        old_proforma_series = provider.proforma_series

        if instance.invoice_series != old_invoice_series:
            for invoice in Invoice.objects.filter(state="draft", provider=provider):
                # update the series for draft invoices
                invoice.series = instance.invoice_series
                invoice.number = None
                invoice.save()

        if instance.proforma_series != old_proforma_series:
            for proforma in Proforma.objects.filter(state="draft", provider=provider):
                # update the series for draft invoices
                proforma.series = instance.proforma_series
                proforma.number = None
                proforma.save()
