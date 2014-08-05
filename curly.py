#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# curly.py - Easily communicate with JSON APIs.
#
# TODO:
# - allow http basic auth
#

from argparse import ArgumentParser
from urllib import urlencode
from urllib2 import HTTPError, Request, urlopen

try:
    from pygments import highlight
    from pygments.lexers import JsonLexer
    from pygments.formatters import TerminalFormatter
    has_pygments = True
except ImportError:
    has_pygments = False

COLOR_CODES = {
    'green': '\033[32m',
    'bgreen': '\033[1;32m',
    'bgrey': '\033[1;30m',
    'reset': '\033[0m'
}


class ApiRequest(Request, object):
    def __init__(self, url, method, **kwargs):
        self.method = method
        super(ApiRequest, self).__init__(url, **kwargs)

    def get_method(self):
        return self.method


def color(text, color_name):
    return COLOR_CODES[color_name]+text+COLOR_CODES['reset']


def extract_values(values):
    return dict(map(lambda s: s.split('='), values))


def curl_command(url, method, data, headers):
    cmd_data = ""
    if data is not None:
        cmd_data = (' -d "%s"' % data)
    cmd_headers = ""
    if headers is not None:
        for k, v in headers.iteritems():
            cmd_headers += (' -H "%s: %s"' % (k, v))
    return "curl -i -X %s%s%s %s" % (method, cmd_headers, cmd_data, url)


ap = ArgumentParser(description="Easily communicate with JSON APIs")
ap.add_argument(
    "url",
    help="API endpoint to hit",
    metavar="URL"
)
ap.add_argument(
    "--method",
    help="Method to use for the HTTP request",
    metavar="METHOD",
    default="GET"
)
ap.add_argument(
    "--data",
    help="POST data to send with request",
    nargs="*",
    metavar="DATA"
)
ap.add_argument(
    "--headers",
    help="Headers to add to the request",
    nargs="*",
    metavar="HEADER"
)
ap.add_argument(
    "--curl",
    help="Show corresponding cURL command",
    action="store_true"
)
args = ap.parse_args()

req = ApiRequest(args.url, args.method)

if args.data is not None:
    args.data = urlencode(extract_values(args.data))
    req.add_data(args.data)
if args.headers is not None:
    args.headers = extract_values(args.headers)
    for k, v in args.headers.iteritems():
        req.add_header(k, v)

try:
    resp = urlopen(req)
except HTTPError as err:
    resp = err

print color("----- REQUEST -----", "green")
print "URL:", color(args.url, "bgreen")
if args.data is not None:
    print "Data:", color(args.data, "bgreen")

if args.curl:
    print ""
    print "cURL:", color(curl_command(args.url, args.method, args.data, args.headers), "bgreen")
if args.headers is not None:
    print "Headers:"
    for k, v in args.headers.iteritems():
        print "  -", color("%s: %s" % (k, v), "bgreen")
print ""

print color("----- RESPONSE: %d -----" % resp.code, "green")
print resp.headers
if has_pygments:
    print highlight(resp.read(), JsonLexer(), TerminalFormatter())
else:
    print resp.read()

