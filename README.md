# Rafal's Fuzzy Matching Tool

A web-based fuzzy matching tool built with Streamlit and RapidFuzz for finding similar strings using various fuzzy matching algorithms.

## Features

- **Line-by-Line Matching**: Match each line from the first text box against all lines in the second text box
- **Top 3 Matches**: View the best match, 2nd best match, and 3rd best match for each query value
- **Detailed Results Table**: See matching values and their probability scores in separate columns
- **Multiple Algorithms**: Support for 6 different fuzzy matching methods:
  - Ratio (standard Levenshtein distance)
  - Partial Ratio (best substring match)
  - Token Sort Ratio
  - Token Set Ratio
  - Partial Token Sort Ratio
  - Partial Token Set Ratio (default)
- **Configurable Threshold**: Set minimum similarity score (0-100) to filter matches
- **Interactive UI**: Clean, user-friendly interface with real-time results

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

3. Use the tool:
   - **First Text Box**: Enter values to match (one per line)
   - **Second Text Box**: Enter reference values to match against (one per line)
   - Click "Find Matches" to see results

4. View the results table with columns:
   - **Query Value**: The value from the first text box
   - **Best Match**: The best matching value from the second text box
   - **Matching Probability**: Similarity score for the best match
   - **2nd Best Match**: The second best matching value
   - **2nd Best Match Probability**: Similarity score for the 2nd best match
   - **3rd Best Match**: The third best matching value
   - **3rd Best Match Probability**: Similarity score for the 3rd best match

## Configuration

Use the sidebar to configure:
- **Matching Method**: Choose the fuzzy matching algorithm (default: Partial Token Set Ratio)
- **Minimum Score Threshold**: Set the minimum similarity score (0-100) - matches below this threshold will show as "-"

## Example

**First Text Box:**
```
John Smith
Jane Doe
Bob Johnson
```

**Second Text Box:**
```
John A. Smith
Johnny Smith
J. Smith
Jane D. Doe
J. Doe
Robert Johnson
Bob J. Johnson
```

The tool will match each line from the first box against all lines in the second box and display the top 3 matches with their probability scores.

## Requirements

- Python 3.7+
- streamlit >= 1.28.0
- rapidfuzz >= 3.0.0

## License

This project is open source and available for use.
