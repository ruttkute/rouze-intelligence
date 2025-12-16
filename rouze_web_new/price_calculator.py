BASE_PRICE = 5000
DATA_SOURCES_COST = {'standard': 0, 'comprehensive': 1500, 'custom': 3000}
FREQUENCY_COST = {'one_time': 0, 'weekly': 1000, 'daily': 2500, 'realtime': 4000}
TEAM_SIZE_COST = {'small': 0, 'medium': 500, 'large': 1000}
FEATURES_COST = {'custom_kpi': 800, 'api_access': 500, 'white_label': 1200, 'dedicated_analyst': 2000, 'custom_training': 500}
SUPPORT_COST = {'email': 0, 'monthly_calls': 200, 'weekly_calls': 500, 'embedded_analyst': 3000}
def calculate_monthly_price(data_sources, frequency, team_size, features, support):
    total = BASE_PRICE + DATA_SOURCES_COST.get(data_sources, 0) + FREQUENCY_COST.get(frequency, 0) + TEAM_SIZE_COST.get(team_size, 0) + SUPPORT_COST.get(support, 0)
    if features:
        for feature in features:
            total += FEATURES_COST.get(feature, 0)
    return total
def get_price_breakdown(data_sources, frequency, team_size, features, support):
    breakdown = {'base': BASE_PRICE, 'data_sources': DATA_SOURCES_COST.get(data_sources, 0), 'frequency': FREQUENCY_COST.get(frequency, 0), 'team_size': TEAM_SIZE_COST.get(team_size, 0), 'features': sum(FEATURES_COST.get(f, 0) for f in features) if features else 0, 'support': SUPPORT_COST.get(support, 0)}
    breakdown['total'] = sum(breakdown.values())
    return breakdown
