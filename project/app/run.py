from app import create_app
import socket

app = create_app()

if __name__ == "__main__":
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)
    app.run(host=hostname)