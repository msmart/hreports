.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/msmart/hreports/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
  * Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with
"enhancement" and "help wanted" is open to whoever wants to implement it.

Improvements:

* Add templates 
* Add version control to config files (e.g. --backup feature)
* Add git commit id of ledger file dir to global variables
* Test if requirements (hledger and pandoc) are met before running queries
* Improve error handling (e.g. template error, hledger query error, etc.)
  * Template Error
  * Hledger Query Error
  * YAML config file error

Write Documentation
~~~~~~~~~~~~~~~~~~~

hreports could always use more documentation, whether as part of the
official hreports docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/msmart/hreports/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `hreports` for local development.

1. Fork the `hreports` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/hreports.git

3. Install your local copy into a virtualenv. Assuming you have
   virtualenvwrapper installed, this is how you set up your fork for local
   development::

    $ mkvirtualenv hreports
    $ cd hreports/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 hreports tests
    $ python setup.py test or py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.3, 3.4 and 3.5, and for PyPy. Check
   https://travis-ci.org/msmart/hreports/pull_requests
   and make sure that the tests pass for all supported Python versions.

Release Checklist
-----------------
- [ ] Update HISTORY.rst
- [ ] Commit the changes::

    git add HISTORY.rst
    git commit -m "Changelog for upcoming release 0.1.1."

- [ ] Update version number (can also be minor or major)::

    bumpversion patch

- [ ] Install the package again for local development, but with the new version number::

    python setup.py develop

- [ ] Run the tests::

    tox

- [ ] Release on PyPI by uploading both sdist and wheel::

    python setup.py sdist bdist_wheel
    twine upload dist/*

- [ ] Test that it pip installs::

    mktmpenv
    pip install my_project
    <try out my_project>
    deactivate

- [ ] Push: `git push`
- [ ] Push tags: `git push --tags`
- [ ] Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, copy and paste the RestructuredText into http://rst.ninjs.org/ to find out what broke the formatting.
- [ ] Edit the release on GitHub (e.g. https://github.com/msmart/hreports/releases). Paste the release notes into the release's release page, and come up with a title for the release.

Tips
----

To run a subset of tests::

    $ python -m unittest tests.test_hreports
