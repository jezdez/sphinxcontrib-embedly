embedly extension
=================

This is a sphinx extension for using Embedly_.

This extension enables you to embed anything that is supported by Embedly_ ,
e.g.::

   .. embedly:: http://www.youtube.com/watch?v=M_eYSuPKP3Y

.. _Embedly: http://embed.ly/


Installation
------------

::

   pip install sphinxcontrib-embedly

Configuration
-------------

Sphinx
^^^^^^

To enable this extension in Sphinx, add ``sphinxcontrib.embedly`` module to
the ``extensions`` option in the ``conf.py`` file.

::

   import os, sys

   # Path to the folder where sphinxcontrib/embedly.py is
   # NOTE: not needed if the package is installed in traditional way
   # using setup.py, easy_install or pip
   sys.path.append(os.path.abspath('/path/to/sphinxcontrib.embedly'))

   # Enabled extensions
   extensions = ['sphinxcontrib.embedly']

Docutils
^^^^^^^^

In case you use pure docutils projects such as Pelican feel free to add
the following somewhere to your code::

   from sphinxcontrib.embedly import setup_docutils
   setup_docutils()


embedly_key
^^^^^^^^^^^
Then set the **required** configuration variable ``embedly_key`` in your
``conf.py`` by signing up for for the free account on Embedly for the
Embed_ product. E.g.::

   embedly_key = '<api-key-copied-from-your-account-page>'

embedly_timeout
^^^^^^^^^^^^^^^

There is also one optional configuration variable, the ``embedly_timeout``
that specifies the default timeout used when fetching the embed code from
Embedly (defaults to 60 seconds). E.g.::

   embedly_timeout = 120

.. _Embed: http://embed.ly/embed

Usage
-----

This directive fetches the embed code for the given URL and adds it into
the generated document.

Examples::

   .. embedly:: http://www.youtube.com/watch?v=M_eYSuPKP3Y

You can specify various options for the embedding as seen above.

Example::

   .. embedly:: http://www.youtube.com/watch?v=M_eYSuPKP3Y
      :width: 450
      :autoplay:
      :frame:

Options
^^^^^^^

:maxwidth: the maximum width of the embed in pixels (optional)
:maxheight: the maximum height of the embed in pixels  (optional)
:width: the scaled width of rich and video embeds in pixels  (optional)
:wmode: the "wmode" parameter to flash objects, options are
        "window", "opaque" and "transparent"  (optional)
:nostyle: boolean when given removes inline style elements from certain
          embeds to be able to style them yourself (optional)
:autoplay: boolean when given tells the video and rich embeds to
           automatically play when the media is loaded (optional)
:videosrc: boolean when given uses the ``video_src`` meta or Open Graph
           tag to create a video object to embed (optional, defaults to 50)
:words: integer value of words to be returned as the description,
        as the closest sentence to that word count (optional)
:chars: integer value of characters after which the description is
        blindly truncated and added "..." (optional)
:frame: boolean when given will wrap all embeds in iframes to help prevent
        XSS attacks (optional, available in the paid products)
:secure: boolean when given will serve embeds with a SSL connection
         (optional, available in the paid products)


Changelog
---------

v0.2 (2014-02-23)
^^^^^^^^^^^^^^^^^

- Handle embeds of the type "rich" such as Slideshare. Thanks to Doug Hellmann.

- Ported over from Bitbucket repo to Github:

    https://github.com/jezdez/sphinxcontrib-embedly

v0.1 (2013-12-30)
^^^^^^^^^^^^^^^^^

- Initial release.