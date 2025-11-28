#!/bin/bash

echo "📊 ROUZE MARKET DEMAND REPORT" > ROUZE_MARKET_DEMAND.txt
echo "Generated: $(date)" >> ROUZE_MARKET_DEMAND.txt
echo "================================" >> ROUZE_MARKET_DEMAND.txt

echo -e "\n🏥 HEALTHCARE VERTICAL\n" >> ROUZE_MARKET_DEMAND.txt
echo "Top discussions showing demand:" >> ROUZE_MARKET_DEMAND.txt
jq -r '.[] | "\(.score) upvotes | \(.title)"' signals/reddit_healthcare_adverse_events.json 2>/dev/null | sort -rn | head -10 >> ROUZE_MARKET_DEMAND.txt

echo -e "\n\n💻 SAAS VERTICAL\n" >> ROUZE_MARKET_DEMAND.txt
echo "Top discussions showing demand:" >> ROUZE_MARKET_DEMAND.txt
jq -r '.[] | "\(.score) upvotes | \(.title)"' signals/reddit_saas_market_analysis.json 2>/dev/null | sort -rn | head -10 >> ROUZE_MARKET_DEMAND.txt

echo -e "\n\n🛒 ECOMMERCE VERTICAL\n" >> ROUZE_MARKET_DEMAND.txt
echo "Top discussions showing demand:" >> ROUZE_MARKET_DEMAND.txt
jq -r '.[] | "\(.score) upvotes | \(.title)"' signals/reddit_ecommerce_validation.json 2>/dev/null | sort -rn | head -10 >> ROUZE_MARKET_DEMAND.txt

echo -e "\n✅ Report saved to ROUZE_MARKET_DEMAND.txt"
cat ROUZE_MARKET_DEMAND.txt
