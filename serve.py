# Local preview server with gzip and caching, so the preview behaves like production hosting.
import gzip, os, sys, mimetypes
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
ROOT = os.path.dirname(os.path.abspath(__file__))
COMP = ('text/', 'application/javascript', 'application/json', 'image/svg+xml')
class H(SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def send_head(s):
        p = s.translate_path(s.path)
        if os.path.isdir(p): p = os.path.join(p, 'index.html')
        if not os.path.isfile(p):
            p = os.path.join(ROOT, '404.html'); code = 404
        else: code = 200
        if os.path.basename(p).startswith('.') or '/_gen' in p or p.endswith('.py'):
            s.send_error(404); return None
        ct = mimetypes.guess_type(p)[0] or 'application/octet-stream'
        data = open(p, 'rb').read()
        s.send_response(code); s.send_header('Content-Type', ct + ('; charset=utf-8' if ct.startswith('text/') or 'javascript' in ct else ''))
        if 'gzip' in s.headers.get('Accept-Encoding', '') and ct.startswith(COMP):
            data = gzip.compress(data, 6); s.send_header('Content-Encoding', 'gzip')
        s.send_header('Cache-Control', 'no-cache' if ct == 'text/html' else 'public, max-age=31536000')
        s.send_header('Content-Length', str(len(data))); s.end_headers()
        import io; return io.BytesIO(data)
    def log_message(s, *a): pass
port = int(sys.argv[1]) if len(sys.argv) > 1 else 4322
ThreadingHTTPServer(('0.0.0.0', port), H).serve_forever()
