# Needs to handle file upload requests and save files to UPLOAD_DIR defined in config.py
# Also serves a simple HTML form for file uploads.


# NEED to check current code for any missing parts or errors and fix them.
# This was written by AI, use with caution and test thoroughly.

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from config import PORT, UPLOAD_DIR


class FileUploadHandler(BaseHTTPRequestHandler):
    """Handle file upload requests."""

    def do_GET(self) -> None:
        """Serve the index.html file."""
        if self.path == "/":
            self.path = "index.html"
        try:
            with Path(self.path[1:]).absolute().open("rb") as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self) -> None:
        """Handle file upload via POST request."""
        if self.path == "/upload":
            content_length = int(self.headers["Content-Length"])
            content_type = self.headers["Content-Type"]

            # Ensure the request is multipart/form-data
            if "multipart/form-data" in content_type:
                boundary = content_type.split("boundary=")[-1].encode()
                body = self.rfile.read(content_length)

                # Parse the uploaded file
                parts = body.split(b"--" + boundary)
                for part in parts:
                    if b"Content-Disposition" in part:
                        headers, file_data = part.split(b"\r\n\r\n", 1)
                        file_data = file_data.rstrip(b"\r\n--")
                        disposition = headers.decode()

                        # Extract the filename
                        if "filename=" in disposition:
                            filename = (
                                disposition.split("filename=")[-1]
                                .split(";")[0]
                                .strip('"')
                            )
                            file_path = os.path.join(UPLOAD_DIR, filename)

                            # Save the file
                            os.makedirs(UPLOAD_DIR, exist_ok=True)
                            with open(file_path, "wb") as f:
                                f.write(file_data)

                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(
                                b"File uploaded successfully!"
                            )
                            return

            # If the request is invalid
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid file upload request.")


def start_server() -> None:
    """Start the HTTP server."""
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, FileUploadHandler)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
