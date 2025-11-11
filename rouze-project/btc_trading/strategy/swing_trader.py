"""
Simple BTC Swing Trading Strategy (2-7 day holds)
Based on structure breaks and trend following
"""

import pandas as pd
import numpy as np
from datetime import datetime
import ccxt

class BTCSwingTrader:
    def __init__(self):
        self.exchange = ccxt.binance()
        self.symbol = 'BTC/USDT'
        
        # Strategy parameters
        self.trend_ema = 20  # Daily trend filter
        self.structure_lookback = 10  # Bars for structure identification
        self.volume_multiplier = 1.3  # Volume threshold
        self.min_rr = 2.0  # Minimum risk/reward
        
    def get_market_data(self):
        """Fetch daily and 4H data"""
        daily = self.exchange.fetch_ohlcv(self.symbol, '1d', 60)
        four_h = self.exchange.fetch_ohlcv(self.symbol, '4h', 120)
        
        df_daily = pd.DataFrame(daily, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df_4h = pd.DataFrame(four_h, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        
        # Add indicators
        df_daily['ema20'] = df_daily['c'].ewm(span=20).mean()
        df_daily['trend'] = df_daily['c'] > df_daily['ema20']
        
        df_4h['vol_avg'] = df_4h['v'].rolling(20).mean()
        df_4h['vol_spike'] = df_4h['v'] > df_4h['vol_avg'] * self.volume_multiplier
        
        return df_daily, df_4h
    
    def identify_structure_break(self, df):
        """Identify recent structure breaks on 4H"""
        
        # Find recent swing highs and lows
        df['swing_high'] = df['h'] == df['h'].rolling(5, center=True).max()
        df['swing_low'] = df['l'] == df['l'].rolling(5, center=True).min()
        
        recent_highs = df[df['swing_high']]['h'].tail(3)
        recent_lows = df[df['swing_low']]['l'].tail(3)
        
        current_price = df['c'].iloc[-1]
        
        # Check for bullish structure break
        if len(recent_highs) > 0:
            recent_high = recent_highs.iloc[-1]
            if current_price > recent_high:
                return 'bullish_break', recent_high
        
        # Check for bearish structure break  
        if len(recent_lows) > 0:
            recent_low = recent_lows.iloc[-1]
            if current_price < recent_low:
                return 'bearish_break', recent_low
                
        return None, None
    
    def calculate_trade_levels(self, break_type, break_level, current_price):
        """Calculate entry, stop, and target levels"""
        
        if break_type == 'bullish_break':
            entry = current_price
            stop = break_level * 0.98  # 2% below break level
            risk = entry - stop
            target_1 = entry + (risk * 2)  # 1:2 R/R
            target_2 = entry + (risk * 3)  # 1:3 R/R
            
            return {
                'direction': 'LONG',
                'entry': entry,
                'stop': stop,
                'target_1': target_1,
                'target_2': target_2,
                'risk_reward': 2.0
            }
            
        elif break_type == 'bearish_break':
            entry = current_price  
            stop = break_level * 1.02  # 2% above break level
            risk = stop - entry
            target_1 = entry - (risk * 2)  # 1:2 R/R
            target_2 = entry - (risk * 3)  # 1:3 R/R
            
            return {
                'direction': 'SHORT',
                'entry': entry,
                'stop': stop,
                'target_1': target_1,
                'target_2': target_2,
                'risk_reward': 2.0
            }
        
        return None
    
    def scan_for_setups(self):
        """Main scanning function"""
        
        try:
            # Get data
            daily, four_h = self.get_market_data()
            
            # Check daily trend
            daily_trend = daily['trend'].iloc[-1]
            current_price = four_h['c'].iloc[-1]
            
            # Check for structure break
            break_type, break_level = self.identify_structure_break(four_h)
            
            # Volume confirmation
            volume_ok = four_h['vol_spike'].iloc[-1]
            
            # Generate signal if all conditions met
            if break_type and volume_ok:
                
                # Trend filter
                if break_type == 'bullish_break' and not daily_trend:
                    return None  # No bullish trades in daily downtrend
                    
                if break_type == 'bearish_break' and daily_trend:
                    return None  # No bearish trades in daily uptrend
                
                # Calculate trade levels
                trade_setup = self.calculate_trade_levels(break_type, break_level, current_price)
                
                if trade_setup:
                    trade_setup.update({
                        'timestamp': datetime.now(),
                        'break_type': break_type,
                        'break_level': break_level,
                        'daily_trend': 'UP' if daily_trend else 'DOWN',
                        'volume_confirmed': volume_ok
                    })
                    
                    return trade_setup
            
            return None
            
        except Exception as e:
            print(f"Scan error: {e}")
            return None
    
    def format_signal(self, setup):
        """Format signal for easy reading"""
        
        if not setup:
            return "No setups found"
        
        signal = f"""
📊 BTC SWING SETUP DETECTED
Direction: {setup['direction']}
Entry: ${setup['entry']:,.2f}
Stop Loss: ${setup['stop']:,.2f}  
Target 1: ${setup['target_1']:,.2f}
Target 2: ${setup['target_2']:,.2f}
Risk/Reward: 1:{setup['risk_reward']:.1f}
Daily Trend: {setup['daily_trend']}
Volume Confirmed: {'✅' if setup['volume_confirmed'] else '❌'}
Break Level: ${setup['break_level']:,.2f}
"""
        return signal


# Quick test/demo function
def run_swing_scanner():
    """Run the swing trading scanner"""
    
    trader = BTCSwingTrader()
    
    print("🔍 Scanning for BTC swing setups...")
    
    setup = trader.scan_for_setups()
    
    if setup:
        print(trader.format_signal(setup))
        
        # Demo trade logging
        print(f"\n📝 DEMO TRADE LOG:")
        print(f"Time: {setup['timestamp']}")
        print(f"Setup: {setup['break_type']} at ${setup['break_level']:,.2f}")
        print(f"Risk: ${abs(setup['entry'] - setup['stop']):,.2f}")
        print(f"Potential Reward: ${abs(setup['target_2'] - setup['entry']):,.2f}")
        
    else:
        print("❌ No swing setups found at this time")
        
        # Show current market status
        try:
            daily, four_h = trader.get_market_data()
            price = four_h['c'].iloc[-1]
            trend = "UP" if daily['trend'].iloc[-1] else "DOWN"
            print(f"\n📊 Current Status:")
            print(f"BTC Price: ${price:,.2f}")
            print(f"Daily Trend: {trend}")
        except:
            pass

if __name__ == "__main__":
    run_swing_scanner()