#!/usr/bin/env python3
"""
Simple "Word of the Day" desktop sticky for macOS.

Reads from Words_alphabetized.txt, picks a stable pseudo-random word+definition
for the current day, and shows it in a small black-on-white window near the
top-left of the screen.
"""

import datetime as _dt
import hashlib
import os
import tkinter as tk
from tkinter import font as tkfont
from typing import List, Tuple


WORDS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Words_alphabetized.txt",
)


def load_words(path: str) -> List[Tuple[str, str]]:
    """Load (word, definition) pairs from the given file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Words file not found: {path}")

    pairs: List[Tuple[str, str]] = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            # Expect \"Word - definition\"; split only on first hyphen.
            # Support a few common variants with spaces around the dash.
            sep = " - "
            if sep in line:
                word, definition = line.split(sep, 1)
            else:
                # Fallback: split on first '-' if no spaced dash
                if "-" in line:
                    word, definition = line.split("-", 1)
                else:
                    # Can't parse this line, skip it
                    continue

            word = word.strip()
            definition = definition.strip()

            # Basic validation to avoid junk entries
            if not word or not definition:
                continue
            if len(word) > 80:
                continue
            pairs.append((word, definition))

    if not pairs:
        raise ValueError(f"No valid word/definition pairs found in {path}")
    return pairs


def pick_word_for_today(pairs: List[Tuple[str, str]]) -> Tuple[str, str]:
    """
    Deterministically pick a 'random' word for today.
    
    Uses the current date as a seed, so the same word is shown all day,
    and a new random word is selected every 24 hours (at midnight).

    If a chosen entry fails validation/display prep, we advance to a new
    candidate (by tweaking the hash input) up to a reasonable attempt limit.
    """
    today = _dt.date.today().isoformat()
    n = len(pairs)

    def index_for_attempt(attempt: int) -> int:
        key = f"{today}:{attempt}".encode("utf-8")
        h = hashlib.sha256(key).hexdigest()
        return int(h, 16) % n

    # Try several candidates in case any particular line is malformed in practice
    max_attempts = min(50, n)
    last_error: Exception | None = None

    for attempt in range(max_attempts):
        try:
            idx = index_for_attempt(attempt)
            word, definition = pairs[idx]

            # Extra sanity checks before returning
            if not word or not definition:
                raise ValueError("Empty word or definition")
            if len(definition) < 3:
                raise ValueError("Definition too short")
            return word, definition
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            continue

    # If we get here, everything failed; raise a descriptive error
    raise RuntimeError(f"Unable to select a valid word for today: {last_error}")


def create_window(word: str, definition: str) -> None:
    """Create and display the tkinter window with the given word and definition."""
    root = tk.Tk()
    root.title("Word of the Day")

    # Appearance: black background, white text
    bg_color = "#000000"
    fg_color = "#FFFFFF"
    root.configure(bg=bg_color)

    # Disable resizing
    root.resizable(False, False)

    # Fonts: word a bit larger and bold, definition slightly smaller
    word_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
    def_font = tkfont.Font(family="Helvetica", size=14)

    # Outer padding to avoid hugging screen edges
    pad_x = 16
    pad_y = 12

    container = tk.Frame(root, bg=bg_color)
    container.pack(fill="both", expand=True, padx=pad_x, pady=pad_y)

    word_label = tk.Label(
        container,
        text=word,
        font=word_font,
        fg=fg_color,
        bg=bg_color,
        anchor="w",
        justify="left",
        wraplength=400,
    )
    word_label.pack(anchor="w")

    definition_label = tk.Label(
        container,
        text=definition,
        font=def_font,
        fg=fg_color,
        bg=bg_color,
        anchor="w",
        justify="left",
        wraplength=400,
    )
    definition_label.pack(anchor="w", pady=(8, 0))

    # Let tkinter compute size, then move window near top-left
    root.update_idletasks()

    width = root.winfo_width()
    height = root.winfo_height()

    # Offset in from absolute top-left to avoid menu bar and hard edge
    x_offset = 20
    y_offset = 40
    geometry = f"{width}x{height}+{x_offset}+{y_offset}"
    root.geometry(geometry)

    root.mainloop()


def create_error_window(message: str) -> None:
    """Show a simple window explaining that the word couldn't be loaded."""
    root = tk.Tk()
    root.title("Word of the Day — Error")
    bg_color = "#000000"
    fg_color = "#FFFFFF"
    root.configure(bg=bg_color)
    root.resizable(False, False)

    msg_font = tkfont.Font(family="Helvetica", size=14)

    label = tk.Label(
        root,
        text=message,
        font=msg_font,
        fg=fg_color,
        bg=bg_color,
        anchor="w",
        justify="left",
        wraplength=420,
    )
    label.pack(padx=16, pady=16)

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x_offset = 20
    y_offset = 40
    geometry = f"{width}x{height}+{x_offset}+{y_offset}"
    root.geometry(geometry)

    root.mainloop()


def main() -> None:
    try:
        pairs = load_words(WORDS_FILE)
        word, definition = pick_word_for_today(pairs)
        create_window(word, definition)
    except Exception as exc:  # noqa: BLE001
        # If anything goes wrong, show an explanatory error card instead of crashing.
        error_msg = f"Unable to load today's word:\n{exc}"
        create_error_window(error_msg)


if __name__ == "__main__":
    # Explicitly use the script's directory as cwd, so relative paths behave.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()


