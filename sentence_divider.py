# ================================================================
#   MINI PROJECT: SENTENCE DIVIDER SIMULATOR
#   Course      : Computer Architecture (CSE360), Section-1
#   Semester    : Spring 2026
#   Language    : Python 3
# ================================================================

import re
import os
from datetime import datetime
from collections import Counter

# ----------------------------------------------------------------
LINE = "=" * 66
DASH = "-" * 66

OUTPUT_SIGNATURE = "##SDIVIDER_OUTPUT##"

# Every completed analysis is stored here automatically
REPORT_HISTORY = []

# ----------------------------------------------------------------
ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "ave",
    "blvd", "dept", "est", "fig", "govt", "inc", "ltd", "max",
    "min", "no",  "jan", "feb", "mar", "apr", "jun", "jul",
    "aug", "sep", "oct", "nov", "dec", "vs",  "etc", "eg",
    "ie",  "approx", "corp", "rev", "gen", "sgt", "capt", "lt",
    "mt",  "rd",  "sq",  "vol", "pp",  "ed",  "tr",  "assoc"
}

STOP_WORDS = {
    "the", "and", "for", "are", "but", "not", "you", "all",
    "can", "had", "her", "was", "one", "our", "out", "who",
    "get", "his", "him", "has", "how", "its", "did", "she",
    "now", "may", "any", "two", "say", "use", "way", "new",
    "old", "day", "man", "see", "too", "own", "off", "let",
    "put", "end", "why", "set", "try", "big", "few", "ran",
    "got", "yes", "yet", "ago", "due", "via", "per", "such",
    "then", "than", "from", "that", "this", "they", "have",
    "with", "will", "been", "more", "also", "into", "when",
    "what", "some", "your", "time", "very", "each", "just",
    "over", "come", "even", "here", "much", "only", "both",
    "well", "does", "down", "said", "like", "long", "make",
    "know", "take", "year", "good", "back", "give", "most",
    "tell", "same", "look", "many", "want", "show", "last",
    "form", "part", "need", "help", "find", "high", "keep",
    "seem", "next", "hard", "open", "real", "sure", "feel",
    "kind", "live", "call", "left", "hold", "went", "came",
    "made", "used", "must", "were", "once", "could", "would",
    "there", "their", "about", "after", "other", "those",
    "these", "where", "which", "while", "never", "every",
    "first", "still", "being", "doing", "going", "think",
    "asked", "again", "might", "shall", "since", "until",
    "under", "quite", "often", "along", "among", "later",
    "above", "below", "role", "even", "just", "very"
}


# ================================================================
#  MODULE 1 — SENTENCE DIVIDER ENGINE
# ================================================================

def is_abbreviation(text, dot_pos):
    start = dot_pos - 1
    while start > 0 and text[start - 1].isalpha():
        start -= 1
    return text[start:dot_pos].lower() in ABBREVIATIONS


def divide_sentences(text):
    sentences, buffer, i, n = [], [], 0, len(text)
    while i < n:
        ch = text[i]
        buffer.append(ch)
        if ch in ".!?":
            if ch == "." and is_abbreviation(text, i):
                i += 1
                continue
            while i + 1 < n and text[i + 1] in ".!?":
                i += 1
                buffer.append(text[i])
            next_i = i + 1
            if next_i >= n or text[next_i].isspace():
                sentence = "".join(buffer).strip()
                if sentence:
                    sentences.append(sentence)
                buffer = []
                while i + 1 < n and text[i + 1].isspace():
                    i += 1
        i += 1
    leftover = "".join(buffer).strip()
    if leftover:
        sentences.append(leftover)
    return sentences


# ================================================================
#  MODULE 2 — STATISTICS ENGINE
# ================================================================

