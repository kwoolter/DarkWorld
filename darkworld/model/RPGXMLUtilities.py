__author__ = 'KeithW'
from xml.dom.minidom import *

# From a specified node get the data value
def xml_get_node_text(node, tag_name: str):
    tag = node.getElementsByTagName(tag_name)

    # If the tag exists then get the data value
    if len(tag) > 0:
        value = tag[0].firstChild.data
    # Else use None
    else:
        value = None

    return value
