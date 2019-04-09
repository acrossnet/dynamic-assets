==============
dynamic-assets
==============

Dynamic-assets is a new Django app for building flexible hierarchies of objects with attributes
conforming to classes.  This is in an early state, and will definitely evolve over time.

Detailed documentation is in the "docs" directory.

This is still a technology preview, and can be easily tested by the *assets* repo. It is also being used in the *rosa* repo.

Quick start
-----------

1. Add "assets" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'assets',
    ]

2. While there are no front-end elements to dynamic assets, there are no urls to include.

3. Run `python manage.py migrate` to create the assets models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a simple hierarchy by hand (you'll need the Admin app enabled).

Caveats
-------

Still undeveloped:
 * Acquisition - acquiring attributes from the containment parent.
 * UI elements, except a simple admin that requires data to be added by editing JSON.

Installing the package
----------------------

While the package is in a peer directory:

in here do:

   python setup.py sdist

In the peer, that wants to import:

   pip install ../dynamic-assets/dist/dynamic-assets-0.1.tar.gz

