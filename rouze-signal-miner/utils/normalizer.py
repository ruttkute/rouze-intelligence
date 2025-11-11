from datetime import datetime, timezone
from typing import Dict, Any, Optional

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def normalized(
    *,
    source: str,
    url: Optional[str],
    author: Optional[str],
    title: Optional[str],
    content: Optional[str],
    upvotes: Optional[int],
    comments_count: Optional[int],
    created_utc: Optional[int],
    extra: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "source": source,
        "url": url,
        "author": author,
        "title": title,
        "content": content,
        "upvotes": upvotes,
        "comments_count": comments_count,
        "created_utc": created_utc,
        "scraped_at": utc_now_iso(),
        "extra": extra or {}
    }
