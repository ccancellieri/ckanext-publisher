ckanext-publisher
=====================================

Let you to manage who is able to publish datasets
into an organization.

``Member``
``Editor``
``Admin``

.. image:: docs/img/private_missing_dataset.png
    :alt: Dataset editing private

.. image:: docs/img/publish_dataset.png
    :alt: Publish dataset

.. image:: docs/img/unpublish_dataset.png
    :alt: dataset editing private


1. A member is a registered user of the platform and can:
    * browse the platform
    * view all published and unpublished datasets

2. An editor is a registered user of the platform and can:
    * view all published datasets
    * view unpublished datasets in assigned organization
    * **create, modify, delete or move the datasets in owned organizations**
    * **cannot publish or unpublish dataset**

3. An admin is a registered user of the platform and can:
    * view all published datasets
    * view unpublished datasets in assigned organization
    * create, modify, delete or move the datasets between owned organizations
    * **create a public dataset**
    * **manage the datasets visibility by publisher or unpublisher it.** manage the organization by adding existing users (as Editor or Admin)


Requirements
------------

Before installing ckanext-publisher, make sure that you have installed the following:

* CKAN 2.8+

Installation
------------

To install ckanext-publisher
1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-publisher Python package into your virtual environment::

     git clone https://bitbucket.org/cioapps/ckanext-publisher.git

3. Install the publisher dependencies::

     python setup.py develop


4. Add ``ckanext-publisher`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload



Configuration
-------------

You must make sure that the following is set in your CKAN config::

    ckan.auth.create_unowned_dataset = false
    ckan.auth.create_dataset_if_not_in_organization = false


Development
-----------

To install ckanext-publisher for development, activate your CKAN virtualenv and do::

    git clone https://bitbucket.org/cioapps/ckanext-publisher.git
    cd ckanext-publisher
    python setup.py develop
    pip install -r dev-requirements.txt

Tests
-----

To run the tests:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate


2. From the CKAN root directory (not the extension root) do::

    pytest --ckan-ini=test.ini ckanext/iauthfunctions/tests

