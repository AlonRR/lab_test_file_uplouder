# Needs to handle file upload requests and save files to UPLOAD_DIR defined in config.py
# Also serves a simple HTML form for file uploads.


# NEED to check current code for any missing parts or errors and fix them.
# This was written by AI, use with caution and test thoroughly.

import cgi
import mimetypes
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from .config import PORT, UPLOAD_DIR


class FileUploadHandler(BaseHTTPRequestHandler):
    """Handle file upload requests."""

    def do_GET(self) -> None:
        """Serve files (index.html by default) from this module directory."""
        base_dir = Path(__file__).parent.resolve()
        req_path = self.path.lstrip("/") or "index.html"
        target = (base_dir / req_path).resolve()

        # Prevent path traversal
        if not str(target).startswith(str(base_dir)):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"403 Forbidden")
            return

        if target.is_dir():
            target = target / "index.html"

        try:
            with target.open("rb") as file:
                self.send_response(200)
                ctype, _ = mimetypes.guess_type(str(target))
                self.send_header(
                    "Content-type",
                    ctype or "application/octet-stream",
                )
                self.end_headers()
                shutil.copyfileobj(file, self.wfile)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self) -> None:
        """Handle file upload via POST request."""
        if self.path != "/upload":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        # Use cgi.FieldStorage to parse multipart form data reliably
        try:
            content_type = self.headers.get("Content-Type", "")
            if not content_type.startswith("multipart/form-data"):
                raise ValueError(
                    "Content-Type must be multipart/form-data",
                )

            # Ensure Content-Length present
            length = int(self.headers.get("Content-Length", 0))

            fs = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={"REQUEST_METHOD": "POST"},
                keep_blank_values=True,
            )

            # Prefer field named 'file' but accept any file field
            file_field = None
            if "file" in fs and getattr(fs["file"], "filename", None):
                file_field = fs["file"]
            else:
                for key in fs.keys():
                    candidate = fs[key]
                    if isinstance(candidate, cgi.FieldStorage) and getattr(
                        candidate,
                        "filename",
                        None,
                    ):
                        file_field = candidate
                        break

            if not file_field or not getattr(file_field, "filename", None):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No file uploaded.")
                return

            filename = Path(file_field.filename).name
            Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
            out_path = Path(UPLOAD_DIR) / filename
            with out_path.open("wb") as out_file:
                shutil.copyfileobj(file_field.file, out_file)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"File uploaded successfully!")
            return

        except Exception as exc:
            self.send_response(400)
            self.end_headers()
            msg = f"Upload failed: {exc}".encode("utf-8", errors="replace")
            self.wfile.write(msg)


def start_server() -> None:
    """Start the HTTP server."""
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, FileUploadHandler)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
