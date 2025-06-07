import json
import select
import socket
import traceback
from db import note_db

HOST = "0.0.0.0"
PORT = 8001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)

sockets_list = [server]
clients = {}

print(f"API Server running on http://{HOST}:{PORT}")


def jsonify(data: dict) -> str:
    return json.dumps(data)


def create_response(
    status_code: int, status_message: str, content_type: str, body: str
):
    """Create HTTP response string"""
    return f"""HTTP/1.1 {status_code} {status_message}
Content-Type: {content_type}

{body}"""


def send_response(
    client_socket: socket.socket,
    status_code: int,
    status_message: str,
    content_type: str,
    body: str,
):
    """Send HTTP response to client and close connection"""
    response = create_response(status_code, status_message, content_type, body)
    client_socket.sendall(response.encode())
    client_socket.close()
    if client_socket in sockets_list:
        sockets_list.remove(client_socket)


def send_json_response(
    client_socket: socket.socket, data: dict, status_code: int = 200
):
    """Send JSON response"""
    send_response(client_socket, status_code, "OK", "application/json", jsonify(data))


def send_error_response(client_socket: socket.socket, status_code: int, message: str):
    """Send error response"""
    status_messages = {
        400: "Bad Request",
        404: "Not Found",
        500: "Internal Server Error",
    }
    send_response(
        client_socket,
        status_code,
        status_messages.get(status_code, "Error"),
        "text/html",
        message,
    )


def parse_client_request(request):
    first_line = request.splitlines()[0]
    method, path, _ = first_line.split()
    headers = {}
    for line in request.splitlines()[1:]:
        if line.strip() == "":
            break
        key, value = line.split(": ", 1)
        headers[key.strip()] = value.strip()
    last_line = request.splitlines()[-1]
    payload = last_line
    if payload.strip() != "":
        payload = json.loads(payload)
    return method, path, headers, payload


def parse_query_params(path: str) -> dict:
    # path => /search?q=hey&qu=h
    params = {}
    if "?" in path:
        path, query_string = path.split("?", 1)
        for param in query_string.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                params[key.strip()] = value.strip()
    return path, params


def handle_get_request(path: str, client_socket: socket.socket):
    """Handle GET requests"""
    path, query_params = parse_query_params(path)
    if path == "/notes":
        response = note_db.get_all_notes()
        send_json_response(client_socket, response)
    elif path == "/":
        send_response(client_socket, 200, "OK", "text/html", open("index.html").read())
    elif path == "/api.js":
        send_response(
            client_socket, 200, "OK", "text/javascript", open("api.js").read()
        )
    elif path == "/search":
        query = query_params["q"]
        response = note_db.search_notes(query)
        send_json_response(client_socket, response)
    else:
        send_error_response(client_socket, 404, "Not found")


def handle_post_request(path: str, payload: str, client_socket: socket.socket):
    """Handle POST requests"""
    if path == "/notes":
        if "title" in payload and "content" in payload:
            note_db.create_note(payload["title"], payload["content"])
            send_json_response(client_socket, {"status": "ok"})
        else:
            send_error_response(client_socket, 400, "Bad request")
    else:
        send_error_response(client_socket, 404, "Not found")


def handle_put_request(path: str, payload: str, client_socket: socket.socket):
    """Handle PUT requests"""
    if path == "/notes":
        note_db.update_note(str(payload["id"]), payload["title"], payload["content"])
        send_json_response(client_socket, {"status": "ok"})
    else:
        send_error_response(client_socket, 404, "Not found")


def handle_delete_request(path: str, payload: str, client_socket: socket.socket):
    """Handle DELETE requests"""
    if path == "/notes":
        note_db.delete_note(str(payload["id"]))
        send_json_response(client_socket, {"status": "ok"})
    else:
        send_error_response(client_socket, 404, "Not found")


def handle_request(client_socket: socket.socket, request: str):
    """Main request handler"""
    method, path, headers, payload = parse_client_request(request)

    request_handlers = {
        "GET": handle_get_request,
        "POST": handle_post_request,
        "PUT": handle_put_request,
        "DELETE": handle_delete_request,
    }

    handler = request_handlers.get(method)
    if handler:
        if method == "GET":
            handler(path, client_socket)
        else:
            handler(path, payload, client_socket)
    else:
        send_error_response(client_socket, 405, "Method Not Allowed")


def start_server(*args, **kwargs):
    while True:
        rs, _, _ = select.select(sockets_list, [], [])
        for s in rs:
            if s == server:
                client_socket, client_address = server.accept()
                client_socket.setblocking(False)
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
                print(f"New client from {client_address}")
            else:
                try:
                    s: socket.socket
                    request = s.recv(4096).decode()
                    handle_request(s, request)
                except Exception as e:
                    traceback.print_exc()
                    if s in clients:
                        del clients[s]
                    if s in sockets_list:
                        sockets_list.remove(s)
                    s.close()


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        server.close()
        sockets_list.clear()
        clients.clear()
    except Exception as e:
        print(e)
        server.close()
        sockets_list.clear()
        clients.clear()
