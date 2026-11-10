import subprocess
import time
import urllib.request

def test_server():
    print("Launching Streamlit in background...")
    proc = subprocess.Popen([
        "python", "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.headless", "true"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        time.sleep(4)
        print("Probing http://localhost:8501 ...")
        resp = urllib.request.urlopen("http://localhost:8501", timeout=5)
        print(f"Server response code: {resp.getcode()}")
        content = resp.read().decode('utf-8')
        print(f"Content length: {len(content)} bytes")
        if "Streamlit" in content or "bioron" in content.lower():
            print("Streamlit app probed successfully!")
        else:
            print("Response received, app running.")
    except Exception as e:
        print(f"Error during probe: {e}")
    finally:
        print("Stopping background Streamlit process...")
        proc.terminate()
        proc.kill()
        print("Test complete.")

if __name__ == '__main__':
    test_server()
