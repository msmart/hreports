========
hreports
========


.. image:: https://img.shields.io/pypi/v/hreports.svg
        :target: https://pypi.python.org/pypi/hreports

.. image:: https://img.shields.io/travis/msmart/hreports.svg
        :target: https://travis-ci.org/msmart/hreports

.. image:: https://readthedocs.org/projects/hreports/badge/?version=latest&v=0.1
        :target: https://hreports.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/msmart/hreports/shield.svg
     :target: https://pyup.io/repos/github/msmart/hreports/
     :alt: Updates


A simple wrapper to create and manage reports based on hledger queries.


* Free software: MIT license
* Documentation: https://hreports.readthedocs.io.


Features
--------

hreports saves shortcuts to hledger queries to conveniently manage multiple
queries with different settings and ledger files.In addition, hreports can save
the query output to pdfs with jinja templates using Pandoc.

* Conveniently create and manage multiple heldger queries
* Customize the representation of hledger query results with templates
* Save report results in pdf format
* Parametrize queries
* Use case: generate invoices with a single command, e.g. ``hreports save
  invoice_client1``
* Use case: Manage tax reports, e.g. ``hreports show tax_2017``

Quickstart
----------
Ensure that hledger_ is installed. If you want to save generate pdf reports
pandoc_ and a PDF engine such as wkhtml2pdf_ need to be installed as well.

Use pip to install hreports::

    $ pip install hreports

The starting point of running hledger queries is having a ledger to run queries
against. Imagine following simple hlegder file::

    $ cat cash-account.ledger
    1917/12/14 * Income
        assets:cash  10 USD
        income:client1

    1917/12/12 * Expense
        assets:cash  5 USD
        expense:milk

and a hledger timesheet::

    $ cat timesheet.ledger
    1917/12/14 * Time
        (consulting:clien1)  1


The following command creates a report named `balance` that executes the query
`hledger bal --depth 1` on the ledger `cash.ledger`::

    $ hreports create balance --query "bal --depth 1" --ledger cash.ledger

When executed, hreports stores the query data in a config file for future
reference. Now hreports can render the query by running::

    $ hreports show balance
                   5 USD  assets
    --------------------
                   5 USD

This makes it easy to store many different queries on different ledger files
and executing them by refering to their hreports name.

Templating
^^^^^^^^^^
Sometimes, it is helpful to add context to query results. hreports uses jinja
templates to customize the representation of reports. The query results are
added to the `output` variabel in the context of the template. In addition,
the report configuration data, global configuration and custom variables
are added.

Imagine the folowing simple template::

    $ cat balance.template
    The balance on {{ now }} the balance was

    {{ output|last }}

hreports can now use this template to embed query results::

    $ hreports show balance --template balance.template
    The balance on 2017-12-15 15:39:11.519658 was:

                       5 USD 

If you need this information for future reference, create a pdf of it by
executing::

    $ hreports save balance --template balance.template
    Saved balance.pdf

If you keep reusing this command, simply your life by updating the report::

    $ hreports update balance --template balance.template

Now hreports will always use the `balance.template` when rendering the balance
report.

Templating is also helpful when you use hledger for timetracking and
invoicing.  Create a hreport and a simple demo template. Add a custom
variable name ("hourly_rate") and value ("20") with the `-var` option::

    $ hreports create timesheet --ledger timesheet.ledger -q "bal" -var hourly_rate 20 --template invoice.template

    $ cat invoice.template
    {% set hours = output|last|float|round(2) %}
    {% set net = hours *  hourly_rate|float  %}
    Please pay me {{ net }} USD.
    Signed {{ now|datetime("%Y/%m/%d") }}

    $ hreports show timesheet
    Please pay me 20.0 USD.
    Signed on 2017/12/15

Admittedly, this is a somewhat simple example. But feel free to check out
`heldger edit --template invoice_de.template` for a fully fledged template of a
German invoice.

Finally, all report configuration data is stored in a simple YAML file which
can be manipulated manually if preferred. To inspect and manipulated the
config file run::

    $ hreports edit


Roadmap
---------
* Add documentation
* Add tests

Credits
---------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _hledger: https://hledger.org
.. _pandoc: https://pandoc.org
.. _wkhtml2pdf: https://wkhtmltopdf.org
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

