import socket
"""
The socket module provides an interface to the BSD socket interface. 
It can be used to write network clients and servers, 
or to create custom network protocols.
"""
import threading
"""
The threading module provides a simple API for writing 
threaded programs in Python. It includes a number of 
classes and functions for working with threads, 
such as Thread, which represents a single thread of execution, 
and Lock, which provides a means of synchronizing access to a resource.
"""
import argparse
"""
The argparse module provides a simple and flexible interface to 
define command-line options and arguments, and to parse their values. 
It allows you to easily add options and arguments to your scripts, 
and parse the command line or a list of arguments.
"""
from os import listdir
"""
The os module provides a portable way of using operating system dependent functionality. 
It contains functions for performing actions like creating, deleting, and modifying files and directories, 
as well as functions for interacting with the environment, system processes, and the shell.
"""
from os.path import isfile, join
"""
The os.path module provides functions for manipulating filenames and paths. 
These functions provide a high-level interface to operations on filenames and paths 
that are operating system-independent.
"""

class HttpServer:
    """
    The HttpServer class implements a simple HTTP server that can serve files from a directory, 
    echo back requests, or return information about the user-agent.
    """
    def __init__(self, directory):
        self.directory = directory if directory else ""
        """
        The __init__ method initializes the instance variables of the class. 
        In this case, the directory variable is initialized to the value passed to the constructor. 
        If no directory is passed, the variable is initialized to an empty string.
        """

    def thread_handling(self):
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True) 
        """
        The thread_handling method creates a socket and listens for incoming connections. 
        It creates a new thread to handle each incoming connection.
        """
        try:
            while True:
                conn, addr = server_socket.accept() # wait client connection
                thread = threading.Thread(target=self.handle_request, args=(conn,))
                thread.daemon = True
                thread.start()
        finally:
            conn.close()
        """
        The finally block ensures that the socket is closed, even if an exception occurs.
        """

    def send_response(self, conn, status, response, content_type="text/plain"):
        conn.sendall(f"HTTP/1.1 {status}\r\n".encode())
        conn.sendall(f"Content-Type: {content_type}\r\n".encode())
        conn.sendall(f"Content-Length: {len(response)}\r\n\r\n".encode())
        conn.sendall(f"{response}\r\n\r\n".encode())
        """
        The send_response method sends a response back to the client. 
        The status code, response body, and content type are sent as headers.
        """

    def handle_request(self, conn):
        data = conn.recv(1024).decode()
        """
        The handle_request method receives data from the client, 
        decodes it, and splits it into lines. 
        The first line of the request contains the HTTP method, path, and version.
        """
        request = data.split("\r\n")
        first_line = request[0]
        http_method, path, http_version = first_line.split(" ")
        """
        The http_method, path, and http_version variables are extracted from the first line.
        """
        headers = {}
        body = None
        for i in range(1, len(request)):
            line = request[i]
            if line == "":
                continue
            elif ": " in line:
                header, value = line.split(": ")
                headers[header] = value
            else:
                body = line
        """
        The headers variable is initialized to an empty dictionary. 
        The for loop iterates over the remaining lines of the request, 
        parsing out the headers and setting the body variable to the remaining data.
        """
        if http_method == "GET" and path == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            """
            If the HTTP method is GET and the path is "/", 
            the response is "HTTP/1.1 200 OK\r\n\r\n".
            """
        elif http_method == "GET" and path.startswith("/echo"):
            response = path.removeprefix("/echo/")
            self.send_response(conn, "200 OK", response)
            """
            If the HTTP method is GET and the path starts with "/echo/", 
            the response is the remainder of the path, without "/echo/".
            """
        elif http_method == "GET" and path == ("/user-agent"):
            response = headers["User-Agent"]
            self.send_response(conn, "200 OK", response)
            """
            If the HTTP method is GET and the path is "/user-agent", 
            the response is the value of the "User-Agent" header.
            """
        elif http_method == "GET" and path.startswith("/files"):
            filename = path.removeprefix("/files/")
            files = [
                fl for fl in listdir(self.directory) if isfile(join(self.directory, fl))
                ]
            if filename in files:
                file_content = ""
                with open(join(self.directory, filename), "r") as content:
                    file_content = content.read()
                self.send_response(
                    conn, "200 OK", file_content, "application/octet-stream"
                )
            else:
                self.send_response(conn, "404 Not Found", "")
            """
            If the HTTP method is GET and the path starts with "/files/", 
            the response is the contents of the file with the given name, 
            or a 404 Not Found response if the file does not exist.
            """
        elif http_method == "POST" and path.startswith("/files"):
            filename = path.removeprefix("/files/")
            try:
                with open(join(self.directory, filename), "wb") as file:
                    file.write(body.encode())
                self.send_response(conn, "201 Created", "")
            except Exception as e:
                self.send_response(
                    conn, "500 Internal Server Error", f"Error writing file: {e}"
                    )
        else:
            self.send_response(conn, "404 Not Found", "")
        """
        If the HTTP method is not recognized, a 404 Not Found response is sent.
        """

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory")
    args = parser.parse_args()

    directory = args.directory

    server = HttpServer(directory)
    server.thread_handling()

if __name__ == "__main__":
    main()
