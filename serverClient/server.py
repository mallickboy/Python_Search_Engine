import socket
from urllib.parse import parse_qs
import json

results=[
  {
    "icon": "https://example.com/icon1.png",
    "domain": "example.com",
    "title": "Example Website",
    "desc": "This is an example description for the first website."
  },
  {
    "icon": "https://example.org/icon2.png",
    "domain": "example.org",
    "title": "Another Example",
    "desc": "This is another example description for the second website."
  },
  {
    "icon": "https://example.net/icon3.png",
    "domain": "example.net",
    "title": "Yet Another Example",
    "desc": "This is yet another example description for the third website."
  }
]




def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    # print(request_data)
    if not request_data:
        return

    # Extract the HTTP method and the path from the request
    method = request_data.split(' ')[0]
    path = request_data.split(' ')[1]

    # If the method is GET and the path is '/', serve the webpage
    if method == 'GET' and path == '/':
        # Send HTTP response with the webpage containing a form
        IndexHtm=open('index.html')
        content=IndexHtm.read()
        http_response = "HTTP/1.1 200 OK" +'\n'+content
        client_socket.sendall(http_response.encode('utf-8'))


        
    # If the method is POST and the path is '/submit', process the submitted data


    elif method == 'POST' and path == '/submit':
        # Extract the data submitted via the form
        
        content_length_start = request_data.find('Content-Length:') + len('Content-Length:')
        content_length_end = request_data.find('\r\n', content_length_start)
        content_length = int(request_data[content_length_start:content_length_end].strip())
        end_of_data = request_data.find('\r\n\r\n')
        post_data = request_data[end_of_data+4:]
        print("post dta",post_data)
        parsed_data = json.loads(post_data)
        print(parsed_data)
        # Check if the 'data' key exists in the parsed data
        if 'data' in parsed_data:
            submitted_data = parsed_data['data']
        else:
            submitted_data = "No data submitted"

        # Send HTTP response with the submitted data
        http_response = json.dumps(results)
        client_socket.sendall(http_response.encode('utf-8'))

    client_socket.close()

def main():
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server is listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Received connection from {client_address}")
            handle_request(client_socket)
    except KeyboardInterrupt:
        print("Shutting down the server.")
        server_socket.close()

if __name__ == "__main__":
    main()
