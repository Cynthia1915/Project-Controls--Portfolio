#!/usr/bin/env python3
"""Post-process relative-hour Monte Carlo samples without inventing calendar dates.

Input: outputs of network_monte_carlo.py. This does NOT reproduce Primavera P6
calendars, constraints, data-date logic, or contractual completion confidence.
"""
import argparse
import csv
import json
import math
from pathlib import Path


def percentile(sorted_values, probability):
    if not sorted_values or not 0 <= probability <= 1:
        raise ValueError("Nonempty samples and probability between 0 and 1 required")
    position = (len(sorted_values) - 1) * probability
    lower, upper = math.floor(position), math.ceil(position)
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * (position - lower)


def report(summary, samples, bins=20):
    if bins < 1 or not samples:
        raise ValueError("At least one sample and one histogram bin required")
    if not all(math.isfinite(x) and x >= 0 for x in samples):
        raise ValueError("Samples must be finite nonnegative relative hours")
    if summary.get("runs") != len(samples):
        raise ValueError("Sample count differs from summary runs")
    nominal = float(summary["nominal_relative_work_hours"])
    if not math.isfinite(nominal) or nominal < 0:
        raise ValueError("Invalid deterministic reference")
    values = sorted(samples)
    minimum, maximum = values[0], values[-1]
    width = (maximum - minimum) / bins if maximum > minimum else 1.0
    counts = [0] * bins
    for value in values:
        index = min(int((value - minimum) / width), bins - 1)
        counts[index] += 1
    histogram = [
        {"lower_relative_hours": round(minimum + i * width, 4),
         "upper_relative_hours": round(minimum + (i + 1) * width, 4),
         "samples": count}
        for i, count in enumerate(counts)
    ]
    return {
        "project": "Hyperscale Data Center (synthetic case study)",
        "target_milestone": summary["target_milestone"],
        "runs": len(values),
        "seed": summary.get("seed"),
        "nominal_relative_work_hours": round(nominal, 2),
        "p10_relative_work_hours": round(percentile(values, .1), 2),
        "p50_relative_work_hours": round(percentile(values, .5), 2),
        "p80_relative_work_hours": round(percentile(values, .8), 2),
        "p90_relative_work_hours": round(percentile(values, .9), 2),
        "mean_relative_work_hours": round(sum(values) / len(values), 2),
        "probability_exceeding_nominal": round(sum(x > nominal for x in values) / len(values), 4),
        "p80_contingency_relative_hours": round(percentile(values, .8) - nominal, 2),
        "histogram": histogram,
        "validation_status": "UNVALIDATED_P6_CALENDAR_EQUIVALENCE",
        "interpretation": (
            "All values are relative continuous-hour network outputs. "
            "The probability of exceeding the deterministic reference is NOT "
            "the probability of missing the contractual RFS date. "
            "No absolute finish dates, calibrated risk correlations, or P6-equivalent "
            "completion probabilities are asserted."
        )
    }


def load_samples(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if "relative_work_hours" not in (reader.fieldnames or []):
            raise ValueError("Missing relative_work_hours column")
        return [float(row["relative_work_hours"]) for row in reader]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", required=True, help="network_risk_summary.json")
    parser.add_argument("--samples", required=True, help="network_risk_samples.csv")
    parser.add_argument("--output", default="risk_outputs/relative_risk_report.json")
    parser.add_argument("--bins", type=int, default=20)
    args = parser.parse_args()
    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    result = report(summary, load_samples(args.samples), bins=args.bins)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "histogram"}, indent=2))


if __name__ == "__main__":
    main()
