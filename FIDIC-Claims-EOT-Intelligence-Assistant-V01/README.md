# FIDIC Claims & Extension of Time (EOT) Intelligence Assistant V01

## Overview

This project is a proof-of-concept analytics assistant for construction claims and Extension of Time (EOT) assessment using project controls data and FIDIC-based logic.

The objective is to support early identification of delay events, potential EOT entitlement, contractual risk, and required follow-up actions.

This project does not replace contractual, legal, or claims expert judgment. It is designed as a decision-support tool.

---

## Business Problem

Construction projects often experience delays caused by different parties or events.

Project teams need to quickly understand:

* Which activities were affected?
* What type of delay occurred?
* Who may be responsible?
* Could the delay potentially justify an EOT?
* Was notice issued?
* Is evidence available?
* What action should management take?

---

## Input Files

### 1. Performance Dataset

File:

```text
Performance_Dataset_June2026.xlsx
```

Used to provide:

* Activity ID
* Activity code
* Activity name
* Planned progress
* Actual progress
* Progress variance
* SPI
* CPI
* Float
* Baseline duration

---

### 2. Delay Register

File:

```text
Delay_Register.xlsx
```

Used to provide:

* Delay ID
* Related activity
* Delay event description
* Delay days
* Delay type
* Notice status
* Evidence availability

---

## Delay Types Used

The model classifies delays into:

* Employer
* Contractor
* Exceptional Event
* Third Party
* Unknown

---

## FIDIC-Based Logic

### Employer Delay

Typical examples:

* Late drawing approval
* Late access
* Late approvals
* Employer instruction changes

Model output:

```text
Potential EOT = Yes
```

---

### Contractor Delay

Typical examples:

* Equipment breakdown
* Poor planning
* Late procurement
* Subcontractor underperformance

Model output:

```text
Potential EOT = No
```

---

### Exceptional Event

Typical examples:

* Severe rainfall
* Flooding
* Government restrictions
* Force majeure-type events

Model output:

```text
Potential EOT = Potential
```

---

### Third Party / Unknown

Model output:

```text
Potential EOT = Requires Review
```

---

## Contractual Risk Logic

The model checks whether:

* Notice was issued
* Evidence is available

### High Risk

```text
No notice + No evidence
```

### Medium Risk

```text
Notice missing OR evidence missing
```

### Low Risk

```text
Notice issued + evidence available
```

---

## EOT Confidence Logic

### High Confidence

Potential EOT is Yes and documentation risk is low.

### Medium Confidence

Potential EOT exists but notice or evidence is incomplete.

### Low Confidence

Potential EOT is weak or documentation is insufficient.

---

## Outputs

The model produces:

* Claims intelligence table
* Potential EOT classification
* Contractual risk level
* EOT confidence level
* Recommended actions

---

## Example Recommendations

* Issue contractual notice
* Collect supporting evidence
* Perform critical path analysis
* Prepare EOT submission
* Review contractual entitlement
* Monitor and document delay event

---

## Project Workflow

```text
Performance Dataset
        +
Delay Register
        ↓
Merge Activity and Delay Data
        ↓
Classify Delay Type
        ↓
Assess Potential EOT
        ↓
Evaluate Notice and Evidence
        ↓
Assign Contractual Risk
        ↓
Generate Recommendations
```

---

## Technologies Used

* Python
* Pandas
* NumPy
* Google Colab
* Excel
* Project Controls concepts
* FIDIC-based delay classification logic

---

## Assumptions

* Delay events were created for portfolio demonstration purposes.
* Delay types are simplified.
* The model uses rule-based logic.
* The model does not perform full legal entitlement assessment.
* The model does not perform full critical path delay analysis.

---

## Limitations

This is a Version 1 proof of concept.

It does not include:

* Detailed FIDIC clause mapping
* Full critical path impact analysis
* Concurrent delay analysis
* As-planned versus as-built analysis
* Time impact analysis
* Contractual notice period checking
* Legal interpretation

---

## Future Improvements for V02

Future versions could include:

* FIDIC clause reference mapping
* Critical path impact assessment
* Delay notice deadline tracker
* Concurrent delay detection
* Evidence checklist automation
* EOT days calculation
* Claim report generation
* Dashboard for contractual exposure

---

## Purpose

The purpose of this project is to demonstrate how construction management, project controls, contract management, and analytics can be combined into a simple decision-support assistant for delay and EOT assessment.
