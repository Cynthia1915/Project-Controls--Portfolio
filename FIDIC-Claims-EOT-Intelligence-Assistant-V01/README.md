# FIDIC Claims & EOT Intelligence | Exploratory Decision-Support Prototype

**Delay Event Screening · Notice and Evidence Tracking · Claims Readiness**

[← Portfolio](../README.md)

## Management question

**Which reported delay events need immediate evidence gathering, notice review and specialist assessment?**

This independent portfolio proof of concept combines a modeled performance dataset with a delay-event register to produce **screening classifications and follow-up recommendations**.

It is intended to support **early documentation triage**, **not** determine legal entitlement, compensability or the number of extension-of-time days.

## Inputs

- Modeled project performance data: activity identifiers, planned/actual progress, performance indicators, float and baseline durations.
- Delay register: event descriptions, related activities, delay categories, notice status and evidence availability.

See the [data folder](./Data/).

## Screening workflow

```text
Performance data + delay register
                ↓
     Event / activity matching
                ↓
     Rule-based event category
                ↓
     Notice and evidence review
                ↓
   Documentation priority / actions
```

The original model groups events under employer, contractor, exceptional event, third-party or unknown categories. These categories are **only preliminary prompts for review**.

**Do not interpret a label such as “potential EOT” or a high confidence score as an entitlement finding.** FIDIC rights and obligations depend on the particular contract edition and amendments, facts, critical-path impact, concurrency, causation, notice requirements and applicable law.

## Outputs and evidence

- [Prototype notebook](./notebook/)
- [Illustrative outputs](./outputs/)
- [Screenshots](./screenshots/)

The outputs may help a project-controls or contracts team prioritize **notice review, event records, contemporaneous evidence and specialist delay analysis**.

## Limitations

This V01 **does not** conduct a forensic CPM delay analysis, time impact analysis, as-planned versus as-built comparison, concurrency assessment, contract-specific clause interpretation or legal entitlement determination.

**Professional boundary:** The tool is a demonstration of analytics and documentation workflow, not legal advice, a FIDIC-compliant claims assessment or a substitute for qualified planning/claims professionals.

**Status:** Synthetic proof-of-concept portfolio project.
