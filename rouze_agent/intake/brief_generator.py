# ~/Desktop/rouze/rouze_agent/intake/brief_generator.py

class ResearchBriefGenerator:
    """Convert client intake responses into executable research plan"""
    
    @staticmethod
    def generate_brief(industry, all_answers):
        """Generate structured research brief from intake answers"""
        
        brief = {
            'industry': industry,
            'client_objective': all_answers.get('objective', ''),
            'timeline': all_answers.get('timeline', 'Standard (7-14 days)'),
            'data_sources': [],
            'analysis_methods': [],
            'deliverable_format': 'Executive Brief + HTML Dashboard',
            'research_parameters': {}
        }
        
        # Industry-specific brief enhancement
        if industry == 'healthcare':
            brief['data_sources'] = [
                'drugs_com_reviews',
                'webmd_forums',
                'fda_maude_database',
                'twitter_patient_signals',
                'reddit_health_communities'
            ]
            brief['analysis_methods'] = [
                'adverse_event_detection',
                'chi_square_significance',
                'risk_scoring',
                'regulatory_timeline_prediction'
            ]
            if 'pharma' in str(all_answers.get('product_category', '')).lower():
                brief['research_parameters']['therapeutic_area'] = all_answers.get('therapeutic_area', '')
                brief['research_parameters']['signal_type'] = all_answers.get('signal_type', 'both')
        
        elif industry == 'saas':
            brief['data_sources'] = [
                'g2_reviews',
                'reddit_product_discussions',
                'github_issues',
                'stack_overflow_trends',
                'product_hunt_feedback'
            ]
            brief['analysis_methods'] = [
                'feature_gap_analysis',
                'sentiment_comparison',
                'competitor_positioning',
                'pricing_sensitivity'
            ]
            brief['research_parameters']['competitors'] = all_answers.get('competitors', [])
            brief['research_parameters']['target_segment'] = all_answers.get('target_market', 'All segments')
        
        elif industry == 'ecommerce':
            brief['data_sources'] = [
                'amazon_reviews',
                'tiktok_trends',
                'instagram_hashtags',
                'reddit_shopping_communities',
                'youtube_unboxing_videos'
            ]
            brief['analysis_methods'] = [
                'viral_prediction',
                'sentiment_tracking',
                'influencer_impact',
                'competitive_pricing'
            ]
        
        return brief