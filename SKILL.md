## Global Rules (apply to every step)

- **State tracking**: Before starting any step, check whether `session_state.json` exists and whether this step is already marked `"status": "done"`. If it is, skip directly to the next incomplete step — do NOT re-ask clarifying questions, re-parse the document, or regenerate outputs that already exist and are valid.
- After finishing each step, write/update `session_state.json`:
  ```json
  {"step": 2, "status": "done", "output_file": "outline.json", "notes": ""}
  ```
- **Never restart the whole pipeline** because a later step failed. If Step 4 fails, retry only Step 4 (or only the specific slide(s) affected) — never re-run Steps 1–3.
- **Schema compliance is mandatory.** Every generated JSON file must strictly match the schema defined in this document. If a generated file does not match, regenerate only that file — do not invent an alternate schema on the fly.
- If interrupted and resumed, always re-read `session_state.json` first before doing anything else.

---

## Step 1: Requirements Interview

Confirm the following before parsing documents (skip questions if already provided by the user):
- **Audience & Context**: Target audience and presentation setting.
- **Duration / Slide Count**: Target presentation length (time limit directly dictates slide budget and speaker note length).
- **Style & Branding**: Specific template, color palette, or corporate logo preferences.
- **Scope & Focus**: Essential chapters to include or skip.
- **Language**: Output language for slides and notes.

---

## Step 2: Document Parsing & Outline Generation

### Parsing
Extract content from `.docx` or `.pdf` files into `content_inventory.json`:
1. **Document Hierarchy**: Title/Heading tree.
2. **Key Findings**: Concise 1-2 sentence summaries per section.
3. **Metrics & Data**: Numerical values, trends, and context for chart generation.
4. **Embedded Assets**: For each embedded image, extract and store together in `content_inventory.json`:
   - `path`: the extracted image file's location.
   - `context`: the 1–2 sentences of text immediately before and after where the image appears in the source document.
   - `caption`: the document's own caption or alt-text for the image, if present; otherwise `null`.
   An image record with no `context` is not usable for matching in Step 3 — never store an image path without its surrounding text.
5. **Tables**: Select high-value summary points or full table structures.

### Outline Planning (`outline.json`)
Construct `outline.json` matching the exact layout rules below.

**Write incrementally and validate as you go:**
- First write `meta` plus slide 1 only. Immediately parse the file back (`json.load()` or equivalent) to confirm it is valid JSON.
- Then append remaining slides one at a time, or in small batches of 2–3. Re-validate after every write.
- If validation fails, regenerate ONLY the last chunk that was written — never discard and rewrite the entire file from scratch.
- Output must be pure JSON: no markdown code fences, no comments, no trailing prose, no non-JSON characters.

Layout options:

- **Cover Layouts (`cover_layout`)**: `CENTER_COVER`, `LEFT_FOCUS_COVER`, `BOTTOM_LEFT_COVER`
- **TOC Layouts (`toc_layout`)**: `SINGLE_COLUMN`, `TWO_COLUMN`
- **Content Layouts (`layout`)**:
  - `PROCESS_FLOW`: Sequential steps, workflows, or step-by-step guides.
  - `COMPARISON`: Pros/cons, side-by-side comparisons, or exactly 2 sections.
  - `DIGGING_DEEPER` / `DIGGING_DEEPER2`: Deep-dive analysis or root causes (2 or 3+ sections).
  - `EXECUTIVE_SUMMARY`: Key takeaways, conclusions, or executive summaries.
  - `TIMELINE`: Time series, milestones, or historical progress.
  - `THREE_COLUMN`: 3 distinct key points or topics.
  - `BIG_NUMBER`: Single key metric or high-impact data highlight.
  - `LEFT_NAV_THREE_INSIGHT`: 3 strategic insights with a left navigation line.
  - `LEFT_TEXT` / `RIGHT_TEXT`: Standard text page reserving 50% width for **Dual Visual Engines**.

#### Outline JSON Schema
```json
[
  {
    "title": "Presentation Title",
    "cover_layout": "CENTER_COVER",
    "toc_layout": "TWO_COLUMN",
    "layout": "LEFT_TEXT",
    "sections": [{"heading": "Subtitle", "content": "Presenter info"}]
  },
  {
    "title": "Agenda / Key Points",
    "layout": "THREE_COLUMN",
    "sections": [
      {"heading": "Point 1", "content": "Details 1"},
      {"heading": "Point 2", "content": "Details 2"},
      {"heading": "Point 3", "content": "Details 3"}
    ]
  }
]
```

---

## Step 3: Slide Generation & Dual Visual Engines (Template-Driven Execution)

CRITICAL DIRECTIVE: The `USER_DESIGNATED_TEMPLATE` is your Single Source of Truth (SSOT). Do NOT select arbitrary styles, invent speculative themes, or deviate from the template's design system. Slide generation must be orchestrated through the following Dual Visual Engines:

### [Prerequisite: Design Token Extraction]
Before emitting any slide code/content, extract and lock down the template’s core design tokens:
- **Color Palette**: Primary brand color, secondary/accent colors, background base (dark/light), card fill/surface color, border stroke color, and text hierarchy (`#text-primary`, `#text-muted`).
- **Typography**: Header font family, body font family, size scale, font weights, and line-height ratios.
- **Surface & Geometry**: Border radius values (`border-radius`), stroke widths, box shadows, and card background opacities.
- **Spatial Grid**: Slide safe margins, container gaps, and internal card padding.

