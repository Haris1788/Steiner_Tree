import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Paris Couple Itinerary 2026", layout="wide")

# --- DATA: MAPPING PLACES, COSTS, AND COORDINATES ---
data = {
    "Place": [
        "Eiffel Tower (Champ de Mars)", "Champs-Élysées", "Arc de Triomphe", 
        "Louvre Museum", "Seine River (C N River)", "Montmartre Street Artists", 
        "Sainte-Chapelle", "Musée Rodin", "Mont-Saint-Michel (Normandy)", 
        "Galeries Lafayette Haussmann", "Petit Palais", "Bonte Schuch Cafe", 
        "Palais de la Découverte"
    ],
    "Lat": [48.8584, 48.8698, 48.8738, 48.8606, 48.8566, 48.8867, 48.8555, 48.8553, 48.6361, 48.8737, 48.8660, 48.8540, 48.8662],
    "Lon": [2.2945, 2.3079, 2.2950, 2.3376, 2.3522, 2.3350, 2.3450, 2.3158, -1.5115, 2.3322, 2.3146, 2.3450, 2.3107],
    "Category": ["Sight", "Shopping", "Sight", "Museum", "Experience", "Art", "Sight", "Museum", "Excursion", "Shopping", "Museum", "Food", "Science"],
    "Cost_Per_Person": [0, 0, 13, 22, 18, 0, 11.5, 13, 60, 0, 0, 25, 12],
    "Img": ["🗼", "🛍️", "🏛️", "🎨", "🚢", "🎨", "⛪", "🗿", "🏰", "🏢", "🏛️", "☕", "🔬"]
}

df = pd.DataFrame(data)

# --- SIDEBAR: INPUTS & BUDGET ---
st.sidebar.header("🗺️ Trip Controls")
selected_places = st.sidebar.multiselect("Select Places to Visit", df["Place"].tolist(), default=df["Place"].tolist())

st.sidebar.divider()
st.sidebar.subheader("💰 Shopping & Stay Budget")
hotel_night = st.sidebar.slider("Hotel Cost/Night (€)", 80, 500, 150)
shopping_budget = st.sidebar.number_input("Clothing & Cosmetics Budget (€)", 0, 5000, 400)

# --- LOGIC ---
filtered_df = df[df["Place"].isin(selected_places)]
ticket_total = (filtered_df["Cost_Per_Person"].sum()) * 2
accommodation_total = hotel_night * 4
grand_total = ticket_total + accommodation_total + shopping_budget + 200 # +200 for food/metro base

# --- MAIN DASHBOARD ---
st.title("🇫🇷 Your Paris 4-Day Couple Dashboard")
st.markdown(f"**Travel Dates:** March 21 - March 24, 2026")

col1, col2, col3 = st.columns(3)
col1.metric("Total Expenses", f"€{grand_total}")
col2.metric("Tickets (Couple)", f"€{ticket_total}")
col3.metric("Places to Visit", len(selected_places))

st.divider()

# --- MAP SECTION ---
st.subheader("📍 Interactive Route Map")
# Special check for Mont-Saint-Michel to zoom out if selected
center_lat = 48.8566 if "Mont-Saint-Michel (Normandy)" not in selected_places else 48.7
fig = px.scatter_mapbox(filtered_df, lat="Lat", lon="Lon", hover_name="Place", 
                        hover_data=["Category", "Cost_Per_Person"],
                        color="Category", zoom=11, height=500)
fig.update_layout(mapbox_style="carto-positron")
st.plotly_chart(fig, use_container_width=True)

# --- ITINERARY & LOCAL TIPS ---
st.subheader("📅 Smart Itinerary & Logistics")
tabs = st.tabs(["Day 1: Central", "Day 2: Art & Style", "Day 3: Normandy", "Day 4: Views"])

with tabs[0]:
    st.write("### 🗼 The Iconic Axis")
    st.info("Start at **Champ de Mars** for the view. Walk to **Musée Rodin** (15 min walk). Evening: **Seine River Cruise**.")
    st.write("**Budget Tip:** Eat at *Bouillon Chartier* near Montparnasse for a historic €20 dinner.")

with tabs[1]:
    st.write("### 🎨 Culture & Luxury")
    st.info("Morning: **Louvre** (Pre-book 9 AM!). Afternoon: **Champs-Élysées** to **Arc de Triomphe**.")
    st.write("**Shopping Tip:** Visit **CityPharma** (Rue du Four) for the world's cheapest branded French cosmetics.")

with tabs[2]:
    st.write("### 🏰 The Island Miracle")
    st.info("Train from *Gare Montparnasse* to **Mont-Saint-Michel**. Plan for a full 12-hour day.")

with tabs[3]:
    st.write("### 🎨 Bohemian Finale")
    st.info("Morning: **Montmartre**. Afternoon: **Petit Palais** (Free!) & **Galeries Lafayette** (Free rooftop view).")

# --- EXPENSE BREAKDOWN ---
st.divider()
st.subheader("📊 Expense Breakdown")
st.table(filtered_df[["Img", "Place", "Category", "Cost_Per_Person"]])

st.success("✅ **Tip for Frankfurt Return:** Book your ICE/Thalys train 3 months in advance to save 60% on tickets!")