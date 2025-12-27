import os
import sys
import requests
from datetime import datetime

# -----------------------------
# ENV INPUTS
# -----------------------------
FIRST_NAME = os.getenv("FIRST_NAME", "").strip()
MIDDLE_NAME = os.getenv("MIDDLE_NAME", "").strip()
LAST_NAME = os.getenv("LAST_NAME", "").strip()
EMAIL = os.getenv("EMAIL", "").strip()
MEMBER_ID = os.getenv("MEMBER_ID", "").strip()

ORG_NAME = "support-vdac"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# -----------------------------
# VALIDATION
# -----------------------------
if not FIRST_NAME or not LAST_NAME or not MEMBER_ID:
    print("❌ Required inputs missing")
    sys.exit(1)

if not GITHUB_TOKEN:
    print("❌ GitHub token missing")
    sys.exit(1)

# -----------------------------
# REPO NAME LOGIC
# -----------------------------
year = datetime.now().year
first_letter = FIRST_NAME[0].lower()
last_name_trimmed = LAST_NAME[:-1].lower()

repo_name = f"st{year}-{first_letter}{last_name_trimmed}-{MEMBER_ID.lower()}"

print(f"✅ Creating repository: {repo_name}")

# -----------------------------
# GITHUB API CALL
# -----------------------------
url = f"https://api.github.com/orgs/{ORG_NAME}/repos"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

payload = {
    "name": repo_name,
    "private": True,
    "auto_init": True,
    "description": f"Student repo for {FIRST_NAME} {LAST_NAME} ({MEMBER_ID})"
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 201:
    print("🎉 Repository created successfully")
    print(response.json()["html_url"])
else:
    print("❌ Failed to create repository")
    print(response.status_code, response.text)
    sys.exit(1)
