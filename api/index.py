from http.server import BaseHTTPRequestHandler
from io import BytesIO
import json, random, uuid
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        post_data = parse_qs(body.decode('utf-8'))
        phone_number = post_data.get('phone_number', [None])[0]
        otp_count = post_data.get('otp_count', [None])[0]

        if not phone_number or not otp_count:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid input'}).encode('utf-8'))
            return

        # Simulate OTP sending process
        result_message = f'Successfully sent {otp_count} OTP(s) to {phone_number}'

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': result_message}).encode('utf-8'))
        return
