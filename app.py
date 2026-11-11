import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------------
st.set_page_config(
    page_title="TATA Data Visualisation",
    page_icon="📊",
    layout="wide",
)

BAR_COLOR = "#4E79A7"   # Tableau-like blue
MAP_COLOR = "#2A9D8F"   # teal for the map

st.markdown(
    """
    <style>
        .block-container {padding-top: 1rem; padding-bottom: 1rem;}
        .title-bar {
            background-color: #000000; color: #FFFFFF;
            padding: 8px 16px; font-size: 26px; font-weight: 700;
            margin-bottom: 16px; letter-spacing: 0.5px;
        }
        .section-title {
            font-size: 14px; font-weight: 700; color: #333333;
            text-transform: uppercase; margin-bottom: 4px;
        }
        .kpi-value {font-size: 34px; font-weight: 600; color: #1f3b5c;}
    </style>
    <div class="title-bar">TATA DATA VISUALISATION: FORAGE JOB SIMULATION VIRTUAL INTERNSHIP</div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Dummy data (modelled on the reference image)
# ------------------------------------------------------------------
TOTAL_CUSTOMERS = 406_829
TOTAL_REVENUE = 9_747_747.93

top_customers = pd.DataFrame(
    {
        "Customer ID": ["12346", "15749", "17450", "15098", "18102",
                        "12939", "12357", "17940", "14646", "12931"],
        "Revenue": [77_183.60, 44_534.30, 41_200.00, 38_970.00, 36_450.75,
                    4_161.06, 4_176.00, 3_761.30, 3_540.20, 3_310.45],
    }
).sort_values("Revenue", ascending=False)

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

monthly_revenue = pd.DataFrame(
    {
        "Invoice Date": MONTHS,
        # Shape follows the reference chart: small ups and downs,
        # a jump from September, a peak in November and a sharp drop in December
        "Revenue": [550_000, 500_000, 680_000, 490_000, 720_000, 690_000,
                    680_000, 680_000, 1_000_000, 1_050_000, 1_480_000,
                    430_000],
    }
)

country_profit = pd.DataFrame(
    {
        "Country": [
            "Netherlands", "EIRE", "Germany", "France", "Australia",
            "Switzerland", "Spain", "Belgium", "Sweden", "Japan", "Norway",
            "Portugal", "Finland", "Channel Islands", "Denmark", "Italy",
            "Cyprus", "Austria", "Hong Kong", "Singapore", "Israel", "Poland",
            "Greece", "Iceland", "Canada", "Malta", "United Arab Emirates",
            "USA", "Lebanon", "Lithuania", "Brazil", "RSA", "Czech Republic",
            "Bahrain", "Saudi Arabia",
        ],
        "Profit": [
            285_000, 255_000, 205_000, 185_000, 135_000, 55_000, 50_000,
            38_000, 36_000, 35_000, 34_000, 30_000, 28_000, 26_000, 25_000,
            22_000, 20_000, 19_000, 18_000, 17_000, 16_000, 15_500, 14_000,
            13_500, 13_000, 12_000, 11_000, 10_500, 9_500, 9_000, 8_500,
            8_000, 7_000, 6_500, 6_000,
        ],
        "ISO": [
            "NLD", "IRL", "DEU", "FRA", "AUS", "CHE", "ESP", "BEL", "SWE",
            "JPN", "NOR", "PRT", "FIN", "JEY", "DNK", "ITA", "CYP", "AUT",
            "HKG", "SGP", "ISR", "POL", "GRC", "ISL", "CAN", "MLT", "ARE",
            "USA", "LBN", "LTU", "BRA", "ZAF", "CZE", "BHR", "SAU",
        ],
        "Products Sold": [
            2_400, 2_300, 1_900, 1_700, 1_300, 520, 480, 400, 380, 350, 340,
            300, 280, 260, 250, 220, 200, 190, 180, 170, 160, 155, 140, 135,
            130, 120, 110, 105, 95, 90, 85, 80, 70, 65, 60,
        ],
    }
)

# ------------------------------------------------------------------
# Layout
# ------------------------------------------------------------------
left, right = st.columns([1.1, 1])

with left:
    # --- KPIs -------------------------------------------------------
    k1, k2 = st.columns(2)
    with k1:
        st.markdown('<div class="section-title">Total Customers</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-value">{TOTAL_CUSTOMERS:,}</div>', unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="section-title">Total Revenue</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-value">${TOTAL_REVENUE:,.2f}</div>', unsafe_allow_html=True)

    st.divider()

    # --- Top 10 customers + Monthly revenue -------------------------
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">Top 10 Customers</div>', unsafe_allow_html=True)
        fig_top = px.bar(
            top_customers.sort_values("Revenue"),
            x="Revenue",
            y="Customer ID",
            orientation="h",
            text=top_customers.sort_values("Revenue")["Revenue"].map("${:,.2f}".format),
        )
        fig_top.update_traces(marker_color=BAR_COLOR, textposition="outside", cliponaxis=False)
        fig_top.update_yaxes(type="category", title="Customer ID")
        fig_top.update_xaxes(title="Revenue", tickprefix="$")
        fig_top.update_layout(
            height=330, margin=dict(l=0, r=60, t=10, b=0),
            plot_bgcolor="white",
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with c2:
        st.markdown('<div class="section-title">Monthly Revenue Generated</div>', unsafe_allow_html=True)
        fig_month = px.line(
            monthly_revenue,
            x="Invoice Date",
            y="Revenue",
            markers=True,
            category_orders={"Invoice Date": MONTHS},
        )
        fig_month.update_traces(
            line_color=BAR_COLOR,
            line_width=2,
            marker=dict(size=5, color=BAR_COLOR),
            hovertemplate="%{x}<br>Revenue: $%{y:,.0f}<extra></extra>",
        )
        # X axis: month labels at the bottom, no axis title (title sits on top)
        fig_month.update_xaxes(title=None, showgrid=False)
        # Y axis: 0K, 500K, 1000K, 1500K like the reference chart
        fig_month.update_yaxes(
            title="Revenue",
            range=[0, 1_600_000],
            tickvals=[0, 500_000, 1_000_000, 1_500_000],
            ticktext=["0K", "500K", "1000K", "1500K"],
            gridcolor="#E5E5E5",
        )
        # "Invoice Date" heading centred above the plot
        fig_month.add_annotation(
            text="Invoice Date",
            xref="paper", yref="paper",
            x=0.5, y=1.12, showarrow=False,
            font=dict(size=12, color="#555555"),
        )
        fig_month.update_layout(
            height=330, margin=dict(l=0, r=10, t=40, b=0),
            plot_bgcolor="white",
        )
        st.plotly_chart(fig_month, use_container_width=True)

    # --- Product distribution map -----------------------------------
    st.markdown('<div class="section-title">Product Distribution by Countries</div>', unsafe_allow_html=True)
    fig_map = px.choropleth(
        country_profit,
        locations="ISO",
        color="Products Sold",
        hover_name="Country",
        color_continuous_scale=["#D8F0EC", MAP_COLOR, "#0B4F47"],
    )
    fig_map.update_geos(
        showframe=False, showcoastlines=False,
        projection_type="natural earth", showcountries=True,
        countrycolor="#BBBBBB",
    )
    fig_map.update_layout(
        height=360, margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(title="Products"),
    )
    st.plotly_chart(fig_map, use_container_width=True)

with right:
    st.markdown('<div class="section-title">Profits Generated by Countries</div>', unsafe_allow_html=True)
    df_sorted = country_profit.sort_values("Profit", ascending=True)
    fig_country = px.bar(
        df_sorted,
        x="Profit",
        y="Country",
        orientation="h",
        text=df_sorted["Profit"].map("${:,.0f}".format),
    )
    fig_country.update_traces(marker_color=BAR_COLOR, textposition="outside", cliponaxis=False)
    fig_country.update_xaxes(title="Revenue", tickprefix="$")
    fig_country.update_yaxes(title="Country")
    fig_country.update_layout(
        height=960, margin=dict(l=0, r=70, t=10, b=0),
        plot_bgcolor="white",
    )
    st.plotly_chart(fig_country, use_container_width=True)

