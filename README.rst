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

hreports saves shortcuts to hledger query to conveniently manage multiple queries with different settings and ledger files. In addition, hreports can save the query output to pdfs with jinja templates using Pandoc.

* Generate invoices with a single command, e.g. ``hreports save invoice_client1``
* Manage tax reports, e.g. ``hreports show tax_2017``

Roadmap
---------
* Add documentation
* Add tests

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

