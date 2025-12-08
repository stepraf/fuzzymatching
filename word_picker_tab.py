import streamlit as st
import pandas as pd
import re
from collections import defaultdict


def _remove_bracketed_content(text: str) -> str:
    """Remove content inside (), [] or {} (including the brackets themselves)."""
    # Remove (...) content
    text = re.sub(r"\([^)]*\)", "", text)
    # Remove [...] content
    text = re.sub(r"\[[^]]*\]", "", text)
    # Remove {...} content
    text = re.sub(r"\{[^}]*\}", "", text)
    return text


def _has_letter_and_number(text: str) -> bool:
    """Return True if text contains at least one letter and at least one digit."""
    has_alpha = any(ch.isalpha() for ch in text)
    has_digit = any(ch.isdigit() for ch in text)
    return has_alpha and has_digit


def render_word_picker_tab() -> None:
    """Render the Word Picker tab."""
    st.header("Word Picker")

    col1, col2 = st.columns(2)

    with col1:
        raw_strings_to_search_for = st.text_area(
            "Strings to search for",
            placeholder="Enter strings to search for (one per line)...",
            height=200,
            help="Each line will become a row in the 'strings_to_search_for' dataframe.",
        )

    with col2:
        raw_data_to_search = st.text_area(
            "Data to search",
            placeholder="Enter data to search (one line per row)...",
            height=200,
            help="Each line will become a row in the 'data_to_search' dataframe.",
        )

    keep_alphanumeric_only = st.checkbox(
        "Keep only strings that contain both letters and numbers (for matching)",
        value=False,
        help=(
            "When enabled, only tokens that contain at least one letter and at least one "
            "number will be used for matching."
        ),
    )

    if st.button("Run Word Picker", type="primary"):
        if not raw_strings_to_search_for:
            st.error("Please enter at least one line in 'Strings to search for'.")
            return

        if not raw_data_to_search:
            st.error("Please enter at least one line in 'Data to search'.")
            return

        # Build base dataframes (one column each, one row per input line)
        strings_to_search_for = pd.DataFrame(
            [
                line.strip()
                for line in raw_strings_to_search_for.split("\n")
                if line.strip()
            ],
            columns=["string"],
        )

        data_to_search = pd.DataFrame(
            [line.strip() for line in raw_data_to_search.split("\n") if line.strip()],
            columns=["data"],
        )

        # Expand strings_to_search_for into individual "words"/tokens
        # - First remove any content inside brackets () [] {}.
        # - Then replace commas with spaces.
        # - Then treat whitespace-separated tokens as individual strings.
        # - Optionally keep only tokens that contain both letters and numbers.
        # - Finally, remove tokens shorter than 4 characters before searching.
        # We also prepare a mapping from each token to all original source rows that contain it.
        expanded_tokens = []
        token_sources: dict[str, list[str]] = defaultdict(list)
        for value in strings_to_search_for["string"]:
            cleaned_value = _remove_bracketed_content(value)
            cleaned_value = cleaned_value.replace(",", " ")
            for token in cleaned_value.split():
                token_clean = token.strip()
                if not token_clean:
                    continue
                if keep_alphanumeric_only and not _has_letter_and_number(token_clean):
                    continue
                if len(token_clean) >= 4:
                    expanded_tokens.append(token_clean)
                    token_sources[token_clean.lower()].append(value)

        if not expanded_tokens:
            st.warning(
                "No valid tokens remained after cleaning (bracket removal, comma handling, "
                "length filter, and optional letter+number filter). Nothing to match."
            )
            return

        # Unique list of tokens for the expanded dataframe
        strings_to_search_for_expanded = pd.DataFrame(
            sorted(set(expanded_tokens)), columns=["string"]
        )

        # Perform case-insensitive substring matching
        matches = []
        for data_value in data_to_search["data"]:
            data_lower = data_value.lower()
            for token in strings_to_search_for_expanded["string"]:
                token_lower = token.lower()
                if token_lower in data_lower:
                    # Rematch this token against all original rows that contained it
                    for source_string in token_sources.get(token_lower, []):
                        matches.append(
                            {
                                "data_to_search": data_value,
                                "matched_string": token,
                                "source_string": source_string,
                            }
                        )

        if matches:
            result_df = pd.DataFrame(matches)
            st.success(
                f"Found {len(result_df)} match(es) across "
                f"{data_to_search.shape[0]} row(s) of data."
            )

            # Show the intermediate dataframes if helpful
            with st.expander("Show intermediate dataframes"):
                st.subheader("strings_to_search_for")
                st.dataframe(strings_to_search_for, use_container_width=True, hide_index=True)

                st.subheader("strings_to_search_for_expanded")
                st.dataframe(
                    strings_to_search_for_expanded,
                    use_container_width=True,
                    hide_index=True,
                )

                st.subheader("data_to_search")
                st.dataframe(data_to_search, use_container_width=True, hide_index=True)

            st.subheader("Matched Rows")
            st.dataframe(result_df, use_container_width=True, hide_index=True)
        else:
            st.warning(
                "No rows in 'Data to search' contain any of the strings from "
                "'strings_to_search_for_expanded' (case-insensitive, substring match)."
            )


