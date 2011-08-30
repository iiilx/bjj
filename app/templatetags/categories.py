from django.template import Node
from django.template import Library
from django.utils.html import escape
import memcache
from bjj import settings

cache = memcache.Client(['127.0.0.1:11211'])

register = Library()

class CategoriesNode(Node):
    def __init__(self):
        pass

    def __repr__(self):
        return "<Categories Node>"

    def render(self, context):
        return cache.get('%s-all-cats' % settings.PREFIX)

def do_CategoryList(parser, token):
    return CategoriesNode()
do_CategoryList = register.tag('catlist', do_CategoryList)
