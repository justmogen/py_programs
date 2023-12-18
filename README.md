Certainly! Here's the information provided in a more standard README.md format:

markdown
Copy code
# HTTP Server

This is a simple HTTP server written in Python that can handle GET and POST requests. The server can serve files from a specified directory and can also echo back messages sent in the request.

## Requirements

- Python 3.x

## Usage

To run the server, execute the following command:

```bash
python http_server.py --directory <directory_path>
Replace <directory_path> with the path to the directory from which files should be served. If no directory is specified, the server will serve files from the current directory.

Once the server is running, you can send HTTP requests to it using curl or any other HTTP client. Here are some examples:

Sending a GET request to the root path /
curl -v http://localhost:4221/

This should return a 200 OK response.

Sending a GET request to the /echo path with a message
curl -v http://localhost:4221/echo/Hello%20World

This should return a 200 OK response with the message "Hello World."

Sending a GET request to the /user-agent path
curl -v -H "User-Agent: My User Agent" http://localhost:4221/user-agent

This should return a 200 OK response with the user agent string.

Sending a GET request to the /files path with a filename
curl -v http://localhost:4221/files/myfile.txt

This should return a 200 OK response with the contents of the file "myfile.txt" in the server's directory.

Sending a POST request to the /files path with a filename and contents
curl -v -X POST -d "Hello World" http://localhost:4221/files/myfile.txt

This should return a 201 Created response and create a file "myfile.txt" in the server's directory with the contents "Hello World."
