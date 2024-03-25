import socket
from urllib.parse import parse_qs
import json
import os
from dotenv import load_dotenv
import os
load_dotenv()
from pinecone import Pinecone 

from sentence_transformers import SentenceTransformer
model=SentenceTransformer("msmarco-distilbert-base-v3")

def search_pinecone(model,query,table,namespace,res):
    pc=Pinecone(api_key=os.getenv("PINECONE_KEY"),environment=os.getenv("PINECONE_ENVIRONMENT"))
    index=pc.Index(table)
    
    result=index.query(
        namespace=namespace,
        vector=model.encode(query).tolist(),
        top_k=res,
        include_values=False,
        include_metadata=True,
        # filter={"genre": {"$eq": "action"}}
    )
    return result
def get_title_and_link_and_desc(obj):    
    descList = obj['metadata']['desc'].split('|@|')
    desc = ' '.join(descList)    
    return {'title': obj['metadata']['title'], 'link': obj['metadata']['link'], 'desc': desc}

STATIC_DIR='./'
def serve_static_file(client_socket, path):
    # Determine the file path relative to the STATIC_DIR
    file_path = os.path.join(STATIC_DIR, path.lstrip('/'))

    # Check if the file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Read the file content
        with open(file_path, 'rb') as file:
            content = file.read()

        # Send HTTP response with the file content
        http_response = "HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n".format(
            get_content_type(file_path), len(content)).encode('utf-8') + content
        client_socket.sendall(http_response)
    else:
        # If file not found, send a 404 response
        http_response = "HTTP/1.1 404 Not Found\r\n\r\n"
        client_socket.sendall(http_response.encode('utf-8'))

def get_content_type(file_path):
    # Map file extensions to MIME types
    mime_types = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.gif': 'image/gif'
        # Add more MIME types as needed
    }
    # Get the file extension
    ext = os.path.splitext(file_path)[1]
    # Lookup and return the corresponding MIME type
    return mime_types.get(ext.lower(), 'application/octet-stream')

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
        if 'searchTopic' in parsed_data:
            submitted_data = parsed_data['searchTopic']
        else:
            submitted_data = "No data submitted"
        print("Submitteddata",submitted_data)
        # Send HTTP response with the submitted data
        objarray=search_pinecone(model,submitted_data,'search','ns2',5)['matches']
        result_array = [get_title_and_link_and_desc(o) for o in objarray]

        http_response_body = json.dumps(result_array)
        http_response = (
            'HTTP/1.1 200 OK\r\n' + 
            'Content-Type: application/json\r\n' +
            f'Content-Length: {len(http_response_body)}\r\n' +
            '\r\n' +
            http_response_body
        )
        client_socket.sendall(http_response.encode('utf-8'))

   
    else:
        # Check if the requested path corresponds to a static file
        serve_static_file(client_socket, path)
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
