#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import argparse

# using SNAP_USER_COMMON if available, else default to ./common for dev
joblib_temp = os.environ.get("JOBLIB_TEMP_FOLDER", "./joblib")
Path(joblib_temp).mkdir(parents=True, exist_ok=True)

CONFIG_DIR = Path(os.environ.get("SNAP_USER_COMMON", "./common"))
ENV_PATH = CONFIG_DIR / ".env"

def write_env_file(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with ENV_PATH.open("w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")

def run_config():
    print("Setup PySearch configuration")

    # loading existing env values if available
    existing = {}
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=ENV_PATH)
        keys = ["PINECONE_KEY", "PINECONE_ENVIRONMENT", "HOST", "PORT", "GUNICORN", "GUNICORN_WORKERS", "GET_RESULT_COUNT"]
        existing = {key: os.getenv(key, "") for key in keys}

    def prompt(key, message, default_val):
        current = existing.get(key, "")
        fallback = current or default_val
        val = input(f"{message} (default: {fallback}): ").strip()
        return val or fallback

    config = {
        "PINECONE_KEY": prompt("PINECONE_KEY", "PINECONE_KEY", ""),
        "PINECONE_ENVIRONMENT": prompt("PINECONE_ENVIRONMENT", "PINECONE_ENVIRONMENT", ""),
        "HOST": prompt("HOST", "HOST", "0.0.0.0"),
        "PORT": prompt("PORT", "PORT", "8000"),
        "GUNICORN": prompt("GUNICORN", "Use Gunicorn? (True/False)", "False"),
        "GUNICORN_WORKERS": prompt("GUNICORN_WORKERS", "Gunicorn workers", "1"),
        "GET_RESULT_COUNT": prompt("GET_RESULT_COUNT", "No of relevant results to serve", "50")
    }

    write_env_file(config)
    print(f"Configuration saved to {ENV_PATH}")

def run_app():
    if not ENV_PATH.exists():
        print(f"ERROR: Config file {ENV_PATH} missing. Run with --config first.", file=sys.stderr)
        sys.exit(1)

    load_dotenv(dotenv_path=ENV_PATH)

    if not os.getenv("PINECONE_KEY") or not os.getenv("PINECONE_ENVIRONMENT"):
        print("ERROR: PINECONE_KEY or PINECONE_ENVIRONMENT missing in config.", file=sys.stderr)
        sys.exit(1)

    host = os.getenv("HOST", "0.0.0.0")
    try:
        port = int(os.getenv("PORT", "8000"))
    except ValueError:
        print("Invalid PORT value; must be an integer.", file=sys.stderr)
        sys.exit(1)

    use_gunicorn = os.getenv("GUNICORN", "False").lower() == "true"
    workers = os.getenv("GUNICORN_WORKERS", "1")
    try:
        workers = int(workers)
    except ValueError:
        print("Invalid GUNICORN_WORKERS value; must be an integer.", file=sys.stderr)
        workers = 1  # fallback

    if use_gunicorn:
        import subprocess
        subprocess.run([
            "gunicorn",
            "--bind", f"{host}:{port}",
            "--workers", str(workers),
            "app:app"
        ])
    else:
        import app
        app.app.run(host=host, port=port)

def main():
    parser = argparse.ArgumentParser(
        description="PySearch CLI - Configure and run the application"
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Run initial setup and create the .env configuration file"
    )
    args = parser.parse_args()

    if not ENV_PATH.exists() or args.config:
        run_config()
        return

    run_app()

if __name__ == "__main__":
    main()
