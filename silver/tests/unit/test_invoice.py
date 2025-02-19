# Copyright (c) 2015 Presslabs SRL
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

from datetime import date, timedelta
from decimal import Decimal

from six.moves import zip

from django.test import TestCase

from silver.models import DocumentEntry, Proforma, Invoice
from silver.fixtures.factories import (
    ProformaFactory,
    InvoiceFactory,
    DocumentEntryFactory,
    CustomerFactory,
)


class TestInvoice(TestCase):
    @staticmethod
    def test_pay_invoice_related_proforma_state_change_to_paid():
        proforma = ProformaFactory.create()
        proforma.issue()
        proforma.create_invoice()

        assert proforma.related_document.state == Invoice.STATES.ISSUED

        proforma.related_document.pay()

        assert proforma.related_document.state == Invoice.STATES.PAID
        assert proforma.state == Proforma.STATES.PAID

    @staticmethod
    def test_clone_invoice_into_draft():
        invoice = InvoiceFactory.create()
        invoice.issue()
        invoice.pay()

        entries = DocumentEntryFactory.create_batch(3)
        invoice.invoice_entries.add(*entries)

        clone = invoice.clone_into_draft()

        assert clone.state == Invoice.STATES.DRAFT
        assert clone.paid_date is None
        assert clone.issue_date is None
        assert clone.related_document is None
        assert clone.series != invoice.series or clone.number != invoice.number
        assert clone.sales_tax_percent == invoice.sales_tax_percent
        assert clone.sales_tax_name == invoice.sales_tax_name

        assert not clone.archived_customer
        assert not clone.archived_provider
        assert clone.customer == invoice.customer
        assert clone.provider == invoice.provider

        assert clone.currency == invoice.currency
        assert clone._last_state == clone.state
        assert clone.pk != invoice.pk
        assert clone.id != invoice.id
        assert not clone.pdf

        assert clone.invoice_entries.count() == 3
        assert invoice.invoice_entries.count() == 3

        entry_fields = [entry.name for entry in DocumentEntry._meta.get_fields()]
        for clone_entry, original_entry in zip(
            clone.invoice_entries.all(), invoice.invoice_entries.all()
        ):
            for entry in entry_fields:
                if entry not in ("id", "proforma", "invoice"):
                    assert getattr(clone_entry, entry) == getattr(original_entry, entry)
        assert invoice.state == Invoice.STATES.PAID

    @staticmethod
    def test_cancel_issued_invoice_with_related_proforma():
        proforma = ProformaFactory.create()
        proforma.issue()

        if not proforma.related_document:
            proforma.create_invoice()

        proforma.related_document.cancel()

        assert (
            proforma.related_document.state == proforma.state == Invoice.STATES.CANCELED
        )

    @staticmethod
    def _get_decimal_places(number):
        return max(0, -number.as_tuple().exponent)

    def test_invoice_total_decimal_points(self):
        invoice_entries = DocumentEntryFactory.create_batch(3)
        invoice = InvoiceFactory.create(invoice_entries=invoice_entries)

        assert self._get_decimal_places(invoice.total) == 2

    def test_invoice_total_before_tax_decimal_places(self):
        invoice_entries = DocumentEntryFactory.create_batch(3)
        invoice = InvoiceFactory.create(invoice_entries=invoice_entries)

        invoice.sales_tax_percent = Decimal("20.00")

        assert self._get_decimal_places(invoice.total_before_tax) == 2

    def test_invoice_tax_value_decimal_places(self):
        invoice_entries = DocumentEntryFactory.create_batch(3)
        invoice = InvoiceFactory.create(invoice_entries=invoice_entries)

        invoice.sales_tax_percent = Decimal("20.00")

        assert self._get_decimal_places(invoice.tax_value) == 2

    def test_invoice_total_with_tax_integrity(self):
        invoice_entries = DocumentEntryFactory.create_batch(5)
        invoice = InvoiceFactory.create(invoice_entries=invoice_entries)

        invoice.sales_tax_percent = Decimal("20.00")

        self.assertEqual(invoice.total, invoice.total_before_tax + invoice.tax_value)

    @staticmethod
    def test_draft_invoice_series_number():
        invoice = InvoiceFactory.create()
        invoice.number = None

        assert invoice.series_number == "%s-draft-id:%d" % (invoice.series, invoice.pk)

        invoice.series = None

        assert invoice.series_number == "draft-id:%d" % invoice.pk

    @staticmethod
    def test_issues_invoice_series_number():
        invoice = InvoiceFactory.create(state=Invoice.STATES.ISSUED)

        assert invoice.series_number == "%s-%s" % (invoice.series, invoice.number)

    @staticmethod
    def test_invoice_due_today_queryset():
        invoices = InvoiceFactory.create_batch(5)

        invoices[0].due_date = date.today()
        invoices[0].save()

        invoices[1].due_date = date.today()
        invoices[1].issue()

        invoices[2].due_date = date.today() - timedelta(days=1)
        invoices[2].issue()
        invoices[2].pay()

        invoices[3].due_date = date.today()
        invoices[3].issue()
        invoices[3].cancel()

        invoices[4].due_date = date.today() + timedelta(days=1)
        invoices[4].issue()

        queryset = Invoice.objects.due_today()

        assert queryset.count() == 1
        assert invoices[1] in queryset

    @staticmethod
    def test_invoice_due_this_month_queryset():
        invoices = InvoiceFactory.create_batch(4)

        invoices[0].due_date = date.today().replace(day=20)
        invoices[0].issue()

        invoices[1].due_date = date.today().replace(day=1)
        invoices[1].issue()

        invoices[2].due_date = date.today() - timedelta(days=31)
        invoices[2].issue()

        invoices[3].issue()
        invoices[3].cancel()

        queryset = Invoice.objects.due_this_month()

        assert queryset.count() == 2
        for invoice in invoices[:2]:
            assert invoice in queryset

    @staticmethod
    def test_invoice_overdue_queryset():
        invoices = InvoiceFactory.create_batch(3)

        invoices[0].due_date = date.today() - timedelta(days=1)
        invoices[0].issue()

        invoices[1].due_date = date.today() - timedelta(days=3)
        invoices[1].issue()

        invoices[2].due_date = date.today() - timedelta(days=31)
        invoices[2].issue()
        invoices[2].pay()

        queryset = Invoice.objects.overdue()

        assert queryset.count() == 2
        for invoice in invoices[:2]:
            assert invoice in queryset

    @staticmethod
    def test_invoice_overdue_since_last_month_queryset():
        invoices = InvoiceFactory.create_batch(3)

        invoices[0].due_date = date.today().replace(day=1)
        invoices[0].issue()

        invoices[1].due_date = date.today() - timedelta(days=31)
        invoices[1].issue()

        queryset = Invoice.objects.overdue_since_last_month()

        assert queryset.count() == 1
        assert invoices[1] in queryset

    def test_customer_currency_used_for_transaction_currency(self):
        customer = CustomerFactory.create(currency="EUR")
        invoice = InvoiceFactory.create(customer=customer, transaction_currency=None)

        self.assertEqual(invoice.transaction_currency, "EUR")

    def test_invoice_currency_used_for_transaction_currency(self):
        customer = CustomerFactory.create(currency=None)
        invoice = InvoiceFactory.create(
            customer=customer, currency="EUR", transaction_currency=None
        )

        self.assertEqual(invoice.transaction_currency, "EUR")

    @staticmethod
    def test_invoice_create_storno_from_canceled_state():
        invoice = InvoiceFactory.create(invoice_entries=[DocumentEntryFactory.create()])
        invoice.issue()
        invoice.cancel()
        storno = invoice.create_storno()

        assert -invoice.total == storno.total != 0
        assert storno.related_document == invoice
        assert invoice.customer == storno.customer
        assert invoice.provider == storno.provider

    @staticmethod
    def test_invoice_create_storno_from_paid_state():
        invoice = InvoiceFactory.create(invoice_entries=[DocumentEntryFactory.create()])
        invoice.issue()
        invoice.pay()
        storno = invoice.create_storno()

        assert -invoice.total == storno.total != 0
        assert storno.related_document == invoice
        assert invoice.customer == storno.customer
        assert invoice.provider == storno.provider

    def test_invoice_create_storno_from_unallowed_states(self):
        invoice = InvoiceFactory.create()
        assert invoice.state == invoice.STATES.DRAFT
        self.assertRaises(ValueError, invoice.create_storno)

        invoice.issue()
        self.assertRaises(ValueError, invoice.create_storno)

    @staticmethod
    def test_invoice_storno_issue():
        invoice = InvoiceFactory.create()
        invoice.issue()
        invoice.pay()
        storno = invoice.create_storno()

        storno.issue()
        assert storno.state == storno.STATES.ISSUED
        assert storno.issue_date == date.today()
        assert not storno.due_date
