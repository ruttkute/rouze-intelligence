#!/usr/bin/env python3
import os
from typing import Optional
from dotenv import load_dotenv
import praw
from prawcore.exceptions import ResponseException

def mask(s: Optional[str]) -> str:
    if not s:
        return "None"
    s = str(s)
    return s if len(s) <= 8 else f"{s[:4]}...{s[-4:]} (len={len(s)})"

def poke(reddit: praw.Reddit) -> str:
    reddit.read_only = True
    for post in reddit.subreddit("test").hot(limit=1):
        return f"OK. Sample post: {post.title[:80]}"
    return "OK (no posts returned)."

def main():
    load_dotenv()

    cid   = (os.getenv("REDDIT_CLIENT_ID") or "").strip()
    csec  = (os.getenv("REDDIT_CLIENT_SECRET") or "").strip()          # blank is fine for Installed App
    ua    = (os.getenv("REDDIT_USER_AGENT") or "").strip()
    user  = (os.getenv("REDDIT_USERNAME") or "").strip()
    pwd   = (os.getenv("REDDIT_PASSWORD") or "").strip()

    print("Client ID:     ", mask(cid))
    print("Client Secret: ", "EMPTY (installed app)" if csec == "" else mask(csec))
    print("User Agent:    ", ua)
    if user or pwd:
        print("Username:      ", user if user else "None")
        print("Password:      ", "***" if pwd else "None")

    if not (cid and ua):
        print("\nMissing required values. Put these in .env at project root (no quotes):\n"
              "REDDIT_CLIENT_ID=...\n"
              "REDDIT_CLIENT_SECRET=    # blank if Installed App\n"
              "REDDIT_USER_AGENT=rouze-signal-miner/0.1 by <your_reddit_username>\n"
              "Optional for Script app: REDDIT_USERNAME=... and REDDIT_PASSWORD=...\n")
        return

    # ---- Flow A: Script app (password grant) ----
    if user and pwd and csec:
        print("\nTrying Script app (password grant)...")
        try:
            r = praw.Reddit(client_id=cid, client_secret=csec, user_agent=ua,
                            username=user, password=pwd)
            print(poke(r))
            return
        except Exception as e:
            print("Script flow failed:", repr(e))

    # ---- Flow B: Client credentials (app-only) ----
    if csec:
        print("\nTrying app-only (client_credentials) flow...")
        try:
            r = praw.Reddit(client_id=cid, client_secret=csec, user_agent=ua)
            print(poke(r))
            return
        except ResponseException as e:
            print("Client credentials failed (401).")
        except Exception as e:
            print("Client credentials failed:", repr(e))

    # ---- Flow C: Installed app (no secret) + device id ----
    print("\nTrying Installed app (no secret) with device_id...")
    try:
        r = praw.Reddit(client_id=cid, client_secret=None, user_agent=ua,
                        device_id="DO_NOT_TRACK_THIS_DEVICE")
        print(poke(r))
        return
    except Exception as e:
        print("Installed-app flow failed:", repr(e))

    print("\nAll flows failed. Most common fixes:\n"
          "• App type mismatch: \n"
          "    - Installed app → leave REDDIT_CLIENT_SECRET blank.\n"
          "    - Script app → set REDDIT_CLIENT_SECRET and add REDDIT_USERNAME / REDDIT_PASSWORD.\n"
          "    - Web app → use real SECRET (client_credentials).\n"
          "• Copy values exactly, no quotes, no trailing spaces.\n"
          "• USER_AGENT must be descriptive: 'rouze-signal-miner/0.1 by <username>'.")
    
if __name__ == "__main__":
    main()
