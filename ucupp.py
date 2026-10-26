#!/usr/bin/env python3
"""
UCUPP - Ultimate Common User Passwords Profiler
An exhaustive password wordlist generator based on personal data, for
EXCLUSIVE use in your own cybersecurity labs (test virtual machines,
fictional users, authorized audits).

Unlike classic CUPP, this script DOES combine with each other:
  - base words (first name, surname, nickname, pet, child, partner, etc.)
  - their leetspeak variants
  - their casing variants (lowercase / Capitalized / UPPERCASE)
  - fragments of each date (day, month, full year, short year)
  - separators between word and number ("", "_", "-", ".")
  - optional special characters at the end

Usage:
    python3 ucupp.py
    (it will interactively ask you for the data, just like CUPP)

Repository: https://github.com/ivanvoit/ucupp
License: MIT
"""

import itertools
import sys

LEET_MAP = {
    "a": ["a", "4", "@"],
    "e": ["e", "3"],
    "i": ["i", "1", "!"],
    "o": ["o", "0"],
    "s": ["s", "5", "$"],
    "t": ["t", "7"],
}

SEPARATORS = ["", "_", "-", "."]
SPECIAL_CHARS = ["", "!", "#", "@", "*"]


def leet_variants(word, max_variants=64):
    """Generates leetspeak variants of a word, capping the amount so a long
    word with many substitutable letters doesn't explode combinatorially on
    its own."""
    word = word.lower()
    options_per_char = []
    for ch in word:
        options_per_char.append(LEET_MAP.get(ch, [ch]))

    variants = set()
    # full product of possible substitutions
    for combo in itertools.product(*options_per_char):
        variants.add("".join(combo))
        if len(variants) >= max_variants:
            break
    variants.add(word)  # make sure the original is always included
    return variants


def case_variants(word):
    """lowercase, Capitalized, UPPERCASE."""
    return {word.lower(), word.capitalize(), word.upper()}


def date_fragments(date_str):
    """date_str in DDMMYYYY format. Returns a list of useful fragments:
    dd, mm, yyyy, yy, ddmm, mmyyyy, yyyymmdd, etc."""
    if not date_str or len(date_str) != 8 or not date_str.isdigit():
        return []
    dd, mm, yyyy = date_str[0:2], date_str[2:4], date_str[4:8]
    yy = yyyy[2:4]
    frags = {dd, mm, yyyy, yy, dd + mm, mm + yyyy, mm + yy,
             dd + mm + yyyy, dd + mm + yy, yyyy + mm + dd}
    return [f for f in frags if f]


def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return ""


def collect_words():
    """Collects base words from the user (like CUPP, but you can add as
    many as you want)."""
    print("\n[+] Enter the target's information (leave blank if not applicable)\n")
    fields = {
        "First name": ask("> First name: "),
        "Surname": ask("> Surname: "),
        "Nickname": ask("> Nickname: "),
        "Pet": ask("> Pet's name: "),
        "Child": ask("> Child's name: "),
        "Partner": ask("> Partner's name: "),
        "Company": ask("> Company name: "),
    }
    extra = ask("> Extra keywords, comma-separated: ")
    extra_words = [w.strip() for w in extra.split(",") if w.strip()]

    words = [v for v in fields.values() if v] + extra_words
    return words


def collect_dates():
    print("\n[+] Dates (DDMMYYYY format, leave blank if not applicable)\n")
    dates = []
    for label in ["Target's birthdate", "Partner's birthdate", "Child's birthdate"]:
        d = ask(f"> {label}: ")
        if d:
            dates.append(d)
    return dates


def generate(words, dates, use_leet, use_numbers, max_total=800_000):
    all_words = set()

    # 1. Variants of each base word: lowercase/uppercase + optional leet
    base_variants = set()
    for w in words:
        for cw in case_variants(w):
            base_variants.add(cw)
        if use_leet:
            for lv in leet_variants(w):
                base_variants.add(lv)
                base_variants.add(lv.capitalize())
                base_variants.add(lv.upper())

    all_words |= base_variants

    # 2. Fragments of all dates
    date_frags = set()
    for d in dates:
        date_frags |= set(date_fragments(d))

    # 3. Combination word + separator + date_fragment (+ reversed order)
    combined = set()
    if use_numbers and date_frags:
        for w in base_variants:
            for sep in SEPARATORS:
                for frag in date_frags:
                    combined.add(f"{w}{sep}{frag}")
                    combined.add(f"{frag}{sep}{w}")
                    if len(combined) >= max_total:
                        break
                if len(combined) >= max_total:
                    break
            if len(combined) >= max_total:
                break

    all_words |= combined

    # 3b. Full-uppercase version of every combined word+date string (not
    # just the uppercase of the base word alone), so e.g. "john-1990"
    # also yields "JOHN-1990".
    upper_combined = set()
    if len(all_words) < max_total:
        for w in combined:
            upper_combined.add(w.upper())
            if len(all_words) + len(upper_combined) >= max_total:
                break

    all_words |= upper_combined

    # 4. Add a trailing special character on top of the already-combined
    # results (not just on standalone words), stopping once we hit the limit
    final_set = set(all_words)
    if len(final_set) < max_total:
        for w in list(all_words):
            for sc in SPECIAL_CHARS:
                if sc:
                    final_set.add(w + sc)
                if len(final_set) >= max_total:
                    break
            if len(final_set) >= max_total:
                break

    return final_set


def main():
    print("=" * 60)
    print(" UCUPP - Ultimate Common User Passwords Profiler")
    print(" FOR USE IN YOUR OWN TESTING LABS ONLY")
    print("=" * 60)

    words = collect_words()
    if not words:
        print("[-] No base words entered. Exiting.")
        sys.exit(1)

    dates = collect_dates()

    use_leet = ask("> Enable leetspeak? (Y/n): ").lower() != "n"
    use_numbers = ask("> Combine words with dates? (Y/n): ").lower() != "n"
    max_total_str = ask("> Maximum number of combinations [800000]: ")
    max_total = int(max_total_str) if max_total_str.isdigit() else 800_000

    print("\n[+] Generating combinations, this may take a few seconds...")
    result = generate(words, dates, use_leet, use_numbers, max_total)

    out_file = ask("> Output file name [ucupp_output.txt]: ") or "ucupp_output.txt"
    with open(out_file, "w") as f:
        for w in sorted(result):
            f.write(w + "\n")

    print(f"\n[+] Done. Generated {len(result)} combinations.")
    print(f"[+] Saved to: {out_file}")


if __name__ == "__main__":
    main()
