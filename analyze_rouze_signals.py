import json
import os
from collections import Counter

def analyze_reddit_signals(filepath, vertical_name):
    """Analyze Reddit signal JSON"""
    print(f"\n{'='*60}")
    print(f"📊 {vertical_name} VERTICAL ANALYSIS")
    print(f"{'='*60}")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Handle both list and nested data structures
        items = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and 'data' in data:
            if isinstance(data['data'], list):
                items = data['data']
            elif 'children' in data['data']:
                items = [child.get('data', {}) for child in data['data']['children']]
        
        if not items:
            print(f"⚠️  No items found in {filepath}")
            return
        
        print(f"✅ Total signals: {len(items)}")
        
        # Extract titles and scores
        titles = []
        total_score = 0
        total_comments = 0
        
        for item in items[:100]:  # First 100
            if isinstance(item, dict):
                title = item.get('title', '')
                score = item.get('score', 0)
                comments = item.get('comments', item.get('num_comments', 0))
                
                if title:
                    titles.append((title, score, comments))
                    total_score += score
                    total_comments += comments
        
        if titles:
            avg_engagement = (total_score + total_comments) // len(titles) if titles else 0
            print(f"\n📈 Engagement metrics:")
            print(f"   • Average upvotes: {total_score // len(titles)}")
            print(f"   • Average comments: {total_comments // len(titles)}")
            print(f"   • Total engagement: {total_score + total_comments}")
            
            print(f"\n🔥 Top 10 discussions (most upvoted):")
            sorted_titles = sorted(titles, key=lambda x: x[1], reverse=True)
            for i, (title, score, comments) in enumerate(sorted_titles[:10], 1):
                print(f"   {i}. [{score} upvotes] {title[:70]}...")
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Analyze all verticals
print("\n\n🎯 ROUZE MARKET DEMAND SIGNALS ANALYSIS\n")

analyze_reddit_signals('signals/reddit_healthcare_adverse_events.json', '🏥 HEALTHCARE - Adverse Events')
analyze_reddit_signals('signals/reddit_healthcare_market_research.json', '🏥 HEALTHCARE - Market Research')
analyze_reddit_signals('signals/reddit_saas_market_analysis.json', '💻 SAAS - Market Analysis')
analyze_reddit_signals('signals/reddit_saas_startups.json', '💻 SAAS - Startups')
analyze_reddit_signals('signals/reddit_ecommerce_validation.json', '🛒 ECOMMERCE - Validation')
analyze_reddit_signals('signals/reddit_ecommerce_dropshipping.json', '🛒 ECOMMERCE - Dropshipping')

print("\n\n" + "="*60)
print("✅ ANALYSIS COMPLETE")
print("="*60)
