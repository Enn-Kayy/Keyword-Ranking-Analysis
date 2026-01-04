import os
from dotenv import load_dotenv
from pathlib import Path


# Load environment variables from the project-level .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path, override=True)

# API keys
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Google search configuration
LOCATION = "Noida,Uttar Pradesh,India"
GOOGLE_DOMAIN = "google.co.in"
GL = "in"
HL = "en"

# Search result configuration
RESULTS_PER_PAGE = 100
