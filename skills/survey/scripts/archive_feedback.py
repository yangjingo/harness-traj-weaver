"""Archive human-loop feedback — serves survey HTML + POST endpoint that writes to .metaharness/."""
import http.server
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

def _detect_version():
    changelog = os.path.join(REPO_ROOT, 'CHANGELOG.md')
    try:
        with open(changelog) as f:
            for line in f:
                if line.startswith('## ['):
                    import re
                    m = re.match(r'## \[([0-9.]+)\]', line)
                    if m:
                        return f'v{m.group(1)}'
    except Exception:
        pass
    return 'v0.1.0'

VERSION = os.environ.get('METAHARNESS_VERSION', _detect_version())
OUTPUT_DIR = os.path.join(REPO_ROOT, '.metaharness', VERSION, 'outputs')

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
            self.wfile.write(json.dumps({'ok': True, 'path': f'.metaharness/{VERSION}/outputs/{fname}'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        super().do_GET()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8767
    print(f'Meta-Harness dev server: http://127.0.0.1:{port}')
    http.server.HTTPServer(('127.0.0.1', port), Handler).serve_forever()
