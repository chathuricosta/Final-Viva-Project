from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import os

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Default file to serve
        file_path = 'index.html'

        # Adjusting the file path based on the URL
        if self.path == '/login':
            file_path = 'login.html'
        elif self.path == '/register':
            file_path = 'register.html'

        # Handling query parameters for success messages
        query_params = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        success_message = query_params.get('success', [''])[0]

        # Try to open and serve the file
        try:
            # Open the file requested in binary mode
            file_to_open = open(file_path, 'rb')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            # Read the file content
            file_content = file_to_open.read()

            # If there is a success message, append it to the file content
            if success_message:
                success_message_html = f'<div style="color: green;">{success_message}</div>'
                file_content = file_content.replace(b'<!-- Add a placeholder for success messages -->', success_message_html.encode('utf-8'))

            self.wfile.write(file_content)
            file_to_open.close()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("File not found", 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        post_data = urlparse.parse_qs(post_data)  # Parse the data

        username = post_data.get('username', [None])[0]
        password = post_data.get('password', [None])[0]

        if self.path == '/register':
            # You should save these to a database or file in a real application
            print(f"Registering user: {username}, Password: {password}")

            # Display success message on the index page
            success_message = f"Successfully registered {username}!"
            self.send_response(301)
            self.send_header('Location','/?success=' + success_message)
            self.end_headers()

        elif self.path == '/login':
            # Display success message on the index page
            success_message = f"Successfully logged in as {username}!"
            self.send_response(301)
            self.send_header('Location','/?success=' + success_message)
            self.end_headers()

# Set up and start the server
httpd = HTTPServer(('localhost', 8080), WebServer)
print("Server started at localhost:8080")
httpd.serve_forever()
