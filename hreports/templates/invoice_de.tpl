---
papersize: a4
margin-left: 25mm
margin-right: 25mm
margin-top: 45mm
margin-bottom: 20mm
{% set hours = output|last|float|round(2) %} 
{% set net = output|last|float *  hourly_rate|float  %} 
{% set vat = output|last|float * hourly_rate|float * VAT|float  %}
{% set sum = vat + net %} 
---
{{ name }} | {{ street }} | {{ zipcode }} {{ city }}

{{ customer }}  
{{ customer_street }}  
{{ customer_zipcode_city }} 

{{ city }}, {{ invoice_date or now|datetime("%d.%m.%Y") }}

# Rechnung: {{ project }}
## Rechnungsnummer: {{ invoice_number or now|datetime("%Y%m%d") }}  
## Leistungszeitraum: Monat der Rechnungsstellung 


| Pos | Beschreibung                   | Anzahl                   | Einheit   | Preis pro Einheit                      | Gesamt                           |
| :-- | :-------------                 | --------:                | --------: | -------:                               | -------:                         |
| 1   | {{ description }} | {{ hours|german_float }} | Stunden   | €{{ hourly_rate }}                     | €{{ net|german_float }}          |
|     |                                |                          |           | Umsatzsteuer ({{ VAT_RATE }})  | €{{ vat|round(2)|german_float }} |
|     |                                |                          |           | **Gesamt**                             | **€{{ sum|german_float }}**      |



Bitte überweisen Sie den Rechnungsbetrag innerhalb von 30 Tagen
auf untenstehendes Konto bei der ING DiBa.

Vielen Dank für Ihr Vertrauen.

Mit freundlichen Grüßen

{{ name }}

{{ company }} | {{ street }} | {{ zipcode }} {{ city }} | {{ phone }} | {{ email }}  
Steuer-Nummer: {{ tax_id }} | Bankverbindung | IBAN {{ iban }} | BIC: {{ bic }} 


