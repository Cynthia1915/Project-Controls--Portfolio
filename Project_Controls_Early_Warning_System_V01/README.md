# Project Controls Early Warning System V01

## Overview

The Project Controls Early Warning System V01 is a proof-of-concept analytics solution designed to automatically detect schedule, cost, progress, and float-related issues before they escalate into major project problems.

The objective is to transform project performance data into actionable management alerts and recommendations that support proactive decision-making.

This project demonstrates how project controls data can be converted into an executive decision-support system using Python and analytics techniques.

---

## Business Problem

Traditional dashboards often explain what has already happened.

Project managers and executives need answers to questions such as:

* Which activities require immediate attention?
* Which activities are showing signs of deterioration?
* Which activities may become critical?
* Where should management focus its efforts?
* What actions should be taken next?

The Early Warning System was developed to provide proactive alerts rather than reactive reporting.

---

## Project Objectives

* Detect schedule issues
* Detect cost issues
* Detect progress issues
* Detect activities with low schedule flexibility
* Prioritize activities requiring management attention
* Generate recommendations and escalation actions
* Produce executive-level performance indicators

---

## Data Source

### Performance Dataset

File:

Performance_Dataset_June2026.xlsx

The dataset contains:

* Activity IDs
* Activity codes
* Activity names
* Baseline durations
* Total float
* Planned progress
* Actual progress
* Progress variance
* Budget cost
* Planned Value (PV)
* Earned Value (EV)
* Actual Cost (AC)
* Schedule Performance Index (SPI)
* Cost Performance Index (CPI)

---

## Methodology

### Step 1 – Schedule Monitoring

Activities are flagged when:

SPI < 0.90

Meaning:

The activity is significantly behind schedule.

---

### Step 2 – Cost Monitoring

Activities are flagged when:

CPI < 0.90

Meaning:

The activity is spending money inefficiently.

---

### Step 3 – Progress Monitoring

Activities are flagged when:

Progress Variance < -10%

Meaning:

Actual progress is significantly behind plan.

---

### Step 4 – Float Monitoring

Activities are flagged when:

Float ≤ 5 days

Meaning:

The activity has limited schedule flexibility and may become critical.

---

## Alert Score Logic

Each issue contributes to an alert score.

| Issue          | Score |
| -------------- | ----- |
| Schedule Issue | 1     |
| Cost Issue     | 1     |
| Progress Issue | 1     |
| Float Issue    | 2     |

Float receives a higher weight because activities with limited float have a greater probability of affecting project completion.

---

## Alert Levels

### Green

Healthy activity.

### Yellow

Requires monitoring.

### Orange

High concern requiring management attention.

### Red

Executive escalation required.

---

## Outputs

The model generates:

* Issue counts
* Alert scores
* Alert levels
* Executive recommendations
* Top escalation activities
* Executive KPI dashboard
* Exportable Excel reports

---

## Example Recommendations

### Green

Continue normal monitoring.

### Yellow

Increase monitoring frequency and investigate performance trends.

### Orange

Develop a recovery plan and review schedule and cost exposure.

### Red

Executive escalation required. Immediate recovery actions and management review needed.

---

## Project Workflow

Performance Dataset
↓
Issue Detection
↓
Alert Scoring
↓
Alert Classification
↓
Management Recommendations
↓
Executive KPIs
↓
Decision Support Report

---

## Technologies Used

* Python
* Pandas
* NumPy
* Google Colab
* Excel
* Project Controls concepts
* Earned Value Management principles

---

## Skills Demonstrated

### Project Controls

* Schedule monitoring
* Cost monitoring
* Progress assessment
* Float analysis
* KPI development

### Analytics

* Data processing
* Rule-based classification
* Alert generation
* Management reporting
* Decision-support analytics

### Construction Management

* Proactive issue identification
* Performance management
* Escalation planning
* Executive reporting

---

## Limitations

This is a Version 1 proof of concept.

The model does not include:

* Resource loading analysis
* Portfolio-level analysis
* Machine learning prediction
* Probabilistic forecasting
* Real-time data integration
* Multi-project dependencies

---

## Future Improvements (V02)

Potential enhancements include:

* Machine learning risk prediction
* Portfolio control tower integration
* Automated email alerts
* Interactive dashboard development
* Trend analysis
* Recovery scenario simulations
* Real-time Primavera integration

---

## Purpose

The purpose of this project is to demonstrate how project controls data can be transformed into an Early Warning System that helps management identify issues early, prioritize activities, and take proactive actions before project performance deteriorates.

