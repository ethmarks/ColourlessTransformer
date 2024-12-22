import subprocess
import sys

# Check if the script is being run directly
if __name__ == "__main__":
    # Check if Streamlit is installed and run the Streamlit app
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
