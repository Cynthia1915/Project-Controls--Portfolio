# Primavera P6 Baseline Risk Intelligence Engine V1

## Overview

A PMO analytics project developed to identify high-risk activities and vulnerable work packages before project execution begins.

Traditional schedule reviews focus on the critical path. This project extends that approach by evaluating activity risk, dependency impact, package exposure, and schedule vulnerability across an entire Primavera P6 baseline schedule.

## Methodology

### Activity Risk Engine

Activity Risk Score =

* 40% Float Risk
* 25% Dependency Impact
* 15% Duration Exposure
* 10% Package Risk
* 10% Gateway Risk

### Package Exposure Engine

Package Exposure Score based on:

* Critical Density
* Critical Activities
* Successor Impact
* Remaining Duration

## Tools

* Primavera P6
* Python
* Pandas
* Google Colab

## Results

* 4,218 activities analyzed
* 197 critical activities identified
* 9 executive-level risks prioritized
* Steel Structure Works critical density ≈ 49%
* MEP approval identified as a major schedule driver

## Repository Structure

* Carousel → Executive presentation
* Notebook → Full Python implementation
* Screenshots → Key outputs and findings

## Future Enhancements

* Interactive PMO Dashboard
* Portfolio-Level Risk Analysis
* Predictive Schedule Intelligence
* Streamlit Web Application

