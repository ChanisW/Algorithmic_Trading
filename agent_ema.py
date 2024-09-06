import pandas as pd

class EMAAgent:
    def __init__(self, short_window=12, long_window=26, initial_balance=100000):
        self.name = "EMA Agent"
        self.short_window = short_window
        self.long_window = long_window
        self.cash = initial_balance
        self.position = 0
        self.holdings = 0

    def calculate_ema(self, data, window):
        return data['Close'].ewm(span=window, adjust=False).mean().iloc[-1]

    def generate_signals(self, data):
        short_ema = self.calculate_ema(data, self.short_window)
        long_ema = self.calculate_ema(data, self.long_window)
        if short_ema > long_ema and self.position == 0:
            return 1
        elif short_ema < long_ema and self.position > 0:
            return 2
        else:
            return 0

    def trade(self, data):
        signal = self.generate_signals(data)
        price = data['Close'].iloc[-1]
        if signal == 1 and self.position == 0:
            if self.cash > 0:
                self.holdings = self.cash / price
                self.cash = 0
                self.position = 1
                print(f"{pd.Timestamp.now()}: {self.name} Buy at {price}")
        elif signal == 2 and self.position > 0:
            if self.holdings > 0:
                self.cash = self.holdings * price
                self.holdings = 0
                self.position = 0
                print(f"{pd.Timestamp.now()}: {self.name} Sell at {price}")
        else:
            print(f"{pd.Timestamp.now()}: {self.name} Hold")

    def get_portfolio_value(self, current_price):
        return self.cash + (self.holdings * current_price)

    def train(self, data):
        """Train the agent to find the best parameters."""
        best_short_window = self.short_window
        best_long_window = self.long_window
        best_profit = -float('inf')
        
        for short in range(5, 30, 5):
            for long in range(20, 50, 5):
                self.short_window = short
                self.long_window = long
                data_copy = data.copy()
                self.trade(data_copy)
                final_value = self.get_portfolio_value(data_copy['Close'].iloc[-1])
                if final_value > best_profit:
                    best_profit = final_value
                    best_short_window = short
                    best_long_window = long
        
        self.short_window = best_short_window
        self.long_window = best_long_window
        print(f"Trained {self.name} with Short Window: {self.short_window}, Long Window: {self.long_window}")
