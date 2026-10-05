import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="CPT 2026 Election Analytics",
    page_icon="🗳️",
    layout="wide"
)

# ---------- Page header ----------
st.title("City of Cape Town — Local Government Election Analytics")
st.markdown(
    """
**Analysis date:** 05 October 2026 (30 days before Election Day)  
**Prediction target:** 04 November 2026  
**Metro:** City of Cape Town (CPT), Western Cape  
"""
)
st.warning(
    "2026 values are **model estimates** with uncertainty. "
    "They are **not** historical facts and **not** a prediction of who will govern."
)

# ---------- Sidebar ----------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Historical analysis",
        "Model outputs (2026)",
        "Uncertainty & limits",
        "Sources",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Label guide")
st.sidebar.write("🟢 Historical observation")
st.sidebar.write("🟡 Derived from history")
st.sidebar.write("🔵 Prediction (04 Nov 2026)")

# ---------- Data used by dashboard ----------
party_df = pd.DataFrame({
    "party": ["DA", "ANC", "EFF", "ACDP"],
    "share_2016_hist": [0.6965, 0.2548, 0.0331, 0.0127],
    "share_2021_hist": [0.6044, 0.1928, 0.0428, 0.0000],
    "share_2026_pred": [0.7365, 0.1881, 0.0754, 0.0000],
    "share_2026_low": [0.60, 0.15, 0.05, 0.00],
    "share_2026_high": [0.74, 0.22, 0.08, 0.01],
})

ward_df = pd.DataFrame({
    "ward_id": ["19100021", "19100085", "19100035"],
    "selection_reason": ["Strong DA ward", "Competitive ward", "Stronger ANC ward"],
    "leader_2016_hist": ["DA", "ANC", "ANC"],
    "leader_2026_pred": ["DA", "ANC", "ANC"],
    "confidence": ["Higher", "Lower", "Higher"],
})

