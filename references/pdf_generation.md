# PDF Generation Reference

## Overview

The resume PDF is generated using ReportLab's Platypus layout engine. The design is a clean,
single-column, ATS-friendly layout using only Helvetica (built-in, no font installation needed).

## Design Specifications

### Page Setup
- **Page size**: US Letter (8.5" x 11" / 612 x 792 points)
- **Margins**: 0.5" top/bottom, 0.6" left/right (tight but readable, maximizes content space)
- **Font**: Helvetica family only (Helvetica, Helvetica-Bold, Helvetica-Oblique)

### Typography Scale
| Element | Font | Size | Leading | Space After |
|---------|------|------|---------|-------------|
| Name | Helvetica-Bold | 18pt | 22pt | 2pt |
| Contact info | Helvetica | 9pt | 11pt | 6pt |
| Section header | Helvetica-Bold | 11pt | 14pt | 4pt |
| Job title + company | Helvetica-Bold | 10pt | 13pt | 1pt |
| Dates / location | Helvetica-Oblique | 9pt | 11pt | 2pt |
| Body / bullets | Helvetica | 9.5pt | 12pt | 2pt |
| Skills text | Helvetica | 9pt | 11pt | 1pt |

### Section Order
1. Header (name + contact)
2. Professional Summary
3. Skills
4. Experience
5. Education
6. Projects (optional)

### Visual Rules
- Section headers: ALL CAPS, with a thin horizontal rule (0.5pt) underneath
- Bullet character: "•" (U+2022) followed by a space
- No indentation for bullets — use hanging indent via ReportLab's `leftIndent` and `firstLineIndent`
- Consistent spacing between sections (10pt)
- No color — pure black and white
- No images, icons, or graphics

## JSON Input Schema

The `generate_resume_pdf.py` script expects a JSON file with this structure:

```json
{
  "name": "Full Name",
  "contact": {
    "location": "City, Country",
    "email": "email@example.com",
    "phone": "+40 xxx xxx xxx",
    "linkedin": "linkedin.com/in/handle",
    "portfolio": "portfolio-url.com"
  },
  "summary": "2-3 sentence professional summary...",
  "skills": [
    {
      "category": "Category Name",
      "items": "Skill 1, Skill 2, Skill 3"
    }
  ],
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "location": "City, Country",
      "start_date": "Mon YYYY",
      "end_date": "Mon YYYY or Present",
      "bullets": [
        "Achievement or responsibility bullet point",
        "Another bullet point"
      ]
    }
  ],
  "education": [
    {
      "degree": "Degree Name",
      "institution": "University Name",
      "location": "City, Country",
      "start_date": "YYYY",
      "end_date": "YYYY",
      "details": "Optional: honors, relevant coursework, GPA"
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "description": "Brief description with technologies used",
      "url": "optional-url.com"
    }
  ]
}
```

## Generating the PDF

```bash
python scripts/generate_resume_pdf.py input.json output.pdf
```

The script handles:
- Auto page breaks (one or two pages as content requires)
- Consistent styling across all sections
- ATS-safe formatting (no tables, no columns, standard fonts)
- Proper unicode handling for bullet characters
