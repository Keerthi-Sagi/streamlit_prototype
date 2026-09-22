import streamlit as st
import pandas as pd
import pycountry
import plotly.express as px
import plotly.express as px
from urllib.parse import quote, unquote


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IS Journals Research Analytics",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================

# GLOBAL DESIGN / CSS
st.markdown("""

<style>

/* APP */

.block-container {

    max-width: 1450px;
    padding-top: 4.5rem !important;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;

}

/* TYPOGRAPHY */
h1 {
    font-size: 2.15rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em;

}
h2 {

    font-size: 1.55rem !important;
    font-weight: 650 !important;

}

h3 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;

}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.15);

}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* METRIC CARDS */
div[data-testid="stMetric"] {
    background: rgba(128,128,128,0.055);
    border: 1px solid rgba(128,128,128,0.14);
    border-radius: 12px;
    padding: 18px 20px;

}

div[data-testid="stMetricLabel"] {
    font-size: 0.85rem;
}

div[data-testid="stMetricValue"] {
    font-size: 1.75rem;
    font-weight: 650;
}

/* INPUTS */

div[data-baseweb="input"] {
    border-radius: 9px;
}

div[data-baseweb="select"] > div {
    border-radius: 9px;
}

/* DATAFRAME */

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(128,128,128,0.15);
    border-radius: 12px;
    overflow: hidden;
}

/* DIVIDERS */

hr {
    margin-top: 1.4rem !important;
    margin-bottom: 1.4rem !important;
    opacity: 0.2;
}

/* CUSTOM TEXT */

.small-muted {
    font-size: 0.85rem;
    opacity: 0.65;
}

.section-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    opacity: 0.55;
    text-transform: uppercase;
}

</style>

""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/dss_cleaned.csv")

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # Temporary journal column.
    # Later all 11 journals will use this same structure.
    df["Journal"] = "Decision Support Systems"

    return df


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("IS Journals")
st.sidebar.caption("Research Analytics Portal")
st.sidebar.divider()


# ============================================================
# JOURNAL SELECTION
# ============================================================

journal_options = sorted(
    df["Journal"].dropna().unique()
)

selected_journal = st.sidebar.selectbox(
    "Journal",
    journal_options
)


# ============================================================
# PAGE NAVIGATION
# ============================================================

pages = [
    "Overview",
    "Authors",
    "Institutions",
    "Countries",
    "Research Topics",
    "Articles",
    "Methodology"
]


# Check whether the URL specifies a page
page_from_url = st.query_params.get("page")


if page_from_url in pages:

    default_page_index = pages.index(
        page_from_url
    )

else:

    default_page_index = 0


page = st.sidebar.radio(
    "Explore",
    pages,
    index=default_page_index
)


# ============================================================
# YEAR FILTER
# ============================================================

st.sidebar.divider()


min_year = int(
    df["Year"].min()
)

max_year = int(
    df["Year"].max()
)


year_range = st.sidebar.slider(
    "Publication years",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["Journal"] == selected_journal)
    &
    (df["Year"] >= year_range[0])
    &
    (df["Year"] <= year_range[1])
].copy()


# # ============================================================
# # HEADER
# # ============================================================

# st.title("IS Journals Research Analytics")

# st.markdown(
#     f"### {selected_journal}"
# )

# st.caption(
#     f"Research publications from "
#     f"{year_range[0]} to {year_range[1]}"
# )

# st.divider()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def split_values(series):

    values = []

    for cell in series.dropna():

        for value in str(cell).split("|"):

            value = value.strip()

            if value:
                values.append(value)

    return values


def unique_count(series):

    return len(
        set(split_values(series))
    )


def country_code_to_name(code):

    if pd.isna(code):
        return None

    code = str(code).strip().upper()

    try:
        country = pycountry.countries.get(
            alpha_2=code
        )

        if country:
            return country.name

    except Exception:
        pass

    # Keep original value if it is already
    # a country name or cannot be identified.
    return code

# ============================================================
# SESSION STATE
# ============================================================

if "selected_author" not in st.session_state:
    st.session_state.selected_author = None

# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">Journal Overview</div>',
        unsafe_allow_html=True
    )

    st.header("Decision Support Systems")

    st.caption(
        f"Research activity and scholarly impact · "
        f"{year_range[0]}–{year_range[1]}"
    )


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_articles = len(filtered_df)

    total_citations = filtered_df[
        "Citation count"
    ].sum()

    avg_citations = (
        filtered_df["Citation count"].mean()
        if total_articles > 0
        else 0
    )

    total_authors = unique_count(
        filtered_df["Author"]
    )

    total_institutions = unique_count(
        filtered_df["Institution"]
    )

    total_countries = unique_count(
        filtered_df["Country"]
    )


    # ========================================================
    # PRIMARY KPI CARDS
    # ========================================================

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Publications",
        f"{total_articles:,}"
    )

    k2.metric(
        "Total Citations",
        f"{total_citations:,}"
    )

    k3.metric(
        "Authors",
        f"{total_authors:,}"
    )

    k4.metric(
        "Avg. Citations / Paper",
        f"{avg_citations:,.1f}"
    )


    # ========================================================
    # SECONDARY SUMMARY
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "Institutions",
        f"{total_institutions:,}"
    )

    s2.metric(
        "Countries",
        f"{total_countries:,}"
    )


    # International collaboration
    international_count = (
        filtered_df[
            "International collaboration"
        ]
        .astype(str)
        .str.lower()
        .eq("true")
        .sum()
    )

    international_rate = (
        international_count /
        total_articles * 100
        if total_articles > 0
        else 0
    )

    s3.metric(
        "International Collaboration",
        f"{international_rate:.1f}%"
    )


    # ========================================================
    # PUBLICATION TREND
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">Publication Activity</div>',
        unsafe_allow_html=True
    )

    st.subheader("Publications Over Time")


    yearly_publications = (
        filtered_df
        .groupby("Year")
        .agg(
            Publications=("DOI", "nunique")
        )
        .reset_index()
    )


    fig_publications = px.line(
        yearly_publications,
        x="Year",
        y="Publications",
        markers=True
    )


    fig_publications.update_layout(
        height=400,
        xaxis_title="Publication Year",
        yaxis_title="Publications",
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=40
        )
    )


    fig_publications.update_xaxes(
        dtick=1
    )


    st.plotly_chart(
        fig_publications,
        use_container_width=True
    )


    # ========================================================
    # CITATION + OPEN ACCESS
    # ========================================================

    st.divider()

    left, right = st.columns([1.7, 1])


    # --------------------------------------------------------
    # CITATION IMPACT
    # --------------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-label">Scholarly Impact</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Citation Impact by Publication Year"
        )


        yearly_citations = (
            filtered_df
            .groupby("Year")
            .agg(
                Citations=("Citation count", "sum")
            )
            .reset_index()
        )


        fig_citations = px.bar(
            yearly_citations,
            x="Year",
            y="Citations"
        )


        fig_citations.update_layout(
            height=390,
            xaxis_title="Publication Year",
            yaxis_title="Citations",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=40
            )
        )


        st.plotly_chart(
            fig_citations,
            use_container_width=True
        )


    # --------------------------------------------------------
    # OPEN ACCESS
    # --------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-label">Accessibility</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Open Access"
        )


        access_data = (
            filtered_df[
                "Open access"
            ]
            .value_counts()
            .reset_index()
        )

        access_data.columns = [
            "Access",
            "Publications"
        ]


        fig_access = px.pie(
            access_data,
            names="Access",
            values="Publications",
            hole=0.6
        )


        fig_access.update_layout(
            height=390,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=20
            ),
            legend_title_text=""
        )


        st.plotly_chart(
            fig_access,
            use_container_width=True
        )


    # ========================================================
    # LEADING RESEARCH
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">Research Landscape</div>',
        unsafe_allow_html=True
    )

    st.subheader("Leading Research Areas")


    # --------------------------------------------------------
    # TOPICS
    # --------------------------------------------------------

    topic_values = split_values(
        filtered_df["Topic"]
    )


    topic_counts = (
        pd.Series(topic_values)
        .value_counts()
        .head(10)
        .reset_index()
    )


    topic_counts.columns = [
        "Topic",
        "Publications"
    ]


    # --------------------------------------------------------
    # INSTITUTIONS
    # --------------------------------------------------------

    institution_values = split_values(
        filtered_df["Institution"]
    )


    institution_counts = (
        pd.Series(institution_values)
        .value_counts()
        .head(10)
        .reset_index()
    )


    institution_counts.columns = [
        "Institution",
        "Publications"
    ]


    chart1, chart2 = st.columns(2)


    # --------------------------------------------------------
    # TOP TOPICS
    # --------------------------------------------------------

    with chart1:

        st.markdown("#### Top Research Topics")


        topic_chart_data = (
            topic_counts
            .sort_values(
                "Publications",
                ascending=True
            )
        )


        fig_top_topics = px.bar(
            topic_chart_data,
            x="Publications",
            y="Topic",
            orientation="h"
        )


        fig_top_topics.update_layout(
            height=450,
            xaxis_title="Publications",
            yaxis_title="",
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=40
            )
        )


        st.plotly_chart(
            fig_top_topics,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TOP INSTITUTIONS
    # --------------------------------------------------------

    with chart2:

        st.markdown("#### Leading Institutions")


        institution_chart_data = (
            institution_counts
            .sort_values(
                "Publications",
                ascending=True
            )
        )


        fig_institutions = px.bar(
            institution_chart_data,
            x="Publications",
            y="Institution",
            orientation="h"
        )


        fig_institutions.update_layout(
            height=450,
            xaxis_title="Publications",
            yaxis_title="",
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=40
            )
        )


        st.plotly_chart(
            fig_institutions,
            use_container_width=True
        )


    # ========================================================
    # HIGH IMPACT PUBLICATIONS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">Publication Highlights</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Most Cited Publications"
    )


    top_articles = (
        filtered_df[
            [
                "Title",
                "Year",
                "Author",
                "Citation count"
            ]
        ]
        .sort_values(
            "Citation count",
            ascending=False
        )
        .head(10)
        .copy()
    )


    top_articles = top_articles.rename(
        columns={
            "Citation count":
                "Citations"
        }
    )


    st.dataframe(
        top_articles,

        use_container_width=True,

        hide_index=True,

        column_config={

            "Title":
                st.column_config.TextColumn(
                    "Article",
                    width="large"
                ),

            "Year":
                st.column_config.NumberColumn(
                    "Year",
                    format="%d"
                ),

            "Author":
                st.column_config.TextColumn(
                    "Authors",
                    width="medium"
                ),

            "Citations":
                st.column_config.NumberColumn(
                    "Citations",
                    format="%d"
                )
        }
    )


    # ========================================================
    # METHODOLOGY NOTE
    # ========================================================

    st.caption(
        "Citation counts are cumulative and therefore "
        "older publications have had more time to accumulate "
        "citations. Topic classifications are provided by "
        "OpenAlex."
    )

    # --------------------------------------------------------
    # KPI ROW
    # --------------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Publications",
        f"{total_articles:,}"
    )

    col2.metric(
        "Citations",
        f"{total_citations:,}"
    )

    col3.metric(
        "Authors",
        f"{total_authors:,}"    )

    col4.metric(
        "Institutions",
        f"{total_institutions:,}"
    )

    col5.metric(
        "Countries",
        f"{total_countries:,}"
    )


    st.divider()

    st.subheader(
        "About this collection"
    )

    st.write(
        f"""
        This collection contains **{total_articles:,} publications**
        from **{selected_journal}** between
        **{year_range[0]} and {year_range[1]}**.

        Use the navigation menu to explore authors,
        institutions, countries, research topics and
        individual publications.
        """
    )

# ============================================================
# AUTHORS
# ============================================================

elif page == "Authors":

    # ========================================================
    # CHECK URL FOR SELECTED AUTHOR
    # ========================================================

    author_from_url = st.query_params.get("author")

    if author_from_url:
        st.session_state.selected_author = unquote(
            str(author_from_url)
        )

    elif "selected_author" not in st.session_state:
        st.session_state.selected_author = None


    # ========================================================
    # BUILD AUTHOR-LEVEL DATA
    # ========================================================

    author_rows = []

    for _, row in filtered_df.iterrows():

        if pd.isna(row["Author"]):
            continue

        authors = [
            author.strip()
            for author in str(row["Author"]).split("|")
            if author.strip()
        ]

        # Remove duplicate author names within an article
        authors = list(dict.fromkeys(authors))

        for author in authors:

            author_rows.append(
                {
                    "Author": author,
                    "DOI": row["DOI"],
                    "Title": row["Title"],
                    "Year": row["Year"],
                    "Date": row["Date"],
                    "Citations": row["Citation count"],
                    "Topic": row["Topic"],
                    "Keyword": row["Keyword"]
                }
            )

    author_df = pd.DataFrame(author_rows)


    # ========================================================
    # AUTHOR DIRECTORY / RANKING
    # ========================================================

    if st.session_state.selected_author is None:

        # ----------------------------------------------------
        # PAGE HEADER
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">'
            'Research Community'
            '</div>',
            unsafe_allow_html=True
        )

        st.header("Authors")

        st.caption(
            f"Researchers publishing in "
            f"{selected_journal} · "
            f"{year_range[0]}–{year_range[1]}"
        )


        # ====================================================
        # BUILD AUTHOR SUMMARY
        # ====================================================

        author_summary = (
            author_df
            .groupby("Author")
            .agg(
                Publications=(
                    "DOI",
                    "nunique"
                ),
                Citations=(
                    "Citations",
                    "sum"
                ),
                First_Publication=(
                    "Year",
                    "min"
                ),
                Latest_Publication=(
                    "Year",
                    "max"
                )
            )
            .reset_index()
        )

        author_summary["Citations_per_Paper"] = (
            author_summary["Citations"]
            /
            author_summary["Publications"]
        )


        # ====================================================
        # KPI CARDS
        # ====================================================

        a1, a2, a3, a4 = st.columns(4)

        a1.metric(
            "Authors",
            f"{len(author_summary):,}"
        )

        a2.metric(
            "Authors with 5+ Papers",
            f"{(
                author_summary['Publications'] >= 5
            ).sum():,}"
        )

        a3.metric(
            "Most Papers by One Author",
            f"{int(
                author_summary[
                    'Publications'
                ].max()
            ):,}"
        )

        a4.metric(
            "Highest Citation Total",
            f"{int(
                author_summary[
                    'Citations'
                ].max()
            ):,}"
        )


        # ====================================================
        # SEARCH / FILTER / RANKING CONTROLS
        # ====================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        search_col, min_col, sort_col = st.columns(
            [2.4, 1, 1.4]
        )

        with search_col:

            author_search = st.text_input(
                "Search authors",
                placeholder="Search by author name..."
            )

        with min_col:

            min_author_papers = st.number_input(
                "Minimum papers",
                min_value=1,
                value=1,
                step=1
            )

        with sort_col:

            author_sort = st.selectbox(
                "Rank by",
                [
                    "Publications",
                    "Citations",
                    "Citations per Paper",
                    "Latest Publication"
                ]
            )


        # ====================================================
        # FILTER AUTHORS
        # ====================================================

        display_authors = author_summary[
            author_summary[
                "Publications"
            ] >= min_author_papers
        ].copy()

        if author_search:

            display_authors = display_authors[
                display_authors[
                    "Author"
                ].str.contains(
                    author_search,
                    case=False,
                    na=False
                )
            ]


        # ====================================================
        # AUTHOR RANKING LOGIC
        # ====================================================

        if author_sort == "Publications":

            # Primary:
            #   Publication count
            #
            # Tie-breakers:
            #   1. Total citations
            #   2. Citations per paper
            #   3. Author name

            display_authors = (
                display_authors
                .sort_values(
                    [
                        "Publications",
                        "Citations",
                        "Citations_per_Paper",
                        "Author"
                    ],
                    ascending=[
                        False,
                        False,
                        False,
                        True
                    ]
                )
                .reset_index(drop=True)
            )


        elif author_sort == "Citations":

            # Primary:
            #   Total citations
            #
            # Tie-breakers:
            #   1. Publications
            #   2. Citations per paper
            #   3. Author name

            display_authors = (
                display_authors
                .sort_values(
                    [
                        "Citations",
                        "Publications",
                        "Citations_per_Paper",
                        "Author"
                    ],
                    ascending=[
                        False,
                        False,
                        False,
                        True
                    ]
                )
                .reset_index(drop=True)
            )


        elif author_sort == "Citations per Paper":

            # Primary:
            #   Average citations per publication
            #
            # Tie-breakers:
            #   1. Total citations
            #   2. Publications
            #   3. Author name

            display_authors = (
                display_authors
                .sort_values(
                    [
                        "Citations_per_Paper",
                        "Citations",
                        "Publications",
                        "Author"
                    ],
                    ascending=[
                        False,
                        False,
                        False,
                        True
                    ]
                )
                .reset_index(drop=True)
            )


        elif author_sort == "Latest Publication":

            # Primary:
            #   Latest publication year
            #
            # Tie-breakers:
            #   1. Publications
            #   2. Citations
            #   3. Author name

            display_authors = (
                display_authors
                .sort_values(
                    [
                        "Latest_Publication",
                        "Publications",
                        "Citations",
                        "Author"
                    ],
                    ascending=[
                        False,
                        False,
                        False,
                        True
                    ]
                )
                .reset_index(drop=True)
            )


        # ====================================================
        # ADD DISPLAY RANK
        # ====================================================

        display_authors.insert(
            0,
            "Rank",
            range(
                1,
                len(display_authors) + 1
            )
        )


        # ====================================================
        # AUTHOR RANKING HEADER
        # ====================================================

        st.divider()

        title_col, count_col = st.columns(
            [3, 1]
        )

        with title_col:

            st.subheader(
                "Author Ranking"
            )

        with count_col:

            st.markdown(
                f"""
                <p style="
                    text-align:right;
                    padding-top:10px;
                    font-size:0.9rem;
                    opacity:0.65;
                ">
                    <b>{len(display_authors):,}</b>
                    authors found
                </p>
                """,
                unsafe_allow_html=True
            )

        st.caption(
            "Click an author name to view "
            "their research profile."
        )


        # ====================================================
        # PREPARE RANKING TABLE
        # ====================================================

        ranking_table = (
            display_authors[
                [
                    "Rank",
                    "Author",
                    "Publications",
                    "Citations",
                    "Citations_per_Paper",
                    "First_Publication",
                    "Latest_Publication"
                ]
            ]
            .head(100)
            .copy()
        )

        ranking_table = ranking_table.rename(
            columns={
                "Citations_per_Paper":
                    "Citations / Paper",

                "First_Publication":
                    "First",

                "Latest_Publication":
                    "Latest"
            }
        )


        # ====================================================
        # CREATE CLICKABLE AUTHOR LINKS
        # ====================================================

        ranking_table["Author Link"] = (
            ranking_table["Author"]
            .apply(
                lambda name:
                f"?page=Authors&author="
                f"{quote(str(name))}"
            )
        )


        # ====================================================
        # FINAL RANKING TABLE
        # ====================================================

        ranking_display = (
            ranking_table[
                [
                    "Rank",
                    "Author Link",
                    "Publications",
                    "Citations",
                    "Citations / Paper",
                    "First",
                    "Latest"
                ]
            ]
            .copy()
        )


        st.dataframe(
            ranking_display,
            use_container_width=True,
            hide_index=True,
            height=650,

            column_config={

                "Rank":
                    st.column_config.NumberColumn(
                        "#",
                        width="small",
                        format="%d"
                    ),

                "Author Link":
                    st.column_config.LinkColumn(
                        "Author",
                        display_text=r"author=(.*)",
                        width="large"
                    ),

                "Publications":
                    st.column_config.ProgressColumn(
                        "Papers",
                        min_value=0,
                        max_value=int(
                            author_summary[
                                "Publications"
                            ].max()
                        ),
                        format="%d"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d"
                    ),

                "Citations / Paper":
                    st.column_config.NumberColumn(
                        "Cit. / Paper",
                        format="%.1f"
                    ),

                "First":
                    st.column_config.NumberColumn(
                        "First",
                        format="%d"
                    ),

                "Latest":
                    st.column_config.NumberColumn(
                        "Latest",
                        format="%d"
                    )
            }
        )


        # ====================================================
        # RANKING METHODOLOGY
        # ====================================================

        if author_sort == "Publications":

            ranking_note = (
                "Authors are ranked by number of publications. "
                "Ties are resolved by total citations, followed "
                "by citations per paper."
            )

        elif author_sort == "Citations":

            ranking_note = (
                "Authors are ranked by total citations. "
                "Ties are resolved by publication count, "
                "followed by citations per paper."
            )

        elif author_sort == "Citations per Paper":

            ranking_note = (
                "Authors are ranked by average citations per "
                "publication. Ties are resolved by total "
                "citations, followed by publication count."
            )

        else:

            ranking_note = (
                "Authors are ranked by their most recent "
                "publication year. Ties are resolved by "
                "publication count, followed by total citations."
            )

        st.caption(
            f"Ranking methodology: {ranking_note} "
            f"Metrics are calculated within the selected "
            f"{selected_journal} publication period."
        )


    # ========================================================
    # AUTHOR PROFILE
    # ========================================================

    else:

        selected_author = (
            st.session_state.selected_author
        )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        if st.button(
            "← Back to Authors"
        ):

            st.session_state.selected_author = None

            st.query_params.clear()

            st.query_params["page"] = "Authors"

            st.rerun()


        # ====================================================
        # SELECT AUTHOR ARTICLES
        # ====================================================

        author_articles = (
            author_df[
                author_df[
                    "Author"
                ] == selected_author
            ]
            .drop_duplicates(
                subset="DOI"
            )
            .copy()
        )


        # ====================================================
        # AUTHOR NOT FOUND
        # ====================================================

        if author_articles.empty:

            st.warning(
                "No publications were found for this author "
                "within the currently selected filters."
            )

            if st.button(
                "Return to Authors"
            ):

                st.session_state.selected_author = None

                st.query_params.clear()

                st.query_params["page"] = "Authors"

                st.rerun()

            st.stop()


        # ====================================================
        # AUTHOR METRICS
        # ====================================================

        total_papers = (
            author_articles[
                "DOI"
            ].nunique()
        )

        total_author_citations = int(
            author_articles[
                "Citations"
            ]
            .fillna(0)
            .sum()
        )

        average_citations = (
            total_author_citations
            / total_papers
            if total_papers > 0
            else 0
        )

        first_year = int(
            author_articles[
                "Year"
            ].min()
        )

        latest_year = int(
            author_articles[
                "Year"
            ].max()
        )


        # ====================================================
        # DSS H-INDEX
        # ====================================================

        citation_values = sorted(
            author_articles[
                "Citations"
            ]
            .fillna(0)
            .astype(int)
            .tolist(),
            reverse=True
        )

        h_index = 0

        for i, citation_count in enumerate(
            citation_values,
            start=1
        ):

            if citation_count >= i:
                h_index = i

            else:
                break


        # ====================================================
        # AUTHOR INITIALS
        # ====================================================

        initials = "".join(
            [
                word[0].upper()

                for word
                in selected_author.split()

                if word
            ][:2]
        )


        # ====================================================
        # PROFILE HEADER
        # ====================================================

        profile_left, profile_right = (
            st.columns(
                [0.7, 5],
                vertical_alignment="center"
            )
        )

        with profile_left:

            st.markdown(
                f"""
                <div style="
                    width:78px;
                    height:78px;
                    border-radius:50%;
                    background:#17243A;
                    color:white;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:1.40rem;
                    font-weight:700;
                    letter-spacing:0.04em;
                ">
                    {initials}
                </div>
                """,
                unsafe_allow_html=True
            )

        with profile_right:

            st.markdown(
                '<div class="section-label">'
                'Author Profile'
                '</div>',
                unsafe_allow_html=True
            )

            st.header(
                selected_author
            )

            st.caption(
                f"{selected_journal} · "
                f"{first_year}–{latest_year}"
            )


        # ====================================================
        # SUMMARY METRICS
        # ====================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Papers",
            f"{total_papers:,}"
        )

        m2.metric(
            "Total Citations",
            f"{total_author_citations:,}"
        )

        m3.metric(
            "Citations / Paper",
            f"{average_citations:,.1f}"
        )

        m4, m5, m6 = st.columns(3)

        m4.metric(
            "DSS h-index",
            f"{h_index:,}"
        )

        m5.metric(
            "First Publication",
            f"{first_year}"
        )

        m6.metric(
            "Latest Publication",
            f"{latest_year}"
        )

        st.caption(
            "The DSS h-index is calculated only from "
            "publications and citation counts contained "
            "in the currently selected dataset."
        )


        # ====================================================
        # OUTPUT OVER TIME
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-label">'
            'Publication Activity'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Output Over Time"
        )

        author_yearly = (
            author_articles
            .groupby("Year")
            .agg(
                Publications=(
                    "DOI",
                    "nunique"
                )
            )
            .reset_index()
        )

        fig_author_output = px.bar(
            author_yearly,
            x="Year",
            y="Publications"
        )

        fig_author_output.update_layout(
            height=330,
            xaxis_title="",
            yaxis_title="Publications",
            showlegend=False,
            margin=dict(
                l=20,
                r=20,
                t=10,
                b=30
            )
        )

        fig_author_output.update_xaxes(
            dtick=1
        )

        st.plotly_chart(
            fig_author_output,
            use_container_width=True
        )


        # ====================================================
        # LEADING RESEARCH TOPICS
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-label">'
            'Research Profile'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Leading Research Topics"
        )

        topic_values = split_values(
            author_articles[
                "Topic"
            ]
        )

        if topic_values:

            author_topics = (
                pd.Series(
                    topic_values
                )
                .value_counts()
                .head(10)
                .reset_index()
            )

            author_topics.columns = [
                "Topic",
                "Publications"
            ]

            topic_plot = (
                author_topics
                .sort_values(
                    "Publications",
                    ascending=True
                )
            )

            fig_author_topics = px.bar(
                topic_plot,
                x="Publications",
                y="Topic",
                orientation="h"
            )

            fig_author_topics.update_layout(
                height=400,
                xaxis_title="Publications",
                yaxis_title="",
                showlegend=False,
                margin=dict(
                    l=10,
                    r=20,
                    t=10,
                    b=30
                )
            )

            st.plotly_chart(
                fig_author_topics,
                use_container_width=True
            )

        else:

            st.info(
                "No topic metadata is available "
                "for this author's publications."
            )


        # ====================================================
        # MOST CITED PUBLICATIONS
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-label">'
            'Citation Impact'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Most Cited Publications"
        )

        top_author_articles = (
            author_articles[
                [
                    "Year",
                    "Title",
                    "Citations"
                ]
            ]
            .sort_values(
                "Citations",
                ascending=False
            )
            .head(10)
            .copy()
        )

        st.dataframe(
            top_author_articles,
            use_container_width=True,
            hide_index=True,

            column_config={

                "Year":
                    st.column_config.NumberColumn(
                        "Year",
                        width="small",
                        format="%d"
                    ),

                "Title":
                    st.column_config.TextColumn(
                        "Publication",
                        width="large"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d"
                    )
            }
        )


        # ====================================================
        # ALL PUBLICATIONS
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-label">'
            'Research Output'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Publications"
        )

        publication_table = (
            author_articles[
                [
                    "Year",
                    "Title",
                    "Citations",
                    "DOI"
                ]
            ]
            .sort_values(
                [
                    "Year",
                    "Citations"
                ],
                ascending=[
                    False,
                    False
                ]
            )
            .copy()
        )


        # ====================================================
        # DOI LINKS
        # ====================================================

        publication_table[
            "DOI Link"
        ] = (
            publication_table[
                "DOI"
            ]
            .apply(
                lambda doi:
                (
                    f"https://doi.org/{doi}"

                    if pd.notna(doi)
                    and str(doi).strip()

                    else None
                )
            )
        )

        publication_table = (
            publication_table[
                [
                    "Year",
                    "Title",
                    "Citations",
                    "DOI Link"
                ]
            ]
        )


        # ====================================================
        # PUBLICATION TABLE
        # ====================================================

        st.dataframe(
            publication_table,
            use_container_width=True,
            hide_index=True,
            height=550,

            column_config={

                "Year":
                    st.column_config.NumberColumn(
                        "Year",
                        width="small",
                        format="%d"
                    ),

                "Title":
                    st.column_config.TextColumn(
                        "Publication",
                        width="large"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d"
                    ),

                "DOI Link":
                    st.column_config.LinkColumn(
                        "DOI",
                        display_text="Open DOI"
                    )
            }
        )

# ============================================================
# INSTITUTIONS
# ============================================================

elif page == "Institutions":

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">Research Community</div>',
        unsafe_allow_html=True
    )

    st.header("Institutions")

    st.caption(
        f"{selected_journal} · "
        f"{year_range[0]}–{year_range[1]}"
    )


    # ========================================================
    # BUILD INSTITUTION-LEVEL DATA
    # ========================================================

    institution_rows = []

    for _, row in filtered_df.iterrows():

        if pd.isna(row["Institution"]):
            continue

        institutions = [
            institution.strip()
            for institution in str(row["Institution"]).split("|")
            if institution.strip()
        ]

        # Remove duplicates within the same article
        institutions = list(dict.fromkeys(institutions))

        for institution in institutions:

            institution_rows.append({
                "Institution": institution,
                "DOI": row["DOI"],
                "Year": row["Year"],
                "Citations": row["Citation count"],
                "Title": row["Title"]
            })


    institution_df = pd.DataFrame(
        institution_rows
    )


    if not institution_df.empty:

        # ====================================================
        # INSTITUTION SUMMARY
        # ====================================================

        institution_summary = (
            institution_df
            .groupby("Institution")
            .agg(
                Publications=("DOI", "nunique"),
                Citations=("Citations", "sum"),
                First_Publication=("Year", "min"),
                Latest_Publication=("Year", "max")
            )
            .reset_index()
        )


        # ====================================================
        # KPI CARDS
        # ====================================================

        total_institutions = (
            institution_summary[
                "Institution"
            ].nunique()
        )

        active_institutions = (
            institution_summary[
                "Publications"
            ] >= 5
        ).sum()

        most_publications = (
            institution_summary[
                "Publications"
            ].max()
        )

        highest_citations = (
            institution_summary[
                "Citations"
            ].max()
        )


        k1, k2, k3, k4 = st.columns(4)

        k1.metric(
            "Institutions",
            f"{total_institutions:,}"
        )

        k2.metric(
            "Institutions with 5+ Papers",
            f"{active_institutions:,}"
        )

        k3.metric(
            "Most Publications",
            f"{most_publications:,}"
        )

        k4.metric(
            "Highest Citation Total",
            f"{highest_citations:,}"
        )


        # ====================================================
        # SEARCH / FILTERS
        # ====================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-label">'
            'Find Institutions'
            '</div>',
            unsafe_allow_html=True
        )


        search_col, min_col, sort_col = (
            st.columns(
                [2.5, 1, 1.4]
            )
        )


        with search_col:

            institution_search = (
                st.text_input(
                    "Search institution",
                    placeholder=(
                        "Search by institution name..."
                    )
                )
            )


        with min_col:

            min_institution_papers = (
                st.number_input(
                    "Minimum papers",
                    min_value=1,
                    value=1,
                    step=1,
                    key="institution_min_papers"
                )
            )


        with sort_col:

            institution_sort = (
                st.selectbox(
                    "Sort by",
                    [
                        "Publications",
                        "Citations",
                        "Latest Publication",
                        "Institution"
                    ],
                    key="institution_sort"
                )
            )


        # ====================================================
        # APPLY FILTERS
        # ====================================================

        display_institutions = (
            institution_summary[
                institution_summary[
                    "Publications"
                ] >= min_institution_papers
            ]
            .copy()
        )


        if institution_search:

            display_institutions = (
                display_institutions[
                    display_institutions[
                        "Institution"
                    ]
                    .str.contains(
                        institution_search,
                        case=False,
                        na=False
                    )
                ]
            )


        sort_mapping = {

            "Publications":
                "Publications",

            "Citations":
                "Citations",

            "Latest Publication":
                "Latest_Publication",

            "Institution":
                "Institution"
        }


        display_institutions = (
            display_institutions
            .sort_values(
                sort_mapping[
                    institution_sort
                ],
                ascending=(
                    institution_sort
                    == "Institution"
                )
            )
        )


        # ====================================================
        # REGISTER HEADER
        # ====================================================

        st.divider()

        title_col, count_col = (
            st.columns([3, 1])
        )


        with title_col:

            st.subheader(
                "Institution Register"
            )


        with count_col:

            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    padding-top:10px;
                    font-size:0.9rem;
                    opacity:0.65;
                ">
                    <b>{len(display_institutions):,}</b>
                    institutions found
                </div>
                """,
                unsafe_allow_html=True
            )


        # ====================================================
        # ROW LIMIT
        # ====================================================

        institution_limit = (
            st.selectbox(
                "Show",
                [25, 50, 100, 250],
                index=1,
                format_func=lambda x:
                    f"{x} institutions",
                key="institution_rows"
            )
        )


        table_df = (
            display_institutions
            .head(institution_limit)
            .copy()
        )


        table_df = table_df.rename(
            columns={

                "First_Publication":
                    "First Publication",

                "Latest_Publication":
                    "Latest Publication"
            }
        )


        # ====================================================
        # TABLE
        # ====================================================

        st.dataframe(
            table_df,

            use_container_width=True,

            hide_index=True,

            height=650,

            column_config={

                "Institution":
                    st.column_config.TextColumn(
                        "Institution",
                        width="large"
                    ),

                "Publications":
                    st.column_config.NumberColumn(
                        "Papers",
                        format="%d"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d"
                    ),

                "First Publication":
                    st.column_config.NumberColumn(
                        "First",
                        format="%d"
                    ),

                "Latest Publication":
                    st.column_config.NumberColumn(
                        "Latest",
                        format="%d"
                    )
            }
        )


        st.caption(
            "Institution counts represent participation "
            "in publications. A publication involving "
            "multiple institutions is counted once for "
            "each participating institution."
        )


    else:

        st.warning(
            "No institution information is available "
            "for the selected period."
        )


