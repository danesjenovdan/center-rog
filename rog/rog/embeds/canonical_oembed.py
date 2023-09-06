import re
from urllib import request as urllib_request
from urllib.error import URLError
from urllib.request import Request

from wagtail.embeds.exceptions import EmbedNotFoundException
from wagtail.embeds.finders.oembed import OEmbedFinder


class CanonicalOEmbedFinder(OEmbedFinder):
    def _get_canonical_url(self, url):
        request = Request(url)
        request.add_header("User-agent", "Mozilla/5.0")
        try:
            r = urllib_request.urlopen(request)
            html = r.read().decode("utf-8")
        except URLError:
            raise EmbedNotFoundException

        canonical_tag_match = re.search(
            r'<link rel="canonical" href="([^"]+)"', html, re.I
        )
        if canonical_tag_match is None:
            return url

        canonical_url = canonical_tag_match.group(1)
        if not canonical_url or not canonical_url.startswith("http"):
            return url

        return canonical_url

    def find_embed(self, url, max_width=None, max_height=None):
        # Find provider
        endpoint = self._get_endpoint(url)
        if endpoint is None:
            raise EmbedNotFoundException

        # Canonicalize URL
        canonical_url = self._get_canonical_url(url)

        # Find embed with canonicalized URL
        embed = super().find_embed(canonical_url, max_width, max_height)
        return embed


embed_finder_class = CanonicalOEmbedFinder
