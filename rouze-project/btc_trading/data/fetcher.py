"""
BTC Data Fetcher - Free real-time data from exchanges
File: btc_trading/data/fetcher.py
"""

import ccxt
import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime, timedelta
import os
import json

class DataFetcher:
    """
    Fetches BTC price data from multiple free sources
    No TradingView subscription required
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize multiple exchanges for redundancy
        self.exchanges = {
            'binance': ccxt.binance({
                'enableRateLimit': True,
                'sandbox': False,
            }),
            'coinbase': ccxt.coinbasepro({
                'enableRateLimit': True,
                'sandbox': False,
            }),
            'kraken': ccxt.kraken({
                'enableRateLimit': True,
            })
        }
        
        self.primary_exchange = 'binance'
        self.backup_exchanges = ['coinbase', 'kraken']
        
        # Data cache
        self.cache_dir = 'btc_trading/data/historical'
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.logger.info("DataFetcher initialized with multiple exchange sources")
    
    def test_connections(self):
        """Test all exchange connections"""
        results = {}
        
        for name, exchange in self.exchanges.items():
            try:
                markets = exchange.load_markets()
                results[name] = {"status": "connected", "markets": len(markets)}
                self.logger.info(f"{name}: Connected ({len(markets)} markets)")
            except Exception as e:
                results[name] = {"status": "error", "error": str(e)}
                self.logger.error(f"{name}: Connection failed - {e}")
        
        return results
    
    def get_live_data(self, symbol='BTC/USDT', timeframe='1h', limit=100):
        """
        Get live OHLCV data from exchange
        
        Args:
            symbol: Trading pair (default: BTC/USDT)
            timeframe: Candlestick timeframe (1m, 5m, 15m, 1h, 4h, 1d)
            limit: Number of candles to fetch
        
        Returns:
            pandas.DataFrame: OHLCV data with additional indicators
        """
        
        # Try primary exchange first
        for exchange_name in [self.primary_exchange] + self.backup_exchanges:
            try:
                exchange = self.exchanges[exchange_name]
                
                # Fetch OHLCV data
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                
                # Convert to DataFrame
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                
                # Add basic indicators immediately available
                df = self._add_basic_indicators(df)
                
                self.logger.info(f"Fetched {len(df)} {timeframe} candles from {exchange_name}")
                
                # Cache the data
                self._cache_data(df, symbol, timeframe)
                
                return df
                
            except Exception as e:
                self.logger.warning(f"Failed to fetch from {exchange_name}: {e}")
                continue
        
        # If all exchanges fail, try to load from cache
        self.logger.error("All exchanges failed, attempting to load from cache")
        return self._load_cached_data(symbol, timeframe)
    
    def get_current_price(self, symbol='BTC/USDT'):
        """Get current BTC price quickly"""
        
        for exchange_name in [self.primary_exchange] + self.backup_exchanges:
            try:
                exchange = self.exchanges[exchange_name]
                ticker = exchange.fetch_ticker(symbol)
                
                return {
                    'price': ticker['last'],
                    'bid': ticker['bid'],
                    'ask': ticker['ask'],
                    'volume_24h': ticker['quoteVolume'],
                    'timestamp': datetime.now(),
                    'exchange': exchange_name
                }
                
            except Exception as e:
                self.logger.warning(f"Failed to get price from {exchange_name}: {e}")
                continue
        
        raise Exception("Failed to get current price from all exchanges")
    
    def get_order_book(self, symbol='BTC/USDT', limit=50):
        """Get current order book for liquidity analysis"""
        
        try:
            exchange = self.exchanges[self.primary_exchange]
            orderbook = exchange.fetch_order_book(symbol, limit)
            
            return {
                'bids': orderbook['bids'][:10],  # Top 10 bids
                'asks': orderbook['asks'][:10],  # Top 10 asks
                'timestamp': datetime.now(),
                'exchange': self.primary_exchange
            }
            
        except Exception as e:
            self.logger.error(f"Failed to fetch orderbook: {e}")
            return None
    
    def get_multi_timeframe_data(self, symbol='BTC/USDT', timeframes=['1h', '4h', '1d']):
        """
        Get data from multiple timeframes for confluence analysis
        Based on your research: Daily for bias, 4H for setup, 1H for entry
        """
        
        data = {}
        
        for tf in timeframes:
            self.logger.info(f"Fetching {tf} data for {symbol}")
            
            try:
                # Adjust limit based on timeframe
                limit = 200 if tf == '1h' else 100 if tf == '4h' else 50
                df = self.get_live_data(symbol, tf, limit)
                
                if df is not None and not df.empty:
                    data[tf] = df
                    time.sleep(1)  # Rate limiting
                    
            except Exception as e:
                self.logger.error(f"Failed to fetch {tf} data: {e}")
        
        return data
    
    def _add_basic_indicators(self, df):
        """Add basic indicators that don't require external libraries"""
        
        # Moving averages for trend analysis
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # Volume analysis (critical for your research)
        df['volume_sma_20'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma_20']
        df['volume_spike'] = df['volume_ratio'] > 1.4  # Your research: 140% threshold
        
        # Price change analysis
        df['price_change'] = df['close'].pct_change()
        df['price_change_abs'] = df['price_change'].abs()
        
        # High/Low analysis for liquidity zones
        df['high_20'] = df['high'].rolling(window=20).max()
        df['low_20'] = df['low'].rolling(window=20).min()
        
        # Recent highs/lows for equal level detection
        df['is_pivot_high'] = (df['high'] == df['high'].rolling(window=5, center=True).max())
        df['is_pivot_low'] = (df['low'] == df['low'].rolling(window=5, center=True).min())
        
        return df
    
    def _cache_data(self, df, symbol, timeframe):
        """Cache data to local storage"""
        
        try:
            filename = f"{symbol.replace('/', '')}_{timeframe}_{datetime.now().strftime('%Y%m%d')}.csv"
            filepath = os.path.join(self.cache_dir, filename)
            
            df.to_csv(filepath)
            self.logger.debug(f"Data cached to {filepath}")
            
        except Exception as e:
            self.logger.warning(f"Failed to cache data: {e}")
    
    def _load_cached_data(self, symbol, timeframe):
        """Load data from cache if exchanges fail"""
        
        try:
            # Look for today's cache file
            filename = f"{symbol.replace('/', '')}_{timeframe}_{datetime.now().strftime('%Y%m%d')}.csv"
            filepath = os.path.join(self.cache_dir, filename)
            
            if os.path.exists(filepath):
                df = pd.read_csv(filepath, index_col=0, parse_dates=True)
                self.logger.info(f"Loaded cached data from {filepath}")
                return df
            
            # If no cache for today, look for yesterday
            yesterday = datetime.now() - timedelta(days=1)
            filename = f"{symbol.replace('/', '')}_{timeframe}_{yesterday.strftime('%Y%m%d')}.csv"
            filepath = os.path.join(self.cache_dir, filename)
            
            if os.path.exists(filepath):
                df = pd.read_csv(filepath, index_col=0, parse_dates=True)
                self.logger.warning(f"Using yesterday's cached data from {filepath}")
                return df
                
        except Exception as e:
            self.logger.error(f"Failed to load cached data: {e}")
        
        return None
    
    def get_exchange_info(self):
        """Get exchange information and status"""
        
        info = {}
        
        for name, exchange in self.exchanges.items():
            try:
                # Test connection
                markets = exchange.load_markets()
                
                # Get BTC market info
                btc_market = markets.get('BTC/USDT', {})
                
                info[name] = {
                    'status': 'online',
                    'total_markets': len(markets),
                    'btc_market': btc_market.get('info', {}),
                    'fees': {
                        'maker': exchange.fees.get('trading', {}).get('maker', 'unknown'),
                        'taker': exchange.fees.get('trading', {}).get('taker', 'unknown')
                    }
                }
                
            except Exception as e:
                info[name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return info


# Quick test function
if __name__ == "__main__":
    # Test the data fetcher
    import logging
    logging.basicConfig(level=logging.INFO)
    
    fetcher = DataFetcher()
    
    print("Testing exchange connections...")
    connections = fetcher.test_connections()
    for exchange, status in connections.items():
        print(f"{exchange}: {status}")
    
    print("\nFetching current BTC price...")
    try:
        price = fetcher.get_current_price()
        print(f"BTC Price: ${price['price']:,.2f} from {price['exchange']}")
    except Exception as e:
        print(f"Error getting price: {e}")
    
    print("\nFetching 1H OHLCV data...")
    try:
        df = fetcher.get_live_data('BTC/USDT', '1h', 50)
        print(f"Data shape: {df.shape}")
        print(f"Latest close: ${df['close'].iloc[-1]:,.2f}")
        print(f"Volume spike detected: {df['volume_spike'].iloc[-1]}")
    except Exception as e:
        print(f"Error getting OHLCV: {e}")