# ============================================================
# COUNTRIES
# ============================================================

elif page == "Countries":

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">Geographic Analysis</div>',
        unsafe_allow_html=True
    )

    st.header("Countries")

    st.caption(
        f"{selected_journal} · "
        f"{year_range[0]}–{year_range[1]}"
    )


    # ========================================================
    # BUILD COUNTRY-LEVEL DATA
    # ========================================================

    country_rows = []

    for _, row in filtered_df.iterrows():

        if pd.isna(row["Country"]):
            continue

        countries = [
            country.strip()
            for country in str(row["Country"]).split("|")
            if country.strip()
        ]

        # Remove duplicate countries within one article
        countries = list(
            dict.fromkeys(countries)
        )

        for country_code in countries:

            country_rows.append({
                "Country Code": country_code.upper(),

                "Country":
                    country_code_to_name(
                        country_code
                    ),

                "DOI": row["DOI"],

                "Year": row["Year"],

                "Citations":
                    row["Citation count"]
            })


    country_df = pd.DataFrame(
        country_rows
    )


    if not country_df.empty:

        # ====================================================
        # COUNTRY SUMMARY
        # ====================================================

        country_summary = (
            country_df
            .groupby(
                ["Country Code", "Country"]
            )
            .agg(
                Publications=("DOI", "nunique"),

                Citations=("Citations", "sum"),

                First_Publication=("Year", "min"),

                Latest_Publication=("Year", "max")
            )
            .reset_index()
        )


        # ====================================================
        # KPI CARDS
        # ====================================================

        total_countries = (
            country_summary[
                "Country"
            ].nunique()
        )


        countries_10_plus = (
            country_summary[
                "Publications"
            ] >= 10
        ).sum()


        most_publications = (
            country_summary[
                "Publications"
            ].max()
        )


        highest_citations = (
            country_summary[
                "Citations"
            ].max()
        )


        k1, k2, k3, k4 = st.columns(4)


        k1.metric(
            "Countries",
            f"{total_countries:,}"
        )


        k2.metric(
            "Countries with 10+ Papers",
            f"{countries_10_plus:,}"
        )


        k3.metric(
            "Most Publications",
            f"{most_publications:,}"
        )


        k4.metric(
            "Highest Citation Total",
            f"{highest_citations:,}"
        )


        # ====================================================
        # SEARCH / SORT
        # ====================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-label">'
            'Explore Countries'
            '</div>',
            unsafe_allow_html=True
        )


        search_col, min_col, sort_col = (
            st.columns(
                [2.5, 1, 1.4]
            )
        )


        with search_col:

            country_search = (
                st.text_input(
                    "Search country",
                    placeholder=(
                        "Search by country name..."
                    )
                )
            )


        with min_col:

            min_country_papers = (
                st.number_input(
                    "Minimum papers",
                    min_value=1,
                    value=1,
                    step=1,
                    key="country_min_papers"
                )
            )


        with sort_col:

            country_sort = (
                st.selectbox(
                    "Sort by",
                    [
                        "Publications",
                        "Citations",
                        "Latest Publication",
                        "Country"
                    ],
                    key="country_sort"
                )
            )


        # ====================================================
        # FILTER
        # ====================================================

        display_countries = (
            country_summary[
                country_summary[
                    "Publications"
                ] >= min_country_papers
            ]
            .copy()
        )


        if country_search:

            display_countries = (
                display_countries[
                    display_countries[
                        "Country"
                    ]
                    .str.contains(
                        country_search,
                        case=False,
                        na=False
                    )
                ]
            )


        sort_mapping = {

            "Publications":
                "Publications",

            "Citations":
                "Citations",

            "Latest Publication":
                "Latest_Publication",

            "Country":
                "Country"
        }


        display_countries = (
            display_countries
            .sort_values(
                sort_mapping[
                    country_sort
                ],
                ascending=(
                    country_sort
                    == "Country"
                )
            )
        )


        # ====================================================
        # REGISTER
        # ====================================================

        st.divider()

        title_col, count_col = (
            st.columns([3, 1])
        )


        with title_col:

            st.subheader(
                "Country Register"
            )


        with count_col:

            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    padding-top:10px;
                    font-size:0.9rem;
                    opacity:0.65;
                ">
                    <b>{len(display_countries):,}</b>
                    countries found
                </div>
                """,
                unsafe_allow_html=True
            )


        # ====================================================
        # TABLE
        # ====================================================

        country_table = (
            display_countries
            .rename(
                columns={
                    "First_Publication":
                        "First Publication",

                    "Latest_Publication":
                        "Latest Publication"
                }
            )
        )


        st.dataframe(
            country_table[
                [
                    "Country",
                    "Country Code",
                    "Publications",
                    "Citations",
                    "First Publication",
                    "Latest Publication"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=600,

            column_config={

                "Country":
                    st.column_config.TextColumn(
                        "Country",
                        width="large"
                    ),

                "Country Code":
                    st.column_config.TextColumn(
                        "Code",
                        width="small"
                    ),

                "Publications":
                    st.column_config.NumberColumn(
                        "Papers",
                        format="%d"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d"
                    ),

                "First Publication":
                    st.column_config.NumberColumn(
                        "First",
                        format="%d"
                    ),

                "Latest Publication":
                    st.column_config.NumberColumn(
                        "Latest",
                        format="%d"
                    )
            }
        )


        st.caption(
            "Country counts represent participation in "
            "publications. An internationally collaborative "
            "article is counted once for each participating "
            "country."
        )


    else:

        st.warning(
            "No country information is available "
            "for the selected period."
        )


# ============================================================
# RESEARCH TOPICS
# ============================================================

elif page == "Research Topics":

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">Research Landscape</div>',
        unsafe_allow_html=True
    )

    st.header("Research Topics")

    st.caption(
        f"{selected_journal} · "
        f"{year_range[0]}–{year_range[1]}"
    )


    # ========================================================
    # BUILD TOPIC-LEVEL DATA
    # ========================================================

    topic_rows = []

    for _, row in filtered_df.iterrows():

        if pd.isna(row["Topic"]):
            continue

        topics = [
            topic.strip()
            for topic in str(row["Topic"]).split("|")
            if topic.strip()
        ]

        # Remove duplicate topics within one article
        topics = list(dict.fromkeys(topics))

        for topic in topics:

            topic_rows.append({
                "Topic": topic,
                "DOI": row["DOI"],
                "Year": row["Year"],
                "Citations": row["Citation count"]
            })


    topic_df = pd.DataFrame(topic_rows)


    if not topic_df.empty:

        # ====================================================
        # TOPIC SUMMARY
        # ====================================================

        topic_summary = (
            topic_df
            .groupby("Topic")
            .agg(
                Publications=("DOI", "nunique"),
                Citations=("Citations", "sum"),
                First_Publication=("Year", "min"),
                Latest_Publication=("Year", "max")
            )
            .reset_index()
        )


        # ====================================================
        # KPI CARDS
        # ====================================================

        total_topics = topic_summary["Topic"].nunique()

        active_topics = (
            topic_summary["Publications"] >= 10
        ).sum()

        largest_topic = (
            topic_summary["Publications"].max()
        )

        topic_publications = len(
            filtered_df[
                filtered_df["Topic"].notna()
            ]
        )

        topic_coverage = (
            topic_publications /
            len(filtered_df) * 100
            if len(filtered_df) > 0
            else 0
        )


        k1, k2, k3, k4 = st.columns(4)

        k1.metric(
            "Research Topics",
            f"{total_topics:,}"
        )

        k2.metric(
            "Topics with 10+ Papers",
            f"{active_topics:,}"
        )

        k3.metric(
            "Largest Topic",
            f"{largest_topic:,} papers"
        )

        k4.metric(
            "Topic Coverage",
            f"{topic_coverage:.1f}%"
        )


        # ====================================================
        # TOP TOPICS
        # ====================================================

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-label">Research Concentration</div>',
            unsafe_allow_html=True
        )

        st.subheader("Leading Research Topics")


        top_n = st.slider(
            "Number of topics",
            min_value=5,
            max_value=30,
            value=15,
            step=5
        )


        top_topics = (
            topic_summary
            .sort_values(
                "Publications",
                ascending=False
            )
            .head(top_n)
            .sort_values(
                "Publications",
                ascending=True
            )
        )


        fig_topics = px.bar(
            top_topics,
            x="Publications",
            y="Topic",
            orientation="h",
            hover_data={
                "Citations": True,
                "Publications": True
            }
        )


        fig_topics.update_layout(
            xaxis_title="Number of Publications",
            yaxis_title="",
            height=max(450, top_n * 32),
            margin=dict(
                l=10,
                r=20,
                t=20,
                b=40
            )
        )


        st.plotly_chart(
            fig_topics,
            use_container_width=True
        )


        # ====================================================
        # TOPIC TREND EXPLORER
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-label">Topic Evolution</div>',
            unsafe_allow_html=True
        )

        st.subheader("Topic Trends Over Time")


        trend_topics = (
            topic_summary
            .sort_values(
                "Publications",
                ascending=False
            )
            .head(30)["Topic"]
            .tolist()
        )


        default_topics = trend_topics[:3]


        selected_topics = st.multiselect(
            "Select topics",
            options=trend_topics,
            default=default_topics,
            max_selections=5
        )


        if selected_topics:

            topic_trend = (
                topic_df[
                    topic_df["Topic"].isin(
                        selected_topics
                    )
                ]
                .groupby(
                    ["Year", "Topic"]
                )
                .agg(
                    Publications=("DOI", "nunique")
                )
                .reset_index()
            )


            fig_trend = px.line(
                topic_trend,
                x="Year",
                y="Publications",
                color="Topic",
                markers=True
            )


            fig_trend.update_layout(
                xaxis_title="Publication Year",
                yaxis_title="Publications",
                hovermode="x unified",
                height=480,
                legend_title_text="Topic"
            )


            fig_trend.update_xaxes(
                dtick=1
            )


            st.plotly_chart(
                fig_trend,
                use_container_width=True
            )

        else:

            st.info(
                "Select at least one topic to view "
                "its publication trend."
            )


        # ====================================================
        # TOPIC REGISTER
        # ====================================================

        st.divider()

        title_col, count_col = st.columns([3, 1])


        with title_col:

            st.subheader("Topic Register")


        with count_col:

            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    padding-top:10px;
                    font-size:0.9rem;
                    opacity:0.65;
                ">
                    <b>{len(topic_summary):,}</b>
                    topics identified
                </div>
                """,
                unsafe_allow_html=True
            )


        topic_search = st.text_input(
            "Search topics",
            placeholder="Search by topic name..."
        )


        topic_table = topic_summary.copy()


        if topic_search:

            topic_table = topic_table[
                topic_table["Topic"]
                .str.contains(
                    topic_search,
                    case=False,
                    na=False
                )
            ]


        topic_table = (
            topic_table
            .sort_values(
                "Publications",
                ascending=False
            )
            .rename(
                columns={
                    "First_Publication":
                        "First Publication",

                    "Latest_Publication":
                        "Latest Publication"
                }
            )
        )


        st.dataframe(
            topic_table,

            use_container_width=True,

            hide_index=True,

            height=550,

            column_config={

                "Topic":
                    st.column_config.TextColumn(
                        "Research Topic",
                        width="large"
                    ),

                "Publications":
                    st.column_config.NumberColumn(
                        "Papers",
                        format="%d"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d"
                    ),

                "First Publication":
                    st.column_config.NumberColumn(
                        "First",
                        format="%d"
                    ),

                "Latest Publication":
                    st.column_config.NumberColumn(
                        "Latest",
                        format="%d"
                    )
            }
        )


        st.caption(
            "Topics are based on OpenAlex research "
            "classifications. A publication may be "
            "associated with multiple topics."
        )


    else:

        st.warning(
            "No topic information is available "
            "for the selected period."
        )


