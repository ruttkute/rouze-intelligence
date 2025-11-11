"""
Liquidity Sweep Analysis - Based on Your Research Files
File: btc_trading/analysis/liquidity_sweeps.py

Implements your research findings:
- 65-70% success rate when properly identified
- Volume spikes and rapid reversal characteristics
- Daily timeframe order blocks (75-85% respect rates)
- Equal highs/lows liquidity zone detection
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

class LiquiditySweepAnalyzer:
    """
    Implements institutional liquidity sweep detection
    Based on research showing 65-70% success rates
    """
    
    def __init__(self, config=None):
        self.logger = logging.getLogger(__name__)
        
        # Research-based parameters
        self.equal_level_threshold = 0.003  # 0.3% for equal levels
        self.min_touches = 2  # Minimum touches for liquidity zone
        self.volume_multiplier = 1.4  # Research: 140% average volume
        self.lookback_period = 30  # Bars to look back
        self.rejection_threshold = 0.008  # 0.8% minimum rejection
        self.max_candles_for_rejection = 2  # Within 1-2 candles per research
        
        # Order block settings (Research: 75-85% respect rate on daily)
        self.ob_significant_move_threshold = 0.02  # 2% move to identify OB
        self.ob_max_age = 50  # Maximum age of order block in bars
        
        self.logger.info("LiquiditySweepAnalyzer initialized with research parameters")
    
    def analyze(self, df: pd.DataFrame) -> Dict:
        """
        Main analysis function
        
        Args:
            df: OHLCV DataFrame with volume indicators
            
        Returns:
            Dict with analysis results and signals
        """
        
        if df is None or df.empty:
            return {"error": "No data provided"}
        
        # Ensure we have required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume', 'volume_spike']
        if not all(col in df.columns for col in required_cols):
            return {"error": f"Missing required columns: {required_cols}"}
        
        try:
            # Core analysis components
            liquidity_zones = self._detect_liquidity_zones(df)
            order_blocks = self._detect_order_blocks(df)
            sweeps = self._detect_liquidity_sweeps(df, liquidity_zones)
            market_structure = self._analyze_market_structure(df)
            
            # Generate final assessment
            signals = self._generate_signals(df, sweeps, order_blocks, market_structure)
            
            return {
                "timestamp": datetime.now(),
                "liquidity_zones": liquidity_zones,
                "order_blocks": order_blocks,
                "sweeps": sweeps,
                "market_structure": market_structure,
                "signals": signals,
                "current_price": df['close'].iloc[-1],
                "volume_status": "spike" if df['volume_spike'].iloc[-1] else "normal"
            }
            
        except Exception as e:
            self.logger.error(f"Analysis error: {e}")
            return {"error": str(e)}
    
    def _detect_liquidity_zones(self, df: pd.DataFrame) -> Dict:
        """
        Detect equal highs and lows (liquidity zones)
        Research: These are where stop losses cluster
        """
        
        equal_highs = []
        equal_lows = []
        
        # Find pivot points first
        df['pivot_high'] = df['high'] == df['high'].rolling(window=5, center=True).max()
        df['pivot_low'] = df['low'] == df['low'].rolling(window=5, center=True).min()
        
        # Get recent pivot highs for equal level analysis
        recent_highs = df[df['pivot_high']]['high'].tail(20)
        recent_lows = df[df['pivot_low']]['low'].tail(20)
        
        # Find equal highs
        for i, high1 in enumerate(recent_highs):
            touch_count = 0
            similar_levels = []
            
            for j, high2 in enumerate(recent_highs):
                if i != j and self._is_equal_level(high1, high2):
                    touch_count += 1
                    similar_levels.append(high2)
            
            if touch_count >= self.min_touches - 1:
                equal_highs.append({
                    'level': high1,
                    'touches': touch_count + 1,
                    'similar_levels': similar_levels,
                    'strength': 'strong' if touch_count >= 3 else 'medium'
                })
        
        # Find equal lows
        for i, low1 in enumerate(recent_lows):
            touch_count = 0
            similar_levels = []
            
            for j, low2 in enumerate(recent_lows):
                if i != j and self._is_equal_level(low1, low2):
                    touch_count += 1
                    similar_levels.append(low2)
            
            if touch_count >= self.min_touches - 1:
                equal_lows.append({
                    'level': low1,
                    'touches': touch_count + 1,
                    'similar_levels': similar_levels,
                    'strength': 'strong' if touch_count >= 3 else 'medium'
                })
        
        # Remove duplicates and sort
        equal_highs = self._deduplicate_levels(equal_highs)
        equal_lows = self._deduplicate_levels(equal_lows)
        
        return {
            'equal_highs': equal_highs[-5:],  # Keep only 5 most recent
            'equal_lows': equal_lows[-5:],   # Keep only 5 most recent
            'total_resistance_zones': len(equal_highs),
            'total_support_zones': len(equal_lows)
        }
    
    def _detect_order_blocks(self, df: pd.DataFrame) -> Dict:
        """
        Detect order blocks (Research: 75-85% respect rate on daily timeframe)
        Order block = last opposing candle before significant move
        """
        
        bullish_obs = []
        bearish_obs = []
        
        # Look for significant moves to identify order blocks
        for i in range(10, len(df) - 1):  # Start from index 10 to have lookback
            
            # Check for significant move up (bullish OB formation)
            current_close = df['close'].iloc[i]
            five_bars_ago = df['close'].iloc[i-5]
            move_up = (current_close - five_bars_ago) / five_bars_ago
            
            if move_up >= self.ob_significant_move_threshold:
                # Look for last bearish candle before this move
                for j in range(i-1, i-6, -1):  # Look back 5 bars
                    if df['close'].iloc[j] < df['open'].iloc[j]:  # Bearish candle
                        bullish_obs.append({
                            'timestamp': df.index[j],
                            'high': df['high'].iloc[j],
                            'low': df['low'].iloc[j],
                            'age': i - j,
                            'move_size': move_up,
                            'strength': 'strong' if move_up >= 0.04 else 'medium'
                        })
                        break
            
            # Check for significant move down (bearish OB formation)
            move_down = (five_bars_ago - current_close) / five_bars_ago
            
            if move_down >= self.ob_significant_move_threshold:
                # Look for last bullish candle before this move
                for j in range(i-1, i-6, -1):  # Look back 5 bars
                    if df['close'].iloc[j] > df['open'].iloc[j]:  # Bullish candle
                        bearish_obs.append({
                            'timestamp': df.index[j],
                            'high': df['high'].iloc[j],
                            'low': df['low'].iloc[j],
                            'age': i - j,
                            'move_size': move_down,
                            'strength': 'strong' if move_down >= 0.04 else 'medium'
                        })
                        break
        
        # Filter by age (remove old order blocks)
        current_bar = len(df) - 1
        bullish_obs = [ob for ob in bullish_obs if current_bar - df.index.get_loc(ob['timestamp']) <= self.ob_max_age]
        bearish_obs = [ob for ob in bearish_obs if current_bar - df.index.get_loc(ob['timestamp']) <= self.ob_max_age]
        
        return {
            'bullish_order_blocks': bullish_obs[-3:],  # Keep 3 most recent
            'bearish_order_blocks': bearish_obs[-3:],  # Keep 3 most recent
            'total_bullish_obs': len(bullish_obs),
            'total_bearish_obs': len(bearish_obs)
        }
    
    def _detect_liquidity_sweeps(self, df: pd.DataFrame, liquidity_zones: Dict) -> Dict:
        """
        Detect liquidity sweeps and reversals
        Research: 65-70% success rate when properly identified
        """
        
        sweeps = []
        
        # Check recent bars for sweep patterns
        for i in range(max(5, len(df) - 20), len(df)):  # Check last 20 bars
            
            # Bullish sweep detection
            for zone in liquidity_zones['equal_lows']:
                level = zone['level']
                
                # Check if price swept below level
                if df['low'].iloc[i] <= level and (i == 0 or df['low'].iloc[i-1] > level):
                    
                    # Check for immediate rejection (within 1-2 candles)
                    rejection_found = False
                    for j in range(i, min(i + self.max_candles_for_rejection + 1, len(df))):
                        if df['close'].iloc[j] > level:
                            # Calculate rejection strength
                            rejection_size = (df['close'].iloc[j] - df['low'].iloc[i]) / df['low'].iloc[i]
                            
                            if rejection_size >= self.rejection_threshold:
                                # Check volume confirmation
                                volume_confirmed = df['volume_spike'].iloc[i] or df['volume_spike'].iloc[j]
                                
                                if volume_confirmed:
                                    sweeps.append({
                                        'type': 'bullish_sweep',
                                        'timestamp': df.index[i],
                                        'swept_level': level,
                                        'sweep_low': df['low'].iloc[i],
                                        'rejection_close': df['close'].iloc[j],
                                        'rejection_strength': rejection_size,
                                        'volume_confirmed': volume_confirmed,
                                        'zone_strength': zone['strength'],
                                        'confidence': self._calculate_confidence(zone, rejection_size, volume_confirmed)
                                    })
                                    rejection_found = True
                                    break
                    
                    if rejection_found:
                        break
            
            # Bearish sweep detection
            for zone in liquidity_zones['equal_highs']:
                level = zone['level']
                
                # Check if price swept above level
                if df['high'].iloc[i] >= level and (i == 0 or df['high'].iloc[i-1] < level):
                    
                    # Check for immediate rejection
                    rejection_found = False
                    for j in range(i, min(i + self.max_candles_for_rejection + 1, len(df))):
                        if df['close'].iloc[j] < level:
                            # Calculate rejection strength
                            rejection_size = (df['high'].iloc[i] - df['close'].iloc[j]) / df['close'].iloc[j]
                            
                            if rejection_size >= self.rejection_threshold:
                                # Check volume confirmation
                                volume_confirmed = df['volume_spike'].iloc[i] or df['volume_spike'].iloc[j]
                                
                                if volume_confirmed:
                                    sweeps.append({
                                        'type': 'bearish_sweep',
                                        'timestamp': df.index[i],
                                        'swept_level': level,
                                        'sweep_high': df['high'].iloc[i],
                                        'rejection_close': df['close'].iloc[j],
                                        'rejection_strength': rejection_size,
                                        'volume_confirmed': volume_confirmed,
                                        'zone_strength': zone['strength'],
                                        'confidence': self._calculate_confidence(zone, rejection_size, volume_confirmed)
                                    })
                                    rejection_found = True
                                    break
                    
                    if rejection_found:
                        break
        
        return {
            'recent_sweeps': sweeps,
            'total_sweeps': len(sweeps),
            'bullish_sweeps': len([s for s in sweeps if s['type'] == 'bullish_sweep']),
            'bearish_sweeps': len([s for s in sweeps if s['type'] == 'bearish_sweep'])
        }
    
    def _analyze_market_structure(self, df: pd.DataFrame) -> Dict:
        """
        Analyze overall market structure for bias
        Research: Important for confluence
        """
        
        # Simple trend analysis using moving averages
        sma_20 = df['close'].rolling(20).mean()
        sma_50 = df['close'].rolling(50).mean()
        
        current_price = df['close'].iloc[-1]
        current_sma_20 = sma_20.iloc[-1]
        current_sma_50 = sma_50.iloc[-1]
        
        # Determine trend
        if current_sma_20 > current_sma_50 and current_price > current_sma_20:
            trend = 'bullish'
        elif current_sma_20 < current_sma_50 and current_price < current_sma_20:
            trend = 'bearish'
        else:
            trend = 'neutral'
        
        # Recent price action
        recent_high = df['high'].tail(20).max()
        recent_low = df['low'].tail(20).min()
        price_position = (current_price - recent_low) / (recent_high - recent_low)
        
        return {
            'trend': trend,
            'price_vs_sma20': current_price / current_sma_20 - 1,
            'price_vs_sma50': current_price / current_sma_50 - 1,
            'price_position_in_range': price_position,
            'recent_high': recent_high,
            'recent_low': recent_low,
            'volatility': df['close'].pct_change().std() * np.sqrt(24)  # For hourly data
        }
    
    def _generate_signals(self, df: pd.DataFrame, sweeps: Dict, order_blocks: Dict, market_structure: Dict) -> Dict:
        """
        Generate trading signals based on analysis
        Research: Only high-confidence setups for 65-70% win rate
        """
        
        signals = []
        
        # Check for recent sweeps with high confidence
        for sweep in sweeps['recent_sweeps']:
            if sweep['confidence'] >= 0.7:  # High confidence threshold
                
                # Calculate entry and risk levels
                if sweep['type'] == 'bullish_sweep':
                    # Entry above rejection candle high
                    entry_price = sweep['rejection_close'] * 1.001  # Small buffer
                    stop_loss = sweep['swept_level'] * 0.995  # Below swept level
                    
                    # Risk-reward calculation
                    risk = entry_price - stop_loss
                    reward_target = entry_price + (risk * 2.5)  # 2.5:1 R:R minimum
                    
                    # Check trend confluence
                    trend_confluence = market_structure['trend'] in ['bullish', 'neutral']
                    
                    if trend_confluence:
                        signals.append({
                            'type': 'BUY',
                            'timestamp': sweep['timestamp'],
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'target_1': entry_price + (risk * 1.5),  # Partial profit
                            'target_2': reward_target,
                            'risk_reward': 2.5,
                            'confidence': sweep['confidence'],
                            'reasoning': f"Bullish liquidity sweep at {sweep['swept_level']:.2f} with {sweep['rejection_strength']:.1%} rejection",
                            'volume_confirmed': sweep['volume_confirmed']
                        })
                
                elif sweep['type'] == 'bearish_sweep':
                    # Entry below rejection candle low
                    entry_price = sweep['rejection_close'] * 0.999  # Small buffer
                    stop_loss = sweep['swept_level'] * 1.005  # Above swept level
                    
                    # Risk-reward calculation
                    risk = stop_loss - entry_price
                    reward_target = entry_price - (risk * 2.5)  # 2.5:1 R:R minimum
                    
                    # Check trend confluence
                    trend_confluence = market_structure['trend'] in ['bearish', 'neutral']
                    
                    if trend_confluence:
                        signals.append({
                            'type': 'SELL',
                            'timestamp': sweep['timestamp'],
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'target_1': entry_price - (risk * 1.5),  # Partial profit
                            'target_2': reward_target,
                            'risk_reward': 2.5,
                            'confidence': sweep['confidence'],
                            'reasoning': f"Bearish liquidity sweep at {sweep['swept_level']:.2f} with {sweep['rejection_strength']:.1%} rejection",
                            'volume_confirmed': sweep['volume_confirmed']
                        })
        
        return {
            'active_signals': signals,
            'signal_count': len(signals),
            'buy_signals': len([s for s in signals if s['type'] == 'BUY']),
            'sell_signals': len([s for s in signals if s['type'] == 'SELL']),
            'average_confidence': np.mean([s['confidence'] for s in signals]) if signals else 0
        }
    
    def _is_equal_level(self, price1: float, price2: float) -> bool:
        """Check if two price levels are considered equal"""
        return abs(price1 - price2) / min(price1, price2) <= self.equal_level_threshold
    
    def _deduplicate_levels(self, levels: List[Dict]) -> List[Dict]:
        """Remove duplicate similar levels"""
        if not levels:
            return levels
        
        unique_levels = []
        for level in levels:
            is_duplicate = False
            for existing in unique_levels:
                if self._is_equal_level(level['level'], existing['level']):
                    # Keep the one with more touches
                    if level['touches'] > existing['touches']:
                        unique_levels.remove(existing)
                        unique_levels.append(level)
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_levels.append(level)
        
        return sorted(unique_levels, key=lambda x: x['level'])
    
    def _calculate_confidence(self, zone: Dict, rejection_strength: float, volume_confirmed: bool) -> float:
        """
        Calculate confidence score for a setup
        Research: Higher confidence = better success rate
        """
        
        base_confidence = 0.5
        
        # Zone strength factor
        if zone['strength'] == 'strong':
            base_confidence += 0.2
        elif zone['strength'] == 'medium':
            base_confidence += 0.1
        
        # Rejection strength factor
        if rejection_strength >= 0.015:  # 1.5%+ rejection
            base_confidence += 0.2
        elif rejection_strength >= 0.01:  # 1%+ rejection
            base_confidence += 0.1
        
        # Volume confirmation factor
        if volume_confirmed:
            base_confidence += 0.15
        
        # Zone touches factor
        if zone['touches'] >= 4:
            base_confidence += 0.1
        elif zone['touches'] >= 3:
            base_confidence += 0.05
        
        return min(base_confidence, 1.0)  # Cap at 100%


# Test function
if __name__ == "__main__":
    # Test with sample data
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Create sample data
    dates = pd.date_range(start='2025-01-01', periods=100, freq='1H')
    np.random.seed(42)
    
    # Generate realistic BTC-like price data
    price = 50000
    prices = [price]
    volumes = []
    
    for i in range(99):
        price *= (1 + np.random.normal(0, 0.02))  # 2% volatility
        prices.append(price)
        volumes.append(np.random.lognormal(10, 1))
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': prices,
        'high': [p * 1.01 for p in prices],
        'low': [p * 0.99 for p in prices],
        'close': prices,
        'volume': volumes
    })
    
    # Add volume spike indicator
    df['volume_sma_20'] = df['volume'].rolling(20).mean()
    df['volume_spike'] = df['volume'] > df['volume_sma_20'] * 1.4
    
    # Test analyzer
    analyzer = LiquiditySweepAnalyzer()
    results = analyzer.analyze(df)
    
    print("Analysis Results:")
    print(f"Liquidity zones found: {results['liquidity_zones']['total_resistance_zones']} resistance, {results['liquidity_zones']['total_support_zones']} support")
    print(f"Order blocks found: {results['order_blocks']['total_bullish_obs']} bullish, {results['order_blocks']['total_bearish_obs']} bearish")
    print(f"Sweeps detected: {results['sweeps']['total_sweeps']}")
    print(f"Active signals: {results['signals']['signal_count']}")
    
    if results['signals']['active_signals']:
        for signal in results['signals']['active_signals']:
            print(f"Signal: {signal['type']} at {signal['entry_price']:.2f}, confidence: {signal['confidence']:.1%}")