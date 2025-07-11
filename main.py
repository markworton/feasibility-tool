import streamlit as st
import pandas as pd
from utils.geolocation import get_coordinates
from utils.ninja_api import get_ninja_data

st.set_page_config(page_title="Renewable Feasibility Tool", layout="centered")
st.title("🔋 Renewable Energy Feasibility Tool")

# Input form
postcode = st.text_input("Enter UK Postcode")
site_size = st.number_input("Site Size (sqm)", min_value=0)
annual_consumption = st.number_input("Annual Energy Consumption (kWh/year)", min_value=0)

if st.button("Run Feasibility Check"):
    try:
        # 1. Get coordinates
        lat, lon = get_coordinates(postcode)

        # 2. Fetch solar and wind data
        solar_data = get_ninja_data(lat, lon, tech="solar")
        wind_data = get_ninja_data(lat, lon, tech="wind")

        solar_df = pd.DataFrame(solar_data["data"])
        wind_df = pd.DataFrame(wind_data["data"])

        solar_yield = solar_df["electricity"].sum()
        wind_yield = wind_df["electricity"].sum()

        st.success("Assessment Complete!")

        # ---- Solar Section ----
        st.header("☀️ Solar Feasibility")
        st.metric("Annual Solar Yield (kWh/kWp)", f"{solar_yield:.0f}")

        solar_capex = 1000  # £/kWp
        solar_kwp = min(site_size / 10, annual_consumption / solar_yield)
        solar_cost = solar_kwp * solar_capex
        solar_savings = min(solar_yield * solar_kwp, annual_consumption) * 0.20
        solar_payback = solar_cost / solar_savings if solar_savings > 0 else None

        st.write(f"**Estimated System Size:** {solar_kwp:.1f} kWp")
        st.write(f"**CapEx:** £{solar_cost:,.0f}")
        st.write(f"**Annual Savings:** £{solar_savings:,.0f}")
        st.write(f"**Estimated Payback:** {solar_payback:.1f} years" if solar_payback else "N/A")

        # ---- Wind Section ----
        st.divider()
        st.header("💨 Wind Feasibility")
        st.metric("Annual Wind Yield (kWh/kW @100m)", f"{wind_yield:.0f}")

        wind_capex = 1700  # £/kW
        wind_kw = min(site_size / 30, annual_consumption / wind_yield)
        wind_cost = wind_kw * wind_capex
        wind_savings = min(wind_yield * wind_kw, annual_consumption) * 0.20
        wind_payback = wind_cost / wind_savings if wind_savings > 0 else None

        st.write(f"**Estimated System Size:** {wind_kw:.1f} kW")
        st.write(f"**CapEx:** £{wind_cost:,.0f}")
        st.write(f"**Annual Savings:** £{wind_savings:,.0f}")
        st.write(f"**Estimated Payback:** {wind_payback:.1f} years" if wind_payback else "N/A")

    except Exception as e:
        st.error(f"❌ Error: {e}")
