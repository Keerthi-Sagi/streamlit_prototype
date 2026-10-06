import streamlit as st
import pandas as pd
import pycountry
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
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   DESIGN TOKENS
   ========================================================== */

:root {
    --navy: #17243A;
    --navy-soft: #223552;
    --blue: #2563EB;
    --blue-soft: #EFF6FF;
    --text: #172033;
    --muted: #667085;
    --border: #E5E7EB;
    --surface: #FFFFFF;
    --surface-soft: #F8FAFC;
}


/* ==========================================================
   MAIN APPLICATION
   ========================================================== */

.block-container {
    max-width: 1450px;
    padding-top: 3.2rem !important;
    padding-bottom: 4rem;
    padding-left: 3.2rem;
    padding-right: 3.2rem;
}


/* ==========================================================
   TYPOGRAPHY
   ========================================================== */

html,
body,
[class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

h1 {
    font-size: 2.25rem !important;
    font-weight: 720 !important;
    letter-spacing: -0.035em !important;
    line-height: 1.15 !important;
    color: var(--text);
}

h2 {
    font-size: 1.55rem !important;
    font-weight: 680 !important;
    letter-spacing: -0.02em !important;
    color: var(--text);
}

h3 {
    font-size: 1.15rem !important;
    font-weight: 650 !important;
    color: var(--text);
}

p {
    line-height: 1.65;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    border-right: 1px solid var(--border);
    background: #FAFBFC;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] h1 {
    font-size: 1.35rem !important;
    letter-spacing: -0.02em !important;
}


/* Sidebar radio */

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 0.15rem;
}


/* ==========================================================
   SECTION LABELS
   ========================================================== */

.section-label {
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: #2563EB;
    margin-bottom: 0.30rem;
}

.small-muted {
    font-size: 0.85rem;
    color: var(--muted);
}


/* ==========================================================
   METRIC CARDS
   ========================================================== */

div[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 22px;
    min-height: 112px;
    box-shadow:
        0 1px 2px rgba(16, 24, 40, 0.02);
}

div[data-testid="stMetricLabel"] {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 0.01em;
}

div[data-testid="stMetricValue"] {
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text);
}


/* ==========================================================
   DIVIDERS
   ========================================================== */

hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin-top: 2rem !important;
    margin-bottom: 2rem !important;
    opacity: 1 !important;
}


/* ==========================================================
   INPUTS
   ========================================================== */

div[data-baseweb="input"] {
    border-radius: 8px !important;
}

div[data-baseweb="select"] > div {
    border-radius: 8px !important;
}

div[data-baseweb="base-input"] {
    border-radius: 8px !important;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {
    border-radius: 7px;
    border: 1px solid #D0D5DD;
    font-weight: 600;
    min-height: 39px;
    transition:
        border-color 0.15s ease,
        background 0.15s ease;
}

.stButton > button:hover {
    border-color: #2563EB;
    color: #2563EB;
}


/* ==========================================================
   LINK BUTTONS
   ========================================================== */

.stLinkButton a {
    border-radius: 7px !important;
    font-weight: 600 !important;
}


/* ==========================================================
   DATAFRAMES
   ========================================================== */

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 9px;
    overflow: hidden;
}


/* ==========================================================
   ALERTS / INFORMATION BOXES
   ========================================================== */

div[data-testid="stAlert"] {
    border-radius: 8px;
}


/* ==========================================================
   PLOTLY CHART CONTAINERS
   ========================================================== */

div[data-testid="stPlotlyChart"] {
    background: var(--surface);
    border-radius: 8px;
}


/* ==========================================================
   CAPTIONS
   ========================================================== */

div[data-testid="stCaptionContainer"] {
    color: var(--muted);
}


/* ==========================================================
   PROFILE HERO
   Reusable later for Author / Institution / Country /
   Topic / Article profiles
   ========================================================== */

.profile-hero {
    background:
        linear-gradient(
            135deg,
            #17243A 0%,
            #223552 100%
        );

    border-radius: 12px;
    padding: 30px 34px;
    margin-bottom: 24px;
    color: white;
}

.profile-hero-label {
    font-size: 0.70rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #AFC7EE;
    margin-bottom: 8px;
}

.profile-hero-title {
    font-size: 2rem;
    line-height: 1.2;
    font-weight: 720;
    letter-spacing: -0.03em;
    color: white;
    margin: 0;
}

.profile-hero-subtitle {
    font-size: 0.92rem;
    color: #CBD5E1;
    margin-top: 8px;
}


/* ==========================================================
   INITIALS AVATAR
   ========================================================== */

.profile-avatar {
    width: 78px;
    height: 78px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.12);

    border:
        1px solid rgba(255,255,255,0.20);

    color: white;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}


/* ==========================================================
   PROFILE INFORMATION GRID
   ========================================================== */

.profile-info-grid {
    display: grid;

    grid-template-columns:
        repeat(2, minmax(0, 1fr));

    border:
        1px solid var(--border);

    border-radius: 10px;

    overflow: hidden;

    margin-top: 12px;
    margin-bottom: 24px;
}

.profile-info-item {
    padding: 18px 20px;

    border-bottom:
        1px solid var(--border);
}

.profile-info-item:nth-child(odd) {
    border-right:
        1px solid var(--border);
}

.profile-info-label {
    font-size: 0.73rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--muted);
    margin-bottom: 5px;
}

.profile-info-value {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
}


/* ==========================================================
   CONTENT CARD
   ========================================================== */

.research-card {
    background: var(--surface);

    border:
        1px solid var(--border);

    border-radius: 10px;

    padding: 22px 24px;

    margin-bottom: 20px;
}

.research-card-title {
    font-size: 1rem;
    font-weight: 650;
    color: var(--text);
    margin-bottom: 4px;
}

.research-card-caption {
    font-size: 0.82rem;
    color: var(--muted);
}


/* ==========================================================
   PUBLICATION META / BADGES
   ========================================================== */

.journal-badge {
    display: inline-block;

    padding: 3px 8px;

    border-radius: 5px;

    background: #EFF6FF;

    color: #1D4ED8;

    font-size: 0.72rem;

    font-weight: 650;
}


/* ==========================================================
   RESPONSIVE DESIGN
   ========================================================== */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1.3rem;
        padding-right: 1.3rem;
    }

    .profile-info-grid {
        grid-template-columns: 1fr;
    }

    .profile-info-item:nth-child(odd) {
        border-right: none;
    }

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
# SINGLE-CELL MULTI-VALUE HELPER
# ============================================================

def split_cell(value):
    """
    Split a pipe-separated value from a single dataframe cell.

    Example:
    "Author A | Author B | Author C"
    ->
    ["Author A", "Author B", "Author C"]
    """

    if pd.isna(value):
        return []

    values = [
        item.strip()
        for item in str(value).split("|")
        if item.strip()
    ]

    # Remove duplicates while preserving order
    return list(dict.fromkeys(values))


# ============================================================
# DOI NORMALIZATION
# ============================================================

def normalize_doi(doi):
    """
    Convert DOI values into a consistent format for matching.
    """
    if pd.isna(doi):
        return ""
    doi = str(doi).strip()

    doi = doi.replace(
        "https://doi.org/",
        ""
    )
    doi = doi.replace(
        "http://doi.org/",
        ""
    )
    return doi.lower()


# ============================================================
# DOI LINK
# ============================================================

def make_doi_link(doi):
    """
    Convert a DOI into a clickable https://doi.org URL.
    """

    if pd.isna(doi):
        return None
    doi = str(doi).strip()
    if not doi:
        return None
    if doi.startswith(
        "https://doi.org/"
    ):
        return doi
    if doi.startswith(
        "http://doi.org/"
    ):
        return doi.replace(
            "http://doi.org/",
            "https://doi.org/"
        )
    return f"https://doi.org/{doi}"


# ============================================================
# ARTICLE PROFILE HELPER
# ============================================================

