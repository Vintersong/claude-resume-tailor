---
name: resume-tailor
description: >
  Tailors and generates ATS-optimized PDF resumes from a master experience reference file,
  customized to match specific job postings. Use this skill whenever the user asks to create,
  tailor, customize, or generate a resume or CV for a job posting, job application, or position.
  Also trigger when the user pastes a job description and asks for help applying, or mentions
  "resume", "CV", "job application", "tailor my resume", or "apply for this job". Produces a
  clean single-column PDF resume plus an ATS keyword analysis summary.
---

# Resume Tailor Skill

## Overview

This skill takes a job posting and generates a tailored, ATS-compliant PDF resume by:
1. Analyzing the job posting for required skills, keywords, and priorities
2. Loading the user's master experience reference file
3. Auto-detecting the best profile emphasis (game design, data analysis, UX research, development, etc.)
4. Selecting and rewriting relevant experience bullets to match the posting's language
5. Generating a clean single-column PDF
6. Producing an ATS keyword match analysis

## Workflow

### Step 1: Gather Inputs

**Job posting** — The user provides a job posting via:
- Pasted text in the conversation
- A URL (use web_fetch to retrieve it)
- An uploaded file

**Master reference file** — Load from `references/master_resume.md`. If missing, ask the user to provide their experience and save it there for future use.

### Step 2: Analyze the Job Posting

Extract and categorize:
- **Hard skills**: Specific tools, languages, engines, frameworks, methodologies
- **Soft skills**: Leadership, communication, collaboration, etc.
- **Domain keywords**: Industry-specific terms (e.g., "live ops", "agile", "UX research")
- **Required qualifications**: Degrees, years of experience, certifications
- **Nice-to-haves**: Preferred but not required qualifications
- **Role level**: Junior, mid, senior, lead — infer from context
- **Profile type**: Auto-detect which emphasis best fits (game design, data/analytics,
  UX research, software development, general tech, etc.)

### Step 3: Build the Tailored Resume

Using the master reference and job analysis:

1. **Header**: Name, location, email, phone, LinkedIn, portfolio URL
2. **Professional Summary**: 2–3 sentences tailored to the role. Mirror the posting's
   language and priorities. Do NOT use first person.
3. **Skills Section**: Reorganize skills to front-load those matching the posting.
   Group into relevant categories (e.g., "Game Engines & Frameworks", "Programming Languages",
   "Research & Analysis"). Only include skills from the master reference — never fabricate.
4. **Experience**: Select the most relevant positions. Rewrite bullets to:
   - Use action verbs matching the posting's language
   - Incorporate keywords naturally (not stuffed)
   - Quantify results where data exists in the master reference
   - Lead with the most relevant responsibilities
   - Never fabricate experience — only reframe what exists
5. **Education**: Include degrees, institutions, relevant coursework or honors
6. **Projects** (if relevant): Select portfolio projects that demonstrate required skills

**Page length**: Auto-decide based on relevance. Use one page if the relevant experience
fits cleanly; use two if there's substantial relevant experience that would be lost on one page.
Default to one page for junior/mid roles, allow two for senior/lead roles with 8+ years.

### Step 4: ATS Compliance Rules

- Use standard section headers: "Professional Summary", "Skills", "Experience", "Education", "Projects"
- No tables, columns, graphics, icons, or images
- No headers/footers (some ATS strip these)
- Use standard fonts (Helvetica, Arial equivalent)
- Use reverse chronological order within Experience
- Include exact keyword matches from the posting where truthful
- Use both spelled-out and abbreviated forms where relevant (e.g., "User Experience (UX)")
- Dates in consistent format: "Mon YYYY – Mon YYYY" or "Mon YYYY – Present"

### Step 5: Generate PDF

Use the script at `scripts/generate_resume_pdf.py`. Read `references/pdf_generation.md`
for the full ReportLab implementation details.

```bash
python scripts/generate_resume_pdf.py resume_data.json output.pdf
```

The script takes a JSON file containing the structured resume data and produces a clean PDF.

### Step 6: ATS Keyword Analysis

After generating the resume, produce a brief analysis in the conversation:

- **Match percentage**: (matched keywords / total posting keywords) x 100
- **Matched keywords**: List of posting keywords present in the resume
- **Missing keywords**: Posting keywords NOT in the resume, with notes on whether they
  could be honestly added or are genuinely outside the user's experience
- **Profile detected**: Which emphasis was chosen and why

## Important Rules

- **Never fabricate experience, skills, or qualifications.** Only reframe and emphasize
  what exists in the master reference.
- **Never copy job posting language verbatim into the summary.** Paraphrase naturally.
- **Always preserve truthfulness.** If the user lacks a required skill, note it in the
  ATS analysis rather than inventing it.
- **If asked for a cover letter**, generate one tailored to the same posting, but don't
  include one by default.

## File Structure

```
resume-tailor/
├── SKILL.md                          # This file
├── references/
│   ├── master_resume.md              # User's complete experience (user maintains)
│   └── pdf_generation.md             # ReportLab PDF implementation guide
├── scripts/
│   └── generate_resume_pdf.py        # PDF generation script
└── assets/
    └── (generated resumes go to /mnt/user-data/outputs/)
```
