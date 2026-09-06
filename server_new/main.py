import os
import subprocess
import os
import signal
import time
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("./.env")

load_dotenv(dotenv_path= env_path)

# Important ports
GATEWAY_SERVICE_PORT = int(os.getenv("GATEWAY_SERVICE_PORT", 4000))
EMBEDDING_SERVICE_PORT = int(os.getenv("EMBEDDING_SERVICE_PORT", 4001))
SEARCH_SERVICE_PORT = int(os.getenv("SEARCH_SERVICE_PORT", 4002))

class GunicornServiceManager:
    def __init__(self, name: str, app_folder: str, entry_point: str = "main:app", host: str = "0.0.0.0", port: int = 4000):
        self.process, self.name = None, name
        self.app_folder, self.entry_point = app_folder, entry_point
        self.host , self.port = host, port

    def start(self, workers:int =1, timeout:int = 120, worker_connections: int= 1024):
        if self.process is not None:
            print(f"[{self.name}] Already running on port {self.port}.")
            return
        command = [
            "gunicorn",
            "-w", str(workers),
            "-k", "uvicorn.workers.UvicornWorker",
            str(self.entry_point),
            "--bind", f"{self.host}:{self.port}",
            "--timeout", str(timeout),
            "--worker-connections", str(worker_connections)
        ]
        print(f"[{self.name}] Starting service on port {self.port}...")
        self.process = subprocess.Popen(
            command,
            cwd= self.app_folder,
            # stdout=subprocess.DEVNULL, # long running process,no output needed
            # stderr=subprocess.DEVNULL,
            stdout=subprocess.PIPE, # long running process,no output needed
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid # to stop the process
        )
    
    def stop(self):
        if self.process is None:
            print(f"[{self.name}] Service not running.")
            return
        print(f"[{self.name}] Stopping service on port {self.port}...")
        try:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process.wait(timeout=10)
        except Exception as e:
            print(f"[{self.name}] Error while stopping: {e}")
        finally:
            self.process = None
            print(f"[{self.name}] Stopped.")

def main():
    # Instantiate services
    gateway = GunicornServiceManager(name="gateway", port=GATEWAY_SERVICE_PORT, app_folder="./gateway_service")
    embedding = GunicornServiceManager(name="embedding", port=EMBEDDING_SERVICE_PORT, app_folder="./embedding_service")
    search = GunicornServiceManager(name="search", port=SEARCH_SERVICE_PORT, app_folder="./search_service")

    services = [gateway, embedding, search]

    def signal_handler(sig, frame):
        print(f"\nSignal {sig} received. Shutting down services...\n")
        for service in services:
            service.stop()
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Start all services
        gateway.start(workers=4, timeout=90)
        embedding.start(workers=2, timeout=90)
        search.start(workers=3, timeout=75)

        print("\nAll services are running. Press Ctrl+C to stop them.\n")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Shutting down services...\n")
        for service in services:
            service.stop()

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        for service in services:
            service.stop()

if __name__ == "__main__":
    main()
