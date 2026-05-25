"""Minimal HTTP server for Meta-Harness dev — serves static files + POST feedback."""
import http.server
import json
import os
import sys

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'evals', 'v0.1.0', 'outputs')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/submit-feedback':
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
            ts = data.get('timestamp', '').replace(':', '-').split('.')[0][:19]
            fname = f'meta-harness-feedback-{ts}.json'
            fpath = os.path.join(OUTPUT_DIR, fname)
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True, 'path': f'evals/v0.1.0/outputs/{fname}'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        super().do_GET()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8767
    print(f'Meta-Harness dev server: http://127.0.0.1:{port}')
    http.server.HTTPServer(('127.0.0.1', port), Handler).serve_forever()
