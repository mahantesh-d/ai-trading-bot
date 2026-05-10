import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
from .logging_setup import logger

class KiteAuth:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.kite = KiteConnect(api_key=self.api_key)
        self.request_token = None
        self.access_token_path = "access_token.txt"

    def get_access_token(self):
        if os.path.exists(self.access_token_path):
            with open(self.access_token_path, "r") as f:
                access_token = f.read().strip()
                if self._is_token_valid(access_token):
                    logger.info("Access token loaded from file.")
                    return access_token
        
        return self._generate_new_access_token()

    def _is_token_valid(self, access_token):
        try:
            self.kite.set_access_token(access_token)
            self.kite.profile()
            return True
        except Exception as e:
            logger.warning(f"Access token validation failed: {e}")
            return False

    def _generate_new_access_token(self):
        self._get_request_token()
        try:
            data = self.kite.generate_session(self.request_token, api_secret=self.api_secret)
            access_token = data["access_token"]
            with open(self.access_token_path, "w") as f:
                f.write(access_token)
            logger.info("New access token generated and saved.")
            return access_token
        except Exception as e:
            logger.error(f"Error generating access token: {e}")
            raise

    def _get_request_token(self):
        login_url = self.kite.login_url()
        webbrowser.open(login_url)
        logger.info("Please login to Kite and authorize the app.")
        
        class RequestTokenHandler(BaseHTTPRequestHandler):
            def do_GET(s):
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write(b"<html><head><title>Authentication Success</title></head>")
                s.wfile.write(b"<body><p>You have successfully authenticated. You can close this window.</p></body></html>")
                query = urlparse(s.path).query
                params = parse_qs(query)
                if "request_token" in params:
                    self.request_token = params["request_token"][0]

        with HTTPServer(("localhost", 8080), RequestTokenHandler) as httpd:
            logger.info("Waiting for request token on http://localhost:8080")
            while self.request_token is None:
                httpd.handle_request()
        logger.info("Request token received.")