def compute_statistics(sentences):
    if not sentences:
        return {}
    wc = [len(s.split()) for s in sentences]
    cc = [sum(1 for c in s if not c.isspace()) for s in sentences]
    return {
        "total_sentences" : len(sentences),
        "total_words"     : sum(wc),
        "total_chars"     : sum(cc),
        "avg_words"       : sum(wc) / len(sentences),
        "avg_chars"       : sum(cc) / len(sentences),
        "longest_idx"     : wc.index(max(wc)),
        "shortest_idx"    : wc.index(min(wc)),
        "word_counts"     : wc,
        "char_counts"     : cc,
    }


# ================================================================
#  MODULE 3 — WORD FREQUENCY ANALYZER
# ================================================================

def top_words(text, n=5):
    words    = re.findall(r"[a-zA-Z]+", text.lower())
    filtered = [w for w in words if len(w) >= 4 and w not in STOP_WORDS]
    return Counter(filtered).most_common(n)


# ================================================================
#  MODULE 4 — DISPLAY ENGINE
# ================================================================

def display_report(report):
    sentences = report["sentences"]
    stats     = report["stats"]
    freq      = report["freq"]

    if not sentences:
        print("\n  [!] No sentences found.\n")
        return

    print()
    print(LINE)
    print(f"  Report  : {report['title']}")
    print(f"  Time    : {report['timestamp']}")
    print(LINE)
    print(f"  {'No.':<5}  {'Sentence (preview)':<44}  {'Words':>5}  {'Chars':>5}")
    print(DASH)
    for i, sent in enumerate(sentences):
        preview = (sent[:43] + "...") if len(sent) > 46 else sent
        print(f"  {i+1:<5}  {preview:<44}  {stats['word_counts'][i]:>5}  {stats['char_counts'][i]:>5}")
    print(LINE)

    print(f"\n  {'STATISTICS':^62}")
    print(DASH)
    print(f"  {'Total Sentences':<28} : {stats['total_sentences']}")
    print(f"  {'Total Words':<28} : {stats['total_words']}")
    print(f"  {'Total Characters (no spaces)':<28} : {stats['total_chars']}")
    print(f"  {'Avg Words / Sentence':<28} : {stats['avg_words']:.2f}")
    print(f"  {'Avg Characters / Sentence':<28} : {stats['avg_chars']:.2f}")

    if stats["total_sentences"] > 1:
        li, si = stats["longest_idx"], stats["shortest_idx"]
        print(DASH)
        print(f"  Longest  Sentence  → {li+1}  ({stats['word_counts'][li]} words)")
        print(f"    \"{sentences[li]}\"")
        print()
        print(f"  Shortest Sentence  → {si+1}  ({stats['word_counts'][si]} words)")
        print(f"    \"{sentences[si]}\"")

    print(DASH)
    if not freq:
        print("  No significant words found.")
    else:
        lbl = f"TOP {len(freq)}" if len(freq) < 5 else "TOP 5"
        print(f"  {lbl} MOST FREQUENT MEANINGFUL WORDS:")
        for rank, (word, count) in enumerate(freq, 1):
            bar   = "█" * min(count, 20)
            times = "time" if count == 1 else "times"
            print(f"    {rank}. {word:<18} {bar:<20} {count} {times}")
    print(LINE)


# ================================================================
#  MODULE 5 — REPORT HISTORY MENU  
# ================================================================

def make_title(text):
    words = text.split()[:6]
    title = " ".join(words)
    return (title + "...") if len(text.split()) > 6 else title


