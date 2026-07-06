import subprocess
import sys

def main():
    result = subprocess.run([
        "openapi-python-client",
        "generate",
        "--url", "http://localhost:8000/api/openapi.json",
        "--meta", "uv",
        "--overwrite",
        "--config", "openapi_config.yaml"
    ], check=False)
    sys.exit(result.returncode)