---

### [Engine 1: Structural Grid & Boundary Engine]
Engine 1 governs geometry, containment, and 1:1 structural layout alignment:
- **Fixed Canvas Discipline**:
  - Enforce a strict 16:9 canvas ratio fixed at `1280px × 720px` with `overflow: hidden`. Elements must never clip or bleed outside the boundaries.
- **Layout Reproduction**:
  - Accurately reproduce the grid tracks, column proportions, and flex structures of the mapped template slide.
  - Maintain coordinate harmony: Header positions, subtitle offsets, and card gutters must mirror the template’s reference coordinates.
- **Container Boundary Guard**:
  - Dynamically balance content density. When mapping detailed content into fixed containers, refine phrasing or adjust font sizing to avoid text overflow or layout displacement.

---

### [Engine 2: Visual DNA & Component Sync Engine]
Engine 2 guarantees that every visual atom shares the exact cosmetic lineage of the template:
- **Card & Surface Inheritance**:
  - All cards, stat boxes, and content containers must directly adopt the template's background fill, border stroke, and border-radius tokens.
- **Icons, Badges & Accents**:
  - Icon backing plates, circular badges, status tags, and pill chips MUST use the accent palette and corner-radius rules defined in the template.
- **Charts & Data Visuals**:
  - Data visualizations (bars, lines, donuts, gauges) must strictly follow the template’s primary and secondary color sequence. Never fall back to default charting palettes or arbitrary neon contrasts.
- **SVG & Visual Assets**:
  - Visual connectors, milestone nodes, arrows, and dividers must reuse the exact stroke weights, dash patterns, and fill colors of the designated template.
- **Strict Anti-Drift Rule**:
  - Strictly prohibit injecting unstyled elements, conflicting gradients, or arbitrary decorative shapes that do not belong to the template's visual vocabulary.

---

## Step 4: Visual Review & Repair (Max 2 Rounds)

### Primary path (LibreOffice available)
1. **Image Conversion**: Convert `.pptx` to `.pdf` via LibreOffice headless, then render pages to `.png` images.
2. **Batch Inspection**: Combine up to 6 slide images into a single 2x3 contact sheet grid. Send the contact sheet to the vision LLM in one API call.
3. **Review Loop Rules**:
   - **Round 1**: Inspect all slides via contact sheets. Batch-fix all reported layout errors (text overflow, element overlap, image distortion).
   - **Round 2**: Re-render and inspect **ONLY** the slides modified in Round 1 using a single contact sheet.
   - **Halt**: Stop immediately after Round 2. Report any unresolvable issues to the user.

### Fallback path (LibreOffice/headless rendering unavailable)
1. Check for `soffice`/`libreoffice` availability first. If unavailable, do NOT invent an ad-hoc heuristic script on the spot.
2. Instead, run `scripts/layout_bounds_check.py <file.pptx> --json-out review_report.json` — a maintained, deterministic script (see Script References). It checks: shapes positioned off-slide, font sizes outside a readable range, estimated text overflow, and unexpected shape overlaps. It automatically excludes decorative hairlines and background-rectangle-vs-text containment from overlap findings, so those should not be re-flagged manually.
3. Fix any issues the script reports, then re-run it until `total_issue_count` is 0 or remaining issues are explicitly acknowledged as acceptable.
4. Explicitly tell the user that pixel-level visual review was skipped due to the missing rendering tool, and that only structural/geometric checks were performed — this is a lower bar than the primary path and should not be reported as equivalent.

---

## Step 5: Speaker Notes Generation

1. **Calculate Word Budget**: `max_words = duration_minutes * 200 * 0.9` (10% buffer for pacing/transitions). This is a **hard ceiling**, not a target — do not exceed it.
2. **Single Batch Request**: Extract all finalized slide titles and key points into a single prompt. Request a JSON array containing speaker notes for all slides simultaneously (`notes.json`), distributed proportionally to each slide's content weight.
3. **Enforce the ceiling**: After generation, count total words across all notes. If the total exceeds `max_words`, automatically trim before doing anything else — cut lower-priority sentences first (supporting details before core points), and always preserve the opening and closing. Do not ask the user to accept an over-length draft; deliver a version that already fits.
4. **Apply Notes**: Write the generated notes into slide note frames (`slide.notes_slide.notes_text_frame.text`) programmatically.
5. Report the final estimated speaking time to the user so they know it's within the requested budget.

---

## Script References

- `references/outline_schema.md`: Complete JSON structure definitions.
- `references/visual_review_checklist.md`: Visual inspection rules (primary/LibreOffice path).
- `scripts/extract_docs.py`: Document parsing utility. Also responsible for capturing each embedded image's surrounding text (`context`) and native caption (`caption`) during Step 2 parsing, so Asset Matching in Step 3 has something to judge against.
- `scripts/pptx_to_images.py`: PPTX-to-PNG rendering helper.
- `scripts/add_speaker_notes.py`: Programmatic speaker notes injection script.
- `scripts/layout_bounds_check.py`: Deterministic structural QA fallback for Step 4 when LibreOffice is unavailable.

## Development Notes

This section is used for development notes.