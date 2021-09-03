ckanext-publisher
=====================================

|
|

With the default CKAN Installation, metadata records have a dropdown field called **visibility** which allows metadata creators to choose either to make the metadata **public or private**. This makes it difficult for accountability as every metadata creator can easily create metadata and make it public.

The **ckanext-publisher** plugin removes the **visibility** field from the metadata record, replaces it with a **publish/unpublish** button after the record is created. The plugin allows only users with **Admin role** in the organisation to make the metadata record **public or private**.


|
|

**Image Below**: The plugin removes the visibility field so that it can only be set by an **admin**.

.. image:: docs/img/private_field.jpg
    :alt: Dataset editing private
    :height: 200px
    :width: 400px

|
|

**In the image below**: By using the plugin the metadata created is set to **private** automatically.

.. image:: docs/img/package_publish.jpg
    :alt: Publish dataset
    :height: 200px
    :width: 400px

|
|

**In the image below**: If you are an admin you can set the visibility of the metadata either **public** or **private**.

.. image:: docs/img/package_unpublish.jpg
    :alt: dataset editing private
    :height: 200px
    :width: 400px

|
|

**Member**
**Editor**
**Admin**


1. A member is a registered user of the platform and can:
    * view all public datasets on the platform
    * view all unpublished datasets of an organization is a member of but cannot view unpublished datasets of an organization is not a member of

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

|

Requirements
------------

Before installing ckanext-publisher, make sure that you have installed the following:

* CKAN 2.8+


Installation
------------

To install ckanext-publisher:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-publisher Python package into your virtual environment::

     pip install ckanext-publisher


3. Add ``ckanext-publisher`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload



Configuration
-------------

You must make sure that the following is set in your CKAN config::

    ckan.auth.create_unowned_dataset = false
    ckan.auth.create_dataset_if_not_in_organization = false
    ckan.plugins = publisher ...


Development
-----------

To install ckanext-publisher for development, activate your CKAN virtualenv and do::

    git clone https://bitbucket.org/cioapps/ckanext-publisher.git
    cd ckanext-publisher
    python setup.py develop

Tests
-----

To run the tests:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate


2. From the CKAN root directory (not the extension root) do::

    pytest --ckan-ini=test.ini ckanext/publisher/tests

