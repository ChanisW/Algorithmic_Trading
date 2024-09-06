import pandas as pd

class MovingAverageCrossoverAgent:
    def __init__(self, short_window=50, long_window=200):
        self.name = "Moving Average Crossover Agent"
        self.position = 0
        self.cash = 100000
        self.holdings = 0
        self.short_window = short_window
        self.long_window = long_window

    def calculate_moving_averages(self, data):
        data['short_mavg'] = data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        data['long_mavg'] = data['Close'].rolling(window=self.long_window, min_periods=1).mean()
        return data['short_mavg'].iloc[-1], data['long_mavg'].iloc[-1]

    def generate_signals(self, data):
        short_mavg, long_mavg = self.calculate_moving_averages(data)
        if short_mavg > long_mavg:
            return 1
        elif short_mavg < long_mavg:
            return 2
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
        # For simplicity, we'll use a basic grid search approach.
        best_short_window = self.short_window
        best_long_window = self.long_window
        best_profit = -float('inf')
        
        for short in range(10, 100, 10):
            for long in range(100, 300, 20):
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