def export_report_to_file(report, filename=None):
    """Write one report to a .txt file that cannot be re-loaded as input."""
    if not filename:
        safe     = re.sub(r"[^\w\s-]", "", report["title"])
        safe     = re.sub(r"\s+", "_", safe.strip())[:30]
        filename = f"report_{safe}.txt"

    try:
        s = report["stats"]
        with open(filename, "w", encoding="utf-8") as f:
            f.write("  ORIGINAL TEXT:\n")
            preview = report['text'][:200] + "..." if len(report['text']) > 200 else report['text']
            f.write(f"  {preview}\n\n")
            f.write("-" * 50 + "\n")
            f.write("  SENTENCES:\n\n")
            for i, sent in enumerate(report["sentences"]):
                f.write(f"  [{i+1}]  {s['word_counts'][i]} words  |  {s['char_counts'][i]} chars\n")
                f.write(f"       {sent}\n\n")
            f.write("-" * 50 + "\n")
            f.write("  STATISTICS:\n\n")
            f.write(f"  Total Sentences  : {s['total_sentences']}\n")
            f.write(f"  Total Words      : {s['total_words']}\n")
            f.write(f"  Total Characters : {s['total_chars']}\n")
            f.write(f"  Avg Words/Sent   : {s['avg_words']:.2f}\n\n")
            f.write("  TOP WORDS:\n")
            for rank, (word, count) in enumerate(report["freq"], 1):
                f.write(f"  {rank}. {word}  ({count}x)\n")
            f.write("\n" + "=" * 50 + "\n")
        print(f"\n  [OK] Exported  →  '{filename}'")
    except IOError as e:
        print(f"\n  [ERROR] {e}")


def view_report_history():
    """
    Dedicated Report History screen.
    Lists all reports saved this session.
    User can re-read any report or export it to a file.
    """
    while True:
        print()
        print(LINE)
        print(f"  {'R E P O R T   H I S T O R Y':^62}")
        print(DASH)

        if not REPORT_HISTORY:
            print()
            print("  No reports yet.")
            print("  Go to [1] or [2] from the main menu to analyse text.")
            print()
            print(DASH)
            input("  Press Enter to return to main menu...")
            return

        for i, r in enumerate(REPORT_HISTORY):
            sc = r["stats"]["total_sentences"]
            wc = r["stats"]["total_words"]
            print(f"  [{i+1}]  {r['title']}")
            print(f"        {r['timestamp']}  "
                  f"|  {sc} sentence{'s' if sc!=1 else ''}  "
                  f"|  {wc} words")
            print()

        print(DASH)
        print("  Enter a number    → view that report in full")
        print("  Enter E<number>   → export to .txt file  (e.g. E2)")
        print("  Enter 0           → back to main menu")
        print(DASH)

        try:
            raw = input("  Your choice: ").strip().lower()
        except EOFError:
            return

        # back to main menu
        if raw == "0":
            return

        # export:  e1 / e2 / e3
        if raw.startswith("e") and raw[1:].isdigit():
            idx = int(raw[1:]) - 1
            if 0 <= idx < len(REPORT_HISTORY):
                fname = input("  Filename (press Enter for auto-name): ").strip()
                export_report_to_file(REPORT_HISTORY[idx], fname or None)
                input("\n  Press Enter to continue...")
            else:
                print(f"\n  [!] Report #{raw[1:]} does not exist.")
            continue

        # view report by number
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(REPORT_HISTORY):
                display_report(REPORT_HISTORY[idx])
                input("\n  Press Enter to return to history...")
            else:
                print(f"\n  [!] Report #{raw} does not exist.")
            continue

        print("  [!] Invalid input.")


# ================================================================
#  MODULE 6 — ANALYSIS PIPELINE
# ================================================================

def run_analysis(text):
    print(f"\n  [OK] Processing  ({len(text)} characters)...")

    sentences = divide_sentences(text)
    if not sentences:
        print("\n  [!] No sentences found.")
        return

    stats  = compute_statistics(sentences)
    freq   = top_words(text)
    report = {
        "title"     : make_title(text),
        "timestamp" : datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),
        "text"      : text,
        "sentences" : sentences,
        "stats"     : stats,
        "freq"      : freq,
    }

    display_report(report)

    # Auto-save to history — no prompt needed
    REPORT_HISTORY.append(report)
    n = len(REPORT_HISTORY)
    print(f"  [+] Saved to history as Report #{n}  "
          f"(view / export from main menu [3])")


