import http.client

# Non-Persistent HTTP Connection
def non_persistent_http():
    print("Non-Persistent HTTP")
    for i in range(3):
        connection = http.client.HTTPConnection("httpbin.org")
        connection.request("GET", "/get")
        response = connection.getresponse()
        print(f"Response {i + 1} status: {response.status}, reason: {response.reason}")
        print(f"Response {i + 1} data:", response.read().decode())
        connection.close()  # Closing the connection after each request

# Persistent HTTP Connection
def persistent_http():
    print("\nPersistent HTTP")
    connection = http.client.HTTPConnection("httpbin.org")  # Open a single connection
    for i in range(3):
        connection.request("GET", "/get")
        response = connection.getresponse()
        print(f"Response {i + 1} status: {response.status}, reason: {response.reason}")
        print(f"Response {i + 1} data:", response.read().decode())
        # Do NOT close the connection after each request

    connection.close()  # Close the connection after all requests

if __name__ == "__main__":
    non_persistent_http()
    persistent_http()
