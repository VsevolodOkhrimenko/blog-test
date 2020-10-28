Test blog
=========

Test blog project for Ne Kidaem


:License: MIT


Pre-requirements
----------------

Windows
^^^^^^^

All you need is to install `Docker for Windows`_.

.. _Docker for Windows: https://docs.docker.com/docker-for-windows/


Mac
^^^

All you need is to install `Docker for Mac`_.

.. _Docker for Mac: https://docs.docker.com/docker-for-mac/


Linux
^^^^^

You have to install `Docker CE`_ and `docker compose`_.


.. _Docker CE: https://docs.docker.com/install/linux/docker-ce/ubuntu/

.. _docker compose: https://docs.docker.com/compose/install/



Run and build developing app (for production go below)
------------------------------------------------------

Go to project folder

Build developing app
^^^^^^^^^^^^^^^^^^^^

To build app use this command::

    $ docker-compose -f local.yml build

Run developing app
^^^^^^^^^^^^^^^^^^

To run app use this command::

    $ docker-compose -f local.yml up

Then you can open app by:

* localhost_backend_

.. _localhost_backend: http://localhost:8000/

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **superuser account** in development env, use this command::

    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser


* To create N number of dummy users with password '123123123' in development env, use this command::

    $ docker-compose -f local.yml run --rm django python manage.py add_users N

Setting Up Your Posts
^^^^^^^^^^^^^^^^^^^^^

* To create N number of dummy posts, randomly associated to all users in development env, use this command::

    $ docker-compose -f local.yml run --rm django python manage.py add_posts N --user SOME_USER_ID


To add posts to specific user, use optional argument '--user', where value is a user id
