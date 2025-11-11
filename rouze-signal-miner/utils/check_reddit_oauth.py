# utils/check_reddit_oauth.py
import os, json, base64, requests

REQUIRED = ["REDDIT_CLIENT_ID","REDDIT_CLIENT_SECRET","REDDIT_USERNAME","REDDIT_PASSWORD"]
miss = [k for k in REQUIRED if not os.getenv(k)]
if miss:
    raise SystemExit(f"Missing env vars: {', '.join(miss)}")

ua = os.getenv("REDDIT_USER_AGENT", "rouze-signal-miner/0.1 (by u/Even_Regular_2938)")
auth = (os.getenv("REDDIT_CLIENT_ID"), os.getenv("REDDIT_CLIENT_SECRET"))

data = {
    "grant_type": "password",
    "username": os.getenv("REDDIT_USERNAME"),
    "password": os.getenv("REDDIT_PASSWORD"),
    "scope": "read",
}
headers = {"User-Agent": ua, "Content-Type": "application/x-www-form-urlencoded"}

r = requests.post("https://www.reddit.com/api/v1/access_token",
                  data=data, headers=headers, auth=auth)

print("HTTP", r.status_code)
try:
    j = r.json()
except Exception:
    print(r.text)
    raise

print(json.dumps(j, indent=2))
if r.status_code == 200 and "access_token" in j:
    print("\nOK ✓ Token received.")
else:
    print("\nProblem →", j.get("error","?"))
