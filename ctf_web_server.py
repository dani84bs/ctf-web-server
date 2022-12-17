#!/usr/bin/env python3
import http.server
import socketserver
import urllib.parse
import base64
import os
import argparse

PORT = 8000
HOST = ""
RESERVED_DIR = "downloads"


class RequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        file_path = self.path
        parsed_url = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_url.query)
        if query:
            if "b" in query:
                decoded = base64.b64decode(query["b"][0].replace(" ", "+"))
                if 's' in query:
                    path = os.path.join(RESERVED_DIR, query['s'][0])
                    with open(path, "wb") as f:
                        f.write(decoded)
                else:
                    try:
                        decoded.decode("utf-8")
                    except UnicodeDecodeError:
                        pass
                    print("Decoded:")
                    print(decoded)
                    print()
            self.send_error(404)
        else:
            if file_path == "/":
                self.send_error(404)
            super().do_GET()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=PORT)
    parser.add_argument("-b", "--bind", default=HOST)
    args = parser.parse_args()
    os.makedirs(RESERVED_DIR, exist_ok=True)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((args.bind, args.port),
                                RequestHandler) as httpd:
        print("CTF Web Sesrver serving at port", args.port)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
