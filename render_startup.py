import os
import streamlit.web.bootstrap
from streamlit import config

# Get the port from Render's environment variable
port = int(os.environ.get("PORT", 8501))

# Configure Streamlit to use this port
config.set_option("server.port", port)
config.set_option("server.address", "0.0.0.0")
config.set_option("browser.serverAddress", "0.0.0.0")
config.set_option("browser.gatherUsageStats", False)

# Start Streamlit
streamlit.web.bootstrap.run("main.py", "", [], {})