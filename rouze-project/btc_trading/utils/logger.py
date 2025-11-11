# File: btc_trading/utils/logger.py
"""
Logging configuration for the trading system
"""

import logging
import os
from datetime import datetime

def setup_logging(log_level='INFO'):
    """Setup logging configuration"""
    
    # Create logs directory
    log_dir = 'btc_trading/logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    log_file = os.path.join(log_dir, f"trading_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Reduce noise from external libraries
    logging.getLogger('ccxt').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

# File: run_trading_system.py (in project root)
"""
Quick start script for BTC Trading System
Run this file to start the system
"""

import sys
import os

# Add btc_trading to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from btc_trading.main import main
    
    if __name__ == "__main__":
        print("Starting BTC Trading System...")
        main()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you've installed all dependencies:")
    print("pip install ccxt pandas numpy matplotlib plotly requests python-dotenv")
except Exception as e:
    print(f"Error starting system: {e}")

# File: requirements.txt (in project root)
ccxt>=4.0.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
plotly>=5.15.0
requests>=2.31.0
python-dotenv>=1.0.0
websockets>=11.0.0

# File: .env (in project root) - KEEP THIS FILE PRIVATE
# Discord webhook for notifications (optional)
DISCORD_WEBHOOK_URL=

# Email settings (optional)
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_RECIPIENT=

# Exchange API keys (only needed for live trading - NOT recommended initially)
# BINANCE_API_KEY=
# BINANCE_SECRET=