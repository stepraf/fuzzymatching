import streamlit as st
from rapidfuzz import fuzz, process


def render_fuzzy_matching_tab() -> None:
    """Render the original fuzzy matching UI as a tab, including configuration."""
    st.header("Fuzzy Matching")

    # Configuration section (moved from global sidebar into this tab)
    with st.expander("⚙️ Configuration", expanded=True):
        matching_method = st.selectbox(
            "Matching Method",
            [
                "ratio",
                "partial_ratio",
                "token_sort_ratio",
                "token_set_ratio",
                "partial_token_sort_ratio",
                "partial_token_set_ratio",
            ],
            index=5,
            help="Choose the fuzzy matching algorithm",
        )

        score_threshold = st.slider(
            "Minimum Score Threshold",
            min_value=0,
            max_value=100,
            value=70,
            help="Minimum similarity score (0-100) to consider a match",
        )

    col1, col2 = st.columns(2)

    with col1:
        query_strings = st.text_area(
            "First Text Box",
            placeholder="Enter values to match (one per line)...",
            height=200,
            help="Each line will be treated as a separate value to match",
        )

    with col2:
        reference_strings = st.text_area(
            "Second Text Box",
            placeholder="Enter reference values (one per line)...",
            height=200,
            help="Each line will be treated as a separate reference value",
        )

    if st.button("Find Matches", type="primary"):
        if query_strings and reference_strings:
            # Process each line as a separate value
            query_list = [
                line.strip()
                for line in query_strings.split("\n")
                if line.strip()
            ]
            ref_list = [
                line.strip()
                for line in reference_strings.split("\n")
                if line.strip()
            ]

            if not query_list:
                st.error("Please enter at least one value in the first text box")
            elif not ref_list:
                st.error("Please enter at least one value in the second text box")
            else:
                # Match each query value with the top 3 matches from reference values
                results_table = []

                for query in query_list:
                    # Find top 3 matches for this query
                    top_matches = process.extract(
                        query,
                        ref_list,
                        scorer=getattr(fuzz, matching_method),
                        limit=3,
                    )

                    # Normalize to 3 entries (fill with "-" if fewer matches are found)
                    top_matches_list = list(top_matches) if top_matches else []
                    while len(top_matches_list) < 3:
                        top_matches_list.append(("-", 0.0, None))

                    (
                        (best_val, best_score, _),
                        (second_val, second_score, _),
                        (third_val, third_score, _),
                    ) = top_matches_list[:3]

                    # Apply threshold filter - show "-" if score is below threshold
                    best_display = best_val if best_score >= score_threshold else "-"
                    best_prob = (
                        f"{best_score:.2f}%" if best_score >= score_threshold else "-"
                    )

                    second_display = (
                        second_val
                        if (second_val != "-" and second_score >= score_threshold)
                        else "-"
                    )
                    second_prob = (
                        f"{second_score:.2f}%"
                        if (second_val != "-" and second_score >= score_threshold)
                        else "-"
                    )

                    third_display = (
                        third_val
                        if (third_val != "-" and third_score >= score_threshold)
                        else "-"
                    )
                    third_prob = (
                        f"{third_score:.2f}%"
                        if (third_val != "-" and third_score >= score_threshold)
                        else "-"
                    )

                    results_table.append(
                        {
                            "Query Value": query,
                            "Best Match": best_display,
                            "Matching Probability": best_prob,
                            "2nd Best Match": second_display,
                            "2nd Best Match Probability": second_prob,
                            "3rd Best Match": third_display,
                            "3rd Best Match Probability": third_prob,
                        }
                    )

                # Display results in a table
                if results_table:
                    st.success(f"Matched {len(results_table)} value(s)")
                    st.dataframe(results_table, use_container_width=True, hide_index=True)
                else:
                    st.warning("No matches found")
        else:
            st.error("Please enter values in both text boxes")

    # Information section (only visible within the Fuzzy Matching tab)
    with st.expander("ℹ️ About Fuzzy Matching Methods"):
        st.markdown(
            """
        Here's a simple way to pick a method (with examples):

        - **Ratio (basic similarity)**: Compares letters in order. Good when strings are very similar.
          - Example: "John Smith" vs "John Smit" → high score.

        - **Partial Ratio (substring match)**: Looks for the best matching piece inside a longer string.
          - Example: "John Smith" vs "Mr. John Smith, Esq." → high score (because the full name appears inside the longer text).

        - **Token Sort Ratio (ignore word order)**: Splits into words, sorts them, then compares. Use when words may be rearranged.
          - Example: "Smith John" vs "John Smith" → high score.

        - **Token Set Ratio (ignore duplicates and extra words)**: Compares unique words and downplays extras. Use when one string has extra words.
          - Example: "John Smith" vs "John A. Smith" → high score.

        - **Partial Token Sort Ratio (substring + order-insensitive)**: Good when the correct words are present but mixed in a longer phrase.
          - Example: "John Smith" vs "Smith, John A." → high score.

        - **Partial Token Set Ratio (substring + unique words)**: Best when the match is a subset and there are many extra words.
          - Example: "Jane Doe" vs "Dr. Jane M. Doe, PhD" → very high score.

        Tips:
        - Start with **Token Set Ratio** for names and titles.
        - Use **Partial** versions when one side is much longer (e.g., includes prefixes/suffixes).
        - Raise the threshold if you want stricter matches (e.g., 85+).
        """
        )


