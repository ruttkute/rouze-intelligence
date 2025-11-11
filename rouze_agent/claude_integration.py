
#!/usr/bin/env python3

"""ROUZE Claude Intelligence Integration"""

import anthropic

import os

import json

from pathlib import Path

from datetime import datetime

class RouzeClaudeEngine:

    def __init__(self):

        self.api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not self.api_key:

            print("\n❌ No API key found!")

            print("Set with: export ANTHROPIC_API_KEY='sk-ant-api03-YOUR-KEY'")

            raise ValueError("ANTHROPIC_API_KEY required")

        

        self.client = anthropic.Anthropic(api_key=self.api_key)

        self.model = "claude-sonnet-4-5-20250929"

        print("✓ Claude API connected")

    

    def generate_brief(self, data: dict, vertical: str = "general"):

        prompt = f"""Analyze this {vertical} data and create an intelligence brief:

{json.dumps(data, indent=2)}

Include:

1. Executive Summary (3 bullets)

2. Key Insights (with statistics)

3. Business Impact

4. Recommended Actions

"""

        

        print(f"\n🤖 Generating {vertical} brief...")

        

        message = self.client.messages.create(

            model=self.model,

            max_tokens=8000,

            messages=[{"role": "user", "content": prompt}]

        )

        

        return message.content[0].text

    

    def save_brief(self, content: str, vertical: str):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_dir = Path(__file__).parent.parent / "deliveries"

        output_dir.mkdir(exist_ok=True)

        

        filename = f"Claude_Brief_{vertical}_{timestamp}.md"

        filepath = output_dir / filename

        filepath.write_text(content)

        

        return filepath

def main():

    print("=" * 60)

    print("🧬 ROUZE Claude Engine Test")

    print("=" * 60)

    

    test_data = {

        "vertical": "healthcare",

        "signals": 325,

        "adverse_events": 47,

        "baseline_rate": 0.05,

        "observed_rate": 0.145,

        "p_value": 0.0002

    }

    

    try:

        engine = RouzeClaudeEngine()

        brief = engine.generate_brief(test_data, "healthcare")

        filepath = engine.save_brief(brief, "healthcare")

        

        print(f"\n✓ Brief saved: {filepath}")

        print(f"📏 Length: {len(brief)} chars")

        print("\nPREVIEW:")

        print("=" * 60)

        print(brief[:400] + "...")

        

    except Exception as e:

        print(f"\n❌ Error: {e}")

if __name__ == "__main__":

    main()

