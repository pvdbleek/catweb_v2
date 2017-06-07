from flask import Flask, render_template, request, Response
import requests
import random
import platform
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
APPROVED_HOSTS = set(["imageserver"])
CHUNK_SIZE = 1024

# list of cat images
images = [
    "p/imageserver/anigif_enhanced-buzz-31540-1381844535-8.gif",
    "p/imageserver/anigif_enhanced-buzz-1376-1381846217-0.gif",
    "p/imageserver/anigif_enhanced-buzz-3391-1381844336-26.gif",
    "p/imageserver/anigif_enhanced-buzz-29111-1381845968-0.gif",
    "p/imageserver/anigif_enhanced-buzz-3409-1381844582-13.gif",
    "p/imageserver/anigif_enhanced-buzz-19667-1381844937-10.gif",
    "p/imageserver/anigif_enhanced-buzz-26358-1381845043-13.gif",
    "p/imageserver/anigif_enhanced-buzz-18774-1381844645-6.gif",
    "p/imageserver/anigif_enhanced-buzz-25158-1381844793-0.gif",
    "p/imageserver/anigif_enhanced-buzz-11980-1381846269-1.gif"
]

@app.route('/p/<path:url>')
def proxy(url):
    """Fetches the specified URL and streams it out to the client.
    If the request was referred by the proxy itself (e.g. this is an image fetch for
    a previously proxied HTML page), then the original Referer is passed."""
    r = get_source_rsp(url)
    headers = dict(r.headers)
    def generate():
        for chunk in r.iter_content(CHUNK_SIZE):
            yield chunk
    return Response(generate(), headers = headers)

def get_source_rsp(url):
        url = 'http://%s' % url
        # Ensure the URL is approved, else abort
        if not is_approved(url):
            abort(403)
        # Pass original Referer for subsequent resource requests
        proxy_ref = proxy_ref_info(request)
        headers = { "Referer" : "http://%s/%s" % (proxy_ref[0], proxy_ref[1])} if proxy_ref else {}
        # Fetch the URL, and stream it back
        return requests.get(url, stream=True , params = request.args, headers=headers)


def is_approved(url):
    """Indicates whether the given URL is allowed to be fetched.  This
    prevents the server from becoming an open proxy"""
    host = split_url(url)[1]
    return host in APPROVED_HOSTS


def split_url(url):
    """Splits the given URL into a tuple of (protocol, host, uri)"""
    proto, rest = url.split(':', 1)
    rest = rest[2:].split('/', 1)
    host, uri = (rest[0], rest[1]) if len(rest) == 2 else (rest[0], "")
    return (proto, host, uri)


def proxy_ref_info(request):
    """Parses out Referer info indicating the request is from a previously proxied page.
    For example, if:
        Referer: http://localhost:8080/p/google.com/search?q=foo
    then the result is:
        ("google.com", "search?q=foo")
    """
    ref = request.headers.get('referer')
    if ref:
        _, _, uri = split_url(ref)
        if uri.find("/") < 0:
            return None
        first, rest = uri.split("/", 1)
        if first in "pd":
            parts = rest.split("/", 1)
            r = (parts[0], parts[1]) if len(parts) == 2 else (parts[0], "")
            return r
    return None

@app.route('/')
def index():
    url = random.choice(images)
    hostname = platform.node()
    return render_template('index.html', url=url, hostname=hostname)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
