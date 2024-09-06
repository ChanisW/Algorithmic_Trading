import pandas as pd

class MomentumAgent:
    def __init__(self, window=20):
        self.name = "Momentum Agent"
        self.window = window
        self.initial_capital = 100000
        self.holdings = 0
        self.cash = self.initial_capital
        self.last_price = None

    def calculate_momentum(self, df):
        df['Momentum'] = df['Close'].diff(self.window)
        df['Momentum'] = df['Momentum'].fillna(0)
        return df

    def trade(self, df):
        df = self.calculate_momentum(df)
        current_price = df['Close'].iloc[-1]
        momentum = df['Momentum'].iloc[-1]
        signal = 0

        if momentum > 0:
            signal = 1
        elif momentum < 0:
            signal = -1
        else:
            signal = 0

        current_time = pd.Timestamp.now()
        if signal == 1 and self.cash > 0:
            self.holdings = self.cash / current_price
            self.cash = 0
            print(f"{current_time}: Momentum Buy at {current_price:.2f}")
        elif signal == -1 and self.holdings > 0:
            self.cash = self.holdings * current_price
            self.holdings = 0
            print(f"{current_time}: Momentum Sell at {current_price:.2f}")
        else:
            print(f"{current_time}: Momentum Hold")

    def get_portfolio_value(self, current_price):
        return self.cash + (self.holdings * current_price)

    def train(self, data):
        """Train the agent to find the best parameters."""
        best_window = self.window
        best_profit = -float('inf')
        
        for win in range(5, 50, 5):
            self.window = win
            data_copy = data.copy()
            self.trade(data_copy)
            final_value = self.get_portfolio_value(data_copy['Close'].iloc[-1])
            if final_value > best_profit:
                best_profit = final_value
                best_window = win
        
        self.window = best_window
        print(f"Trained {self.name} with Window: {self.window}")