# ============================================================
# ARTICLES
# ============================================================

elif page == "Articles":

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">Publication Explorer</div>',
        unsafe_allow_html=True
    )

    st.header("Articles")

    st.caption(
        f"{selected_journal} · "
        f"{year_range[0]}–{year_range[1]}"
    )


    # ========================================================
    # SEARCH
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)

    search_query = st.text_input(
        "Search publications",
        placeholder=(
            "Search title, author, keyword or topic..."
        )
    )


    # ========================================================
    # FILTER OPTIONS
    # ========================================================

    filter_col1, filter_col2, filter_col3 = st.columns(3)


    # -------------------------
    # TOPIC FILTER
    # -------------------------

    all_topics = sorted(
        set(
            split_values(
                filtered_df["Topic"]
            )
        )
    )


    with filter_col1:

        selected_article_topics = st.multiselect(
            "Topic",
            options=all_topics,
            placeholder="All topics"
        )


    # -------------------------
    # OPEN ACCESS FILTER
    # -------------------------

    access_options = sorted(
        filtered_df["Open access"]
        .dropna()
        .unique()
        .tolist()
    )


    with filter_col2:

        selected_article_access = st.multiselect(
            "Access",
            options=access_options,
            placeholder="All access types"
        )


    # -------------------------
    # MINIMUM CITATIONS
    # -------------------------

    with filter_col3:

        minimum_citations = st.number_input(
            "Minimum citations",
            min_value=0,
            value=0,
            step=1
        )


    # ========================================================
    # START WITH YEAR-FILTERED DATA
    # ========================================================

    article_df = filtered_df.copy()


    # ========================================================
    # APPLY TEXT SEARCH
    # ========================================================

    if search_query:

        search_columns = [
            "Title",
            "Author",
            "Keyword",
            "Topic"
        ]

        search_mask = pd.Series(
            False,
            index=article_df.index
        )

        for column in search_columns:

            search_mask = (
                search_mask |
                article_df[column]
                .fillna("")
                .astype(str)
                .str.contains(
                    search_query,
                    case=False,
                    na=False,
                    regex=False
                )
            )

        article_df = article_df[
            search_mask
        ]


    # ========================================================
    # APPLY TOPIC FILTER
    # ========================================================

    if selected_article_topics:

        def contains_selected_topic(value):

            if pd.isna(value):
                return False

            article_topics = {
                item.strip()
                for item in str(value).split("|")
                if item.strip()
            }

            return bool(
                article_topics.intersection(
                    selected_article_topics
                )
            )


        article_df = article_df[
            article_df["Topic"]
            .apply(contains_selected_topic)
        ]


    # ========================================================
    # APPLY ACCESS FILTER
    # ========================================================

    if selected_article_access:

        article_df = article_df[
            article_df["Open access"]
            .isin(selected_article_access)
        ]


    # ========================================================
    # APPLY CITATION FILTER
    # ========================================================

    article_df = article_df[
        article_df["Citation count"]
        >= minimum_citations
    ]


    # ========================================================
    # RESULTS SUMMARY
    # ========================================================

    st.divider()

    total_results = len(article_df)

    result_citations = (
        article_df["Citation count"].sum()
    )

    result_avg_citations = (
        article_df["Citation count"].mean()
        if total_results > 0
        else 0
    )


    r1, r2, r3 = st.columns(3)


    r1.metric(
        "Publications Found",
        f"{total_results:,}"
    )


    r2.metric(
        "Total Citations",
        f"{result_citations:,}"
    )


    r3.metric(
        "Average Citations",
        f"{result_avg_citations:,.1f}"
    )


    # ========================================================
    # SORT + ROW LIMIT
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)


    sort_col, rows_col = st.columns([2, 1])


    with sort_col:

        article_sort = st.selectbox(
            "Sort publications by",
            [
                "Most Cited",
                "Newest",
                "Oldest",
                "Title A–Z"
            ]
        )


    with rows_col:

        article_limit = st.selectbox(
            "Show",
            [25, 50, 100, 250],
            index=1,
            format_func=lambda x:
                f"{x} publications"
        )


    # ========================================================
    # SORT
    # ========================================================

    if article_sort == "Most Cited":

        article_df = article_df.sort_values(
            "Citation count",
            ascending=False
        )


    elif article_sort == "Newest":

        article_df = article_df.sort_values(
            ["Year", "Date"],
            ascending=False
        )


    elif article_sort == "Oldest":

        article_df = article_df.sort_values(
            ["Year", "Date"],
            ascending=True
        )


    else:

        article_df = article_df.sort_values(
            "Title",
            ascending=True
        )


    # ========================================================
    # PUBLICATION REGISTER
    # ========================================================

    title_col, count_col = st.columns([3, 1])


    with title_col:

        st.subheader(
            "Publication Register"
        )


    with count_col:

        st.markdown(
            f"""
            <div style="
                text-align:right;
                padding-top:10px;
                font-size:0.9rem;
                opacity:0.65;
            ">
                Showing <b>{min(article_limit, total_results):,}</b>
                of <b>{total_results:,}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # DISPLAY TABLE
    # ========================================================

    table_df = (
        article_df[
            [
                "Title",
                "Year",
                "Author",
                "Citation count",
                "Open access",
                "DOI"
            ]
        ]
        .head(article_limit)
        .copy()
    )


    table_df = table_df.rename(
        columns={
            "Citation count": "Citations",
            "Open access": "Access"
        }
    )


    st.dataframe(
        table_df,

        use_container_width=True,

        hide_index=True,

        height=650,

        column_config={

            "Title":
                st.column_config.TextColumn(
                    "Article",
                    width="large"
                ),

            "Year":
                st.column_config.NumberColumn(
                    "Year",
                    format="%d"
                ),

            "Author":
                st.column_config.TextColumn(
                    "Authors",
                    width="medium"
                ),

            "Citations":
                st.column_config.NumberColumn(
                    "Citations",
                    format="%d"
                ),

            "Access":
                st.column_config.TextColumn(
                    "Access"
                ),

            "DOI":
                st.column_config.TextColumn(
                    "DOI"
                )
        }
    )


    # ========================================================
    # EMPTY RESULT MESSAGE
    # ========================================================

    if total_results == 0:

        st.info(
            "No publications match the selected filters."
        )


    st.caption(
        "Search results reflect the currently selected "
        "journal and publication-year range."
    )


# ============================================================
# METHODOLOGY
# ============================================================

elif page == "Methodology":

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">About the Data</div>',
        unsafe_allow_html=True
    )

    st.header("Methodology")

    st.caption(
        "Data source, processing methodology, "
        "coverage and interpretation guidelines"
    )


    # ========================================================
    # DATA SOURCE
    # ========================================================

    st.subheader("Data Source")

    st.markdown("""
    Publication metadata used in this prototype was obtained
    from **OpenAlex**, an open scholarly research database.

    The current prototype focuses on publications from
    **Decision Support Systems**. The same data-processing
    framework is intended to support additional Information
    Systems journals in later stages of the project.
    """)


    # ========================================================
    # DATASET OVERVIEW
    # ========================================================

    st.divider()

    st.subheader("Dataset Overview")


    dataset_rows = len(df)

    dataset_start = int(df["Year"].min())
    dataset_end = int(df["Year"].max())

    dataset_citations = df[
        "Citation count"
    ].sum()


    d1, d2, d3, d4 = st.columns(4)


    d1.metric(
        "Publications",
        f"{dataset_rows:,}"
    )

    d2.metric(
        "Coverage",
        f"{dataset_start}–{dataset_end}"
    )

    d3.metric(
        "Unique DOIs",
        f"{df['DOI'].nunique():,}"
    )

    d4.metric(
        "Total Citations",
        f"{dataset_citations:,}"
    )


    # ========================================================
    # DATA FIELDS
    # ========================================================

    st.divider()

    st.subheader("Data Dimensions")

    col1, col2 = st.columns(2)


    with col1:

        st.markdown("""
        **Publication information**

        - DOI
        - Article title
        - Publication year
        - Publication date
        - Citation count
        - Open-access status
        - Abstract
        """)


    with col2:

        st.markdown("""
        **Research information**

        - Authors
        - Institutions
        - Countries
        - Keywords
        - Topics
        - Subfields
        - Fields
        - Domains
        """)


    # ========================================================
    # DATA COVERAGE
    # ========================================================

    st.divider()

    st.subheader("Metadata Coverage")


    coverage_fields = [
        ("Author", "Author"),
        ("Institution", "Institution"),
        ("Country", "Country"),
        ("Keyword", "Keyword"),
        ("Topic", "Topic"),
        ("Abstract", "Abstract")
    ]


    coverage_rows = []


    for label, column in coverage_fields:

        available = (
            df[column]
            .notna()
            .sum()
        )

        missing = (
            df[column]
            .isna()
            .sum()
        )

        coverage = (
            available / len(df) * 100
            if len(df) > 0
            else 0
        )


        coverage_rows.append({
            "Metadata": label,
            "Available": available,
            "Missing": missing,
            "Coverage (%)": coverage
        })


    coverage_df = pd.DataFrame(
        coverage_rows
    )


    st.dataframe(
        coverage_df,
        use_container_width=True,
        hide_index=True,

        column_config={

            "Metadata":
                st.column_config.TextColumn(
                    "Metadata"
                ),

            "Available":
                st.column_config.NumberColumn(
                    "Available",
                    format="%d"
                ),

            "Missing":
                st.column_config.NumberColumn(
                    "Missing",
                    format="%d"
                ),

            "Coverage (%)":
                st.column_config.NumberColumn(
                    "Coverage",
                    format="%.1f%%"
                )
        }
    )


    # ========================================================
    # COUNTING METHODOLOGY
    # ========================================================

    st.divider()

    st.subheader("Counting Methodology")


    st.markdown("""
    **Publications**

    Each DOI represents one publication. DOI is therefore used
    as the primary identifier when calculating publication
    counts.


    **Authors**

    Publications containing multiple authors contribute once
    to the publication count of each listed author.


    **Institutions**

    Publications associated with multiple institutions
    contribute once to each participating institution.


    **Countries**

    Publications involving multiple countries contribute once
    to each participating country. Consequently, country-level
    publication counts should not be summed to estimate the
    total number of articles.


    **Research topics**

    A publication may be associated with multiple OpenAlex
    topics. Topic-level counts therefore represent research
    participation rather than mutually exclusive article
    categories.
    """)


    # ========================================================
    # COLLABORATION
    # ========================================================

    st.divider()

    st.subheader("Collaboration Measures")


    st.markdown("""
    **International collaboration** is defined as a publication
    associated with more than one country.

    **Multi-institution collaboration** is defined as a
    publication associated with more than one institution.

    These indicators are calculated from the pipe-separated
    institution and country metadata associated with each
    publication.
    """)


    # ========================================================
    # IMPORTANT LIMITATIONS
    # ========================================================

    st.divider()

    st.subheader("Important Limitations")


    st.info(
        """
        Citation counts are cumulative. Older publications have
        had more time to accumulate citations than recently
        published articles. Citation totals should therefore not
        be interpreted as a direct measure of relative research
        quality across publication years.
        """
    )


    st.warning(
        """
        Abstract coverage is limited in the current dataset.
        Abstract-based natural-language processing is therefore
        not used as a primary analytical component of this
        prototype.
        """
    )


    st.markdown("""
    Additional considerations:

    - Metadata availability depends on OpenAlex coverage.
    - Author and institution names may contain naming variants.
    - Topic classifications are derived from OpenAlex metadata.
    - Recent publications may have very low citation counts
      because they have had limited time to accumulate citations.
    - Institution and country counts represent participation,
      rather than mutually exclusive publication ownership.
    """)


    # ========================================================
    # AUTHOR-INSTITUTION LIMITATION
    # ========================================================

    st.divider()

    st.subheader("Authorship and Affiliation Relationships")


    st.markdown("""
    The current article-level dataset stores authors,
    institutions, and countries as separate multi-value fields.

    For example, an article may contain:

    `Author A | Author B | Author C`

    and:

    `University X | University Y`

    This structure identifies the participants associated with
    the publication, but it does **not** preserve the individual
    author-to-institution relationship.

    Therefore, the current prototype does not infer that a
    particular author belongs to a particular institution unless
    that relationship is explicitly available in the source
    data.
    """)


    # ========================================================
    # PROTOTYPE STATUS
    # ========================================================

    st.divider()

    st.subheader("Prototype Scope")


    st.markdown("""
    This dashboard is currently a **Decision Support Systems
    prototype** used to evaluate the research analytics
    interface and analytical methodology.

    The intended full system will support multiple Information
    Systems journals using a common data model, allowing
    journal-level and cross-journal research analysis.
    """)


    st.caption(
        "Prototype research analytics system · "
        "Data source: OpenAlex"
    )