# =========================================================
if section == "Overview":
    st.header("Overview")
    st.write(
        "This dashboard communicates the principal historical findings, "
        "model outputs for 04 November 2026, and uncertainty for the "
        "City of Cape Town local government election analysis."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Metro", "CPT")
    c2.metric("Largest projected party", "DA")
    c3.metric("Predicted turnout (mean)", "35.4%")
    c4.metric("Estimated votes", "699,950")

    st.subheader("What this solution answers")
    st.markdown(
        """
1. Which relevant party is projected to get the **largest metro vote share**?  
2. Possible **coalition** implications (analytical only — not who will govern)  
3. Projected leader in **three justified wards**  
4. Projected **vote shares** for modelled parties  
5. Projected **voter turnout** (rate + estimated votes)
"""
    )

# =========================================================
elif section == "Historical analysis":
    st.header("Principal historical analysis")
    st.caption("🟢 Historical observations from IEC-based results")

    st.subheader("Metro party vote shares — 2016 vs 2021")
    hist = party_df.set_index("party")[["share_2016_hist", "share_2021_hist"]]

    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        fig, ax = plt.subplots(figsize=(7, 4))
        x = np.arange(len(hist))
        width = 0.35
        ax.bar(x - width / 2, hist["share_2016_hist"], width, label="2016")
        ax.bar(x + width / 2, hist["share_2021_hist"], width, label="2021")
        ax.set_xticks(x)
        ax.set_xticklabels(hist.index)
        ax.set_ylabel("Vote share")
        ax.set_title("CPT metro party shares (historical)")
        ax.legend()
        st.pyplot(fig)
        st.caption("Bar chart: compares categories across two election years.")

    with col_b:
        st.dataframe(
            (hist * 100).round(2).rename(columns={
                "share_2016_hist": "2016 %",
                "share_2021_hist": "2021 %",
            })
        )
        st.markdown(
            """
**Key historical points**
- **DA** remained largest in both years, but share fell (≈70% → ≈60%).
- **ANC** also declined (≈25% → ≈19%).
- **EFF** increased slightly (≈3% → ≈4%).
- Turnout fell from 2016 to 2021 in many wards (see notebook model).
"""
        )

    st.subheader("Selected wards (justified)")
    st.dataframe(ward_df[["ward_id", "selection_reason", "leader_2016_hist"]])
    st.info(
        "Wards chosen for contrast (strong DA / competitive / stronger ANC) "
        "and only from IDs present in both 2016 and 2021 (116-ward system)."
    )

# =========================================================
elif section == "Model outputs (2026)":
    st.header("Model outputs — 04 November 2026")
    st.caption("🔵 Predictions / model estimates")

    st.subheader("A) Projected party vote shares")
    pred = party_df.set_index("party")

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(pred.index, pred["share_2026_pred"], color="steelblue")
        ax.set_ylabel("Predicted share")
        ax.set_title("Projected party share (point estimate)")
        st.pyplot(fig)
        st.caption("Bar chart: compares predicted shares by party.")

    with c2:
        show = pred[["share_2026_pred", "share_2026_low", "share_2026_high"]].copy()
        show = (show * 100).round(1)
        show.columns = ["2026 pred %", "Low %", "High %"]
        st.dataframe(show)
        st.success(
            f"Largest projected party (model output): "
            f"**{pred['share_2026_pred'].idxmax()}**"
        )

    st.markdown(
        """
**Coalition note (analytical only)**  
Projected DA lead is strong, so a single-party majority is more analytically
plausible than a forced coalition. This is **not** a prediction of who will govern.
"""
    )

    st.subheader("B) Projected turnout (CPT)")
    t1, t2, t3 = st.columns(3)
    t1.metric("Mean predicted turnout rate", "35.4%")
    t2.metric("Estimated number of votes", "699,950")
    t3.metric("Test MAE uncertainty", "± 3.9 pp")
    st.caption(
        "Votes ≈ predicted rate × 2021 registered voters (proxy). "
        "🟡 Registration base is historical; 🔵 rate/votes are predictions."
    )

    st.subheader("C) Projected leaders in three wards")
    st.dataframe(ward_df)
    st.caption(
        "Method: persistence from 2016 ward leaders "
        "(defensive where 2021 ward-party panel was not fully modelled)."
    )

# =========================================================
elif section == "Uncertainty & limits":
    st.header("Uncertainty, assumptions and limitations")

    st.subheader("Uncertainty shown in this dashboard")
    st.markdown(
        """
- **Turnout:** ± about **3.9 percentage points** (model test MAE)
- **Party shares:** low/high band from method sensitivity
  (trend estimate vs conservative 2021 baseline around DA ≈ 60%)
- **Ward 19100085:** lower confidence (competitive in 2016)
"""
    )

    st.subheader("Main assumptions")
    st.markdown(
        """
1. Public data available on/before **05 Oct 2026** only  
2. 2016→2021 relationships are informative for 2026  
3. Selected wards are comparable in the 2016/2021 (116-ward) system  
4. Party model focuses on main parties (DA, ANC, EFF, ACDP)
"""
    )

    st.subheader("Limitations")
    st.markdown(
        """
- Simple trend/persistence models; not causal political forecasts  
- Turnout point estimate may be low if the 2016–2021 decline does not continue  
- Ward leaders use persistence where full 2021 ward-party features were limited  
- Unsupported false precision is avoided on purpose
"""
    )

# =========================================================
else:
    st.header("Data sources (traceable)")
    st.markdown(
        """
### Primary
- **IEC** Municipal / Local Government Election results (CPT ward & metro reports)  
  https://results.elections.org.za/home/Downloads/ME-Results  
  https://results.elections.org.za/home/

### Supporting
- **Stats SA** Census 2022 municipal indicators (CPT)  
  https://census.statssa.gov.za/

### Local project files
- See `SOURCES.txt` in the project repository for file-level URLs and merge keys.
"""
    )
    st.success("All election figures used are from credible open sources — no fictional data.")
