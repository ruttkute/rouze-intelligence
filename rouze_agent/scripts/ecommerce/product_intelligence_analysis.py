"""
E-commerce Product Intelligence Analysis
Viral prediction, sentiment analysis, pricing optimization
"""

import pandas as pd
import numpy as np
from scipy import stats

class ProductIntelligenceAnalytics:
    
    def __init__(self, product_name):
        self.product = product_name
        print(f"ECOMMERCE ANALYTICS ENGINE")
        print(f"Product: {product_name}")
    
    def viral_potential_scoring(self, tiktok_data):
        """
        Predict viral product potential
        Based on engagement velocity and sentiment
        """
        
        print(f"\n📈 VIRAL POTENTIAL ANALYSIS")
        print(f"{'='*70}")
        
        # Calculate engagement rate
        tiktok_data['engagement_rate'] = (
            tiktok_data['likes'] + tiktok_data['comments'] + tiktok_data['shares']
        ) / tiktok_data['video_views']
        
        avg_engagement = tiktok_data['engagement_rate'].mean()
        avg_views = tiktok_data['video_views'].mean()
        
        # Viral score (0-100)
        viral_score = min(100, (avg_engagement * 1000) + (avg_views / 50000))
        
        viral_level = "HIGH" if viral_score >= 60 else ("MEDIUM" if viral_score >= 30 else "LOW")
        
        results = {
            'viral_score': round(viral_score, 1),
            'viral_level': viral_level,
            'avg_engagement_rate': f"{avg_engagement*100:.2f}%",
            'avg_video_views': f"{int(avg_views):,}",
            'total_videos_analyzed': len(tiktok_data)
        }
        
        results_df = pd.DataFrame([results])
        results_df.to_csv(f'../../data/ecommerce/analyzed/{self.product.lower().replace(" ", "_")}_viral_potential.csv', index=False)
        
        print(results_df.to_string(index=False))
        
        return results_df
    
    def sentiment_distribution_analysis(self, amazon_reviews):
        """
        Detailed sentiment breakdown with statistical confidence
        """
        
        print(f"\n⭐ SENTIMENT DISTRIBUTION ANALYSIS")
        print(f"{'='*70}")
        
        rating_dist = amazon_reviews['rating'].value_counts().sort_index(ascending=False)
        
        total_reviews = len(amazon_reviews)
        avg_rating = amazon_reviews['rating'].mean()
        
        # Statistical confidence interval
        std_error = stats.sem(amazon_reviews['rating'])
        confidence_interval = stats.t.interval(0.95, len(amazon_reviews)-1, 
                                               loc=avg_rating, scale=std_error)
        
        results = []
        for rating in [5, 4, 3, 2, 1]:
            count = rating_dist.get(rating, 0)
            percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
            
            results.append({
                'rating_stars': f"{rating} stars",
                'review_count': count,
                'percentage': f"{percentage:.1f}%"
            })
        
        results_df = pd.DataFrame(results)
        
        print(results_df.to_string(index=False))
        print(f"\nAverage Rating: {avg_rating:.2f}/5.0")
        print(f"95% Confidence Interval: [{confidence_interval[0]:.2f}, {confidence_interval[1]:.2f}]")
        
        # Save
        results_df.to_csv(f'../../data/ecommerce/analyzed/{self.product.lower().replace(" ", "_")}_sentiment_distribution.csv', index=False)
        
        return results_df


# Execute
if __name__ == "__main__":
    product = 'wireless_earbuds'
    
    analyzer = ProductIntelligenceAnalytics('Wireless Earbuds')
    
    # Load data
    tiktok_data = pd.read_csv(f'../../data/ecommerce/raw/{product}_tiktok_trends.csv')
    amazon_data = pd.read_csv(f'../../data/ecommerce/raw/{product}_amazon_reviews.csv')
    
    # Viral potential
    viral_analysis = analyzer.viral_potential_scoring(tiktok_data)
    
    # Sentiment distribution
    sentiment_analysis = analyzer.sentiment_distribution_analysis(amazon_data)
    
    print(f"\n✓ ECOMMERCE ANALYTICS COMPLETE")