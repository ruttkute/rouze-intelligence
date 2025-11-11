"""
BTC Trading System - Main Execution Script
File: btc_trading/main.py

IMPORTANT: This is for PAPER TRADING and RESEARCH ONLY initially.
Never trade with real money without extensive testing.
"""

import sys
import os
import time
import logging
from datetime import datetime, timedelta
import json

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from btc_trading.data.fetcher import DataFetcher
from btc_trading.analysis.liquidity_sweeps import LiquiditySweepAnalyzer
from btc_trading.utils.logger import setup_logging
from btc_trading.config.settings import *

class BTCTradingSystem:
    """
    Main BTC Trading System
    
    CRITICAL WARNING: This system is for educational and research purposes.
    Trading involves substantial risk of loss. Only use paper trading initially.
    """
    
    def __init__(self, paper_trading_mode=True):
        """
        Initialize the trading system
        
        Args:
            paper_trading_mode: If True, no real money is involved (STRONGLY RECOMMENDED)
        """
        # Setup logging first
        setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # SAFETY: Force paper trading mode initially
        self.paper_trading_mode = True  # Override to always start with paper trading
        
        if not paper_trading_mode:
            self.logger.warning("Real trading mode requested but overridden for safety")
            print("🚨 SAFETY OVERRIDE: System will run in PAPER TRADING mode only")
            print("This protects you from financial losses during testing phase.")
        
        # Initialize components
        try:
            self.data_fetcher = DataFetcher()
            self.analyzer = LiquiditySweepAnalyzer()
            
            # Test exchange connections
            connections = self.data_fetcher.test_connections()
            active_exchanges = [ex for ex, status in connections.items() if status.get('status') == 'connected']
            
            if not active_exchanges:
                raise Exception("No exchange connections available")
            
            self.logger.info(f"System initialized with {len(active_exchanges)} active exchanges")
            
            # Trading state
            self.running = False
            self.analysis_history = []
            self.paper_trades = []
            self.last_signal_time = None
            
        except Exception as e:
            self.logger.error(f"Failed to initialize trading system: {e}")
            raise
    
    def run_single_analysis(self):
        """
        Run a single analysis cycle - useful for testing
        """
        try:
            self.logger.info("Running single analysis cycle...")
            
            # Fetch current data
            df = self.data_fetcher.get_live_data(SYMBOL, '1h', 100)
            if df is None or df.empty:
                self.logger.error("No data received")
                return None
            
            # Run analysis
            analysis = self.analyzer.analyze(df)
            
            # Log results
            current_price = analysis.get('current_price', 'Unknown')
            signals = analysis.get('signals', {})
            signal_count = signals.get('signal_count', 0)
            
            self.logger.info(f"Analysis complete - Price: ${current_price:,.2f}, Signals: {signal_count}")
            
            # Display results
            self._display_analysis_summary(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Analysis error: {e}")
            return None
    
    def run_monitoring_mode(self, update_interval_minutes=5):
        """
        Run continuous monitoring mode
        
        Args:
            update_interval_minutes: How often to check for new signals
        """
        
        print("🚀 Starting BTC Liquidity Sweep Monitor")
        print("📊 Paper Trading Mode Active - No Real Money at Risk")
        print(f"⏰ Update Interval: {update_interval_minutes} minutes")
        print("🛑 Press Ctrl+C to stop")
        print("-" * 60)
        
        self.running = True
        
        try:
            while self.running:
                # Run analysis
                analysis = self.run_single_analysis()
                
                if analysis and not analysis.get('error'):
                    # Check for new signals
                    self._process_signals(analysis)
                    
                    # Store analysis history
                    self.analysis_history.append({
                        'timestamp': datetime.now(),
                        'analysis': analysis
                    })
                    
                    # Keep only last 100 analyses
                    if len(self.analysis_history) > 100:
                        self.analysis_history = self.analysis_history[-100:]
                
                # Wait for next update
                self.logger.info(f"Sleeping for {update_interval_minutes} minutes...")
                time.sleep(update_interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping trading system...")
            self.running = False
        except Exception as e:
            self.logger.error(f"Monitoring error: {e}")
            self.running = False
    
    def _process_signals(self, analysis):
        """Process trading signals (paper trading only)"""
        
        signals = analysis.get('signals', {})
        active_signals = signals.get('active_signals', [])
        
        if not active_signals:
            return
        
        for signal in active_signals:
            # Avoid duplicate signals
            signal_time = signal.get('timestamp')
            if signal_time == self.last_signal_time:
                continue
            
            self.last_signal_time = signal_time
            
            # Paper trade execution
            self._execute_paper_trade(signal)
            
            # Send notifications (if configured)
            self._send_signal_notification(signal)
    
    def _execute_paper_trade(self, signal):
        """
        Execute paper trade (no real money)
        This simulates what would happen in real trading
        """
        
        paper_trade = {
            'id': len(self.paper_trades) + 1,
            'timestamp': datetime.now(),
            'type': signal['type'],
            'entry_price': signal['entry_price'],
            'stop_loss': signal['stop_loss'],
            'target_1': signal['target_1'],
            'target_2': signal['target_2'],
            'confidence': signal['confidence'],
            'reasoning': signal['reasoning'],
            'status': 'open',
            'risk_amount': abs(signal['entry_price'] - signal['stop_loss']),
            'potential_reward': abs(signal['target_2'] - signal['entry_price'])
        }
        
        self.paper_trades.append(paper_trade)
        
        print(f"\n📝 PAPER TRADE #{paper_trade['id']}")
        print(f"   Type: {signal['type']}")
        print(f"   Entry: ${signal['entry_price']:,.2f}")
        print(f"   Stop Loss: ${signal['stop_loss']:,.2f}")
        print(f"   Target 1: ${signal['target_1']:,.2f}")
        print(f"   Target 2: ${signal['target_2']:,.2f}")
        print(f"   Risk/Reward: 1:{signal['risk_reward']:.1f}")
        print(f"   Confidence: {signal['confidence']:.1%}")
        print(f"   Reason: {signal['reasoning']}")
        
        self.logger.info(f"Paper trade executed: {signal['type']} at ${signal['entry_price']:,.2f}")
    
    def _send_signal_notification(self, signal):
        """Send signal notification (implement based on your preferences)"""
        
        # Desktop notification
        try:
            import subprocess
            message = f"BTC {signal['type']} Signal at ${signal['entry_price']:,.2f}"
            
            # macOS notification
            subprocess.run([
                'osascript', '-e', 
                f'display notification "{message}" with title "BTC Trading Signal"'
            ], check=False)
            
        except Exception as e:
            self.logger.debug(f"Notification error: {e}")
    
    def _display_analysis_summary(self, analysis):
        """Display analysis summary"""
        
        if analysis.get('error'):
            print(f"❌ Analysis Error: {analysis['error']}")
            return
        
        # Current market status
        price = analysis.get('current_price', 0)
        volume_status = analysis.get('volume_status', 'normal')
        
        print(f"\n📊 BTC Analysis Summary - {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Current Price: ${price:,.2f}")
        print(f"   Volume Status: {volume_status.upper()}")
        
        # Liquidity zones
        zones = analysis.get('liquidity_zones', {})
        print(f"   Resistance Zones: {zones.get('total_resistance_zones', 0)}")
        print(f"   Support Zones: {zones.get('total_support_zones', 0)}")
        
        # Order blocks
        obs = analysis.get('order_blocks', {})
        print(f"   Bullish Order Blocks: {obs.get('total_bullish_obs', 0)}")
        print(f"   Bearish Order Blocks: {obs.get('total_bearish_obs', 0)}")
        
        # Signals
        signals = analysis.get('signals', {})
        signal_count = signals.get('signal_count', 0)
        
        if signal_count > 0:
            print(f"🚨 ACTIVE SIGNALS: {signal_count}")
            avg_confidence = signals.get('average_confidence', 0)
            print(f"   Average Confidence: {avg_confidence:.1%}")
        else:
            print("   No active signals")
        
        # Market structure
        structure = analysis.get('market_structure', {})
        trend = structure.get('trend', 'unknown')
        print(f"   Market Trend: {trend.upper()}")
    
    def get_performance_summary(self):
        """Get paper trading performance summary"""
        
        if not self.paper_trades:
            print("📊 No paper trades executed yet")
            return
        
        total_trades = len(self.paper_trades)
        open_trades = len([t for t in self.paper_trades if t['status'] == 'open'])
        
        print(f"\n📊 Paper Trading Performance Summary")
        print(f"   Total Trades: {total_trades}")
        print(f"   Open Trades: {open_trades}")
        print(f"   Closed Trades: {total_trades - open_trades}")
        
        # Show recent trades
        print(f"\n📝 Recent Paper Trades:")
        for trade in self.paper_trades[-5:]:
            print(f"   #{trade['id']}: {trade['type']} at ${trade['entry_price']:,.2f} - {trade['status']}")
    
    def run_backtest_mode(self, days_back=30):
        """
        Run historical backtest to validate strategy
        
        Args:
            days_back: Number of days of historical data to test
        """
        
        print(f"🔍 Running backtest on last {days_back} days...")
        
        try:
            # This would require implementing historical data fetching
            # and walking through the data day by day
            print("⚠️  Backtest mode not yet implemented")
            print("   Use single analysis mode to test current market conditions")
            
        except Exception as e:
            self.logger.error(f"Backtest error: {e}")


def main():
    """Main entry point"""
    
    print("🔷 BTC Liquidity Sweep Trading System")
    print("⚠️  IMPORTANT: Paper Trading Mode Only")
    print("   This system is for research and testing purposes")
    print("   Never trade with real money without extensive validation")
    print()
    
    try:
        # Initialize system
        system = BTCTradingSystem(paper_trading_mode=True)
        
        # Interactive menu
        while True:
            print("\n🎛️  Choose an option:")
            print("1. Run single analysis")
            print("2. Start monitoring mode")
            print("3. View performance summary")
            print("4. Test exchange connections")
            print("5. Exit")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                print("\n🔍 Running single analysis...")
                system.run_single_analysis()
                
            elif choice == '2':
                interval = input("Update interval in minutes (default 5): ").strip()
                interval = int(interval) if interval.isdigit() else 5
                system.run_monitoring_mode(interval)
                
            elif choice == '3':
                system.get_performance_summary()
                
            elif choice == '4':
                print("\n🔌 Testing exchange connections...")
                connections = system.data_fetcher.test_connections()
                for exchange, status in connections.items():
                    status_text = "✅ Connected" if status.get('status') == 'connected' else "❌ Failed"
                    print(f"   {exchange}: {status_text}")
                
            elif choice == '5':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
                
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ System error: {e}")
        logging.error(f"System error: {e}")


if __name__ == "__main__":
    main()