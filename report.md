

# 🧠 Learning Report: Building a Basic HTTP Server with Sockets

## 📘 Terminologies

* **Socket**: Interface that performs I/O operations over the network.
* **Server**: A program that listens for client requests and responds accordingly.
* **Client**: A user or program that connects to the server to send requests and receive responses.

---

## ⚙️ Technical Details

* `AF_INET`: Specifies the use of IPv4 addressing.
* `socket.SOCK_STREAM`: Indicates a TCP connection (reliable and connection-oriented).
* `server.listen(5)`: The server can queue up to 5 incoming connections.
* HTTP Version: Uses `HTTP/1.1`.

---

## 🔄 How the Communication Happens

1. A client (e.g., browser) initiates a connection to the server over **TCP**.

2. Once connected, the client sends an **HTTP request** with headers.

3. For example, accessing `openai.com/pricing` would send:

   ```
   GET /pricing HTTP/1.1
   Host: openai.com
   Content-Type: text/html
   ```

4. The server reads the request, processes it, and sends an appropriate **HTTP response**.

5. The connection may then be closed or kept alive based on the headers.

---

## ⛔ Blocking Behavior

* The following socket operations are **blocking by default**:

  * `accept()`
  * `recv()`
  * `send()`
* Blocking means the server **pauses execution** until these operations complete.

---

## ✅ Why Use `select()`

* `select()` helps avoid blocking by:

  * Monitoring **multiple sockets**.
  * Returning **only those sockets** that are ready for:

    * **Reading**
    * **Writing**
    * **Error handling**
* This allows the server to handle **many clients concurrently** without threading or blocking.

---

## ⚠️ Limitation of `select()`

* `select()` has a hard-coded limit of **1024 sockets** on many systems (due to `FD_SETSIZE`).
* For **more than 1024 connections**, alternatives like `poll()` or `epoll()` (Linux) are recommended.
