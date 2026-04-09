#  Sentence Divider Simulator

> **CSE360 — Computer Architecture | Mini Project | Spring 2026**  
> A rule-based sentence boundary detection engine written in Python 3.

---

##  What is this?

This program reads a block of natural language text and **splits it into individual sentences** using a character-scanning engine with intelligent punctuation rules — similar to how a CPU's fetch unit identifies instruction boundaries in a binary data stream.

It goes beyond simple period-splitting by handling:
- Abbreviations like `Mr.` `Dr.` `Mrs.` `Prof.` (these do **not** trigger a split)
- Chained punctuation like `...` `!!!` `?!` (treated as one terminator)
- Decimal numbers like `3.14` (not split)
- Unterminated sentences (no `.` at the end — still captured)

---

##  Features

| Feature | Description |
|---|---|
|  Smart sentence splitting | Rule-based engine, not just `split('.')` |
|  Abbreviation detection | 38 known abbreviations skipped |
|  Statistics | Word count, char count, avg, longest, shortest |
|  Word frequency | Top 5 meaningful words with bar chart, stop-words filtered |
|  Report History | Every analysis auto-saved; re-read or export any time |
|  File input | Load `.txt` files directly |
|  Export | Save any report to a formatted `.txt` file |
|  Zero dependencies | Only Python standard library (`re`, `os`, `collections`, `datetime`) |

---

##  How to Run

```bash
# Python 3.6+ required — no pip installs needed
python3 sentence_divider.py
```

On Windows:
```bash
python sentence_divider.py
```

---

##  Menu Overview

```
==================================================================
            SENTENCE DIVIDER SIMULATOR  |  CSE360
==================================================================
   [1]  Enter text manually
   [2]  Load text from a file
   [3]  View Report History  [2 saved]
   [4]  About / How it works
   [5]  Exit
------------------------------------------------------------------
```

---

##  Sample Output

**Input:**
```
Dr. Smith is a professor at MIT. He teaches Computer Architecture
every semester! Have you attended his class? Students love it!
```

**Output:**
```
==================================================================
  No.    Sentence (preview)                            Words  Chars
------------------------------------------------------------------
  1      Dr. Smith is a professor at MIT.                  5     25
  2      He teaches Computer Architecture every seme...    7     43
  3      Have you attended his class?                      5     24
  4      Students love it!                                 3     15
==================================================================

  STATISTICS
------------------------------------------------------------------
  Total Sentences              : 4
  Total Words                  : 20
  Total Characters (no spaces) : 107
  Avg Words / Sentence         : 5.00
  Avg Characters / Sentence    : 26.75
------------------------------------------------------------------
  Longest  Sentence  → #2  (7 words)
  Shortest Sentence  → #4  (3 words)
------------------------------------------------------------------
  TOP 5 MOST FREQUENT MEANINGFUL WORDS:
    1. smith              █   1 time
    2. professor          █   1 time
    3. teaches            █   1 time
    4. architecture       █   1 time
    5. semester           █   1 time
==================================================================
  [+] Saved to history as Report #1
```

---

##  How the Engine Works

```
Input text
    │
    ▼
Character-by-character scan
    │
    ├── ch == '.'  →  is_abbreviation()?  ──YES──▶  skip, continue
    │                        │
    │                       NO
    │                        ▼
    ├── ch in '.!?' →  consume repeated punct. (... !!! ?!)
    │                        │
    │                        ▼
    │                  next char = space or end?
    │                        │
    │                  YES ──┤  flush buffer → sentence ✓
    │                        │
    │                   NO ──┤  keep scanning
    │
    └── end of string  →  save leftover buffer as final sentence
```

---

##  Report History

Every analysis is **automatically saved** to the session's Report History — no manual save prompt.

From menu `[3]` you can:
- Type a **number** to re-read any past report in full
- Type **E1**, **E2**, etc. to export that report to a `.txt` file
- Type **0** to return to the main menu

Exported files cannot be re-loaded as text input (protected by a file signature), preventing a bug where report formatting was parsed as sentences.

---

##  Project Structure

```
sentence_divider.py
│
├── Module 1 — Sentence Divider Engine    (divide_sentences, is_abbreviation)
├── Module 2 — Statistics Engine          (compute_statistics)
├── Module 3 — Word Frequency Analyzer    (top_words)
├── Module 4 — Display Engine             (display_report)
├── Module 5 — Report History             (view_report_history, export_report_to_file)
├── Module 6 — Analysis Pipeline          (run_analysis)
├── Module 7 — Input Handlers             (manual_input, file_input)
└── Module 8 — Main Menu                  (main)
```

---

##  Relation to Computer Architecture

| CPU Concept | Sentence Divider Analogy |
|---|---|
| Instruction Fetch Unit | Input handler reads a character stream |
| Instruction Decode | Engine decodes punctuation to find boundaries |
| Branch Prediction | Abbreviation check predicts if `.` ends a sentence |
| Pipeline Stages | Input → Scan → Split → Analyze → Display |
| Instruction Queue | Character accumulator buffer |

---

##  Bugs Fixed During Development

- **Stop words** in frequency results (`the`, `are`, `you`) — fixed with a 100-word STOP_WORDS set
- **"TOP 5" label** shown even when fewer words found — fixed with dynamic label
- **Longest = Shortest** printed twice for single-sentence input — suppressed for 1-sentence case
- **Loading `output.txt` as input** produced 10 fake sentences from 4 real ones — fixed with magic file signature

---

##  Requirements

- Python 3.6 or later
- No external packages required

---

**Author:** Md Ashikuzzaman, East West University 

##  License

This project was developed as a mini project for **CSE360 — Computer Architecture, Spring 2026**.  
Free to use for educational purposes.
