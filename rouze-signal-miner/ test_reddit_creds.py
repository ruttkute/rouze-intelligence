#!/usr/bin/env python3
"""
Test script to verify Reddit API credentials
"""

import os
import praw
from dotenv import load_dotenv

def test_reddit_connection():
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET") 
    user_agent = os.getenv("REDDIT_USER_AGENT")
    
    print("🔍 Checking Reddit Credentials...")
    print(f"Client ID: {'✅ Present' if client_id else '❌ Missing'}")
    print(f"Client Secret: {'✅ Present' if client_secret else '❌ Missing'}")  
    print(f"User Agent: {'✅ Present' if user_agent else '❌ Missing'}")
    
    if not all([client_id, client_secret, user_agent]):
        print("\n❌ Missing credentials! Check your .env file.")
        return False
    
    print(f"\nClient ID: {client_id}")
    print(f"User Agent: {user_agent}")
    print(f"Client Secret: {client_secret[:5]}...{client_secret[-5:]}")
    
    # Test connection
    try:
        print("\n🔌 Testing Reddit API connection...")
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret, 
            user_agent=user_agent,
        )
        reddit.read_only = True
        
        # Test by fetching a single post from r/test
        print("📡 Fetching test post from r/test...")
        subreddit = reddit.subreddit("test")
        for post in subreddit.hot(limit=1):
            print(f"✅ Success! Got post: {post.title[:50]}...")
            break
            
        print("🎉 Reddit API connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Reddit API connection failed: {e}")
        return False

if __name__ == "__main__":
    test_reddit_connection()