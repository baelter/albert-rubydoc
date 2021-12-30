# -*- coding: utf-8 -*-

"""Search Rubydoc gems.

Synopsis: <trigger> <filter>"""

from albert import *
from urllib import request, parse
from lxml import html
import re
import time
import os

__title__ = "RudyDoc"
__version__ = "0.4.5"
__triggers__ = "r "
__authors__ = "baelter"

iconPath = iconLookup("rubydoc") or os.path.dirname(__file__)+"/rubydoc.svg"
baseurl = "https://www.rubydoc.info"
user_agent = "org.albert.rubydoc"
limit = 20


def handleQuery(query):
    if query.isTriggered:
        query.disableSort()

        # avoid rate limiting
        time.sleep(0.1)
        if not query.isValid:
            return

        stripped = query.string.strip()

        if stripped:
            results = []

            params = {
                'q': stripped,
            }
            get_url = "%s/find/gems?%s" % (baseurl, parse.urlencode(params))
            req = request.Request(get_url, headers={"User-Agent": user_agent})

            with request.urlopen(req) as response:

                tree = html.fromstring(response.read())
                nodes = tree.xpath("//ul[contains(concat(' ',@class,' '),' libraries ')]/li/a")

                for node in nodes:
                    href = node.get("href")
                    url = "%s%s" % (baseurl, re.sub(r"^#", "", href))
                    title = node.text.strip()
                    summary = "Open RubyDoc for %s" % stripped

                    results.append(Item(id=__title__,
                                        icon=iconPath,
                                        text=title,
                                        subtext=summary if summary else url,
                                        completion=title,
                                        actions=[
                                            UrlAction("Open RubyDoc", url),
                                            ClipAction("Copy URL", url)
                                        ]))

            return results
        else:
            return Item(id=__title__,
                        icon=iconPath,
                        text=__title__,
                        subtext="Enter a query to search RubyDoc")
