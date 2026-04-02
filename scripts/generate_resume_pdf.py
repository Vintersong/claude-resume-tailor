#!/usr/bin/env python3
"""
Resume PDF Generator — ATS-compliant single-column resume.
Uses ReportLab Platypus for clean, parseable output.

Usage:
    python generate_resume_pdf.py input.json output.pdf
"""

import json
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
)


# ── Page Setup ──────────────────────────────────────────────────────────────

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN_LEFT = 0.6 * inch
MARGIN_RIGHT = 0.6 * inch
MARGIN_TOP = 0.5 * inch
MARGIN_BOTTOM = 0.5 * inch

CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT


# ── Styles ──────────────────────────────────────────────────────────────────

def build_styles():
    """Create all paragraph styles for the resume."""
    styles = {}

    styles['Name'] = ParagraphStyle(
        'Name',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=2,
    )

    styles['Contact'] = ParagraphStyle(
        'Contact',
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    styles['SectionHeader'] = ParagraphStyle(
        'SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=2,
    )

    styles['Summary'] = ParagraphStyle(
        'Summary',
        fontName='Helvetica',
        fontSize=9.5,
        leading=12,
        spaceAfter=2,
    )

    styles['JobTitle'] = ParagraphStyle(
        'JobTitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        spaceAfter=0,
    )

    styles['JobMeta'] = ParagraphStyle(
        'JobMeta',
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=11,
        spaceAfter=2,
    )

    styles['Bullet'] = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=9.5,
        leading=12,
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=1,
    )

    styles['SkillCategory'] = ParagraphStyle(
        'SkillCategory',
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        spaceAfter=1,
    )

    styles['Education'] = ParagraphStyle(
        'Education',
        fontName='Helvetica',
        fontSize=9.5,
        leading=12,
        spaceAfter=1,
    )

    styles['ProjectName'] = ParagraphStyle(
        'ProjectName',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        spaceAfter=0,
    )

    styles['ProjectDesc'] = ParagraphStyle(
        'ProjectDesc',
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        spaceAfter=2,
    )

    return styles


# ── Section Builders ────────────────────────────────────────────────────────

def section_rule():
    """Thin horizontal rule under section headers."""
    return HRFlowable(
        width="100%",
        thickness=0.5,
        color="black",
        spaceAfter=4,
        spaceBefore=0,
    )


def build_header(data, styles):
    """Name and contact info."""
    elements = []
    elements.append(Paragraph(data['name'], styles['Name']))

    contact = data.get('contact', {})
    parts = []
    if contact.get('location'):
        parts.append(contact['location'])
    if contact.get('email'):
        parts.append(contact['email'])
    if contact.get('phone'):
        parts.append(contact['phone'])
    if contact.get('linkedin'):
        parts.append(contact['linkedin'])
    if contact.get('portfolio'):
        parts.append(contact['portfolio'])

    if parts:
        contact_line = " &nbsp;|&nbsp; ".join(parts)
        elements.append(Paragraph(contact_line, styles['Contact']))

    return elements


def build_summary(data, styles):
    """Professional summary section."""
    if not data.get('summary'):
        return []
    elements = []
    elements.append(Paragraph("PROFESSIONAL SUMMARY", styles['SectionHeader']))
    elements.append(section_rule())
    elements.append(Paragraph(data['summary'], styles['Summary']))
    return elements


def build_skills(data, styles):
    """Skills section grouped by category."""
    if not data.get('skills'):
        return []
    elements = []
    elements.append(Paragraph("SKILLS", styles['SectionHeader']))
    elements.append(section_rule())

    for skill_group in data['skills']:
        cat = skill_group.get('category', '')
        items = skill_group.get('items', '')
        line = f"<b>{cat}:</b> {items}"
        elements.append(Paragraph(line, styles['SkillCategory']))

    return elements


def build_experience(data, styles):
    """Experience section with job entries and bullets."""
    if not data.get('experience'):
        return []
    elements = []
    elements.append(Paragraph("EXPERIENCE", styles['SectionHeader']))
    elements.append(section_rule())

    for job in data['experience']:
        job_block = []

        # Title and company on one line
        title_line = f"{job['title']} — {job['company']}"
        job_block.append(Paragraph(title_line, styles['JobTitle']))

        # Date and location
        meta_parts = []
        if job.get('start_date') and job.get('end_date'):
            meta_parts.append(f"{job['start_date']} – {job['end_date']}")
        if job.get('location'):
            meta_parts.append(job['location'])
        if meta_parts:
            job_block.append(Paragraph(" | ".join(meta_parts), styles['JobMeta']))

        # Bullets
        for bullet in job.get('bullets', []):
            bullet_text = f"\u2022 {bullet}"
            job_block.append(Paragraph(bullet_text, styles['Bullet']))

        job_block.append(Spacer(1, 4))
        elements.append(KeepTogether(job_block))

    return elements


def build_education(data, styles):
    """Education section."""
    if not data.get('education'):
        return []
    elements = []
    elements.append(Paragraph("EDUCATION", styles['SectionHeader']))
    elements.append(section_rule())

    for edu in data['education']:
        edu_block = []
        title = f"<b>{edu['degree']}</b> — {edu['institution']}"
        if edu.get('location'):
            title += f", {edu['location']}"
        edu_block.append(Paragraph(title, styles['Education']))

        meta_parts = []
        if edu.get('start_date') and edu.get('end_date'):
            meta_parts.append(f"{edu['start_date']} – {edu['end_date']}")
        if edu.get('details'):
            meta_parts.append(edu['details'])
        if meta_parts:
            edu_block.append(Paragraph(" | ".join(meta_parts), styles['JobMeta']))

        edu_block.append(Spacer(1, 2))
        elements.append(KeepTogether(edu_block))

    return elements


def build_projects(data, styles):
    """Optional projects section."""
    if not data.get('projects'):
        return []
    elements = []
    elements.append(Paragraph("PROJECTS", styles['SectionHeader']))
    elements.append(section_rule())

    for proj in data['projects']:
        proj_block = []
        name = proj['name']
        if proj.get('url'):
            name += f" ({proj['url']})"
        proj_block.append(Paragraph(name, styles['ProjectName']))
        if proj.get('description'):
            proj_block.append(Paragraph(proj['description'], styles['ProjectDesc']))
        proj_block.append(Spacer(1, 2))
        elements.append(KeepTogether(proj_block))

    return elements


# ── Main ────────────────────────────────────────────────────────────────────

def generate_resume(input_path, output_path):
    """Generate a PDF resume from JSON data."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
    )

    styles = build_styles()
    story = []

    story.extend(build_header(data, styles))
    story.extend(build_summary(data, styles))
    story.extend(build_skills(data, styles))
    story.extend(build_experience(data, styles))
    story.extend(build_education(data, styles))
    story.extend(build_projects(data, styles))

    doc.build(story)
    print(f"✅ Resume generated: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python generate_resume_pdf.py input.json output.pdf")
        sys.exit(1)
    generate_resume(sys.argv[1], sys.argv[2])
