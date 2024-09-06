import numpy as np
import pandas as pd

class RSIAgent:
    def __init__(self, sma_window=50, rsi_window=14, overbought=70, oversold=30):
        self.name = "RSI Agent"
        self.position = 0
        self.cash = 100000
        self.holdings = 0
        self.sma_window = sma_window
        self.rsi_window = rsi_window
        self.overbought = overbought
        self.oversold = oversold

    def calculate_sma(self, data):
        return data['Close'].rolling(window=self.sma_window, min_periods=1).mean().iloc[-1]

    def calculate_rsi(self, data):
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=self.rsi_window, min_periods=1).mean()
        avg_loss = loss.rolling(window=self.rsi_window, min_periods=1).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]

    def generate_signals(self, data):
        sma = self.calculate_sma(data)
        rsi = self.calculate_rsi(data)
        if data['Close'].iloc[-1] > sma and rsi > self.overbought:
            return 2
        elif data['Close'].iloc[-1] < sma and rsi < self.oversold:
            return 1
        else:
            return 0

    def trade(self, data):
        signal = self.generate_signals(data)
        price = data['Close'].iloc[-1]
        if signal == 1 and self.position <= 0:
            if self.cash > 0:
                self.holdings = self.cash / price
                self.cash = 0
                self.position = 1
                print(f"{pd.Timestamp.now()}: {self.name} Buy at {price}")
        elif signal == 2 and self.position >= 0:
            if self.holdings > 0:
                self.cash = self.holdings * price
                self.holdings = 0
                self.position = -1
                print(f"{pd.Timestamp.now()}: {self.name} Sell at {price}")
        else:
            print(f"{pd.Timestamp.now()}: {self.name} Hold")

    def get_portfolio_value(self, current_price):
        return self.cash + (self.holdings * current_price)

    def train(self, data):
        """Train the agent to find the best parameters."""
        best_sma_window = self.sma_window
        best_rsi_window = self.rsi_window
        best_overbought = self.overbought
        best_oversold = self.oversold
        best_profit = -float('inf')
        
        for sma in range(10, 100, 10):
            for rsi in range(10, 30, 2):
                for overbought in range(60, 90, 5):
                    for oversold in range(10, 40, 5):
                        self.sma_window = sma
                        self.rsi_window = rsi
                        self.overbought = overbought
                        self.oversold = oversold
                        data_copy = data.copy()
                        self.trade(data_copy)
                        final_value = self.get_portfolio_value(data_copy['Close'].iloc[-1])
                        if final_value > best_profit:
                            best_profit = final_value
                            best_sma_window = sma
                            best_rsi_window = rsi
                            best_overbought = overbought
                            best_oversold = oversold
        
        self.sma_window = best_sma_window
        self.rsi_window = best_rsi_window
        self.overbought = best_overbought
        self.oversold = best_oversold
        print(f"Trained {self.name} with SMA Window: {self.sma_window}, RSI Window: {self.rsi_window}, Overbought: {self.overbought}, Oversold: {self.oversold}")
