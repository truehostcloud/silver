# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("silver", "0009_auto_20150717_1428"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="currency",
            field=models.CharField(
                blank=True,
                max_length=4,
                null=True,
                help_text=b"Used to enforce a certain currency when making transactionsfor the customer.",
                choices=[
                    ("AED", "UAE Dirham"),
                    ("AFN", "Afghani"),
                    ("ALL", "Lek"),
                    ("AMD", "Armenian Dram"),
                    ("ANG", "Netherlands Antillean Guilder"),
                    ("AOA", "Kwanza"),
                    ("ARS", "Argentine Peso"),
                    ("AUD", "Australian Dollar"),
                    ("AWG", "Aruban Florin"),
                    ("AZN", "Azerbaijanian Manat"),
                    ("BAM", "Convertible Mark"),
                    ("BBD", "Barbados Dollar"),
                    ("BDT", "Taka"),
                    ("BGN", "Bulgarian Lev"),
                    ("BHD", "Bahraini Dinar"),
                    ("BIF", "Burundi Franc"),
                    ("BMD", "Bermudian Dollar"),
                    ("BND", "Brunei Dollar"),
                    ("BOB", "Boliviano"),
                    ("BRL", "Brazilian Real"),
                    ("BSD", "Bahamian Dollar"),
                    ("BTN", "Ngultrum"),
                    ("BWP", "Pula"),
                    ("BYR", "Belarusian Ruble"),
                    ("BZD", "Belize Dollar"),
                    ("CAD", "Canadian Dollar"),
                    ("CDF", "Congolese Franc"),
                    ("CHF", "Swiss Franc"),
                    ("CLP", "Chilean Peso"),
                    ("CNY", "Yuan Renminbi"),
                    ("COP", "Colombian Peso"),
                    ("CRC", "Costa Rican Colon"),
                    ("CUC", "Peso Convertible"),
                    ("CUP", "Cuban Peso"),
                    ("CVE", "Cabo Verde Escudo"),
                    ("CZK", "Czech Koruna"),
                    ("DJF", "Djibouti Franc"),
                    ("DKK", "Danish Krone"),
                    ("DOP", "Dominican Peso"),
                    ("DZD", "Algerian Dinar"),
                    ("EGP", "Egyptian Pound"),
                    ("ERN", "Nakfa"),
                    ("ETB", "Ethiopian Birr"),
                    ("EUR", "Euro"),
                    ("FJD", "Fiji Dollar"),
                    ("FKP", "Falkland Islands Pound"),
                    ("GBP", "Pound Sterling"),
                    ("GEL", "Lari"),
                    ("GHS", "Ghana Cedi"),
                    ("GIP", "Gibraltar Pound"),
                    ("GMD", "Dalasi"),
                    ("GNF", "Guinea Franc"),
                    ("GTQ", "Quetzal"),
                    ("GYD", "Guyana Dollar"),
                    ("HKD", "Hong Kong Dollar"),
                    ("HNL", "Lempira"),
                    ("HRK", "Kuna"),
                    ("HTG", "Gourde"),
                    ("HUF", "Forint"),
                    ("IDR", "Rupiah"),
                    ("ILS", "New Israeli Sheqel"),
                    ("INR", "Indian Rupee"),
                    ("IQD", "Iraqi Dinar"),
                    ("IRR", "Iranian Rial"),
                    ("ISK", "Iceland Krona"),
                    ("JMD", "Jamaican Dollar"),
                    ("JOD", "Jordanian Dinar"),
                    ("JPY", "Yen"),
                    ("KES", "Kenyan Shilling"),
                    ("KGS", "Som"),
                    ("KHR", "Riel"),
                    ("KMF", "Comoro Franc"),
                    ("KPW", "North Korean Won"),
                    ("KRW", "Won"),
                    ("KWD", "Kuwaiti Dinar"),
                    ("KYD", "Cayman Islands Dollar"),
                    ("KZT", "Tenge"),
                    ("LAK", "Kip"),
                    ("LBP", "Lebanese Pound"),
                    ("LKR", "Sri Lanka Rupee"),
                    ("LRD", "Liberian Dollar"),
                    ("LSL", "Loti"),
                    ("LYD", "Libyan Dinar"),
                    ("MAD", "Moroccan Dirham"),
                    ("MDL", "Moldovan Leu"),
                    ("MGA", "Malagasy Ariary"),
                    ("MKD", "Denar"),
                    ("MMK", "Kyat"),
                    ("MNT", "Tugrik"),
                    ("MOP", "Pataca"),
                    ("MRO", "Ouguiya"),
                    ("MUR", "Mauritius Rupee"),
                    ("MVR", "Rufiyaa"),
                    ("MWK", "Malawi Kwacha"),
                    ("MXN", "Mexican Peso"),
                    ("MYR", "Malaysian Ringgit"),
                    ("MZN", "Mozambique Metical"),
                    ("NAD", "Namibia Dollar"),
                    ("NGN", "Naira"),
                    ("NIO", "Cordoba Oro"),
                    ("NOK", "Norwegian Krone"),
                    ("NPR", "Nepalese Rupee"),
                    ("NZD", "New Zealand Dollar"),
                    ("OMR", "Rial Omani"),
                    ("PAB", "Balboa"),
                    ("PEN", "Sol"),
                    ("PGK", "Kina"),
                    ("PHP", "Philippine Peso"),
                    ("PKR", "Pakistan Rupee"),
                    ("PLN", "Zloty"),
                    ("PYG", "Guarani"),
                    ("QAR", "Qatari Rial"),
                    ("RON", "Romanian Leu"),
                    ("RSD", "Serbian Dinar"),
                    ("RUB", "Russian Ruble"),
                    ("RWF", "Rwanda Franc"),
                    ("SAR", "Saudi Riyal"),
                    ("SBD", "Solomon Islands Dollar"),
                    ("SCR", "Seychelles Rupee"),
                    ("SDG", "Sudanese Pound"),
                    ("SEK", "Swedish Krona"),
                    ("SGD", "Singapore Dollar"),
                    ("SHP", "Saint Helena Pound"),
                    ("SLL", "Leone"),
                    ("SOS", "Somali Shilling"),
                    ("SRD", "Surinam Dollar"),
                    ("SSP", "South Sudanese Pound"),
                    ("STD", "Dobra"),
                    ("SVC", "El Salvador Colon"),
                    ("SYP", "Syrian Pound"),
                    ("SZL", "Lilangeni"),
                    ("THB", "Baht"),
                    ("TJS", "Somoni"),
                    ("TMT", "Turkmenistan New Manat"),
                    ("TND", "Tunisian Dinar"),
                    ("TOP", "Pa\u2019anga"),
                    ("TRY", "Turkish Lira"),
                    ("TTD", "Trinidad and Tobago Dollar"),
                    ("TWD", "New Taiwan Dollar"),
                    ("TZS", "Tanzanian Shilling"),
                    ("UAH", "Hryvnia"),
                    ("UGX", "Uganda Shilling"),
                    ("USD", "US Dollar"),
                    ("UYU", "Peso Uruguayo"),
                    ("UZS", "Uzbekistan Sum"),
                    ("VEF", "Bol\xedvar"),
                    ("VND", "Dong"),
                    ("VUV", "Vatu"),
                    ("WST", "Tala"),
                    ("XAF", "CFA Franc BEAC"),
                    ("XAG", "Silver"),
                    ("XAU", "Gold"),
                    ("XBA", "Bond Markets Unit European Composite Unit (EURCO)"),
                    ("XBB", "Bond Markets Unit European Monetary Unit (E.M.U.-6)"),
                    ("XBC", "Bond Markets Unit European Unit of Account 9 (E.U.A.-9)"),
                    (
                        "XBD",
                        "Bond Markets Unit European Unit of Account 17 (E.U.A.-17)",
                    ),
                    ("XCD", "East Caribbean Dollar"),
                    ("XDR", "SDR (Special Drawing Right)"),
                    ("XOF", "CFA Franc BCEAO"),
                    ("XPD", "Palladium"),
                    ("XPF", "CFP Franc"),
                    ("XPT", "Platinum"),
                    ("XSU", "Sucre"),
                    ("XTS", "Codes specifically reserved for testing purposes"),
                    ("XUA", "ADB Unit of Account"),
                    (
                        "XXX",
                        "The codes assigned for transactions where no currency is involved",
                    ),
                    ("YER", "Yemeni Rial"),
                    ("ZAR", "Rand"),
                    ("ZMW", "Zambian Kwacha"),
                    ("ZWL", "Zimbabwe Dollar"),
                ],
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="transaction_currency",
            field=models.CharField(
                default="USD",
                help_text=b"The currency used when making a transaction.",
                max_length=4,
                choices=[
                    ("AED", "UAE Dirham"),
                    ("AFN", "Afghani"),
                    ("ALL", "Lek"),
                    ("AMD", "Armenian Dram"),
                    ("ANG", "Netherlands Antillean Guilder"),
                    ("AOA", "Kwanza"),
                    ("ARS", "Argentine Peso"),
                    ("AUD", "Australian Dollar"),
                    ("AWG", "Aruban Florin"),
                    ("AZN", "Azerbaijanian Manat"),
                    ("BAM", "Convertible Mark"),
                    ("BBD", "Barbados Dollar"),
                    ("BDT", "Taka"),
                    ("BGN", "Bulgarian Lev"),
                    ("BHD", "Bahraini Dinar"),
                    ("BIF", "Burundi Franc"),
                    ("BMD", "Bermudian Dollar"),
                    ("BND", "Brunei Dollar"),
                    ("BOB", "Boliviano"),
                    ("BRL", "Brazilian Real"),
                    ("BSD", "Bahamian Dollar"),
                    ("BTN", "Ngultrum"),
                    ("BWP", "Pula"),
                    ("BYR", "Belarusian Ruble"),
                    ("BZD", "Belize Dollar"),
                    ("CAD", "Canadian Dollar"),
                    ("CDF", "Congolese Franc"),
                    ("CHF", "Swiss Franc"),
                    ("CLP", "Chilean Peso"),
                    ("CNY", "Yuan Renminbi"),
                    ("COP", "Colombian Peso"),
                    ("CRC", "Costa Rican Colon"),
                    ("CUC", "Peso Convertible"),
                    ("CUP", "Cuban Peso"),
                    ("CVE", "Cabo Verde Escudo"),
                    ("CZK", "Czech Koruna"),
                    ("DJF", "Djibouti Franc"),
                    ("DKK", "Danish Krone"),
                    ("DOP", "Dominican Peso"),
                    ("DZD", "Algerian Dinar"),
                    ("EGP", "Egyptian Pound"),
                    ("ERN", "Nakfa"),
                    ("ETB", "Ethiopian Birr"),
                    ("EUR", "Euro"),
                    ("FJD", "Fiji Dollar"),
                    ("FKP", "Falkland Islands Pound"),
                    ("GBP", "Pound Sterling"),
                    ("GEL", "Lari"),
                    ("GHS", "Ghana Cedi"),
                    ("GIP", "Gibraltar Pound"),
                    ("GMD", "Dalasi"),
                    ("GNF", "Guinea Franc"),
                    ("GTQ", "Quetzal"),
                    ("GYD", "Guyana Dollar"),
                    ("HKD", "Hong Kong Dollar"),
                    ("HNL", "Lempira"),
                    ("HRK", "Kuna"),
                    ("HTG", "Gourde"),
                    ("HUF", "Forint"),
                    ("IDR", "Rupiah"),
                    ("ILS", "New Israeli Sheqel"),
                    ("INR", "Indian Rupee"),
                    ("IQD", "Iraqi Dinar"),
                    ("IRR", "Iranian Rial"),
                    ("ISK", "Iceland Krona"),
                    ("JMD", "Jamaican Dollar"),
                    ("JOD", "Jordanian Dinar"),
                    ("JPY", "Yen"),
                    ("KES", "Kenyan Shilling"),
                    ("KGS", "Som"),
                    ("KHR", "Riel"),
                    ("KMF", "Comoro Franc"),
                    ("KPW", "North Korean Won"),
                    ("KRW", "Won"),
                    ("KWD", "Kuwaiti Dinar"),
                    ("KYD", "Cayman Islands Dollar"),
                    ("KZT", "Tenge"),
                    ("LAK", "Kip"),
                    ("LBP", "Lebanese Pound"),
                    ("LKR", "Sri Lanka Rupee"),
                    ("LRD", "Liberian Dollar"),
                    ("LSL", "Loti"),
                    ("LYD", "Libyan Dinar"),
                    ("MAD", "Moroccan Dirham"),
                    ("MDL", "Moldovan Leu"),
                    ("MGA", "Malagasy Ariary"),
                    ("MKD", "Denar"),
                    ("MMK", "Kyat"),
                    ("MNT", "Tugrik"),
                    ("MOP", "Pataca"),
                    ("MRO", "Ouguiya"),
                    ("MUR", "Mauritius Rupee"),
                    ("MVR", "Rufiyaa"),
                    ("MWK", "Malawi Kwacha"),
                    ("MXN", "Mexican Peso"),
                    ("MYR", "Malaysian Ringgit"),
                    ("MZN", "Mozambique Metical"),
                    ("NAD", "Namibia Dollar"),
                    ("NGN", "Naira"),
                    ("NIO", "Cordoba Oro"),
                    ("NOK", "Norwegian Krone"),
                    ("NPR", "Nepalese Rupee"),
                    ("NZD", "New Zealand Dollar"),
                    ("OMR", "Rial Omani"),
                    ("PAB", "Balboa"),
                    ("PEN", "Sol"),
                    ("PGK", "Kina"),
                    ("PHP", "Philippine Peso"),
                    ("PKR", "Pakistan Rupee"),
                    ("PLN", "Zloty"),
                    ("PYG", "Guarani"),
                    ("QAR", "Qatari Rial"),
                    ("RON", "Romanian Leu"),
                    ("RSD", "Serbian Dinar"),
                    ("RUB", "Russian Ruble"),
                    ("RWF", "Rwanda Franc"),
                    ("SAR", "Saudi Riyal"),
                    ("SBD", "Solomon Islands Dollar"),
                    ("SCR", "Seychelles Rupee"),
                    ("SDG", "Sudanese Pound"),
                    ("SEK", "Swedish Krona"),
                    ("SGD", "Singapore Dollar"),
                    ("SHP", "Saint Helena Pound"),
                    ("SLL", "Leone"),
                    ("SOS", "Somali Shilling"),
                    ("SRD", "Surinam Dollar"),
                    ("SSP", "South Sudanese Pound"),
                    ("STD", "Dobra"),
                    ("SVC", "El Salvador Colon"),
                    ("SYP", "Syrian Pound"),
                    ("SZL", "Lilangeni"),
                    ("THB", "Baht"),
                    ("TJS", "Somoni"),
                    ("TMT", "Turkmenistan New Manat"),
                    ("TND", "Tunisian Dinar"),
                    ("TOP", "Pa\u2019anga"),
                    ("TRY", "Turkish Lira"),
                    ("TTD", "Trinidad and Tobago Dollar"),
                    ("TWD", "New Taiwan Dollar"),
                    ("TZS", "Tanzanian Shilling"),
                    ("UAH", "Hryvnia"),
                    ("UGX", "Uganda Shilling"),
                    ("USD", "US Dollar"),
                    ("UYU", "Peso Uruguayo"),
                    ("UZS", "Uzbekistan Sum"),
                    ("VEF", "Bol\xedvar"),
                    ("VND", "Dong"),
                    ("VUV", "Vatu"),
                    ("WST", "Tala"),
                    ("XAF", "CFA Franc BEAC"),
                    ("XAG", "Silver"),
                    ("XAU", "Gold"),
                    ("XBA", "Bond Markets Unit European Composite Unit (EURCO)"),
                    ("XBB", "Bond Markets Unit European Monetary Unit (E.M.U.-6)"),
                    ("XBC", "Bond Markets Unit European Unit of Account 9 (E.U.A.-9)"),
                    (
                        "XBD",
                        "Bond Markets Unit European Unit of Account 17 (E.U.A.-17)",
                    ),
                    ("XCD", "East Caribbean Dollar"),
                    ("XDR", "SDR (Special Drawing Right)"),
                    ("XOF", "CFA Franc BCEAO"),
                    ("XPD", "Palladium"),
                    ("XPF", "CFP Franc"),
                    ("XPT", "Platinum"),
                    ("XSU", "Sucre"),
                    ("XTS", "Codes specifically reserved for testing purposes"),
                    ("XUA", "ADB Unit of Account"),
                    (
                        "XXX",
                        "The codes assigned for transactions where no currency is involved",
                    ),
                    ("YER", "Yemeni Rial"),
                    ("ZAR", "Rand"),
                    ("ZMW", "Zambian Kwacha"),
                    ("ZWL", "Zimbabwe Dollar"),
                ],
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="transaction_xe_date",
            field=models.DateField(
                help_text=b"Date of the transaction exchange rate.",
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="transaction_xe_rate",
            field=models.DecimalField(
                decimal_places=4,
                default=1,
                max_digits=16,
                blank=True,
                help_text=b"Currency exchange rate from document currency to transaction_currency.",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="proforma",
            name="transaction_currency",
            field=models.CharField(
                default="USD",
                help_text=b"The currency used when making a transaction.",
                max_length=4,
                choices=[
                    ("AED", "UAE Dirham"),
                    ("AFN", "Afghani"),
                    ("ALL", "Lek"),
                    ("AMD", "Armenian Dram"),
                    ("ANG", "Netherlands Antillean Guilder"),
                    ("AOA", "Kwanza"),
                    ("ARS", "Argentine Peso"),
                    ("AUD", "Australian Dollar"),
                    ("AWG", "Aruban Florin"),
                    ("AZN", "Azerbaijanian Manat"),
                    ("BAM", "Convertible Mark"),
                    ("BBD", "Barbados Dollar"),
                    ("BDT", "Taka"),
                    ("BGN", "Bulgarian Lev"),
                    ("BHD", "Bahraini Dinar"),
                    ("BIF", "Burundi Franc"),
                    ("BMD", "Bermudian Dollar"),
                    ("BND", "Brunei Dollar"),
                    ("BOB", "Boliviano"),
                    ("BRL", "Brazilian Real"),
                    ("BSD", "Bahamian Dollar"),
                    ("BTN", "Ngultrum"),
                    ("BWP", "Pula"),
                    ("BYR", "Belarusian Ruble"),
                    ("BZD", "Belize Dollar"),
                    ("CAD", "Canadian Dollar"),
                    ("CDF", "Congolese Franc"),
                    ("CHF", "Swiss Franc"),
                    ("CLP", "Chilean Peso"),
                    ("CNY", "Yuan Renminbi"),
                    ("COP", "Colombian Peso"),
                    ("CRC", "Costa Rican Colon"),
                    ("CUC", "Peso Convertible"),
                    ("CUP", "Cuban Peso"),
                    ("CVE", "Cabo Verde Escudo"),
                    ("CZK", "Czech Koruna"),
                    ("DJF", "Djibouti Franc"),
                    ("DKK", "Danish Krone"),
                    ("DOP", "Dominican Peso"),
                    ("DZD", "Algerian Dinar"),
                    ("EGP", "Egyptian Pound"),
                    ("ERN", "Nakfa"),
                    ("ETB", "Ethiopian Birr"),
                    ("EUR", "Euro"),
                    ("FJD", "Fiji Dollar"),
                    ("FKP", "Falkland Islands Pound"),
                    ("GBP", "Pound Sterling"),
                    ("GEL", "Lari"),
                    ("GHS", "Ghana Cedi"),
                    ("GIP", "Gibraltar Pound"),
                    ("GMD", "Dalasi"),
                    ("GNF", "Guinea Franc"),
                    ("GTQ", "Quetzal"),
                    ("GYD", "Guyana Dollar"),
                    ("HKD", "Hong Kong Dollar"),
                    ("HNL", "Lempira"),
                    ("HRK", "Kuna"),
                    ("HTG", "Gourde"),
                    ("HUF", "Forint"),
                    ("IDR", "Rupiah"),
                    ("ILS", "New Israeli Sheqel"),
                    ("INR", "Indian Rupee"),
                    ("IQD", "Iraqi Dinar"),
                    ("IRR", "Iranian Rial"),
                    ("ISK", "Iceland Krona"),
                    ("JMD", "Jamaican Dollar"),
                    ("JOD", "Jordanian Dinar"),
                    ("JPY", "Yen"),
                    ("KES", "Kenyan Shilling"),
                    ("KGS", "Som"),
                    ("KHR", "Riel"),
                    ("KMF", "Comoro Franc"),
                    ("KPW", "North Korean Won"),
                    ("KRW", "Won"),
                    ("KWD", "Kuwaiti Dinar"),
                    ("KYD", "Cayman Islands Dollar"),
                    ("KZT", "Tenge"),
                    ("LAK", "Kip"),
                    ("LBP", "Lebanese Pound"),
                    ("LKR", "Sri Lanka Rupee"),
                    ("LRD", "Liberian Dollar"),
                    ("LSL", "Loti"),
                    ("LYD", "Libyan Dinar"),
                    ("MAD", "Moroccan Dirham"),
                    ("MDL", "Moldovan Leu"),
                    ("MGA", "Malagasy Ariary"),
                    ("MKD", "Denar"),
                    ("MMK", "Kyat"),
                    ("MNT", "Tugrik"),
                    ("MOP", "Pataca"),
                    ("MRO", "Ouguiya"),
                    ("MUR", "Mauritius Rupee"),
                    ("MVR", "Rufiyaa"),
                    ("MWK", "Malawi Kwacha"),
                    ("MXN", "Mexican Peso"),
                    ("MYR", "Malaysian Ringgit"),
                    ("MZN", "Mozambique Metical"),
                    ("NAD", "Namibia Dollar"),
                    ("NGN", "Naira"),
                    ("NIO", "Cordoba Oro"),
                    ("NOK", "Norwegian Krone"),
                    ("NPR", "Nepalese Rupee"),
                    ("NZD", "New Zealand Dollar"),
                    ("OMR", "Rial Omani"),
                    ("PAB", "Balboa"),
                    ("PEN", "Sol"),
                    ("PGK", "Kina"),
                    ("PHP", "Philippine Peso"),
                    ("PKR", "Pakistan Rupee"),
                    ("PLN", "Zloty"),
                    ("PYG", "Guarani"),
                    ("QAR", "Qatari Rial"),
                    ("RON", "Romanian Leu"),
                    ("RSD", "Serbian Dinar"),
                    ("RUB", "Russian Ruble"),
                    ("RWF", "Rwanda Franc"),
                    ("SAR", "Saudi Riyal"),
                    ("SBD", "Solomon Islands Dollar"),
                    ("SCR", "Seychelles Rupee"),
                    ("SDG", "Sudanese Pound"),
                    ("SEK", "Swedish Krona"),
                    ("SGD", "Singapore Dollar"),
                    ("SHP", "Saint Helena Pound"),
                    ("SLL", "Leone"),
                    ("SOS", "Somali Shilling"),
                    ("SRD", "Surinam Dollar"),
                    ("SSP", "South Sudanese Pound"),
                    ("STD", "Dobra"),
                    ("SVC", "El Salvador Colon"),
                    ("SYP", "Syrian Pound"),
                    ("SZL", "Lilangeni"),
                    ("THB", "Baht"),
                    ("TJS", "Somoni"),
                    ("TMT", "Turkmenistan New Manat"),
                    ("TND", "Tunisian Dinar"),
                    ("TOP", "Pa\u2019anga"),
                    ("TRY", "Turkish Lira"),
                    ("TTD", "Trinidad and Tobago Dollar"),
                    ("TWD", "New Taiwan Dollar"),
                    ("TZS", "Tanzanian Shilling"),
                    ("UAH", "Hryvnia"),
                    ("UGX", "Uganda Shilling"),
                    ("USD", "US Dollar"),
                    ("UYU", "Peso Uruguayo"),
                    ("UZS", "Uzbekistan Sum"),
                    ("VEF", "Bol\xedvar"),
                    ("VND", "Dong"),
                    ("VUV", "Vatu"),
                    ("WST", "Tala"),
                    ("XAF", "CFA Franc BEAC"),
                    ("XAG", "Silver"),
                    ("XAU", "Gold"),
                    ("XBA", "Bond Markets Unit European Composite Unit (EURCO)"),
                    ("XBB", "Bond Markets Unit European Monetary Unit (E.M.U.-6)"),
                    ("XBC", "Bond Markets Unit European Unit of Account 9 (E.U.A.-9)"),
                    (
                        "XBD",
                        "Bond Markets Unit European Unit of Account 17 (E.U.A.-17)",
                    ),
                    ("XCD", "East Caribbean Dollar"),
                    ("XDR", "SDR (Special Drawing Right)"),
                    ("XOF", "CFA Franc BCEAO"),
                    ("XPD", "Palladium"),
                    ("XPF", "CFP Franc"),
                    ("XPT", "Platinum"),
                    ("XSU", "Sucre"),
                    ("XTS", "Codes specifically reserved for testing purposes"),
                    ("XUA", "ADB Unit of Account"),
                    (
                        "XXX",
                        "The codes assigned for transactions where no currency is involved",
                    ),
                    ("YER", "Yemeni Rial"),
                    ("ZAR", "Rand"),
                    ("ZMW", "Zambian Kwacha"),
                    ("ZWL", "Zimbabwe Dollar"),
                ],
            ),
        ),
        migrations.AddField(
            model_name="proforma",
            name="transaction_xe_date",
            field=models.DateField(
                help_text=b"Date of the transaction exchange rate.",
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="proforma",
            name="transaction_xe_rate",
            field=models.DecimalField(
                decimal_places=4,
                default=1,
                max_digits=16,
                blank=True,
                help_text=b"Currency exchange rate from document currency to transaction_currency.",
                null=True,
            ),
        ),
    ]
