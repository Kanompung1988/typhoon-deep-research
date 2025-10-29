"""PDF and JSON reporting helpers."""

from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Any, Dict

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


@dataclass
class ReportPayload:
  job_id: str
  project_name: str
  metrics: Dict[str, Any]
  metadata: Dict[str, Any]


def build_pdf_report(payload: ReportPayload) -> bytes:
  """Generate a simple PDF summarising the carbon accounting output."""

  buffer = io.BytesIO()
  doc = SimpleDocTemplate(buffer, pagesize=A4, title="CarbonEye Agent Report")
  styles = getSampleStyleSheet()
  story = []

  story.append(Paragraph("<b>CarbonEye Agent</b> — Remote carbon stock analysis", styles["Title"]))
  story.append(Spacer(1, 12))
  story.append(Paragraph(f"Job ID: {payload.job_id}", styles["Normal"]))
  story.append(Paragraph(f"Project: {payload.project_name}", styles["Normal"]))
  story.append(Spacer(1, 12))
  story.append(Paragraph("<b>Key metrics</b>", styles["Heading2"]))

  for key, value in payload.metrics.items():
    story.append(Paragraph(f"{key}: {value}", styles["Normal"]))

  story.append(Spacer(1, 12))
  story.append(Paragraph("<b>Metadata</b>", styles["Heading2"]))
  story.append(Paragraph("<font size=9>" + repr(payload.metadata) + "</font>", styles["Normal"]))

  doc.build(story)
  return buffer.getvalue()


__all__ = ["ReportPayload", "build_pdf_report"]
