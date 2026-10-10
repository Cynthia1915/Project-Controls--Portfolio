# Primavera P6 Baseline Risk Intelligence | Prototype V1

**Baseline Assurance · Schedule Vulnerability · Risk Prioritization**

[← Portfolio](../README.md)

## Management question

**Which work packages and schedule activities warrant attention before execution begins, beyond the conventional critical-path list?**

This independent **portfolio prototype** applies a transparent weighted scoring approach to Primavera P6 baseline information to highlight potential schedule exposure.

## Approach

| Activity risk component | Weight |
| --- | ---: |
| Float risk | 40% |
| Dependency impact | 25% |
| Duration exposure | 15% |
| Package risk | 10% |
| Gateway risk | 10% |

A separate package exposure assessment considers critical density, number of critical activities, successor impact and remaining duration.

**Interpretation:** These weights are **heuristic demonstration assumptions**, not calibrated failure probabilities or industry-certified schedule quality thresholds.

## Illustrative results

The original V1 case-study output reported **4,218 activities screened**, **197 critical activities** and **9 executive-priority risk items**. It highlighted structural work and MEP approval interfaces as potential areas for management review.

These figures are **model outputs from an independent portfolio exercise**, not audited client project outcomes. They should be reproduced from the accompanying artifacts before reuse in a formal presentation.

## Available evidence

- [Executive presentation](./Carousel/)
- [Analysis notebook](./Notebook/)
- [Screenshots](./Screenshots/)

## Recommended management use

Use the screening as a **triage mechanism**: review high-scoring activities, validate P6 logic and calendars, investigate interface dependencies, and assign owners to actions. The score should **not** replace critical-path analysis, formal schedule assurance or project-specific risk workshops.

**Tools:** Primavera P6 concepts, Python, Pandas, Google Colab.

**Status:** Portfolio prototype V1; simulated/model-based demonstration, not a live-client assignment.
