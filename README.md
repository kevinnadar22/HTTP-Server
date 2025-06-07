# Zero-Framework Notes App

> **Built from absolute scratch** - Pure Python, vanilla JavaScript, and HTML/CSS. No Express, No React, No Flask, No databases.

![Notes App Interface](assets/demo.png)

## What Makes This Special

- **100% Framework-Free Backend**: Raw Python sockets, manual HTTP parsing, custom routing
- **Pure Vanilla Frontend**: Zero JavaScript frameworks - just DOM manipulation and fetch API
- **Custom Database**: JSON-based ORM built from scratch with auto-persistence
- **Manual HTTP Protocol**: Hand-crafted request/response handling
- **Async Non-blocking Server**: Built with Python `select` for concurrent connections


## Learning Journey

This project was my learning of **low-level web fundamentals**:
- Understanding HTTP protocol from ground up
- Socket programming and network communication
- Building database abstractions without ORMs

## How the Communication Happens

1. A client (e.g., browser) initiates a connection to the server over **TCP**.

![alt text](assets/step1.png)

2. Once connected, the client sends an **HTTP request** with headers.

3. For example, accessing `openai.com/pricing` would send:

   ```
   GET /pricing HTTP/1.1
   Host: openai.com
   Content-Type: text/html
   ```

![alt text](assets/step2.png)

4. The server reads the request, processes it, and sends an appropriate **HTTP response**.

5. The connection may then be closed or kept alive based on the headers.


**Next Goal**: Building a mini web framework from these learnings

## Quick Start

```bash
# Clone and run - that's it!
git clone https://github.com/kevinnadar22/HTTP-Server
cd HTTP-Server
python main.py
```

Open http://localhost:8000 - Your notes app is ready! ✓


## ✓ Features
- Full CRUD (Create, Read, Update, Delete)
- Real-time search and responsive design
- Auto-saving database and modern UI
- Concurrent connections and error handling
- HTTP compliance and RESTful API

## UI Demo

![Notes App Interface](assets/demo.gif)


## 🛠 Technical Stack

| Layer | Technology | Why No Framework? |
|-------|------------|-------------------|
| **Server** | Raw Python Sockets | Learn HTTP fundamentals |
| **Database** | Custom JSON ORM | Understand data persistence |
| **Frontend** | Vanilla JS + CSS | Master DOM manipulation |

---

## Contact

Feel free to reach out:

- GitHub: [kevinnadar22](https://github.com/kevinnadar22)
- Email: [jesikamaraj@gmail.com](mailto:jesikamaraj@gmail.com)

