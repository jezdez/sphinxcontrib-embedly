# -*- coding: utf-8 -*-
"""
    sphinxcontrib.embedly
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013-2014 by the contributors (see AUTHORS file)
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function, unicode_literals, absolute_import
import os

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

from sphinx.errors import ExtensionError
# from sphinx.util.compat import Directive

from embedly import Embedly as EmbedlyClient

__version__ = '0.1'

DEFAULT_TIMEOUT = 60
USER_AGENT = ('Mozilla/5.0 (compatible; sphinxcontrib-embedly/%s;)' %
              __version__)


class EmbedlyError(ExtensionError):
    category = 'Embedly error'


class EmbedlyRenderer(object):
    def photo(self, node, obj):
        params = {
            'width': obj['width'],
            'height': obj['height'],
            'title': obj.get('title', ''),
            'url': obj['url'],
        }
        return """<img width="{width}"
                       height="{height}"
                       alt="{title}"
                       src="{url}" />""".format(**params)

    def html(self, node, obj):
        return obj['html']

    video = html

    # Sites like slideshare.com use the type "rich"
    rich = html

    def link(self, node, obj):
        parts = []
        obj['title'] = obj.get('title') or obj['url']
        obj['description'] = obj.get('description') or ''
        parts.append("""<a href="{url}" title="{description}">{title}</a>""")
        return "\n".join([part.format(**obj) for part in parts])

    def error(self, node, obj):
        print(obj.__dict__)
        raise EmbedlyError('code %s' % str(obj.get('error_code', 'unknown')))

    def render(self, client, node):
        response = client.oembed(**node.attributes)
        return getattr(self, response['type'], self.error)(node, response)

renderer = EmbedlyRenderer()


class embedly(nodes.General, nodes.Element):
    pass


def wmode(argument):
    """Conversion function for the "wmode" option."""
    return directives.choice(argument, ('window', 'opaque', 'transparent'))


class EmbedlyDirective(Directive):
    """Directive for embedding using Embedly"""
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'maxwidth': directives.nonnegative_int,
        'maxheight': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        'wmode': wmode,
        'nostyle': directives.flag,
        'autoplay': directives.flag,
        'videosrc': directives.flag,
        'words': directives.nonnegative_int,
        'chars': directives.nonnegative_int,
        'frame': directives.flag,
        'secure': directives.flag,
    }

    def run(self):
        node = embedly()
        node['url_or_urls'] = directives.uri(self.arguments[0].strip())
        for option in ['maxwidth', 'maxheight', 'width', 'wmode',
                       'words', 'chars']:
            if option in self.options:
                node[option] = self.options[option]
        for option in ['nostyle', 'autoplay', 'videosrc', 'frame', 'secure']:
            if option in self.options:
                node[option] = True
        return [node]


def html_visit_embedly_docutils(self, node):
    embedly_key = os.environ.get('EMBEDLY_KEY', None)
    if embedly_key is None:
        raise EmbedlyError('The environment variable EMBEDLY_KEY is not set')
    client = EmbedlyClient(key=embedly_key,
                           user_agent=USER_AGENT,
                           timeout=os.environ.get('EMBEDLY_TIMEOUT',
                                                  DEFAULT_TIMEOUT))
    try:
        content = renderer.render(client, node)
    except Exception as e:
        msg = 'embedly "%s" error: %s' % (node['url_or_urls'], e)
        raise EmbedlyError(msg)
    else:
        self.body.append(content)
    raise nodes.SkipNode


def html_visit_embedly_sphinx(self, node):
    if self.builder.config.embedly_key is None:
        raise ValueError('The Sphinx config variable embedly_key must be set')
    client = EmbedlyClient(key=self.builder.config.embedly_key,
                           user_agent=USER_AGENT,
                           timeout=self.builder.config.embedly_timeout)

    try:
        content = renderer.render(client, node)
    except Exception as e:
        msg = 'embedly "%s" error: %s' % (node['url_or_urls'], e)
        self.builder.warn(msg)
    else:
        self.body.append(content)
    raise nodes.SkipNode


def setup(app):
    app.add_node(embedly, html=(html_visit_embedly_sphinx, None))
    app.add_config_value('embedly_key', None, 'env')
    app.add_config_value('embedly_timeout', DEFAULT_TIMEOUT, 'env')
    app.add_directive('embedly', EmbedlyDirective)


def setup_docutils():
    directives.register_directive('embedly', EmbedlyDirective)
    from docutils.writers.html4css1 import HTMLTranslator
    setattr(HTMLTranslator, 'visit_embedly', html_visit_embedly_docutils)
    setattr(HTMLTranslator, 'depart_embedly', lambda self, node: None)
