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

import json
from datetime import timedelta

from annoying.functions import get_object_or_None
from mock import patch
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from six.moves import range

from django.conf import settings
from django.utils import timezone

from silver.models import Invoice, Proforma, PDF
from silver.fixtures.factories import (
    AdminUserFactory,
    CustomerFactory,
    ProviderFactory,
    ProformaFactory,
    SubscriptionFactory,
)
from silver.tests.api.specs.document_entry import document_entry_definition
from silver.tests.utils import build_absolute_test_url

PAYMENT_DUE_DAYS = getattr(settings, "SILVER_DEFAULT_DUE_DAYS", 5)


class TestProformaEndpoints(APITestCase):
    def setUp(self):
        admin_user = AdminUserFactory.create()
        self.client.force_authenticate(user=admin_user)

    def test_post_proforma_without_proforma_entries(self):
        customer = CustomerFactory.create()
        provider = ProviderFactory.create()
        SubscriptionFactory.create()

        url = reverse("proforma-list")
        provider_url = build_absolute_test_url(
            reverse("provider-detail", [provider.pk])
        )
        customer_url = build_absolute_test_url(
            reverse("customer-detail", [customer.pk])
        )

        data = {
            "provider": provider_url,
            "customer": customer_url,
            "currency": "RON",
            "proforma_entries": [],
        }

        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED, response.data

        proforma = get_object_or_None(Proforma, id=response.data["id"])
        assert proforma

        assert response.data == {
            "id": response.data["id"],
            "series": "ProformaSeries",
            "number": None,
            "provider": provider_url,
            "customer": customer_url,
            "archived_provider": {},
            "archived_customer": {},
            "due_date": None,
            "issue_date": None,
            "paid_date": None,
            "cancel_date": None,
            "sales_tax_name": "VAT",
            "sales_tax_percent": "1.00",
            "currency": "RON",
            "transaction_currency": proforma.transaction_currency,
            "transaction_xe_rate": (
                str(proforma.transaction_xe_rate)
                if proforma.transaction_xe_rate
                else None
            ),
            "transaction_xe_date": proforma.transaction_xe_date,
            "pdf_url": None,
            "state": "draft",
            "invoice": None,
            "proforma_entries": [],
            "total": 0,
            "total_in_transaction_currency": 0,
            "transactions": [],
        }

    def test_post_proforma_with_proforma_entries(self):
        customer = CustomerFactory.create()
        provider = ProviderFactory.create()
        SubscriptionFactory.create()

        url = reverse("proforma-list")
        provider_url = build_absolute_test_url(
            reverse("provider-detail", [provider.pk])
        )
        customer_url = build_absolute_test_url(
            reverse("customer-detail", [customer.pk])
        )

        data = {
            "provider": provider_url,
            "customer": customer_url,
            "series": None,
            "number": None,
            "currency": "RON",
            "transaction_xe_rate": 1,
            "proforma_entries": [
                {"description": "Page views", "unit_price": 10.0, "quantity": 20}
            ],
        }

        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        # TODO: Check the body of the response. There were some problems
        # related to the invoice_entries list.

    def test_get_proformas(self):
        batch_size = 50
        ProformaFactory.create_batch(batch_size)

        url = reverse("proforma-list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

        response = self.client.get(url + "?page=2")

        assert response.status_code == status.HTTP_200_OK

    @patch("silver.api.serializers.common.settings")
    def test_get_proforma(self, mocked_settings):
        ProformaFactory.reset_sequence(1)

        upload_path = "%s/documents/" % settings.MEDIA_ROOT
        proforma = ProformaFactory.create(
            pdf=PDF.objects.create(upload_path=upload_path)
        )
        proforma.generate_pdf()

        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})

        for show_pdf_storage_url, pdf_url in [
            (True, build_absolute_test_url(proforma.pdf.url)),
            (False, build_absolute_test_url(reverse("pdf", args=[proforma.pdf.pk]))),
        ]:
            mocked_settings.SILVER_SHOW_PDF_STORAGE_URL = show_pdf_storage_url
            response = self.client.get(url)

            provider_url = build_absolute_test_url(
                reverse("provider-detail", [proforma.provider.pk])
            )
            customer_url = build_absolute_test_url(
                reverse("customer-detail", [proforma.customer.pk])
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.data,
                {
                    "id": proforma.pk,
                    "series": "ProformaSeries",
                    "number": proforma.number,
                    "provider": provider_url,
                    "customer": customer_url,
                    "archived_provider": {},
                    "archived_customer": {},
                    "due_date": None,
                    "issue_date": None,
                    "paid_date": None,
                    "cancel_date": None,
                    "sales_tax_name": "VAT",
                    "sales_tax_percent": "1.00",
                    "currency": "RON",
                    "transaction_currency": proforma.transaction_currency,
                    "transaction_xe_rate": (
                        "%.4f" % proforma.transaction_xe_rate
                        if proforma.transaction_xe_rate
                        else None
                    ),
                    "transaction_xe_date": proforma.transaction_xe_date,
                    "pdf_url": pdf_url,
                    "state": "draft",
                    "invoice": None,
                    "proforma_entries": [],
                    "total": 0,
                    "total_in_transaction_currency": 0,
                    "transactions": [],
                },
            )

    def test_delete_proforma(self):
        url = reverse("proforma-detail", kwargs={"pk": 1})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.data == {"detail": 'Method "DELETE" not allowed.'}

    def test_add_single_proforma_entry(self):
        proforma = ProformaFactory.create()

        url = reverse("proforma-entry-create", kwargs={"document_pk": proforma.pk})
        request_data = {"description": "Page views", "unit_price": 10.0, "quantity": 20}
        response = self.client.post(
            url, data=json.dumps(request_data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_201_CREATED, response.data

        entry = proforma.entries.get(id=response.data["id"])
        document_entry_definition.check_response(entry, response.data, request_data)

        # check proforma entries in new request
        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})
        response = self.client.get(url)

        proforma_entries = response.data.get("proforma_entries", [])
        assert len(proforma_entries) == 1
        document_entry_definition.check_response(
            entry, proforma_entries[0], request_data
        )

    def test_try_to_get_proforma_entries(self):
        url = reverse("proforma-entry-create", kwargs={"document_pk": 1})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.data == {"detail": 'Method "GET" not allowed.'}

    def test_add_multiple_proforma_entries(self):
        proforma = ProformaFactory.create()

        url = reverse("proforma-entry-create", kwargs={"document_pk": proforma.pk})
        request_data = {"description": "Page views", "unit_price": 10.0, "quantity": 20}

        entries_count = 5
        for cnt in range(entries_count):
            response = self.client.post(
                url, data=json.dumps(request_data), content_type="application/json"
            )

            assert response.status_code == status.HTTP_201_CREATED, response.data

            entry = proforma.entries.get(id=response.data["id"])
            document_entry_definition.check_response(entry, response.data, request_data)

        # check proforma entries in new request
        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})
        response = self.client.get(url)
        proforma_entries = response.data.get("proforma_entries", [])
        assert len(proforma_entries) == entries_count

    def test_delete_proforma_entry(self):
        proforma = ProformaFactory.create()

        url = reverse("proforma-entry-create", kwargs={"document_pk": proforma.pk})
        entry_data = {"description": "Page views", "unit_price": 10.0, "quantity": 20}
        entries_count = 10
        for cnt in range(entries_count):
            self.client.post(
                url, data=json.dumps(entry_data), content_type="application/json"
            )

        url = reverse(
            "proforma-entry-update",
            kwargs={
                "document_pk": proforma.pk,
                "entry_pk": list(proforma._entries)[0].pk,
            },
        )
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})
        response = self.client.get(url)
        invoice_entries = response.data.get("proforma_entries", None)
        assert len(invoice_entries) == entries_count - 1

    def test_add_proforma_entry_in_issued_state(self):
        proforma = ProformaFactory.create()
        proforma.issue()

        url = reverse("proforma-entry-create", kwargs={"document_pk": proforma.pk})
        entry_data = {"description": "Page views", "unit_price": 10.0, "quantity": 20}
        response = self.client.post(
            url, data=json.dumps(entry_data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        msg = "Proforma entries can be added only when the proforma is in draft state."
        assert response.data == {"detail": msg}

        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})
        response = self.client.get(url)
        invoice_entries = response.data.get("proforma_entries", None)
        assert len(invoice_entries) == 0

    def test_add_proforma_entry_in_canceled_state(self):
        proforma = ProformaFactory.create()
        proforma.issue()
        proforma.cancel()

        url = reverse("proforma-entry-create", kwargs={"document_pk": proforma.pk})
        entry_data = {"description": "Page views", "unit_price": 10.0, "quantity": 20}
        response = self.client.post(
            url, data=json.dumps(entry_data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        msg = "Proforma entries can be added only when the proforma is in draft state."
        assert response.data == {"detail": msg}

        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})
        response = self.client.get(url)
        invoice_entries = response.data.get("proforma_entries", None)
        assert len(invoice_entries) == 0

    def test_add_proforma_entry_in_paid_state(self):
        proforma = ProformaFactory.create()
        proforma.issue()
        proforma.pay()

        url = reverse("proforma-entry-create", kwargs={"document_pk": proforma.pk})
        entry_data = {"description": "Page views", "unit_price": 10.0, "quantity": 20}
        response = self.client.post(
            url, data=json.dumps(entry_data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        msg = "Proforma entries can be added only when the proforma is in draft state."
        assert response.data == {"detail": msg}

        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})
        response = self.client.get(url)
        invoice_entries = response.data.get("proforma_entries", None)
        assert len(invoice_entries) == 0

    def test_edit_proforma_in_issued_state(self):
        proforma = ProformaFactory.create()
        proforma.issue()

        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})
        data = {"description": "New Page views"}
        response = self.client.patch(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_message = "You cannot edit the document once it is in issued state."
        assert response.data == {"non_field_errors": [error_message]}

    def test_edit_proforma_in_canceled_state(self):
        proforma = ProformaFactory.create()
        proforma.issue()
        proforma.cancel()

        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})
        data = {"description": "New Page views"}
        response = self.client.patch(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_message = "You cannot edit the document once it is in canceled state."
        assert response.data == {"non_field_errors": [error_message]}

    def test_edit_proforma_in_paid_state(self):
        proforma = ProformaFactory.create()
        proforma.issue()
        proforma.pay()

        url = reverse("proforma-detail", kwargs={"pk": proforma.pk})
        data = {"description": "New Page views"}
        response = self.client.patch(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_message = "You cannot edit the document once it is in paid state."
        assert response.data == {"non_field_errors": [error_message]}

    def test_issue_proforma_with_default_dates(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "issued"}
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_200_OK
        due_date = timezone.now().date() + timedelta(days=PAYMENT_DUE_DAYS)
        mandatory_content = {
            "issue_date": timezone.now().date().strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "state": "issued",
        }
        assert response.status_code == status.HTTP_200_OK
        assert all(
            item in list(response.data.items()) for item in mandatory_content.items()
        )
        assert response.data.get("archived_provider", {}) != {}
        assert response.data.get("archived_customer", {}) != {}
        assert Invoice.objects.count() == 0

    def test_issue_proforma_with_custom_issue_date(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "issued", "issue_date": "2014-01-01"}
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_200_OK
        due_date = timezone.now().date() + timedelta(days=PAYMENT_DUE_DAYS)
        mandatory_content = {
            "issue_date": "2014-01-01",
            "due_date": due_date.strftime("%Y-%m-%d"),
            "state": "issued",
        }
        assert response.status_code == status.HTTP_200_OK
        assert all(
            item in list(response.data.items()) for item in mandatory_content.items()
        )
        assert response.data.get("archived_provider", {}) != {}
        assert response.data.get("archived_customer", {}) != {}
        assert Invoice.objects.count() == 0

        proforma = get_object_or_None(Proforma, pk=1)

    def test_issue_proforma_with_custom_issue_date_and_due_date(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "issued", "issue_date": "2014-01-01", "due_date": "2014-01-20"}

        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_200_OK
        mandatory_content = {
            "issue_date": "2014-01-01",
            "due_date": "2014-01-20",
            "state": "issued",
        }
        assert response.status_code == status.HTTP_200_OK
        assert all(
            item in list(response.data.items()) for item in mandatory_content.items()
        )
        assert response.data.get("archived_provider", {}) != {}
        assert response.data.get("archived_customer", {}) != {}
        assert Invoice.objects.count() == 0

        proforma = get_object_or_None(Proforma, pk=1)

    def test_issue_proforma_when_in_issued_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()

        invoices_count = Invoice.objects.count()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "issued"}
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {
            "detail": "A proforma can be issued only if it is in draft state."
        }
        assert Invoice.objects.count() == invoices_count

    def test_issue_proforma_when_in_paid_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()
        proforma.pay()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "issued"}
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {
            "detail": "A proforma can be issued only if it is in draft state."
        }
        assert Invoice.objects.count() == 1

    def test_pay_proforma_with_default_dates(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "paid"}
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        proforma.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        due_date = timezone.now().date() + timedelta(days=PAYMENT_DUE_DAYS)

        invoice_url = build_absolute_test_url(
            reverse("invoice-detail", [proforma.related_document.pk])
        )
        mandatory_content = {
            "issue_date": timezone.now().date().strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "paid_date": timezone.now().date().strftime("%Y-%m-%d"),
            "state": "paid",
            "invoice": invoice_url,
        }
        assert response.status_code == status.HTTP_200_OK
        assert all(
            item in list(response.data.items()) for item in mandatory_content.items()
        )

        invoice = Invoice.objects.all()[0]
        assert proforma.related_document == invoice
        assert invoice.related_document == proforma

    def test_pay_proforma_with_provided_date(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "paid", "paid_date": "2014-05-05"}
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        proforma.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        due_date = timezone.now().date() + timedelta(days=PAYMENT_DUE_DAYS)

        invoice_url = build_absolute_test_url(
            reverse("invoice-detail", [proforma.related_document.pk])
        )
        mandatory_content = {
            "issue_date": timezone.now().date().strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "paid_date": "2014-05-05",
            "state": "paid",
            "invoice": invoice_url,
        }
        assert response.status_code == status.HTTP_200_OK
        assert all(
            item in list(response.data.items()) for item in mandatory_content.items()
        )

        invoice = Invoice.objects.all()[0]
        assert proforma.related_document == invoice
        assert invoice.related_document == proforma

    def test_pay_proforma_when_in_draft_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "paid"}
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {
            "detail": "A proforma can be paid only if it is in issued state."
        }
        assert Invoice.objects.count() == 0

    def test_pay_proforma_when_in_paid_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()
        proforma.pay()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "paid"}
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {
            "detail": "A proforma can be paid only if it is in issued state."
        }
        assert Invoice.objects.count() == 1

    def test_cancel_proforma_with_default_dates(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "canceled"}
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_200_OK
        due_date = timezone.now().date() + timedelta(days=PAYMENT_DUE_DAYS)
        mandatory_content = {
            "issue_date": timezone.now().date().strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "cancel_date": timezone.now().date().strftime("%Y-%m-%d"),
            "state": "canceled",
        }
        assert response.status_code == status.HTTP_200_OK
        assert all(
            item in list(response.data.items()) for item in mandatory_content.items()
        )
        assert Invoice.objects.count() == 0

    def test_cancel_proforma_with_provided_date(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "canceled", "cancel_date": "2014-10-10"}

        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_200_OK
        due_date = timezone.now().date() + timedelta(days=PAYMENT_DUE_DAYS)
        mandatory_content = {
            "issue_date": timezone.now().date().strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "cancel_date": "2014-10-10",
            "state": "canceled",
        }
        assert response.status_code == status.HTTP_200_OK
        assert all(
            item in list(response.data.items()) for item in mandatory_content.items()
        )
        assert Invoice.objects.count() == 0

    def test_cancel_proforma_in_draft_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "canceled"}

        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        asserted_response = "A proforma can be canceled only if it is in issued state."
        assert response.data == {"detail": asserted_response}
        assert Invoice.objects.count() == 0

    def test_cancel_proforma_in_canceled_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()
        proforma.cancel()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "canceled"}

        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        asserted_response = "A proforma can be canceled only if it is in issued state."
        assert response.data == {"detail": asserted_response}
        assert Invoice.objects.count() == 0

    def test_cancel_proforma_in_paid_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()
        proforma.pay()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "canceled"}

        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        asserted_response = "A proforma can be canceled only if it is in issued state."
        assert response.data == {"detail": asserted_response}
        assert Invoice.objects.count() == 1

    def test_illegal_state_change_when_in_draft_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "illegal-state"}

        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {"detail": "Illegal state value."}
        assert Invoice.objects.count() == 0

    def test_illegal_state_change_when_in_issued_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "illegal-state"}

        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {"detail": "Illegal state value."}
        assert Invoice.objects.count() == 0

    def test_illegal_state_change_when_in_paid_state(self):
        provider = ProviderFactory.create()
        customer = CustomerFactory.create()
        proforma = ProformaFactory.create(provider=provider, customer=customer)
        proforma.issue()
        proforma.pay()

        url = reverse("proforma-state", kwargs={"pk": proforma.pk})
        data = {"state": "illegal-state"}

        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {"detail": "Illegal state value."}
        assert Invoice.objects.count() == 1
