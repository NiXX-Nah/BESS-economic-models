# Electricity Energy Storage Market Analytics and Optimisation 

## Overview

This repository showcases research and modelling work on energy storage systems in electricity markets.
The projects focus on understanding how energy storage facility creates value through energy arbitrage, market participation, and long-term investment under uncertainty. 

The repository combines electricity market analysis, price forecasting, mathematical optimisation, and capacity expansion modelling to investigate both operational and strategic decisions for energy storage. 

## Research Areas

1. Short-Term Electricity Market Analysis

   Electricity prices exhibit significant temporal variability due to demand fluctuations, renewable generation, fuel prices, and system constraints. These price dynamics create opportunities for battery storage.

   Topics include:
   Day-ahead electricity market behaviour
   Intraday market dynamics
   Price volatility and market uncertainty
   Revenue opportunities for storage facility
   Market fundamentals affecting storage profitability  


2. Electricity Price Forecasting

   Battery operation depends heavily on future electricity prices, Accurate forecasts improve charging and discharging decisions and directly influence economic performance.
   
   Topics include:
   Time-series forecasting (e.g., ARIMA, GARCH)
   Machine learning methods (e.g., LSTM)
   Forecast evaluation
   Assessment of how forecasting accuracy affects storage revenue


3. Energy Storage Facility Revenue Optimisation

   This research develops optimisation models that determine economically optimal battery operating strategies under different market assumptions.

   Implemented approaches include:

   1) Wholesale Energy Arbitrage
      Optimisation of battery charging and discharging using wholesale electricity prices.
      Methods: Linear Programming, Mixed-Integer Linear Programming (MILP), Pyomo, SciPy.

   2) Multi-Market Revenue Optimisation
      Battery storage can access multiple revenue streams beyond wholesale arbitrage. The optimisation framework determines the economically optimal allocation of battery capacity across competing market opportunities. 
      This section investigates optimisation across multiple market products, including: wholesale electricity markets, ancillary services, capacity markets, other flexibility services.

   3) Stochastic Optimisation
      Future market prices are inherently uncertain.
      This work extends deterministic optimisation by incorporating uncertainty into operational decision-making.
      Topics include: scenario-based optimisation, expected revenue maximisation, risk-aware operational strategies, market uncertainty analysis.


4. Electricity Market Competition
      Battery storage influences the behaviour of other market participants.
      Research in this section investigates: strategic behaviour using game-theoretic models, effects of battery storage on conventional generation, unit commitment modelling. Additional stochastic analysis is performed using Monte Carlo simulation to represent generation asset availability and operational uncertainty.


5. Long-Term Investment Planning
   Battery deployment depends on technology costs, electricity markets, fuel prices, and government policy.
   This section evaluates long-term storage investment using capacity expansion modelling.
   Topics include:
   Optimal battery deployment pathways under increasing penetration of RES
   Fuel price uncertainty
   Policy scenario analysis
   Electricity market evolution

   Future fuel price trajectories are generated using stochastic modelling techniques, including Geometric Brownian motion, to represent long-term market uncertainty.


## Objectives

The aim of this repository is to demonstrate how quantitative methods can be applied to address real-world challenges in electricity markets and battery energy storage. 

The projects illustrate the integration of:
    Electricity market analysis
    Forecasting and machine learning 
    Mathematical optimisation
    Stochastic modelling 
    Long-term investment planning
to support economically informed operational and strategic decision-making in modern power systems. 


## Disclaimer

This repository is intended for research and educational purposes. Some market simulation frameworks build upon established open-source models, which have been adapted and applied to investigate battery storage applications and electricity market behaviour. 

   

   

   

      
      

  


