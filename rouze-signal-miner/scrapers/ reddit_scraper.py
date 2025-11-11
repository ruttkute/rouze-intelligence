import os
import praw
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Try to import from local modules, fall back if not available
try:
    from scrapers.base import BaseScraper
except ImportError:
    print("Warning: Could not import BaseScraper, using basic class")
    class BaseScraper:
        def __init__(self, cfg):
            self.cfg = cfg

try:
    from utils.normalizer import normalized
except ImportError:
    print("Warning: Could not import normalizer, using basic function")
    def normalized(**kwargs):
        return kwargs

class RedditScraper(BaseScraper):
    name = "reddit"
    
    def __init__(self, cfg: dict):
        super().__init__(cfg)
        
        # Load environment variables explicitly
        load_dotenv()
        
        # Get credentials from environment
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT")
        
        # Debug print
        print(f"Client ID present: {'Yes' if self.client_id else 'No'}")
        print(f"Client Secret present: {'Yes' if self.client_secret else 'No'}")
        print(f"User Agent present: {'Yes' if self.user_agent else 'No'}")
        
        # Fail fast if anything is missing
        if not all([self.client_id, self.client_secret, self.user_agent]):
            missing = []
            if not self.client_id: missing.append("REDDIT_CLIENT_ID")
            if not self.client_secret: missing.append("REDDIT_CLIENT_SECRET")
            if not self.user_agent: missing.append("REDDIT_USER_AGENT")
            raise RuntimeError(f"Missing Reddit credentials: {', '.join(missing)}")
        
        # Initialize Reddit API
        try:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent,
            )
            self.reddit.read_only = True
            
            # Test the connection
            print("Testing Reddit connection...")
            # Simple test without accessing user info (which requires OAuth)
            test_sub = self.reddit.subreddit("test")
            print("Reddit connection successful!")
            
        except Exception as e:
            print(f"Reddit authentication failed: {e}")
            raise RuntimeError(f"Reddit authentication failed: {e}")

    def _fetch_sub(self, sub: str, mode: str, limit: int):
        """Fetch posts from a subreddit"""
        try:
            s = self.reddit.subreddit(sub)
            
            if mode == "new":
                return s.new(limit=limit)
            if mode == "hot": 
                return s.hot(limit=limit)
            if mode == "top_day":
                return s.top(time_filter="day", limit=limit)
            if mode == "top_week":
                return s.top(time_filter="week", limit=limit) 
            return s.new(limit=limit)
            
        except Exception as e:
            print(f"Error fetching from r/{sub}: {e}")
            return []

    def run(self) -> List[Dict[str, Any]]:
        """Main scraping method"""
        out: List[Dict[str, Any]] = []
        
        # Get settings from config
        subs = self.cfg.get("subreddits", [])
        mode = self.cfg.get("mode", "top_day")
        limit = int(self.cfg.get("limit_per_subreddit", 100))
        
        print(f"Scraping {len(subs)} subreddits in '{mode}' mode, {limit} posts each")
        
        for sub in subs:
            print(f"Processing r/{sub}...")
            try:
                posts = self._fetch_sub(sub, mode, limit)
                
                for post in posts:
                    try:
                        # Extract post data safely
                        url = f"https://www.reddit.com{post.permalink}" if hasattr(post, 'permalink') else None
                        title = getattr(post, "title", None)
                        author = getattr(post, "author", None)
                        author_name = getattr(author, "name", None) if author else None
                        content = getattr(post, "selftext", None)
                        created_utc = int(post.created_utc) if hasattr(post, "created_utc") and post.created_utc else None
                        upvotes = int(post.score) if hasattr(post, "score") and post.score is not None else None
                        comments_count = int(post.num_comments) if hasattr(post, "num_comments") and post.num_comments is not None else None

                        # Append normalized data
                        post_data = normalized(
                            source="reddit",
                            url=url,
                            author=author_name,
                            title=title,
                            content=content,
                            upvotes=upvotes,
                            comments_count=comments_count,
                            created_utc=created_utc,
                            extras={
                                "subreddit": sub,
                                "id": getattr(post, "id", None),
                                "over_18": bool(getattr(post, "over_18", False)),
                                "link_flair": getattr(post, "link_flair_text", None),
                            },
                        )
                        out.append(post_data)
                        
                    except Exception as post_error:
                        print(f"Error processing post: {post_error}")
                        continue
                        
            except Exception as sub_error:
                print(f"Error processing r/{sub}: {sub_error}")
                continue
        
        print(f"Successfully scraped {len(out)} posts total")
        return out

# Test function for standalone testing
def test_reddit_scraper():
    """Test function to run the scraper independently"""
    load_dotenv()
    
    # Test configuration
    test_cfg = {
        "subreddits": ["test", "python"],
        "mode": "hot",
        "limit_per_subreddit": 5
    }
    
    try:
        scraper = RedditScraper(test_cfg)
        results = scraper.run()
        print(f"Test completed successfully! Got {len(results)} posts")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    test_reddit_scraper()