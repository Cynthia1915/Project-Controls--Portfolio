
# Performance-Driven Risk & Forecasting Engine V03

## Overview

This project demonstrates a performance-driven project controls analytics engine using Primavera schedule data, progress updates, cost data, Earned Value Management, dynamic risk scoring, and Monte Carlo forecasting.

The objective is to move beyond static dashboards and develop a decision-support workflow that helps identify current performance issues, forecast potential delay exposure, and support executive-level project controls decisions.

## Key Capabilities

- Progress performance analysis
- Earned Value Management calculations
- SPI and CPI performance tracking
- Dynamic risk scoring
- Forecast completion analysis
- Performance-based Monte Carlo simulation
- Executive recommendations
- Automated reporting

## Methodology

The model uses a performance dataset containing:

- Baseline schedule duration
- Planned progress
- Actual progress
- Progress variance
- Budget cost
- Planned Value
- Earned Value
- Actual Cost
- SPI
- CPI
- Float information

The engine identifies schedule, cost, progress, and float issues, then combines them into a dynamic risk score. It also uses current SPI performance to estimate forecast durations and perform a simplified Monte Carlo simulation.

## Key Outputs

- Top risk activities
- Top delay drivers
- Dynamic risk score
- Risk category classification
- Forecast delay exposure
- P50, P80, and P90 schedule forecast
- Executive summary report

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Google Colab
- Primavera P6 schedule concepts
- Earned Value Management
- Monte Carlo simulation

## Important Note

This is a portfolio prototype. Some progress and cost data were simulated to demonstrate the project controls workflow.

The Monte Carlo simulation uses the maximum simulated activity duration as a simplified proxy for project completion duration. A full production-grade schedule risk analysis would require Primavera activity relationships, calendars, constraints, and critical path network logic.

## Purpose

This project was built to demonstrate how project controls data can be transformed into performance insights, probabilistic forecasts, and management recommendations.
