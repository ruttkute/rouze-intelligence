#!/usr/bin/env python3
"""
ROUZE Healthcare Intelligence Analyzer
Generates executive briefs for adverse event detection
"""

import anthropic
import os
from dotenv import load_dotenv
import json
from datetime import datetime

class RouzeHealthcareEngine:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            print("\n❌ No API key found!")
            print("Set with: export ANTHROPIC_API_KEY='sk-ant-api03-YOUR-KEY'")
            raise ValueError("ANTHROPIC_API_KEY required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
        
        print("✓ Claude API connected")
    
    def generate_healthcare_brief(self, drug_name: str, patient_data: dict):
        """Generate executive healthcare intelligence brief"""
        
        prompt = f"""Analyze this healthcare data and create an intelligence brief:

**Drug:** {drug_name}
**Data:** {json.dumps(patient_data, indent=2)}

Create a brief following the ROUZE Healthcare methodology:

1. **Executive Summary** (3 bullets)
   - Key finding with statistical significance
   - Competitive intelligence insight
   - Financial impact estimate

2. **Adverse Event Analysis**
   - Frequency comparison (drug vs baseline)
   - Statistical significance (p-value, effect size)
   - Clinical severity assessment

3. **180-Day Competitive Advantage**
   - MAUDE lag analysis
   - Competitor awareness timeline
   - Action window remaining

4. **ROI Proof Points**
   - Proactive cost: $X
   - Reactive cost: $Y
   - Savings: $Z

5. **Recommended Actions** (3 specific next steps)

Use positioning principles:
- Enemy: FDA MAUDE 6-9 month lag
- Urgency: 180-day competitive window
- ROI: $500K-$2M cost avoidance
- Fear: Regulatory surprises
- Opportunity: Early detection advantage
"""
        
        print(f"\n📊 Generating healthcare brief for {drug_name}...")
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    def analyze_sample_data(self):
        """Test with sample Ozempic adverse event data"""
        
        sample_data = {
            "drug_name": "Ozempic (semaglutide)",
            "analysis_period": "2024-Q1 to 2024-Q3",
            "patient_reports": 1247,
            "adverse_events": {
                "nausea": {
                    "frequency": 0.143,  # 14.3%
                    "baseline": 0.045,   # 4.5%
                    "p_value": 0.0001,
                    "effect_size": 0.52,  # Cohen's h
                    "severity": "MODERATE"
                },
                "pancreatitis": {
                    "frequency": 0.023,  # 2.3%
                    "baseline": 0.005,   # 0.5%
                    "p_value": 0.0008,
                    "effect_size": 0.38,
                    "severity": "HIGH"
                }
            },
            "maude_status": "NOT_REPORTED",
            "estimated_maude_date": "2025-04-15"
        }
        
        brief = self.generate_healthcare_brief("Ozempic", sample_data)
        
        # Save to file
        output_path = f"healthcare_brief_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(output_path, 'w') as f:
            f.write(brief)
        
        print(f"\n✅ Brief saved: {output_path}")
        print(f"\n📄 Preview (first 500 chars):")
        print("=" * 60)
        print(brief[:500] + "...")
        print("=" * 60)
        
        return brief

if __name__ == "__main__":
    print("\n🏥 ROUZE Healthcare Intelligence System")
    print("=" * 60)
    
    try:
        engine = RouzeHealthcareEngine()
        engine.analyze_sample_data()
        
        print("\n✅ Analysis complete!")
        print("\n💼 Ready for client acquisition")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
