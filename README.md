<h1 align="center">
Project Setup
</h1>

### Create virtual environment

``` python -m venv search_engine ```

### Activate virtual environment (from parent folder)

```Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass```

``` .\search_engine\Scripts\activate ```

### Install required libraries

``` pip install version_requirements.txt  ```

### Select kernel for Jupiter Notebook ( ipynb )

From top right corner select ``` (parent_folder)/Scripts/python.exe ``` as kernel and run

For python file use ``` python file_name ``` to execute

<h1 align="center">
Output View
</h1>
**Pinecone Side Vectors** 

![pinecone](https://github.com/user-attachments/assets/0bd8a37f-510c-471e-9206-76135b905bd1)

**Client Side Search Results :**

![Screenshot 2024-04-02 211102](https://github.com/user-attachments/assets/0919f4ca-4dc4-4ca4-9ccb-b65507d44f09)

![Screenshot 2024-04-02 210855](https://github.com/user-attachments/assets/11d6e250-1818-4ec9-aeaf-4e146a0fcb55)

![Screenshot 2024-04-02 210658](https://github.com/user-attachments/assets/4a87cff9-89ff-42fc-887b-ea1a1aee1765)



**Server Side Messages :**

![Screenshot 2024-04-02 211726](https://github.com/user-attachments/assets/d5ee1091-24ac-48b5-9253-3120f3f6305d)

![image](https://github.com/user-attachments/assets/750f1b92-2595-4397-9302-3f9d180d5724)

<h1 align="center">
Design and Discussion
</h1>

**Group Members:** Tamal Mallick , Sushanta Das , Suvam Manna 

**Problem Description**:

Building a **search engine for a specific domain** (Python) with the help of **web crawling, Socket**

**programming, sentence embedding and Vector database**, to get relevant result for specific domain. User

will get result of a search query based on **cosine similarity search** in vector database. Also implemented and

integrated **Knapsack Cryptosystem** for securely transmitting user query and search results over network.

**Algorithm and Design:**

**1) Collecting web pages to make our search engine database**

i) Implemented web crawling using multithreading with some starting links containing keyword

“Python”, to collect link of webpage and then metadata (such as title, heading tag, some

paragraph) to gather valuable information about each link. This information will be used to

search for the webpage URL.

ii) We are collecting only the valid link / webpages by ignoring the links with status code in

between (400 ,499)

iii) These data are stored in Vector database (Pinecone) as Word Embeddings (High dimensional

Vectors ,768 dimensions). Now we can search some query, database will return most similar

results (each result having title, link and description).

**2) Building and running the webserver**

i) Webserver is implemented using socket programming with multithreading which will handle

multiple HTTP request coming from clients.

ii) Once the server is running, if anyone search the server URL using web client (Browser) first

the server is sends Required html, CSS and JavaScript file to run the main client program and

access frontend to see outputs.

iii) Once the dedicated client’s program (client.js) is running, in case of Secure mode public key

and private key is generated using knapsack cryptographic algorithm. First server and client

exchange their public keys. Then it will continue to listen for search requests from client.

iv) Now onwards whenever the server receives a search request from client it performs a cosine

similarity search on the vector database/local file and send the top results to the client. In

secure mode encryption and decryption are performed before each send operation and after

each receive operation through socket.

**3) Searching some query**

i) User will visit the link at which server is running (like <http://192.168.29.37:8080/>[).](http://192.168.29.37:8080/)[ ](http://192.168.29.37:8080/)A

webpage will open which has input box and search button. In Secure mode client will receive

public key of server.



ii) When user types some search query and hits submit button, client will send the query to the

server. Server has an endpoint for accepting Post request (POST /submit HTTP/1.1). Server

will accept the request.

iii) Now server will call a function for searching on vector database and finally send the relevant

search results to the client.

iv) Results will be displayed in the client’s webpage.


**Future Work**

Future enhancements and developments for the search engine may include increasing the searching speed,

understand and collect more valuable metadata, providing summery of the top results, refining search

algorithms for enhanced accuracy and relevance, expanding the search database to encompass a broader

range of Python-related content, integrating advanced security features to mitigate emerging threats, and

incorporating user feedback to continuously enhance the user experience and functionality.

**Conclusion**

The creation of a domain-specific search engine tailored for Python represents a significant leap forward in

providing users with a robust platform for accessing relevant information within the Python programming

ecosystem. By seamlessly integrating advanced technologies such as web crawling, vector databases, socket

programming, and cryptographic protocols, this search engine delivers not only swift and accurate search

results but also ensures the security of user interactions. Also, implementation of multithreading and query-

based client holding allow us to save the resources and serve large number of clients at a time.


