import socket
from urllib.parse import parse_qs
import threading
import json
import base64
from base64 import b64decode
import os
from dotenv import load_dotenv
import os
load_dotenv()
from pinecone import Pinecone 
from knapsack import knapsack 

from sentence_transformers import SentenceTransformer
model=SentenceTransformer("msmarco-distilbert-base-v3")
public_key_server,private_key_server,ks=None,None,None

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
    prev=[]
    new_res=[]
    for i,res in    enumerate(result['matches']): 
        show=res['metadata']
        title=show['title']
        if title not in prev:
            new_res.append(res)
            prev.append(title)
    return new_res
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

def generateKeys():
    global public_key_server,private_key_server,ks
    ks=knapsack()
    private_key_server, modulus, public_key_server = ks.private_public_key(8, 8)
    


def encrypt(data,publicKey):
    global ks
    encrypted_text = ks.encryption(data, publicKey)
    return encrypted_text


 
def decrypt(client_encrypted_data):
    global ks
    decrypted_text = ks.decryption(client_encrypted_data)
    return decrypted_text


def handle_request(client_socket):
    print("handlerequest")
    request_data = client_socket.recv(1024).decode('utf-8')
    print(request_data)
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
    elif method == 'GET' and path == '/public-key':
        public_key_server_base64=json.dumps(public_key_server)
        http_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(public_key_server_base64)}\r\nContent-Type: text/plain\r\n\r\n{public_key_server_base64}"
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
        parsed_data = json.loads(post_data,strict=False)
        print(parsed_data)
        # Check if the 'data' key exists in the parsed data
        Client_public_key=parsed_data['publicKey']
        submitted_data = decrypt(parsed_data['searchTopic'])
        
            
        print("Submitteddata",submitted_data)
        # Send HTTP response with the submitted data
        objarray=search_pinecone(model,submitted_data,'search','ns2',50)# matches
        result_array = [get_title_and_link_and_desc(o) for o in objarray]

        http_response_body = json.dumps(result_array)

        print("Public Key of Client",Client_public_key)
        encryptedData=encrypt(http_response_body,Client_public_key)
        http_response = (
            'HTTP/1.1 200 OK\r\n' + 
            'Content-Type: application/json\r\n' +
            f'Content-Length: {len(encryptedData)}\r\n' +
            '\r\n' +
            encryptedData
        )
        

        
        client_socket.sendall(http_response.encode('utf-8'))

   
    else:
        # Check if the requested path corresponds to a static file
        serve_static_file(client_socket, path)
    client_socket.close()
def main():
    
    generateKeys()
    hostname = socket.gethostname()

# Get the IP address associated with the hostname
    ip_address = socket.gethostbyname(hostname)

    host = ip_address
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server is listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Received connection from {client_address}")
            client_thread = threading.Thread(target=handle_request, args=(client_socket,))
            client_thread.start()
            
    except KeyboardInterrupt:
        print("Shutting down the server.")
        server_socket.close()

if __name__ == "__main__":
    main()