### Battery Arbitrage Model (Price-Taking) ###

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime

import pyomo.environ as pyo
from pyomo.opt import SolverFactory

class BatteryOptimizer:
    def __init__(self, prices, config):

        self.prices = prices
        self.config = config
        self.N = len(prices)
        self.model = pyo.ConcreteModel()

    def build_model(self):
        """ Sets up the Pyomo MILP model. """
        model = self.model
        model.T = pyo.Set(initialize=range(self.N), doc='Time steps')

        # Define variables
        model.P_charge = pyo.Var(model.T, bounds=(0, self.config['P_MAX']), doc='Charging power (MW)')
        model.P_discharge = pyo.Var(model.T, bounds=(0, self.config['P_MAX']), doc='Discharging power (MW)')
        model.SOC = pyo.Var(model.T, bounds=(0, self.config['E_CAP']), doc='State of charge (MWh)')
        model.charge_indicator = pyo.Var(model.T, within=pyo.Binary, doc='Charge/discharge indicator')

        # Objective function: maximize profit
        def pbj_rule(model):
            return sum(self.prices[t] * (model.P_discharge[t] - model.P_charge[t]) for t in model.T)
        model.profit = pyo.Objective(rule=pbj_rule, sense=pyo.maximize)

        # Constraints: SOC Dynamics
        def soc_rule(model, t):
            # Round-trip efficiency is applied here
            eff = self.config['EFF']
            if t == 0:
                return model.SOC[t] == self.config['SOC_INIT'] + (model.P_charge[t] * eff - model.P_discharge[t] / eff)
            else:
                return model.SOC[t] == model.SOC[t-1] + (model.P_charge[t] * eff - model.P_discharge[t] / eff)
        model.soc_constraint = pyo.Constraint(model.T, rule=soc_rule)

        # Constraints: Mutually exclusive charging and discharging
        def charge_limit(model, t):
            return model.P_charge[t] <= self.config['P_MAX'] * model.charge_indicator[t]
        model.charge_limit = pyo.Constraint(model.T, rule=charge_limit)

        def discharge_limit(model, t):
            return model.P_discharge[t] <= self.config['P_MAX'] * (1 - model.charge_indicator[t])
        model.discharge_limit = pyo.Constraint(model.T, rule=discharge_limit)

        # Constraints: Cycling constraint (optional)
        """
        def cycling_rule(model, t):
            if t < 24: return pyo.Constraint.Skip
            throughput = sum(model.P_charge[t-i] + model.P_discharge[t-i] for i in range(24))
            return throughput <= self.config['MAX_CYCLES_PER_DAY'] * self.config['E_CAP']
        model.cycling_constraint = pyo.Constraint(model.T, rule=cycling_rule)
        """


    # Solve the optimization problem
    def solve(self, solver_name='glpk'):
        solver = SolverFactory(solver_name)
        results = solver.solve(self.model,tee=True)

        if results.solver.termination_condition == pyo.TerminationCondition.optimal:
            return self.extract_results()
        else:
            raise ValueError("Solver did not find an optimal solution.")

    def extract_results(self):
        model = self.model
        res = pd.DataFrame({
            'Charge_MW': [pyo.value(model.P_charge[t]) for t in model.T],
            'Discharge_MW': [pyo.value(model.P_discharge[t]) for t in model.T],
            'SOC_MWh': [pyo.value(model.SOC[t]) for t in model.T],
            'Price_EUR': self.prices
        })
        return res

    def save_results(self, df, filename=None):
        if filename is None:
            filename = f"battery_optimization_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            df.to_csv(filename, index=True)
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Failed to save results: {e}")

## Plot
def plot_results(df, title="Battery Optimal Dispatch"):

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12,10), sharex=True)

    ax1.plot(df.index, df['Price_EUR'], label='Price (EUR/MWh)', color='blue')
    ax1.set_ylabel('Price (EUR/MWh)')
    ax1.set_title(title)

    ax2.plot(df.index, -df['Charge_MW'], label='Charging Power (MW)', color='green', alpha=0.3)
    ax2.plot(df.index, df['Discharge_MW'], label='Discharging Power (MW)', color='red', alpha=0.3)
    ax2.set_ylabel('Power (MW)')
    ax2.legend()

    ax3.plot(df.index, df['SOC_MWh'], label='State of Charge (MWh)', color='orange')
    ax3.set_ylabel('State of Charge (MWh)')
    ax3.set_xlabel('Time')

    plt.tight_layout()
    plt.show()

"""
## Alternative plot

def plot_results(df, title="Battery Dispatch and Price"):
    # Plots Price and Power on the same chart using dual y-axes
    fig, ax1 = plt.subplots(figsize=(12,6))

    # primary y-axis: power MW
    ax1.fill_between(df.index, -df['Charge_MW'], color='green', alpha=0.3, label='Charging Power (MW)')
    ax1.fill_between(df.index, df['Discharge_MW'], color='red', alpha=0.3, label='Discharging Power (MW)')
    ax1.set_ylabel('Power (MW)', fontsize=12)
    ax1.legend(loc='upper left')

    # secondary y-axis: price EUR/MWh
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['Price_EUR'], color='blue', label='Price (EUR/MWh)')
    ax2.set_ylabel('Price (EUR/MWh)', fontsize=12)
    ax2.legend(loc='upper right')

    plt.title(title, fontsize=14)
    plt.tight_layout()
    plt.show()
"""


if __name__ == "__main__":
    # Configuration 
    BATTERY_CONFIG = {
        'P_MAX': 100.0,  # MW
        'E_CAP': 400.0,  # MWh (4-hour duration at max power)
        'EFF': 0.9,    # Round-trip efficiency
        'SOC_INIT': 200.0,  # Initial state of charge (MWh)
        'MAX_CYCLES_PER_DAY': 1  # Maximum number of full cycles per day
    }

    # Data Loading
    try:
        data_path = os.path.join(os.path.dirname(__file__), '11-NOV-MED.csv')
        df_input = pd.read_csv (data_path, index_col=0, parse_dates=True)
        market_prices = df_input['IndexPriceEUR'].values
    except FileNotFoundError:
        print("Data file not found. Please ensure '11-NOV-MED.csv' is in the same directory.")
        exit(1)

    # Execution
    optimizer = BatteryOptimizer(prices=market_prices, config=BATTERY_CONFIG)
    optimizer.build_model()

    try:
        results_df = optimizer.solve(solver_name ='glpk')
        optimizer.save_results(results_df, filename=os.path.join(os.path.dirname(__file__), "battery_optimization_results.csv"))
        plot_results(results_df.head(168), title="Battery Optimal Dispatch for One Week")
    except Exception as e:
        print(f"An error occurred during optimization: {e}")