def render_article_profile(
    selected_doi,
    filtered_df,
    selected_journal,
    return_page,
    return_label,
    return_params=None,
    selected_author=None
):

    # ========================================================
    # FIND SELECTED ARTICLE
    # ========================================================

    article_match = filtered_df[
        filtered_df["DOI"].apply(normalize_doi)
        ==
        normalize_doi(selected_doi)
    ].copy()

    # ========================================================
    # BACK NAVIGATION HELPER
    # ========================================================

    def go_back():

        st.query_params.clear()
        st.query_params["page"] = return_page

        if return_params:

            for key, value in return_params.items():

                if value is not None:
                    st.query_params[key] = str(value)

        st.rerun()

    # ========================================================
    # ARTICLE NOT FOUND
    # ========================================================

    if article_match.empty:

        st.warning(
            "This article could not be found within "
            "the currently selected journal and year filters."
        )

        if st.button(
            f"← Back to {return_label}",
            key="article_not_found_back"
        ):
            go_back()

        st.stop()

    # One DOI = one article in cleaned dataset
    article = article_match.iloc[0]

    # ========================================================
    # BACK BUTTON
    # ========================================================

    if st.button(
        f"← Back to {return_label}",
        key="article_profile_back"
    ):
        go_back()

    # ========================================================
    # BASIC ARTICLE INFORMATION
    # ========================================================

    article_title = (
        str(article["Title"])
        if pd.notna(article["Title"])
        else "Untitled publication"
    )

    article_year = (
        int(article["Year"])
        if pd.notna(article["Year"])
        else None
    )

    article_citations = (
        int(article["Citation count"])
        if pd.notna(article["Citation count"])
        else 0
    )

    article_date = article["Date"]

    if pd.notna(article_date):

        try:
            article_date_display = pd.to_datetime(
                article_date
            ).strftime("%B %d, %Y")

        except Exception:
            article_date_display = str(article_date)

    else:
        article_date_display = "Not available"

    # ========================================================
    # OPEN ACCESS
    # ========================================================

    open_access = (
        str(article["Open access"])
        if pd.notna(article["Open access"])
        else "Unknown"
    )

    # ========================================================
    # ARTICLE HEADER
    # ========================================================

    st.markdown(
        '<div class="section-label">Article Profile</div>',
        unsafe_allow_html=True
    )

    st.title(article_title)

    st.caption(
        f"{selected_journal}"
        +
        (
            f" · {article_year}"
            if article_year
            else ""
        )
    )

    # ========================================================
    # ARTICLE METRICS
    # ========================================================

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Citations",
        f"{article_citations:,}"
    )

    metric2.metric(
        "Open Access",
        open_access
    )

    metric3.metric(
        "Publication Year",
        article_year
        if article_year
        else "Unknown"
    )

    # ========================================================
    # AUTHORS & CO-AUTHORS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">Research Team</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Authors & Co-authors"
    )

    article_authors = split_cell(
        article["Author"]
    )

    if article_authors:

        author_links = pd.DataFrame(
            {
                "Author": article_authors
            }
        )

        author_links["Profile"] = (
            author_links["Author"]
            .apply(
                lambda name:
                    f"?page=Authors"
                    f"&author={quote(str(name))}"
                    f"&name={quote(str(name))}"
            )
        )

        author_links["Context"] = (
            author_links["Author"]
            .apply(
                lambda name:
                    "Selected author"
                    if (
                        selected_author
                        and name == selected_author
                    )
                    else ""
            )
        )

        st.dataframe(
            author_links[
                [
                    "Profile",
                    "Context"
                ]
            ],

            use_container_width=True,
            hide_index=True,

            column_config={

                "Profile":
                    st.column_config.LinkColumn(
                        "Author",
                        display_text=r"name=([^&]+)",
                        width="large"
                    ),

                "Context":
                    st.column_config.TextColumn(
                        "",
                        width="medium"
                    )
            }
        )

    else:

        st.info(
            "Author information is not available "
            "for this publication."
        )

    # ========================================================
    # INSTITUTIONS REPRESENTED
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">Affiliations</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Institutions Represented"
    )

    institutions = split_cell(
        article["Institution"]
    )

    if institutions:

        st.write(
            " · ".join(institutions)
        )

    else:

        st.caption(
            "Institution information is not available "
            "for this publication."
        )

    st.caption(
        "Institutions are reported at the article level. "
        "The current dataset does not preserve the exact "
        "author-to-institution relationship."
    )

    # ========================================================
    # COUNTRIES REPRESENTED
    # ========================================================

    st.markdown(
        '<div class="section-label" '
        'style="margin-top:25px;">'
        'Geographic Representation'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Countries Represented"
    )

    countries = []

    for country_code in split_cell(
        article["Country"]
    ):

        country_name = country_code_to_name(
            country_code
        )

        if country_name:
            countries.append(
                country_name
            )

    countries = list(
        dict.fromkeys(countries)
    )

    if countries:

        st.write(
            " · ".join(countries)
        )

    else:

        st.caption(
            "Country information is not available "
            "for this publication."
        )

    # ========================================================
    # RESEARCH TOPICS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">Research Content</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Research Topics"
    )

    topics = split_cell(
        article["Topic"]
    )

    if topics:

        st.write(
            " · ".join(topics)
        )

    else:

        st.caption(
            "Topic information is not available "
            "for this publication."
        )

    # ========================================================
    # KEYWORDS
    # ========================================================

    st.markdown(
        '<div class="section-label" '
        'style="margin-top:25px;">'
        'Keywords'
        '</div>',
        unsafe_allow_html=True
    )

    keywords = split_cell(
        article["Keyword"]
    )

    if keywords:

        st.write(
            " · ".join(keywords)
        )

    else:

        st.caption(
            "Keyword information is not available "
            "for this publication."
        )

    # ========================================================
    # RESEARCH CLASSIFICATION
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">'
        'OpenAlex Classification'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Research Classification"
    )

    classification_columns = st.columns(3)

    # --------------------------------------------------------
    # DOMAIN
    # --------------------------------------------------------

    with classification_columns[0]:

        st.markdown(
            "**Domain**"
        )

        domains = split_cell(
            article["Domain"]
        )

        if domains:

            st.write(
                " · ".join(domains)
            )

        else:

            st.caption(
                "Not available"
            )

    # --------------------------------------------------------
    # FIELD
    # --------------------------------------------------------

    with classification_columns[1]:

        st.markdown(
            "**Field**"
        )

        fields = split_cell(
            article["Field"]
        )

        if fields:

            st.write(
                " · ".join(fields)
            )

        else:

            st.caption(
                "Not available"
            )

    # --------------------------------------------------------
    # SUBFIELD
    # --------------------------------------------------------

    with classification_columns[2]:

        st.markdown(
            "**Subfield**"
        )

        subfields = split_cell(
            article["Subfield"]
        )

        if subfields:

            st.write(
                " · ".join(subfields)
            )

        else:

            st.caption(
                "Not available"
            )

    # ========================================================
    # ABSTRACT
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">Abstract</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Abstract"
    )

    if (
        pd.notna(article["Abstract"])
        and
        str(article["Abstract"]).strip()
    ):

        st.write(
            str(
                article["Abstract"]
            ).strip()
        )

    else:

        st.info(
            "An abstract is not available for this "
            "publication in the current dataset."
        )

    # ========================================================
    # ARTICLE INFORMATION
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">'
        'Publication Details'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Article Information"
    )

    info1, info2 = st.columns(2)

    with info1:

        st.markdown(
            "**Journal**"
        )

        st.write(
            selected_journal
        )

        st.markdown(
            "**Publication Date**"
        )

        st.write(
            article_date_display
        )

    with info2:

        st.markdown(
            "**DOI**"
        )

        st.write(
            selected_doi
        )

        st.markdown(
            "**Citation Count**"
        )

        st.write(
            f"{article_citations:,}"
        )

    # ========================================================
    # DOI BUTTON
    # ========================================================

    doi_url = make_doi_link(
        selected_doi
    )

    if doi_url:

        st.link_button(
            "Open DOI ↗",
            doi_url
        )

    # ========================================================
    # DATA NOTE
    # ========================================================

    st.caption(
        "Article metadata and citation information are "
        "based on the current OpenAlex-derived dataset. "
        "Citation counts may change over time."
    )

    st.stop()

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
    # READ URL PARAMETERS
    # ========================================================

    author_from_url = st.query_params.get("author")
    article_from_url = st.query_params.get("article")

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

        # Remove duplicate names within the same article
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
    # AUTHOR DIRECTORY
    # ========================================================

    if st.session_state.selected_author is None:

        # ----------------------------------------------------
        # HEADER
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
        # AUTHOR SUMMARY
        # ====================================================

        author_summary = (
            author_df
            .groupby("Author")
            .agg(
                Publications=("DOI", "nunique"),
                Citations=("Citations", "sum"),
                First_Publication=("Year", "min"),
                Latest_Publication=("Year", "max")
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
            f"{int(author_summary['Publications'].max()):,}"
        )

        a4.metric(
            "Highest Citation Total",
            f"{int(author_summary['Citations'].max()):,}"
        )

        # ====================================================
        # SEARCH / FILTER / SORT
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
            author_summary["Publications"]
            >= min_author_papers
        ].copy()

        if author_search:

            display_authors = display_authors[
                display_authors["Author"].str.contains(
                    author_search,
                    case=False,
                    na=False
                )
            ]

        # ====================================================
        # RANKING LOGIC
        # ====================================================

        if author_sort == "Publications":

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

        else:

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
        # ADD RANK
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
        # RANKING HEADER
        # ====================================================

        st.divider()
        title_col, count_col = st.columns([3, 1])
        with title_col:
            st.subheader("Author Ranking")

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
                    "Citations / Paper",
                    "First",
                    "Latest"
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
        # CLICKABLE AUTHOR LINKS
        # ====================================================

        ranking_table["Author Link"] = (
            ranking_table["Author"].apply(
                lambda name:
                f"?page=Authors"
                f"&author={quote(str(name))}"
            )
        )

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

        # ====================================================
        # DISPLAY AUTHOR TABLE
        # ====================================================

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
    # AUTHOR / ARTICLE PROFILE AREA
    # ========================================================

    else:

        selected_author = (
            st.session_state.selected_author
        )

        # ====================================================
        # ARTICLE PROFILE
        # ====================================================

        if article_from_url:

            selected_doi = unquote(
                str(article_from_url)
            )

            render_article_profile(
                selected_doi=selected_doi,
                filtered_df=filtered_df,
                selected_journal=selected_journal,

                return_page="Authors",

                return_label=selected_author,

                return_params={
                    "author": selected_author
                },

                selected_author=selected_author
            )

        # ====================================================
        # AUTHOR PROFILE
        # ====================================================

        # ====================================================
        # BACK TO AUTHORS
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
                author_df["Author"]
                == selected_author
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
            author_articles["DOI"]
            .nunique()
        )

        total_author_citations = int(
            author_articles["Citations"]
            .fillna(0)
            .sum()
        )

        average_citations = (
            total_author_citations / total_papers
            if total_papers > 0
            else 0
        )

        first_year = int(
            author_articles["Year"].min()
        )

        latest_year = int(
            author_articles["Year"].max()
        )


        # ====================================================
        # DSS H-INDEX
        # ====================================================

        citation_values = sorted(
            author_articles["Citations"]
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
                for word in selected_author.split()
                if word
            ][:2]
        )


        # ====================================================
        # AUTHOR PROFILE HERO
        # ====================================================

        st.markdown(
            f"""
            <div class="profile-hero">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:24px;
                ">

                    <div class="profile-avatar">
                        {initials}
                    </div>

                    <div style="flex:1;">

                        <div class="profile-hero-label">
                            Author Profile
                        </div>

                        <div class="profile-hero-title">
                            {selected_author}
                        </div>

                        <div class="profile-hero-subtitle">
                            {selected_journal}
                            &nbsp;·&nbsp;
                            {first_year}–{latest_year}
                        </div>

                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
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
            author_articles["Topic"]
        )

        if topic_values:

            author_topics = (
                pd.Series(topic_values)
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

        st.subheader("Publications")

        st.caption(
            "Click a publication title to view its article profile."
        )


        # ====================================================
        # PREPARE PUBLICATION TABLE
        # ====================================================

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
                ["Year", "Citations"],
                ascending=[False, False]
            )
            .copy()
        )


        # ====================================================
        # CREATE INTERNAL ARTICLE LINKS
        # ====================================================

        publication_table["Publication"] = (
            publication_table.apply(
                lambda row:
                f"?page=Authors"
                f"&author={quote(str(selected_author))}"
                f"&article={quote(str(row['DOI']))}"
                f"&title={quote(str(row['Title']))}",
                axis=1
            )
        )


        # ====================================================
        # FINAL DISPLAY TABLE
        # ====================================================

        publication_display = (
            publication_table[
                [
                    "Year",
                    "Publication",
                    "Citations",
                    "DOI Link"
                ]
            ]
            .copy()
        )


        # ====================================================
        # DISPLAY PUBLICATIONS
        # ====================================================

        st.dataframe(
            publication_display,
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

                "Publication":
                    st.column_config.LinkColumn(
                        "Publication",
                        display_text=r"title=([^&]+)",
                        width="large"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d",
                        width="small"
                    ),

                "DOI Link":
                    st.column_config.LinkColumn(
                        "DOI",
                        display_text="Open DOI",
                        width="small"
                    )
            }
        )


        # ====================================================
        # METHODOLOGY NOTE
        # ====================================================

        st.caption(
            "Author profiles represent participation in Decision "
            "Support Systems publications. The current dataset does not "
            "preserve exact author-to-institution relationships."
        )


# ============================================================
# INSTITUTIONS
# ============================================================

elif page == "Institutions":

    institution_from_url = st.query_params.get("institution")
    selected_institution = (
        unquote(str(institution_from_url))
        if institution_from_url
        else None
    )

    institution_rows = []

    for _, row in filtered_df.iterrows():

        if pd.isna(row["Institution"]):
            continue

        institutions = list(dict.fromkeys(
            institution.strip()
            for institution in str(row["Institution"]).split("|")
            if institution.strip()
        ))

        for institution in institutions:

            institution_rows.append({
                "Institution": institution,
                "DOI": row["DOI"],
                "Year": row["Year"],
                "Date": row["Date"],
                "Citations": row["Citation count"],
                "Title": row["Title"],
                "Topic": row["Topic"],
                "Keyword": row["Keyword"],
                "Author": row["Author"],
                "Country": row["Country"],
                "Open access": row["Open access"]
            })

    institution_df = pd.DataFrame(institution_rows)

    if institution_df.empty:

        st.warning(
            "No institution information is available "
            "for the selected period."
        )
        st.stop()

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

    if selected_institution is None:

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">Research Community</div>',
            unsafe_allow_html=True
        )
        st.header("Institutions")
        st.caption(
            f"{selected_journal} · "
            f"{year_range[0]}–{year_range[1]}"
        )

        total_institutions = institution_summary["Institution"].nunique()
        active_institutions = (
            institution_summary["Publications"] >= 5
        ).sum()
        most_publications = institution_summary["Publications"].max()
        highest_citations = institution_summary["Citations"].max()

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Institutions", f"{total_institutions:,}")
        k2.metric(
            "Institutions with 5+ Papers",
            f"{active_institutions:,}"
        )
        k3.metric("Most Publications", f"{most_publications:,}")
        k4.metric("Highest Citation Total", f"{highest_citations:,}")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-label">Find Institutions</div>',
            unsafe_allow_html=True
        )

        search_col, min_col, sort_col = st.columns([2.5, 1, 1.4])

        with search_col:
            institution_search = st.text_input(
                "Search institution",
                placeholder=(
                    "Search by institution name..."
                )
            )

        with min_col:
            min_institution_papers = st.number_input(
                "Minimum papers",
                min_value=1,
                value=1,
                step=1,
                key="institution_min_papers"
            )

        with sort_col:
            institution_sort = st.selectbox(
                "Sort by",
                [
                    "Publications",
                    "Citations",
                    "Latest Publication",
                    "Institution"
                ],
                key="institution_sort"
            )

        display_institutions = institution_summary[
            institution_summary["Publications"] >= min_institution_papers
        ].copy()

        if institution_search:
            display_institutions = display_institutions[
                display_institutions["Institution"].str.contains(
                    institution_search,
                    case=False,
                    na=False,
                    regex=False
                )
            ]

        sort_mapping = {
            "Publications": "Publications",
            "Citations": "Citations",
            "Latest Publication": "Latest_Publication",
            "Institution": "Institution"
        }

        display_institutions = display_institutions.sort_values(
            sort_mapping[institution_sort],
            ascending=institution_sort == "Institution"
        )

        display_institutions["Institution Profile"] = (
            display_institutions["Institution"].apply(
                lambda name: (
                    f"?page=Institutions"
                    f"&institution={quote(str(name))}"
                    f"&name={quote(str(name))}"
                )
            )
        )

        st.divider()
        title_col, count_col = st.columns([3, 1])

        with title_col:
            st.subheader("Institution Register")

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

        institution_limit = st.selectbox(
            "Show",
            [25, 50, 100, 250],
            index=1,
            format_func=lambda x: f"{x} institutions",
            key="institution_rows"
        )

        table_df = display_institutions.head(institution_limit).rename(
            columns={
                "First_Publication": "First Publication",
                "Latest_Publication": "Latest Publication"
            }
        )

        institution_display = table_df[
            [
                "Institution Profile",
                "Publications",
                "Citations",
                "First Publication",
                "Latest Publication"
            ]
        ]

        st.dataframe(
            institution_display,
            use_container_width=True,
            hide_index=True,
            height=650,
            column_config={
                "Institution Profile": st.column_config.LinkColumn(
                    "Institution",
                    display_text=r"name=([^&]+)",
                    width="large"
                ),
                "Publications": st.column_config.NumberColumn(
                    "Papers",
                    format="%d"
                ),
                "Citations": st.column_config.NumberColumn(
                    "Citations",
                    format="%d"
                ),
                "First Publication": st.column_config.NumberColumn(
                    "First",
                    format="%d"
                ),
                "Latest Publication": st.column_config.NumberColumn(
                    "Latest",
                    format="%d"
                )
            }
        )

        st.caption(
            "Institution counts represent participation in publications. "
            "A publication involving multiple institutions is counted "
            "once for each participating institution."
        )

    else:

        # ====================================================
        # ARTICLE PROFILE
        # ====================================================

        article_from_url = st.query_params.get("article")

        if article_from_url:

            selected_doi = unquote(
                str(article_from_url)
            )

            render_article_profile(
                selected_doi=selected_doi,
                filtered_df=filtered_df,
                selected_journal=selected_journal,

                return_page="Institutions",

                return_label=selected_institution,

                return_params={
                    "institution": selected_institution
                }
            )

        if st.button("← Back to Institutions"):
            st.query_params.clear()
            st.query_params[
                "page"
            ] = "Institutions"
            st.rerun()

        institution_articles = institution_df[
            institution_df["Institution"] == selected_institution
        ].drop_duplicates(subset=["DOI"]).copy()

        if institution_articles.empty:
            st.warning(
                "The selected institution could not be found within "
                "the current filters."
            )
            st.stop()

        st.markdown(
            '<div class="section-label">Institution Profile</div>',
            unsafe_allow_html=True
        )
        st.title(selected_institution)
        st.caption(
            f"{selected_journal} · "
            f"{year_range[0]}–{year_range[1]}"
        )

        total_papers = institution_articles["DOI"].nunique()
        total_citations = institution_articles["Citations"].fillna(0).sum()
        average_citations = (
            total_citations / total_papers if total_papers else 0
        )
        first_year = int(institution_articles["Year"].min())
        latest_year = int(institution_articles["Year"].max())

        m1, m2, m3 = st.columns(3)
        m1.metric("Publications", f"{total_papers:,}")
        m2.metric("Total Citations", f"{int(total_citations):,}")
        m3.metric("Avg. Citations / Paper", f"{average_citations:,.1f}")

        m4, m5 = st.columns(2)
        m4.metric("First Publication", first_year)
        m5.metric("Latest Publication", latest_year)

        st.divider()
        st.markdown(
            '<div class="section-label">Publication Activity</div>',
            unsafe_allow_html=True
        )
        st.subheader("Output Over Time")

        yearly_output = (
            institution_articles.groupby("Year")
            .agg(Publications=("DOI", "nunique"))
            .reset_index()
            .sort_values("Year")
        )
        output_fig = px.bar(yearly_output, x="Year", y="Publications")
        output_fig.update_layout(
            xaxis_title=None,
            yaxis_title="Publications",
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(output_fig, use_container_width=True)

        st.divider()
        st.markdown(
            '<div class="section-label">Research Focus</div>',
            unsafe_allow_html=True
        )
        st.subheader("Leading Research Topics")

        topic_rows = []
        for _, row in institution_articles.iterrows():
            if pd.isna(row["Topic"]):
                continue
            topics = list(dict.fromkeys(
                topic.strip()
                for topic in str(row["Topic"]).split("|")
                if topic.strip()
            ))
            for topic in topics:
                topic_rows.append({
                    "Topic": topic,
                    "DOI": row["DOI"],
                    "Citations": row["Citations"]
                })

        institution_topics = pd.DataFrame(topic_rows)
        if not institution_topics.empty:
            topic_summary = (
                institution_topics.groupby("Topic")
                .agg(
                    Publications=("DOI", "nunique"),
                    Citations=("Citations", "sum")
                )
                .reset_index()
                .sort_values(
                    [
                        "Publications",
                        "Citations"
                    ],
                    ascending=[
                        False,
                        False
                    ]
                )
                .head(10)
            )
            topic_plot = (
                topic_summary
                .sort_values(
                    "Publications",
                    ascending=True
                )
            )

            fig_topic_institutions = (
                px.bar(
                    topic_plot,
                    x="Publications",
                    y="Topic",
                    orientation="h"
                )
            )

            fig_topic_institutions.update_layout(
                height=420,
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
                fig_topic_institutions,
                use_container_width=True
            )

        else:
            st.caption(
                "Topic information is not available for this institution."
            )

        st.divider()
        st.markdown(
            '<div class="section-label">Geographic Participation</div>',
            unsafe_allow_html=True
        )
        st.subheader("Countries Represented")

        institution_countries = []
        for value in institution_articles["Country"].dropna():
            for code in str(value).split("|"):
                code = code.strip()
                if code:
                    country_name = country_code_to_name(code)
                    if country_name:
                        institution_countries.append(country_name)

        institution_countries = sorted(set(institution_countries))
        if institution_countries:
            st.write(" · ".join(institution_countries))
        else:
            st.caption("Country information is not available.")

        st.caption(
            "Countries are reported at the article level. They should not "
            "be interpreted as the physical location of the selected "
            "institution."
        )

        st.divider()
        st.markdown(
            '<div class="section-label">Research Output</div>',
            unsafe_allow_html=True
        )
        st.subheader("Publications")
        st.caption("Click a publication title to view its article profile.")

        publication_table = (
            institution_articles[["Year", "Title", "Citations", "DOI"]]
            .sort_values(["Year", "Citations"], ascending=[False, False])
            .copy()
        )
        publication_table["Publication"] = publication_table.apply(
            lambda row: (
                f"?page=Institutions"
                f"&institution={quote(str(selected_institution))}"
                f"&article={quote(str(row['DOI']))}"
                f"&title={quote(str(row['Title']))}"
            ),
            axis=1
        )

        def institution_doi_link(doi):
            if pd.isna(doi):
                return None
            doi = str(doi).strip()
            if not doi:
                return None
            if doi.startswith("https://doi.org/"):
                return doi
            if doi.startswith("http://doi.org/"):
                return doi.replace("http://doi.org/", "https://doi.org/")
            return f"https://doi.org/{doi}"

        publication_table["DOI Link"] = publication_table["DOI"].apply(
            institution_doi_link
        )
        publication_display = (
            publication_table[
                [
                    "Year",
                    "Publication",
                    "Citations",
                    "DOI Link"
                ]
            ]
            .copy()
        )


        # ====================================================
        # DISPLAY PUBLICATIONS
        # ====================================================

        st.dataframe(
            publication_display,
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

                "Publication":
                    st.column_config.LinkColumn(
                        "Publication",
                        display_text=r"title=([^&]+)",
                        width="large"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d",
                        width="small"
                    ),

                "DOI Link":
                    st.column_config.LinkColumn(
                        "DOI",
                        display_text="Open DOI",
                        width="small"
                    )
            }
        )


        # ====================================================
        # METHODOLOGY NOTE
        # ====================================================

        st.caption(
            "Institution profiles represent participation in Decision "
            "Support Systems publications. The current dataset does not "
            "preserve exact author-to-institution relationships."
        )


# ============================================================
# COUNTRIES
# ============================================================

elif page == "Countries":

    # ========================================================
    # READ URL PARAMETERS
    # ========================================================

    country_from_url = st.query_params.get("country")

    selected_country = (
        unquote(str(country_from_url))
        if country_from_url
        else None
    )


    # ========================================================
    # BUILD COUNTRY-LEVEL DATA
    # ========================================================

    country_rows = []

    for _, row in filtered_df.iterrows():

        if pd.isna(row["Country"]):
            continue

        countries = split_cell(
            row["Country"]
        )

        for country_code in countries:

            country_name = country_code_to_name(
                country_code
            )

            country_rows.append(
                {
                    "Country Code":
                        str(country_code).upper(),

                    "Country":
                        country_name,

                    "DOI":
                        row["DOI"],

                    "Title":
                        row["Title"],

                    "Year":
                        row["Year"],

                    "Date":
                        row["Date"],

                    "Citations":
                        row["Citation count"],

                    "Author":
                        row["Author"],

                    "Institution":
                        row["Institution"],

                    "Topic":
                        row["Topic"],

                    "Keyword":
                        row["Keyword"],

                    "Open access":
                        row["Open access"]
                }
            )


    country_df = pd.DataFrame(
        country_rows
    )


    # ========================================================
    # NO COUNTRY DATA
    # ========================================================

    if country_df.empty:

        st.warning(
            "No country information is available "
            "for the selected period."
        )

        st.stop()


    # ========================================================
    # COUNTRY SUMMARY
    # ========================================================

    country_summary = (
        country_df
        .groupby(
            [
                "Country Code",
                "Country"
            ]
        )
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


    # ========================================================
    # COUNTRY DIRECTORY
    # ========================================================

    if selected_country is None:

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">'
            'Geographic Analysis'
            '</div>',
            unsafe_allow_html=True
        )

        st.header(
            "Countries"
        )

        st.caption(
            f"{selected_journal} · "
            f"{year_range[0]}–{year_range[1]}"
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

        most_publications = int(
            country_summary[
                "Publications"
            ].max()
        )

        highest_citations = int(
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
        # SEARCH / FILTER / SORT
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

            country_search = st.text_input(
                "Search country",
                placeholder=(
                    "Search by country name..."
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

            country_sort = st.selectbox(
                "Sort by",
                [
                    "Publications",
                    "Citations",
                    "Latest Publication",
                    "Country"
                ],
                key="country_sort"
            )


        # ====================================================
        # FILTER COUNTRIES
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
                        na=False,
                        regex=False
                    )
                ]
            )


        # ====================================================
        # SORTING
        # ====================================================

        if country_sort == "Publications":

            display_countries = (
                display_countries
                .sort_values(
                    [
                        "Publications",
                        "Citations",
                        "Latest_Publication",
                        "Country"
                    ],
                    ascending=[
                        False,
                        False,
                        False,
                        True
                    ]
                )
            )


        elif country_sort == "Citations":

            display_countries = (
                display_countries
                .sort_values(
                    [
                        "Citations",
                        "Publications",
                        "Latest_Publication",
                        "Country"
                    ],
                    ascending=[
                        False,
                        False,
                        False,
                        True
                    ]
                )
            )


        elif country_sort == "Latest Publication":

            display_countries = (
                display_countries
                .sort_values(
                    [
                        "Latest_Publication",
                        "Publications",
                        "Citations",
                        "Country"
                    ],
                    ascending=[
                        False,
                        False,
                        False,
                        True
                    ]
                )
            )


        else:

            display_countries = (
                display_countries
                .sort_values(
                    "Country",
                    ascending=True
                )
            )


        display_countries = (
            display_countries
            .reset_index(
                drop=True
            )
        )


        # ====================================================
        # RANK
        # ====================================================

        display_countries.insert(
            0,
            "Rank",
            range(
                1,
                len(display_countries) + 1
            )
        )


        # ====================================================
        # CLICKABLE COUNTRY LINKS
        # ====================================================

        display_countries[
            "Country Profile"
        ] = (
            display_countries[
                "Country"
            ]
            .apply(
                lambda name:
                f"?page=Countries"
                f"&country={quote(str(name))}"
                f"&name={quote(str(name))}"
            )
        )


        # ====================================================
        # COUNTRY REGISTER
        # ====================================================

        st.divider()


        title_col, count_col = (
            st.columns(
                [3, 1]
            )
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


        st.caption(
            "Click a country name to view "
            "its research profile."
        )


        # ====================================================
        # DISPLAY TABLE
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


        country_display = (
            country_table[
                [
                    "Rank",
                    "Country Profile",
                    "Country Code",
                    "Publications",
                    "Citations",
                    "First Publication",
                    "Latest Publication"
                ]
            ]
            .copy()
        )


        st.dataframe(
            country_display,

            use_container_width=True,

            hide_index=True,

            height=600,

            column_config={

                "Rank":
                    st.column_config.NumberColumn(
                        "#",
                        width="small",
                        format="%d"
                    ),

                "Country Profile":
                    st.column_config.LinkColumn(
                        "Country",
                        display_text=r"name=([^&]+)",
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


    # ========================================================
    # COUNTRY PROFILE
    # ========================================================

    else:

        # ====================================================
        # ARTICLE PROFILE
        # ====================================================

        article_from_url = st.query_params.get("article")

        if article_from_url:

            selected_doi = unquote(
                str(article_from_url)
            )

            render_article_profile(
                selected_doi=selected_doi,
                filtered_df=filtered_df,
                selected_journal=selected_journal,

                return_page="Countries",

                return_label=selected_country,

                return_params={
                    "country": selected_country
                }
            )

        # ====================================================
        # BACK TO COUNTRIES
        # ====================================================

        if st.button(
            "← Back to Countries"
        ):

            st.query_params.clear()

            st.query_params[
                "page"
            ] = "Countries"

            st.rerun()


        # ====================================================
        # SELECT COUNTRY ARTICLES
        # ====================================================

        country_articles = (
            country_df[
                country_df[
                    "Country"
                ] == selected_country
            ]
            .drop_duplicates(
                subset="DOI"
            )
            .copy()
        )


        # ====================================================
        # COUNTRY NOT FOUND
        # ====================================================

        if country_articles.empty:

            st.warning(
                "The selected country could not be found "
                "within the current filters."
            )

            st.stop()


        # ====================================================
        # BASIC METRICS
        # ====================================================

        total_papers = (
            country_articles[
                "DOI"
            ].nunique()
        )

        total_citations = int(
            country_articles[
                "Citations"
            ]
            .fillna(0)
            .sum()
        )

        average_citations = (
            total_citations /
            total_papers
            if total_papers > 0
            else 0
        )

        first_year = int(
            country_articles[
                "Year"
            ].min()
        )

        latest_year = int(
            country_articles[
                "Year"
            ].max()
        )


        # ====================================================
        # COUNTRY PROFILE HEADER
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'Country Profile'
            '</div>',
            unsafe_allow_html=True
        )

        st.title(
            selected_country
        )

        st.caption(
            f"{selected_journal} · "
            f"{first_year}–{latest_year}"
        )


        # ====================================================
        # PROFILE METRICS
        # ====================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        m1, m2, m3 = st.columns(3)


        m1.metric(
            "Publications",
            f"{total_papers:,}"
        )

        m2.metric(
            "Total Citations",
            f"{total_citations:,}"
        )

        m3.metric(
            "Avg. Citations / Paper",
            f"{average_citations:,.1f}"
        )


        m4, m5 = st.columns(2)


        m4.metric(
            "First Publication",
            f"{first_year}"
        )

        m5.metric(
            "Latest Publication",
            f"{latest_year}"
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


        country_yearly = (
            country_articles
            .groupby(
                "Year"
            )
            .agg(
                Publications=(
                    "DOI",
                    "nunique"
                )
            )
            .reset_index()
            .sort_values(
                "Year"
            )
        )


        fig_country_output = px.bar(
            country_yearly,
            x="Year",
            y="Publications"
        )


        fig_country_output.update_layout(
            height=350,
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


        fig_country_output.update_xaxes(
            dtick=1
        )


        st.plotly_chart(
            fig_country_output,
            use_container_width=True
        )


        # ====================================================
        # LEADING RESEARCH TOPICS
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-label">'
            'Research Focus'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Leading Research Topics"
        )


        country_topic_rows = []


        for _, row in (
            country_articles.iterrows()
        ):

            for topic in split_cell(
                row["Topic"]
            ):

                country_topic_rows.append(
                    {
                        "Topic":
                            topic,

                        "DOI":
                            row["DOI"],

                        "Citations":
                            row["Citations"]
                    }
                )


        country_topics = pd.DataFrame(
            country_topic_rows
        )


        if not country_topics.empty:

            topic_summary = (
                country_topics
                .groupby(
                    "Topic"
                )
                .agg(
                    Publications=(
                        "DOI",
                        "nunique"
                    ),

                    Citations=(
                        "Citations",
                        "sum"
                    )
                )
                .reset_index()
                .sort_values(
                    [
                        "Publications",
                        "Citations"
                    ],
                    ascending=[
                        False,
                        False
                    ]
                )
                .head(10)
            )


            topic_plot = (
                topic_summary
                .sort_values(
                    "Publications",
                    ascending=True
                )
            )


            fig_country_topics = px.bar(
                topic_plot,
                x="Publications",
                y="Topic",
                orientation="h"
            )


            fig_country_topics.update_layout(
                height=420,
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
                fig_country_topics,
                use_container_width=True
            )


        else:

            st.info(
                "Topic information is not available "
                "for this country's publications."
            )


        # ====================================================
        # INSTITUTIONAL PARTICIPATION
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-label">'
            'Institutional Participation'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Leading Institutions"
        )


        country_institution_rows = []


        for _, row in (
            country_articles.iterrows()
        ):

            for institution in split_cell(
                row["Institution"]
            ):

                country_institution_rows.append(
                    {
                        "Institution":
                            institution,

                        "DOI":
                            row["DOI"],

                        "Citations":
                            row["Citations"]
                    }
                )


        country_institutions = (
            pd.DataFrame(
                country_institution_rows
            )
        )


        if not country_institutions.empty:

            institution_summary = (
                country_institutions
                .groupby(
                    "Institution"
                )
                .agg(
                    Publications=(
                        "DOI",
                        "nunique"
                    ),

                    Citations=(
                        "Citations",
                        "sum"
                    )
                )
                .reset_index()
                .sort_values(
                    [
                        "Publications",
                        "Citations",
                        "Institution"
                    ],
                    ascending=[
                        False,
                        False,
                        True
                    ]
                )
                .head(10)
            )


            institution_plot = (
                institution_summary
                .sort_values(
                    "Publications",
                    ascending=True
                )
            )


            fig_country_institutions = (
                px.bar(
                    institution_plot,
                    x="Publications",
                    y="Institution",
                    orientation="h"
                )
            )


            fig_country_institutions.update_layout(
                height=440,
                xaxis_title="Publications",
                yaxis_title="",
                showlegend=False,
                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=30
                )
            )


            st.plotly_chart(
                fig_country_institutions,
                use_container_width=True
            )


        else:

            st.info(
                "Institution information is not "
                "available for this country's publications."
            )


        st.caption(
            "Institutions shown here are institutions "
            "participating in publications associated with "
            f"{selected_country}. The current dataset does not "
            "preserve the exact institution-to-country "
            "relationship, so this should not be interpreted "
            "as a list of institutions physically located "
            "in the selected country."
        )


        # ====================================================
        # PUBLICATIONS
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

        st.caption(
            "Publications associated with "
            f"{selected_country}."
        )


        # ====================================================
        # PREPARE PUBLICATION TABLE
        # ====================================================

        publication_table = (
            country_articles[
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
        # INTERNAL ARTICLE LINKS
        # ====================================================

        publication_table[
            "Publication"
        ] = (
            publication_table
            .apply(
                lambda row:
                    f"?page=Countries"
                    f"&country={quote(str(selected_country))}"
                    f"&article={quote(str(row['DOI']))}"
                    f"&title={quote(str(row['Title']))}",
                axis=1
            )
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
                make_doi_link
            )
        )


        publication_display = (
            publication_table[
                [
                    "Year",
                    "Publication",
                    "Citations",
                    "DOI Link"
                ]
            ]
            .copy()
        )


        # ====================================================
        # DISPLAY PUBLICATIONS
        # ====================================================

        st.dataframe(
            publication_display,
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

                "Publication":
                    st.column_config.LinkColumn(
                        "Publication",
                        display_text=r"title=([^&]+)",
                        width="large"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d",
                        width="small"
                    ),

                "DOI Link":
                    st.column_config.LinkColumn(
                        "DOI",
                        display_text="Open DOI",
                        width="small"
                    )
            }
        )


        # ====================================================
        # METHODOLOGY NOTE
        # ====================================================

        st.caption(
            "Country profiles represent participation in "
            f"{selected_journal} publications. Publications "
            "involving multiple countries are included in "
            "the profile of each participating country."
        )


# ============================================================
# RESEARCH TOPICS
# ============================================================

elif page == "Research Topics":

    # ========================================================
    # READ URL PARAMETERS
    # ========================================================

    topic_from_url = st.query_params.get("topic")

    selected_topic = (
        unquote(str(topic_from_url))
        if topic_from_url
        else None
    )


    # ========================================================
    # BUILD TOPIC-LEVEL DATA
    # ========================================================

    topic_rows = []

    for _, row in filtered_df.iterrows():

        if pd.isna(row["Topic"]):
            continue

        topics = split_cell(
            row["Topic"]
        )

        for topic in topics:

            topic_rows.append(
                {
                    "Topic": topic,
                    "DOI": row["DOI"],
                    "Title": row["Title"],
                    "Year": row["Year"],
                    "Date": row["Date"],
                    "Citations": row["Citation count"],
                    "Author": row["Author"],
                    "Institution": row["Institution"],
                    "Country": row["Country"],
                    "Keyword": row["Keyword"],
                    "Open access": row["Open access"]
                }
            )


    topic_df = pd.DataFrame(
        topic_rows
    )


    # ========================================================
    # NO TOPIC DATA
    # ========================================================

    if topic_df.empty:

        st.warning(
            "No topic information is available "
            "for the selected period."
        )

        st.stop()


    # ========================================================
    # TOPIC SUMMARY
    # ========================================================

    topic_summary = (
        topic_df
        .groupby("Topic")
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


    topic_summary[
        "Citations_per_Paper"
    ] = (
        topic_summary["Citations"]
        /
        topic_summary["Publications"]
    )


    # ========================================================
    # TOPIC DIRECTORY
    # ========================================================

    if selected_topic is None:

        # ----------------------------------------------------
        # PAGE HEADER
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">'
            'Research Landscape'
            '</div>',
            unsafe_allow_html=True
        )

        st.header(
            "Research Topics"
        )

        st.caption(
            f"{selected_journal} · "
            f"{year_range[0]}–{year_range[1]}"
        )


        # ====================================================
        # KPI CARDS
        # ====================================================

        total_topics = (
            topic_summary[
                "Topic"
            ].nunique()
        )

        active_topics = (
            topic_summary[
                "Publications"
            ] >= 10
        ).sum()

        largest_topic = int(
            topic_summary[
                "Publications"
            ].max()
        )

        topic_publications = (
            filtered_df[
                filtered_df[
                    "Topic"
                ].notna()
            ]
            ["DOI"]
            .nunique()
        )

        topic_coverage = (
            topic_publications
            /
            filtered_df[
                "DOI"
            ].nunique()
            * 100
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
        # LEADING TOPICS
        # ====================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-label">'
            'Research Concentration'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Leading Research Topics"
        )


        top_n = st.slider(
            "Number of topics",
            min_value=5,
            max_value=30,
            value=15,
            step=5,
            key="topic_top_n"
        )


        top_topics = (
            topic_summary
            .sort_values(
                [
                    "Publications",
                    "Citations"
                ],
                ascending=[
                    False,
                    False
                ]
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
            height=max(
                450,
                top_n * 32
            ),
            margin=dict(
                l=10,
                r=20,
                t=20,
                b=40
            ),
            showlegend=False
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
            '<div class="section-label">'
            'Topic Evolution'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "Topic Trends Over Time"
        )


        trend_topics = (
            topic_summary
            .sort_values(
                [
                    "Publications",
                    "Citations"
                ],
                ascending=[
                    False,
                    False
                ]
            )
            .head(30)[
                "Topic"
            ]
            .tolist()
        )


        default_topics = (
            trend_topics[:3]
        )


        selected_topics = (
            st.multiselect(
                "Select topics",
                options=trend_topics,
                default=default_topics,
                max_selections=5,
                key="topic_trend_selection"
            )
        )


        if selected_topics:

            topic_trend = (
                topic_df[
                    topic_df[
                        "Topic"
                    ].isin(
                        selected_topics
                    )
                ]
                .groupby(
                    [
                        "Year",
                        "Topic"
                    ]
                )
                .agg(
                    Publications=(
                        "DOI",
                        "nunique"
                    )
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

        title_col, count_col = (
            st.columns(
                [3, 1]
            )
        )


        with title_col:

            st.subheader(
                "Topic Register"
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
                    <b>{len(topic_summary):,}</b>
                    topics identified
                </div>
                """,
                unsafe_allow_html=True
            )


        st.caption(
            "Click a research topic to view "
            "its detailed research profile."
        )


        # ====================================================
        # SEARCH / FILTER / SORT
        # ====================================================

        search_col, min_col, sort_col = (
            st.columns(
                [2.4, 1, 1.4]
            )
        )


        with search_col:

            topic_search = st.text_input(
                "Search topics",
                placeholder=(
                    "Search by topic name..."
                )
            )


        with min_col:

            min_topic_papers = (
                st.number_input(
                    "Minimum papers",
                    min_value=1,
                    value=1,
                    step=1,
                    key="topic_min_papers"
                )
            )


        with sort_col:

            topic_sort = st.selectbox(
                "Sort by",
                [
                    "Publications",
                    "Citations",
                    "Citations per Paper",
                    "Latest Publication",
                    "Topic"
                ],
                key="topic_sort"
            )


        # ====================================================
        # FILTER TOPICS
        # ====================================================

        topic_table = (
            topic_summary[
                topic_summary[
                    "Publications"
                ] >= min_topic_papers
            ]
            .copy()
        )


        if topic_search:

            topic_table = (
                topic_table[
                    topic_table[
                        "Topic"
                    ]
                    .str.contains(
                        topic_search,
                        case=False,
                        na=False,
                        regex=False
                    )
                ]
            )


        # ====================================================
        # SORT TOPICS
        # ====================================================

        if topic_sort == "Publications":

            topic_table = (
                topic_table
                .sort_values(
                    [
                        "Publications",
                        "Citations",
                        "Topic"
                    ],
                    ascending=[
                        False,
                        False,
                        True
                    ]
                )
            )


        elif topic_sort == "Citations":

            topic_table = (
                topic_table
                .sort_values(
                    [
                        "Citations",
                        "Publications",
                        "Topic"
                    ],
                    ascending=[
                        False,
                        False,
                        True
                    ]
                )
            )


        elif topic_sort == "Citations per Paper":

            topic_table = (
                topic_table
                .sort_values(
                    [
                        "Citations_per_Paper",
                        "Citations",
                        "Publications",
                        "Topic"
                    ],
                    ascending=[
                        False,
                        False,
                        False,
                        True
                    ]
                )
            )


        elif topic_sort == "Latest Publication":

            topic_table = (
                topic_table
                .sort_values(
                    [
                        "Latest_Publication",
                        "Publications",
                        "Citations",
                        "Topic"
                    ],
                    ascending=[
                        False,
                        False,
                        False,
                        True
                    ]
                )
            )


        else:

            topic_table = (
                topic_table
                .sort_values(
                    "Topic",
                    ascending=True
                )
            )


        topic_table = (
            topic_table
            .reset_index(
                drop=True
            )
        )


        # ====================================================
        # RANK
        # ====================================================

        topic_table.insert(
            0,
            "Rank",
            range(
                1,
                len(topic_table) + 1
            )
        )


        # ====================================================
        # CLICKABLE TOPIC LINKS
        # ====================================================

        topic_table[
            "Topic Profile"
        ] = (
            topic_table[
                "Topic"
            ]
            .apply(
                lambda name:
                    f"?page={quote('Research Topics')}"
                    f"&topic={quote(str(name))}"
                    f"&name={quote(str(name))}"
            )
        )


        # ====================================================
        # RENAME COLUMNS
        # ====================================================

        topic_table = (
            topic_table
            .rename(
                columns={
                    "Citations_per_Paper":
                        "Citations / Paper",

                    "First_Publication":
                        "First Publication",

                    "Latest_Publication":
                        "Latest Publication"
                }
            )
        )


        # ====================================================
        # FINAL DISPLAY
        # ====================================================

        topic_display = (
            topic_table[
                [
                    "Rank",
                    "Topic Profile",
                    "Publications",
                    "Citations",
                    "Citations / Paper",
                    "First Publication",
                    "Latest Publication"
                ]
            ]
            .copy()
        )


        st.dataframe(
            topic_display,
            use_container_width=True,
            hide_index=True,
            height=600,

            column_config={

                "Rank":
                    st.column_config.NumberColumn(
                        "#",
                        width="small",
                        format="%d"
                    ),

                "Topic Profile":
                    st.column_config.LinkColumn(
                        "Research Topic",
                        display_text=r"name=([^&]+)",
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

                "Citations / Paper":
                    st.column_config.NumberColumn(
                        "Cit. / Paper",
                        format="%.1f"
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


    # ========================================================
    # TOPIC PROFILE
    # ========================================================

    else:

        # ====================================================
        # ARTICLE PROFILE
        # ====================================================

        article_from_url = (
            st.query_params.get(
                "article"
            )
        )


        if article_from_url:

            selected_doi = unquote(
                str(article_from_url)
            )


            render_article_profile(
                selected_doi=selected_doi,
                filtered_df=filtered_df,
                selected_journal=selected_journal,

                return_page="Research Topics",

                return_label=selected_topic,

                return_params={
                    "topic":
                        selected_topic
                }
            )


        # ====================================================
        # BACK TO RESEARCH TOPICS
        # ====================================================

        if st.button(
            "← Back to Research Topics"
        ):

            st.query_params.clear()

            st.query_params[
                "page"
            ] = "Research Topics"

            st.rerun()


        # ====================================================
        # SELECT TOPIC ARTICLES
        # ====================================================

        topic_articles = (
            topic_df[
                topic_df[
                    "Topic"
                ] == selected_topic
            ]
            .drop_duplicates(
                subset="DOI"
            )
            .copy()
        )


        # ====================================================
        # TOPIC NOT FOUND
        # ====================================================

        if topic_articles.empty:

            st.warning(
                "The selected research topic could not "
                "be found within the current filters."
            )

            st.stop()


        # ====================================================
        # BASIC METRICS
        # ====================================================

        total_papers = (
            topic_articles[
                "DOI"
            ].nunique()
        )


        total_citations = int(
            topic_articles[
                "Citations"
            ]
            .fillna(0)
            .sum()
        )


        average_citations = (
            total_citations /
            total_papers
            if total_papers > 0
            else 0
        )


        first_year = int(
            topic_articles[
                "Year"
            ].min()
        )


        latest_year = int(
            topic_articles[
                "Year"
            ].max()
        )


        # ====================================================
        # TOPIC PROFILE HEADER
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'Research Topic Profile'
            '</div>',
            unsafe_allow_html=True
        )


        st.title(
            selected_topic
        )


        st.caption(
            f"{selected_journal} · "
            f"{first_year}–{latest_year}"
        )


        # ====================================================
        # PROFILE METRICS
        # ====================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        m1, m2, m3 = (
            st.columns(3)
        )


        m1.metric(
            "Publications",
            f"{total_papers:,}"
        )


        m2.metric(
            "Total Citations",
            f"{total_citations:,}"
        )


        m3.metric(
            "Citations / Paper",
            f"{average_citations:,.1f}"
        )


        m4, m5 = (
            st.columns(2)
        )


        m4.metric(
            "First Publication",
            f"{first_year}"
        )


        m5.metric(
            "Latest Publication",
            f"{latest_year}"
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


        topic_yearly = (
            topic_articles
            .groupby(
                "Year"
            )
            .agg(
                Publications=(
                    "DOI",
                    "nunique"
                )
            )
            .reset_index()
            .sort_values(
                "Year"
            )
        )


        fig_topic_output = px.bar(
            topic_yearly,
            x="Year",
            y="Publications"
        )


        fig_topic_output.update_layout(
            height=350,
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


        fig_topic_output.update_xaxes(
            dtick=1
        )


        st.plotly_chart(
            fig_topic_output,
            use_container_width=True
        )


        # ====================================================
        # LEADING AUTHORS
        # ====================================================

        st.divider()


        st.markdown(
            '<div class="section-label">'
            'Research Community'
            '</div>',
            unsafe_allow_html=True
        )


        st.subheader(
            "Leading Authors"
        )


        topic_author_rows = []


        for _, row in topic_articles.iterrows():

            for author in split_cell(
                row["Author"]
            ):

                topic_author_rows.append(
                    {
                        "Author": author,
                        "DOI": row["DOI"],
                        "Citations":
                            row["Citations"]
                    }
                )


        topic_authors = pd.DataFrame(
            topic_author_rows
        )


        if not topic_authors.empty:

            topic_author_summary = (
                topic_authors
                .groupby(
                    "Author"
                )
                .agg(
                    Publications=(
                        "DOI",
                        "nunique"
                    ),

                    Citations=(
                        "Citations",
                        "sum"
                    )
                )
                .reset_index()
                .sort_values(
                    [
                        "Publications",
                        "Citations",
                        "Author"
                    ],
                    ascending=[
                        False,
                        False,
                        True
                    ]
                )
                .head(10)
            )


            author_plot = (
                topic_author_summary
                .sort_values(
                    "Publications",
                    ascending=True
                )
            )


            fig_topic_authors = px.bar(
                author_plot,
                x="Publications",
                y="Author",
                orientation="h"
            )


            fig_topic_authors.update_layout(
                height=420,
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
                fig_topic_authors,
                use_container_width=True
            )


        else:

            st.info(
                "Author information is not available "
                "for publications in this topic."
            )


        # ====================================================
        # INSTITUTIONS AND COUNTRIES
        # ====================================================

        st.divider()


        institution_col, country_col = (
            st.columns(2)
        )


        # ----------------------------------------------------
        # LEADING INSTITUTIONS
        # ----------------------------------------------------

        with institution_col:

            st.markdown(
                '<div class="section-label">'
                'Institutional Participation'
                '</div>',
                unsafe_allow_html=True
            )


            st.subheader(
                "Leading Institutions"
            )


            institution_rows = []


            for _, row in (
                topic_articles.iterrows()
            ):

                for institution in split_cell(
                    row["Institution"]
                ):

                    institution_rows.append(
                        {
                            "Institution":
                                institution,

                            "DOI":
                                row["DOI"],

                            "Citations":
                                row["Citations"]
                        }
                    )


            topic_institutions = (
                pd.DataFrame(
                    institution_rows
                )
            )


            if not topic_institutions.empty:

                institution_summary = (
                    topic_institutions
                    .groupby(
                        "Institution"
                    )
                    .agg(
                        Publications=(
                            "DOI",
                            "nunique"
                        ),

                        Citations=(
                            "Citations",
                            "sum"
                        )
                    )
                    .reset_index()
                    .sort_values(
                        [
                            "Publications",
                            "Citations",
                            "Institution"
                        ],
                        ascending=[
                            False,
                            False,
                            True
                        ]
                    )
                    .head(10)
                )


                institution_plot = (
                    institution_summary
                    .sort_values(
                        "Publications",
                        ascending=True
                    )
                )


                fig_topic_institutions = (
                    px.bar(
                        institution_plot,
                        x="Publications",
                        y="Institution",
                        orientation="h"
                    )
                )


                fig_topic_institutions.update_layout(
                    height=430,
                    xaxis_title="Publications",
                    yaxis_title="",
                    showlegend=False,
                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=30
                    )
                )


                st.plotly_chart(
                    fig_topic_institutions,
                    use_container_width=True
                )


            else:

                st.caption(
                    "Institution information "
                    "is not available."
                )


        # ----------------------------------------------------
        # LEADING COUNTRIES
        # ----------------------------------------------------

        with country_col:

            st.markdown(
                '<div class="section-label">'
                'Geographic Participation'
                '</div>',
                unsafe_allow_html=True
            )


            st.subheader(
                "Leading Countries"
            )


            country_rows = []


            for _, row in (
                topic_articles.iterrows()
            ):

                for country_code in split_cell(
                    row["Country"]
                ):

                    country_name = (
                        country_code_to_name(
                            country_code
                        )
                    )


                    if country_name:

                        country_rows.append(
                            {
                                "Country":
                                    country_name,

                                "DOI":
                                    row["DOI"],

                                "Citations":
                                    row["Citations"]
                            }
                        )


            topic_countries = (
                pd.DataFrame(
                    country_rows
                )
            )


            if not topic_countries.empty:

                country_summary = (
                    topic_countries
                    .groupby(
                        "Country"
                    )
                    .agg(
                        Publications=(
                            "DOI",
                            "nunique"
                        ),

                        Citations=(
                            "Citations",
                            "sum"
                        )
                    )
                    .reset_index()
                    .sort_values(
                        [
                            "Publications",
                            "Citations",
                            "Country"
                        ],
                        ascending=[
                            False,
                            False,
                            True
                        ]
                    )
                    .head(10)
                )


                country_plot = (
                    country_summary
                    .sort_values(
                        "Publications",
                        ascending=True
                    )
                )


                fig_topic_countries = (
                    px.bar(
                        country_plot,
                        x="Publications",
                        y="Country",
                        orientation="h"
                    )
                )


                fig_topic_countries.update_layout(
                    height=430,
                    xaxis_title="Publications",
                    yaxis_title="",
                    showlegend=False,
                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=30
                    )
                )


                st.plotly_chart(
                    fig_topic_countries,
                    use_container_width=True
                )


            else:

                st.caption(
                    "Country information "
                    "is not available."
                )


        # ====================================================
        # INTERPRETATION NOTE
        # ====================================================

        st.caption(
            "Institution and country information is reported "
            "at the article level. The current dataset does "
            "not preserve exact author-to-institution or "
            "institution-to-country relationships."
        )


        # ====================================================
        # PUBLICATIONS
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


        st.caption(
            "Click a publication title to view "
            "its article profile."
        )


        # ====================================================
        # PREPARE PUBLICATION TABLE
        # ====================================================

        publication_table = (
            topic_articles[
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
        # INTERNAL ARTICLE LINKS
        # ====================================================

        publication_table[
            "Publication"
        ] = (
            publication_table
            .apply(
                lambda row:
                    f"?page={quote('Research Topics')}"
                    f"&topic={quote(str(selected_topic))}"
                    f"&article={quote(str(row['DOI']))}"
                    f"&title={quote(str(row['Title']))}",
                axis=1
            )
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
                make_doi_link
            )
        )


        publication_display = (
            publication_table[
                [
                    "Year",
                    "Publication",
                    "Citations",
                    "DOI Link"
                ]
            ]
            .copy()
        )


        # ====================================================
        # DISPLAY PUBLICATIONS
        # ====================================================

        st.dataframe(
            publication_display,
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

                "Publication":
                    st.column_config.LinkColumn(
                        "Publication",
                        display_text=r"title=([^&]+)",
                        width="large"
                    ),

                "Citations":
                    st.column_config.NumberColumn(
                        "Citations",
                        format="%d",
                        width="small"
                    ),

                "DOI Link":
                    st.column_config.LinkColumn(
                        "DOI",
                        display_text="Open DOI",
                        width="small"
                    )
            }
        )


        # ====================================================
        # METHODOLOGY NOTE
        # ====================================================

        st.caption(
            "Topic classifications are based on OpenAlex. "
            "A publication may be associated with multiple "
            "research topics, so topic publication counts "
            "are not mutually exclusive."
        )


# ============================================================
# ARTICLES
# ============================================================

elif page == "Articles":

    article_from_url = st.query_params.get("article")

    if article_from_url:
        selected_doi = unquote(str(article_from_url))
        render_article_profile(
            selected_doi=selected_doi,
            filtered_df=filtered_df,
            selected_journal=selected_journal,
            return_page="Articles",
            return_label="Articles"
        )

    st.markdown(
        '<div class="section-label">Publication Explorer</div>',
        unsafe_allow_html=True
    )
    st.header("Articles")
    st.caption(
        f"Browse publications from {selected_journal} · "
        f"{year_range[0]}–{year_range[1]}"
    )

    article_df = filtered_df.copy()
    article_df["Citation count"] = pd.to_numeric(
        article_df["Citation count"], errors="coerce"
    ).fillna(0)

    total_articles = article_df["DOI"].nunique()
    total_citations = int(article_df["Citation count"].sum())
    average_citations = (
        article_df["Citation count"].mean()
        if total_articles > 0 else 0
    )
    open_access_count = (
        article_df["Open access"].fillna("").astype(str)
        .str.strip().str.lower().eq("open access").sum()
    )
    open_access_rate = (
        open_access_count / total_articles * 100
        if total_articles > 0 else 0
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Publications", f"{total_articles:,}")
    k2.metric("Total Citations", f"{total_citations:,}")
    k3.metric("Avg. Citations / Paper", f"{average_citations:,.1f}")
    k4.metric("Open Access", f"{open_access_rate:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-label">Find Publications</div>',
        unsafe_allow_html=True
    )
    search_col, topic_col = st.columns([2.3, 1.7])
    with search_col:
        article_search = st.text_input(
            "Search publications",
            placeholder="Search by title, author or DOI...",
            key="article_search"
        )

    article_topics = sorted(set(split_values(article_df["Topic"])))
    with topic_col:
        selected_article_topic = st.selectbox(
            "Research topic", ["All topics"] + article_topics,
            key="article_topic_filter"
        )

    filter_col1, filter_col2, filter_col3 = st.columns([1.2, 1.2, 1.4])
    with filter_col1:
        access_filter = st.selectbox(
            "Access", ["All", "Open Access", "Closed Access"],
            key="article_access_filter"
        )
    with filter_col2:
        minimum_citations = st.number_input(
            "Minimum citations", min_value=0, value=0, step=1,
            key="article_min_citations"
        )
    with filter_col3:
        article_sort = st.selectbox(
            "Sort by", ["Newest", "Oldest", "Most Cited", "Title"],
            key="article_sort"
        )

    display_articles = article_df.copy()
    if article_search:
        search_text = article_search.strip()
        title_match = display_articles["Title"].fillna("").astype(str).str.contains(
            search_text, case=False, na=False, regex=False
        )
        author_match = display_articles["Author"].fillna("").astype(str).str.contains(
            search_text, case=False, na=False, regex=False
        )
        doi_match = display_articles["DOI"].fillna("").astype(str).str.contains(
            search_text, case=False, na=False, regex=False
        )
        display_articles = display_articles[title_match | author_match | doi_match]

    if selected_article_topic != "All topics":
        display_articles = display_articles[
            display_articles["Topic"].fillna("").astype(str).apply(
                lambda value: selected_article_topic in split_cell(value)
            )
        ]

    if access_filter == "Open Access":
        display_articles = display_articles[
            display_articles["Open access"].fillna("").astype(str)
            .str.strip().str.lower().eq("open access")
        ]
    elif access_filter == "Closed Access":
        display_articles = display_articles[
            display_articles["Open access"].fillna("").astype(str)
            .str.strip().str.lower().eq("closed access")
        ]

    display_articles = display_articles[
        display_articles["Citation count"] >= minimum_citations
    ]

    if article_sort == "Newest":
        display_articles = display_articles.sort_values(
            ["Year", "Citation count", "Title"], ascending=[False, False, True]
        )
    elif article_sort == "Oldest":
        display_articles = display_articles.sort_values(
            ["Year", "Citation count", "Title"], ascending=[True, False, True]
        )
    elif article_sort == "Most Cited":
        display_articles = display_articles.sort_values(
            ["Citation count", "Year", "Title"], ascending=[False, False, True]
        )
    else:
        display_articles = display_articles.sort_values(
            ["Title", "Year"], ascending=[True, False]
        )
    display_articles = display_articles.reset_index(drop=True)

    st.divider()
    title_col, count_col = st.columns([3, 1])
    with title_col:
        st.subheader("Publication Register")
    with count_col:
        st.markdown(
            f'<div style="text-align:right;padding-top:10px;'
            f'font-size:0.9rem;opacity:0.65;"><b>'
            f'{len(display_articles):,}</b> publications found</div>',
            unsafe_allow_html=True
        )
    st.caption("Click a publication title to view its complete article profile.")

    article_limit = st.selectbox(
        "Show", [25, 50, 100, 250], index=1,
        format_func=lambda x: f"{x} publications", key="article_rows"
    )
    publication_table = display_articles[
        ["Year", "Title", "Author", "Citation count", "Open access", "DOI"]
    ].head(article_limit).copy()
    publication_table["Publication"] = publication_table.apply(
        lambda row: (
            f"?page=Articles&article={quote(str(row['DOI']))}"
            f"&title={quote(str(row['Title']))}"
        ),
        axis=1
    )
    publication_table["DOI Link"] = publication_table["DOI"].apply(make_doi_link)

    def display_access_status(value):
        if pd.isna(value):
            return "—"
        value = str(value).strip()
        if not value:
            return "—"
        normalized = value.lower()
        if normalized == "open access":
            return "Open Access"
        if normalized == "closed access":
            return "Closed Access"
        return "—"

    publication_table["Access"] = publication_table["Open access"].apply(
        display_access_status
    )

    def display_article_authors(value):
        authors = split_cell(value)
        if not authors:
            return "—"
        if len(authors) <= 2:
            return ", ".join(authors)
        return f"{authors[0]}, {authors[1]} + {len(authors) - 2} more"

    publication_table["Authors"] = publication_table["Author"].apply(
        display_article_authors
    )
    publication_display = publication_table[
        ["Year", "Publication", "Authors", "Citation count", "Access", "DOI Link"]
    ].rename(columns={"Citation count": "Citations"}).copy()

    if publication_display.empty:
        st.info("No publications match the selected filters.")
    else:
        st.dataframe(
            publication_display,
            use_container_width=True,
            hide_index=True,
            height=650,
            column_config={
                "Year": st.column_config.NumberColumn(
                    "Year", width="small", format="%d"
                ),
                "Publication": st.column_config.LinkColumn(
                    "Publication", display_text=r"title=([^&]+)", width="large"
                ),
                "Authors": st.column_config.TextColumn(
                    "Authors", width="medium"
                ),
                "Citations": st.column_config.NumberColumn(
                    "Citations", width="small", format="%d"
                ),
                "Access": st.column_config.TextColumn(
                    "Access", width="small"
                ),
                "DOI Link": st.column_config.LinkColumn(
                    "DOI", display_text="Open DOI", width="small"
                )
            }
        )

    st.caption(
        "Citation counts are cumulative and may change over time. "
        "Open-access status is based on the available metadata. A dash "
        "indicates that access status is not available in the current dataset."
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