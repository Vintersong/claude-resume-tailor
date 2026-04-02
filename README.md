# 📄 claude-resume-tailor

> **A Claude skill that handles the work of tailoring resumes for ATS systems — so you don't have to.**

Stop manually rewriting your resume for every job posting. This skill lets Claude analyze any job description and produce a clean, keyword-optimized, ATS-compliant PDF resume — automatically — from a single master reference file you maintain once.

---

## What it does

- **Analyzes** a job posting for required skills, keywords, and role priorities
- **Selects and rewrites** the most relevant bullets from your experience without fabricating anything
- **Auto-detects** the best profile emphasis (engineering, game design, data analysis, UX research, etc.)
- **Generates** a clean, single-column ATS-compliant PDF using ReportLab
- **Reports** a keyword match analysis so you know exactly how well your resume fits

---

## What's in this repo

| File | Purpose |
|------|---------|
| `SKILL.md` | The Claude skill — instructions for analyzing a job post and tailoring a resume |
| `references/master_resume.md` | Template for your complete experience (fill this in once) |
| `references/pdf_generation.md` | ReportLab PDF layout and JSON schema reference |
| `scripts/generate_resume_pdf.py` | Python script that renders the tailored resume as a PDF |

---

## How it works

1. **Fill in** `references/master_resume.md` with your real experience (do this once)
2. **Paste a job posting** into your Claude conversation — URL, text, or uploaded file
3. **Claude tailors your resume**: selects relevant experience, mirrors the posting's language, front-loads matching skills
4. **Export** a clean ATS-friendly PDF via the included Python script

```bash
python scripts/generate_resume_pdf.py resume_data.json output.pdf
```

---

## Why ATS matters

Most large companies run resumes through Applicant Tracking Systems before a human ever sees them. If your resume doesn't contain the right keywords in the right format, it gets filtered out automatically — no matter how qualified you are.

This skill takes care of that busywork: keyword matching, section ordering, formatting rules, and clean output. You keep one honest master resume; Claude handles a tailored version for each role.

---

## Notes

- The included template is sanitized and contains **no personal information** — replace all placeholders before using it for a real application
- Claude will **never fabricate** experience, skills, or qualifications — only reframe and emphasize what's in your master reference
- This repo is meant to be **copied and adapted** to your own workflow

---

## 📜 License

MIT