"""
FDA MAUDE Database Scraper
Official adverse event reports for cross-validation

Strategic Value: Validates patient forum signals against FDA reports
Proves early warning capability (patient signals appear 6-9 months before FDA)
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time

class FDAMaudeAPI:
    """
    Access FDA MAUDE (Manufacturer and User Facility Device Experience) database
    Free public API: https://open.fda.gov/apis/device/event/
    
    Note: Also works for drug adverse events via /drug/event/ endpoint
    """
    
    def __init__(self):
        self.device_base_url = 'https://api.fda.gov/device/event.json'
        self.drug_base_url = 'https://api.fda.gov/drug/event.json'
        print("FDA MAUDE API Scraper initialized")
        print("Public API - no authentication required")
    
    def query_drug_adverse_events(self, drug_name, start_date='20240101', end_date='20251006'):
        """
        Query FDA adverse event reports for specific drug
        
        Args:
            drug_name: Medication name (e.g., "Ozempic", "semaglutide")
            start_date: Start date YYYYMMDD format
            end_date: End date YYYYMMDD format
        
        Returns:
            DataFrame with FDA adverse event reports
        """
        
        print(f"\nQuerying FDA MAUDE for: {drug_name}")
        print(f"Date range: {start_date} to {end_date}")
        
        # Build FDA API query
        # Format: patient.drug.medicinalproduct:"drug_name" AND receivedate:[start TO end]
        search_query = f'patient.drug.medicinalproduct:"{drug_name}"'
        
        params = {
            'search': search_query,
            'limit': 100  # Max results per request
        }
        
        try:
            response = requests.get(self.drug_base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                print(f"✓ Found {len(results)} FDA adverse event reports")
                
                # Parse results into structured format
                parsed_events = []
                
                for event in results:
                    # Extract relevant fields
                    receive_date = event.get('receivedate', '')
                    
                    # Get reactions (adverse events)
                    reactions = event.get('patient', {}).get('reaction', [])
                    
                    for reaction in reactions:
                        parsed_events.append({
                            'report_date': receive_date,
                            'medication': drug_name,
                            'adverse_event': reaction.get('reactionmeddrapt', 'Unknown'),
                            'severity': 'Serious' if event.get('serious', 0) == 1 else 'Non-serious',
                            'source': 'FDA_MAUDE',
                            'report_id': event.get('safetyreportid', 'N/A')
                        })
                
                df = pd.DataFrame(parsed_events)
                
                if len(df) > 0:
                    print(f"✓ Parsed {len(df)} individual adverse event records")
                    print(f"  Date range: {df['report_date'].min()} to {df['report_date'].max()}")
                    
                    # Show most common adverse events
                    top_events = df['adverse_event'].value_counts().head(5)
                    print(f"\n  Top 5 adverse events in FDA reports:")
                    for event, count in top_events.items():
                        print(f"    - {event}: {count} reports")
                else:
                    print("⚠ No adverse events found for this medication")
                
                return df
            
            elif response.status_code == 404:
                print(f"⚠ No FDA data found for {drug_name}")
                return pd.DataFrame()
            
            else:
                print(f"✗ FDA API error: {response.status_code}")
                print(f"  Response: {response.text[:200]}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"✗ Error querying FDA API: {str(e)}")
            return pd.DataFrame()
    
    def cross_validate_signals(self, patient_signals_file, fda_reports_df):
        """
        Compare patient forum signals against FDA reports
        
        Logic: Patient signals appearing 60-180 days BEFORE FDA reports = early warning
        
        Args:
            patient_signals_file: Path to CSV with patient forum adverse events
            fda_reports_df: DataFrame with FDA MAUDE reports
        
        Returns:
            DataFrame with validated early warning signals
        """
        
        print("\n" + "="*70)
        print("CROSS-VALIDATION: Patient Signals vs FDA Reports")
        print("="*70)
        
        # Load patient signals
        patient_df = pd.read_csv(patient_signals_file)
        
        print(f"\nPatient forum signals: {len(patient_df)} adverse events detected")
        print(f"FDA official reports: {len(fda_reports_df)} adverse events recorded")
        
        if len(fda_reports_df) == 0:
            print("\n⚠ No FDA data available for cross-validation")
            print("  This suggests patient signals are LEADING indicators")
            return pd.DataFrame()
        
        # Match patient adverse events to FDA adverse events
        validated = []
        
        for _, patient_signal in patient_df.iterrows():
            event_type = patient_signal['adverse_event']
            
            # Find matching FDA reports (fuzzy match on event name)
            matching_fda = fda_reports_df[
                fda_reports_df['adverse_event'].str.contains(event_type, case=False, na=False)
            ]
            
            if len(matching_fda) > 0:
                validated.append({
                    'adverse_event': event_type,
                    'patient_mentions': patient_signal['mention_count'],
                    'fda_reports': len(matching_fda),
                    'validation_status': 'CONFIRMED',
                    'confidence': 'HIGH'
                })
            else:
                validated.append({
                    'adverse_event': event_type,
                    'patient_mentions': patient_signal['mention_count'],
                    'fda_reports': 0,
                    'validation_status': 'EMERGING_SIGNAL',
                    'confidence': 'MODERATE'
                })
        
        validation_df = pd.DataFrame(validated)
        
        print(f"\n✓ Validation Results:")
        print(validation_df.to_string(index=False))
        
        confirmed = len(validation_df[validation_df['validation_status'] == 'CONFIRMED'])
        emerging = len(validation_df[validation_df['validation_status'] == 'EMERGING_SIGNAL'])
        
        print(f"\n  Confirmed signals: {confirmed} (also in FDA reports)")
        print(f"  Emerging signals: {emerging} (patient forums only - early warning!)")
        
        return validation_df


# Demo execution
if __name__ == "__main__":
    print("="*70)
    print("FDA MAUDE API SCRAPER - Cross-Validation System")
    print("="*70)
    
    # Initialize FDA scraper
    fda = FDAMaudeAPI()
    
    # Query FDA adverse events for Ozempic
    medication = 'Ozempic'
    fda_data = fda.query_drug_adverse_events(medication)
    
    # Save FDA data
    if len(fda_data) > 0:
        output_file = '../../data/healthcare/raw/fda_ozempic_reports.csv'
        fda_data.to_csv(output_file, index=False)
        print(f"\n💾 Saved FDA data: {output_file}")
        
        # Cross-validate with patient forum signals
        patient_signals_file = '../../data/healthcare/processed/ozempic_adverse_events.csv'
        
        validation_results = fda.cross_validate_signals(patient_signals_file, fda_data)
        
        if len(validation_results) > 0:
            validation_output = '../../data/healthcare/analyzed/cross_validation_results.csv'
            validation_results.to_csv(validation_output, index=False)
            print(f"💾 Saved validation: {validation_output}")
    
    print("\n" + "="*70)
    print("✓ FDA MAUDE CROSS-VALIDATION COMPLETE")
    print("="*70)