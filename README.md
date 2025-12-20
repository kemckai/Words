# Word of the Day

A simple desktop application for macOS that displays a word of the day in a transparent overlay window. The app automatically refreshes every 24 hours with a new word and definition.

## Features

- **Daily Word Display**: Shows a word and its definition in a small window
- **40% Opacity**: Window is semi-transparent (60% transparent) to reduce visual distraction
- **Automatic Refresh**: Automatically updates with a new word every 24 hours at midnight
- **Error Recovery**: Automatically retries with new random words if errors occur
- **Deterministic Selection**: Same word is shown throughout the day (based on current date)
- **Persistent Window**: Runs continuously, refreshing automatically

## Requirements

- macOS
- Python 3.11 with Tkinter support (Homebrew Python 3.11 recommended)
- `Words_alphabetized.txt` file containing word-definition pairs

## Installation

1. Ensure you have Python 3.11 with Tkinter installed. If using Homebrew:
   ```bash
   brew install python@3.11
   ```

2. Clone or download this repository

3. Ensure `Words_alphabetized.txt` is in the same directory as `word_of_the_day.py`

## Usage

### Running the Application

**Option 1: Using the launcher script (recommended)**
```bash
./WordOfTheDay.command
```

**Option 2: Running directly with Python**
```bash
python3.11 word_of_the_day.py
```

The window will appear in the top-left corner of your screen with the current day's word.

### Window Behavior

- The window displays near the top-left of the screen (offset 20px from left, 40px from top)
- Window is set to 40% opacity (60% transparent) for minimal visual distraction
- Window automatically updates at midnight with a new word
- Closing the window exits the application

## File Format

The `Words_alphabetized.txt` file should contain word-definition pairs, one per line, in the format:

```
word - definition
```

Example:
```
serendipity - the occurrence and development of events by chance in a happy or beneficial way
ephemeral - lasting for a very short time
```

## How It Works

1. **Word Selection**: Uses the current date to deterministically select a word, ensuring the same word is shown all day
2. **Refresh Mechanism**: Calculates time until next midnight and schedules automatic refresh
3. **Error Handling**: If word loading fails, the app retries up to 10 times with random offsets to select different words
4. **Window Updates**: Updates the existing window labels instead of creating new windows

## Technical Details

- Built with Python 3.11 and Tkinter
- Uses SHA-256 hashing for deterministic word selection
- Window transparency achieved via macOS `-alpha` attribute
- Scheduled refreshes using Tkinter's `after()` method

## License

This project is provided as-is for personal use.