# ================================================================
#  MODULE 7 — INPUT HANDLERS
# ================================================================

def manual_input():
    print()
    print(DASH)
    print("  Enter your paragraph below.")
    print("  Press Enter on a BLANK LINE when you are done.")
    print(DASH)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    text = " ".join(lines).strip()
    if not text:
        print("\n  [!] No input. Returning to menu.")
        return
    run_analysis(text)


def file_input():
    filename = input("\n  Enter filename (e.g., input.txt): ").strip()
    if not filename:
        print("\n  [!] No filename entered.")
        return
    if not os.path.isfile(filename):
        print(f"\n  [ERROR] File not found: '{filename}'")
        return
    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw = f.read()
    except UnicodeDecodeError:
        try:
            with open(filename, "r", encoding="latin-1") as f:
                raw = f.read()
        except Exception as e:
            print(f"\n  [ERROR] {e}")
            return
    except Exception as e:
        print(f"\n  [ERROR] {e}")
        return

    if raw.startswith(OUTPUT_SIGNATURE):
        print(f"\n  [ERROR] '{filename}' is a saved report file,")
        print( "          not a text input file.")
        print( "  View saved reports from main menu [3].")
        return

    text = raw.strip()
    if not text:
        print("\n  [!] File is empty.")
        return
    print(f"\n  [OK] Loaded: '{filename}'  ({len(text)} characters)")
    run_analysis(text)


# ================================================================
#  MODULE 8 — ABOUT SCREEN
# ================================================================

def show_about():
    print()
    print(LINE)
    print(f"  {'ABOUT THIS PROJECT':^62}")
    print(LINE)
    print("  Project   : Sentence Divider Simulator")
    print("  Course    : CSE360 — Computer Architecture")
    print("  Section   : 1  |  Semester : Spring 2026")
    print("  Language  : Python 3")
    print(DASH)
    print("  HOW IT WORKS\n")
    print("  Scans a character stream to detect sentence boundaries,")
    print("  like a CPU fetch unit identifying instruction boundaries")
    print("  in a binary data stream.\n")
    print("  SPLITTING RULES:")
    print("    Terminators    :  .  !  ?")
    print("    Abbreviations  :  Mr. Dr. Mrs. Prof. — SKIPPED")
    print("    Chained punct. :  ...  !!!  ?!  — one terminator")
    print("    Decimal nums   :  3.14, 99.5 — not split")
    print("    Unterminated   :  last sentence saved without .\n")
    print("  HISTORY & EXPORT:")
    print("    Every analysis is auto-saved to Report History.")
    print("    Use menu [3] to re-read or export any report.")
    print(LINE)


# ================================================================
#  MAIN MENU
# ================================================================

def main():
    print()
    print(LINE)
    print(f"  {'SENTENCE DIVIDER SIMULATOR':^62}")
    print(LINE)

    while True:
        count = len(REPORT_HISTORY)
        hist  = f"View Report History  [{count} saved]" if count else "View Report History  [empty]"

        print("\n \n")
        print(f"  {'M A I N   M E N U':^62}")
        print(DASH)
        print("   [1]  Enter text manually")
        print("   [2]  Load text from a file")
        print(f"   [3]  {hist}")
        print("   [4]  About / How it works")
        print("   [5]  Exit")
        print(DASH)

        try:
            choice = input("   Choose (1-5): ").strip()
        except EOFError:
            break

        if   choice == "1": manual_input()
        elif choice == "2": file_input()
        elif choice == "3": view_report_history()
        elif choice == "4": show_about()
        elif choice == "5":
            print()
            print(LINE)
            print(f"  {'Thank you! Goodbye.':^62}")
            print(LINE)
            print()
            break
        else:
            print(f"  [!] Invalid choice. Enter 1 – 5.")


if __name__ == "__main__":
    main()
