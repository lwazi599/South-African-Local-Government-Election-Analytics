# South-African-Local-Government-Election-Analytics

## CPT 2026 Local Election Forecasting

Evidence-based ML solution for City of Cape Town (CPT) local government election analytics.

- Election Day target: 04 November 2026
- Notebook: `01.CPT_2026_Local_Election_Forecasting.ipynb`
- Dashboard: `02.Streamlit_Dashboard_app.py`
- Sources: see `03.SOURCES.txt`
- AI prompts record: `ai_prompts.txt`
- Datasets used: Datasets used
- `derived_iec_2011_cpt_voter_turnout_wards.csv`
- `derived_iec_2016_cpt_voter_turnout_wards.csv`
- `derived_iec_2021_cpt_voter_turnout_wards.csv`
- `openelections_2016_cpt_ward_party_votes.csv`
- `statssa_census2022_person_indicators_CPT.csv`
- `iec_2021_lge_cpt_detailed_results_muni.xls`

2026 outputs are model estimates with uncertainty, not governance predictions.
Run dashboard
bash
streamlit run 02.Streamlit_Dashboard_app.py
