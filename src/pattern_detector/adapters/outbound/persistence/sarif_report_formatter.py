"""OASIS SARIF v2.1.0 report formatter for Haskell Pattern Detector."""

from __future__ import annotations

import json
from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ReportFormatterPort


class SarifReportFormatter(ReportFormatterPort):
    """Outputs results in OASIS SARIF v2.1.0 standard JSON format for CI/CD and GitHub Security Scanning."""

    def format(self, report: DetectionReport) -> str:
        sarif_data = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "DPX-Haskell",
                            "semanticVersion": "0.1.0",
                            "informationUri": "https://github.com/bivex/DPX-Haskell",
                            "rules": [],
                        }
                    },
                    "results": [
                        {
                            "ruleId": d.pattern_type.value,
                            "level": "error" if d.pattern_category.value in ("type_safety", "resilience") else "note",
                            "message": {"text": d.summary},
                            "locations": [
                                {
                                    "physicalLocation": {
                                        "artifactLocation": {"uri": str(d.primary_location.file_path) if d.primary_location else ""},
                                        "region": {
                                            "startLine": d.primary_location.line if d.primary_location else 1,
                                            "startColumn": d.primary_location.column if d.primary_location else 1,
                                        },
                                    }
                                }
                            ]
                            if d.primary_location
                            else [],
                        }
                        for d in report.detections
                    ],
                }
            ],
        }
        return json.dumps(sarif_data, indent=2)
