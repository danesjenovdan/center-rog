"""
Provides XML parsing support.
"""

from rest_framework.parsers import BaseParser


class XMLParser(BaseParser):
    """
    XML parser.
    """

    # media_type = "application/xml"
    media_type = "*/*"

    def parse(self, stream, media_type=None, parser_context=None):
        print(media_type)
        return stream.read()
