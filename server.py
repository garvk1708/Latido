import os
import subprocess

def run():
    port = int(os.environ.get("PORT", 8501))  # Vercel will provide PORT
    subprocess.run(["streamlit", "run", "main.py", "--server.port", str(port), "--server.address", "0.0.0.0"])

if __name__ == "__main__":
    run()
