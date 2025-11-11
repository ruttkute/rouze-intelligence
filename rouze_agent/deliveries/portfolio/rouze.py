#!/usr/bin/env python3
"""
ROUZE - Unified Command Interface
Single entry point for all Rouze operations
"""

import sys
import os
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        show_help()
        return
        
    command = sys.argv[1].lower()
    
    if command == "morning":
        morning_briefing()
    elif command == "analyze":
        run_analysis(sys.argv[2:])
    elif command == "deliver":
        create_delivery(sys.argv[2:])
    elif command == "pitch":
        generate_pitch(sys.argv[2:])
    elif command == "status":
        show_status()
    elif command == "project":
        start_project()
    else:
        print(f"Unknown command: {command}")
        show_help()

def show_help():
    print("""
    🧬 ROUZE - Unified Command Interface
    
    Commands:
      rouze morning     - Daily briefing across all systems
      rouze analyze     - Run signal analysis
      rouze deliver     - Create client deliverable
      rouze pitch       - Generate proposal
      rouze status      - System health dashboard
      rouze project     - Start new project workflow
    """)

def morning_briefing():
    """Unified morning briefing"""
    from rouze_master import RouzeMaster
    rouze = RouzeMaster()
    rouze.daily_briefing()

if __name__ == "__main__":
    main()