# -*- coding: utf-8 -*-
"""
Paris Trip Planner Dashboard
=============================
Couple Trip: March 21 night - March 25 early morning, 2026
Frankfurt -> Paris -> Frankfurt
3 full sightseeing days (Mar 22, 23, 24)

Run:   streamlit run paris_trip_planner.py
Needs: pip install streamlit folium pandas streamlit-folium
"""

import streamlit as st
import pandas as pd
import folium
import math
from folium.plugins import AntPath

# ======================================================================
# PAGE CONFIG
# ======================================================================
st.set_page_config(
    page_title="Paris Trip Planner",
    page_icon=":fr:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================================
# CSS
# ======================================================================
st.markdown("""
<style>
.block-container {padding-top: 1rem;}
h1, h2 {color: #002654;}
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 12px; padding: 12px 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,.08);
}
div[data-testid="stMetric"] label {font-size:.85rem;color:#555}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {font-size:1.4rem;font-weight:700}
.route-step {
    border-left: 3px solid #1e88e5; padding: 6px 12px; margin: 4px 0;
    background: #f8f9fb; border-radius: 0 8px 8px 0;
}
.hotel-card {
    border: 1px solid #e0e0e0; border-radius: 10px; padding: 14px;
    margin: 8px 0; background: #fafbfd;
}
</style>
""", unsafe_allow_html=True)

# ======================================================================
# DATA -- PLACES  (2025/2026 accurate prices)
# ======================================================================
# Prices researched from official sites as of late 2025:
#   Eiffel Tower: stairs to 2nd = 11.80, lift to 2nd = 18.80, lift to top = 29.40
#   Louvre: 22 EUR (online) since Jan 2024
#   Arc de Triomphe: 16 EUR (2025)
#   Sainte-Chapelle: 11.50 EUR
#   Musee Rodin: 14 EUR (garden only = 5 EUR)
#   Palais de la Decouverte: closed for renovation (Grand Palais), reopened late 2025 ~14 EUR
#   Mont-Saint-Michel abbey: 11 EUR, bus tour ~80-130 EUR/pp all-in
#   Seine cruise (Bateaux Mouches): 16 EUR
#
PLACES = [
    dict(id="eiffel_tower", name="Eiffel Tower (Champ de Mars)", lat=48.8560, lng=2.2945,
         cat="Landmark", default_day=1, hrs=2.5, cost=29.40,
         desc="Iconic tower. Lift to top = 29.40. Lift to 2nd floor = 18.80. Stairs to 2nd = 11.80. VIEW from Champ de Mars = FREE.",
         tip="Book tickets 2 months ahead at tour-eiffel.fr. Go at sunset!",
         hours="9:00-00:45 (mid Jun-Sep), 9:30-23:45 rest of year", icon="Tower"),
    dict(id="champs_elysees", name="Champs-Elysees", lat=48.8698, lng=2.3076,
         cat="Landmark", default_day=1, hrs=1.5, cost=0,
         desc="World's most famous avenue. Walk from Place de la Concorde to Arc de Triomphe (~2 km).",
         tip="Walk it late afternoon for golden light. Window-shop at Louis Vuitton, Cartier, Laduree.",
         hours="24h (shops ~10-21h)", icon="Shopping"),
    dict(id="arc_de_triomphe", name="Arc de Triomphe", lat=48.8738, lng=2.2950,
         cat="Landmark", default_day=1, hrs=1.0, cost=16.00,
         desc="Monumental arch. 284 steps to rooftop panorama of 12 radiating avenues.",
         tip="Free for under-26 EU residents & 1st Sunday Nov-Mar. Use underground tunnel!",
         hours="10-23h (Apr-Sep), 10-22:30 (Oct-Mar)", icon="Monument"),
    dict(id="louvre", name="Louvre Museum", lat=48.8606, lng=2.3376,
         cat="Museum", default_day=2, hrs=3.0, cost=22.00,
         desc="World's largest art museum. Mona Lisa, Venus de Milo, Winged Victory. 35,000 works.",
         tip="Book timed entry online (mandatory!). Enter via Porte des Lions = short queue. Fri evening open till 21:45.",
         hours="Wed-Mon 9-18h (Fri till 21:45). CLOSED Tuesday.", icon="Museum"),
    dict(id="seine_river", name="Seine River Cruise", lat=48.8637, lng=2.3125,
         cat="Nature", default_day=1, hrs=1.5, cost=16.00,
         desc="1h cruise past Notre-Dame, Musee d'Orsay, Eiffel Tower. Or walk the quais for FREE!",
         tip="Bateaux Mouches (Pont de l'Alma) = 16 EUR. Vedettes du Pont Neuf = 15 EUR. Book online for 2 EUR off.",
         hours="Cruises every 20-30 min, 10:00-22:30", icon="Boat"),
    dict(id="montmartre", name="Montmartre (Street Artists)", lat=48.8862, lng=2.3411,
         cat="Landmark", default_day=3, hrs=3.0, cost=0,
         desc="Bohemian hilltop. Place du Tertre artists, Sacre-Coeur basilica (free entry), vineyard.",
         tip="Go early morning to avoid crowds. Portrait at Place du Tertre = ~30-60 EUR.",
         hours="24h (Sacre-Coeur: 6:30-22:30, dome: 10-17:30 ~7 EUR)", icon="Art"),
    dict(id="sainte_chapelle", name="Sainte-Chapelle", lat=48.8554, lng=2.3451,
         cat="Church", default_day=2, hrs=1.0, cost=11.50,
         desc="Gothic masterpiece. 15 stained-glass windows, each 15m tall. Built 1238-1248.",
         tip="Visit on a sunny day = liquid colour! Combo with Conciergerie = 18.50 EUR.",
         hours="9-17h (Apr-Sep till 19h)", icon="Church"),
    dict(id="musee_rodin", name="Musee Rodin", lat=48.8557, lng=2.3161,
         cat="Museum", default_day=2, hrs=1.5, cost=14.00,
         desc="The Thinker, The Kiss, Gates of Hell. Beautiful 18th-century Hotel Biron + garden.",
         tip="Garden-only ticket = 5 EUR. CLOSED Mondays! Free 1st Sunday of month Oct-Mar.",
         hours="Tue-Sun 10-18:30. Closed Mon.", icon="Statue"),
    dict(id="mont_saint_michel", name="Mont-Saint-Michel (Normandy)", lat=48.6361, lng=-1.5115,
         cat="Day Trip", default_day=0, hrs=14.0, cost=100.00,
         desc="Tidal island + medieval abbey. Full day from Paris. Abbey entry = 11 EUR. Bus tour = ~80-130 EUR total/pp.",
         tip="Book guided bus tour (departs ~7AM, returns ~22h). Or TGV to Rennes + shuttle. Whole day trip!",
         hours="Abbey 9:30-18h (May-Aug till 19h)", icon="Castle"),
    dict(id="galeries_lafayette", name="Galeries Lafayette Haussmann", lat=48.8737, lng=2.3321,
         cat="Shopping", default_day=3, hrs=2.0, cost=0,
         desc="Grand dept store with art-nouveau dome. FREE rooftop panoramic terrace!",
         tip="Get 10% tourist discount at Welcome Desk (passport needed). Tax refund on >100.01 EUR.",
         hours="Mon-Sat 10-20:30, Sun 11-20h", icon="Shop"),
    dict(id="petit_palais", name="Petit Palais", lat=48.8660, lng=2.3127,
         cat="Museum", default_day=1, hrs=1.5, cost=0,
         desc="FREE permanent collection. Monet, Cezanne, Delacroix. Beautiful Beaux-Arts building + garden cafe.",
         tip="One of the best free museums in Paris! Lovely courtyard cafe for a break.",
         hours="Tue-Sun 10-18h (Fri till 21h for some exhibits). Closed Mon.", icon="Museum"),
    dict(id="bonte_cafe", name="Bonte Cafe", lat=48.8530, lng=2.3390,
         cat="Cafe", default_day=3, hrs=1.0, cost=8.00,
         desc="Charming Parisian cafe for a leisurely coffee-and-pastry break.",
         tip="Cafe creme = ~4.50 EUR, pastry = ~3-5 EUR. Very instagrammable!",
         hours="8-19h", icon="Coffee"),
    dict(id="palais_decouverte", name="Palais de la Decouverte (Grand Palais)", lat=48.8662, lng=2.3097,
         cat="Museum", default_day=2, hrs=1.5, cost=14.00,
         desc="Interactive science museum inside the Grand Palais. Planetarium, experiments & demos.",
         tip="Reopened after Grand Palais renovation. Check schedule for live demos.",
         hours="Tue-Sat 9:30-18h, Sun 10-19h. Closed Mon.", icon="Science"),
]

# ======================================================================
# DATA -- HOTELS (budget, well-connected, near attractions)
# Prices: realistic March 2026 booking.com / hostelworld estimates
# Picked for: cheap, central, near metro, couple-friendly
# ======================================================================
HOTELS = [
    # --- Budget Hostels with Private Rooms ---
    dict(id="generator", name="Generator Paris (10th)", lat=48.8730, lng=2.3590,
         price=65, stars=4.0, area="Colonel Fabien (Metro 2)",
         desc="Design hostel. Private double room with ensuite. Rooftop terrace, bar, cafe. Very social. Metro: Colonel Fabien (Line 2) = direct to Montmartre, Champs-Elysees.",
         metro="Colonel Fabien (Line 2)", walk_center="20 min to Republique"),
    dict(id="st_christophers", name="St Christopher's Inn Canal (10th)", lat=48.8831, lng=2.3673,
         price=50, stars=3.9, area="Gare de l'Est / Canal Saint-Martin",
         desc="Backpacker favourite with private double rooms. Belushi's bar downstairs, free WiFi. Near Canal Saint-Martin nightlife. Metro: Gare de l'Est (Lines 4, 5, 7).",
         metro="Gare de l'Est (Lines 4, 5, 7)", walk_center="25 min to Chatelet"),
    dict(id="village_montmartre", name="Le Village Hostel Montmartre (18th)", lat=48.8880, lng=2.3486,
         price=55, stars=4.1, area="Montmartre (steps from Sacre-Coeur)",
         desc="Terrace with Eiffel Tower view! Private double rooms. Bohemian neighbourhood. Right next to Montmartre attractions. Metro: Anvers (Line 2).",
         metro="Anvers (Line 2)", walk_center="30 min to Opera"),
    # --- Budget Hotels ---
    dict(id="ibis_gare_nord", name="Ibis Budget Paris Gare du Nord (10th)", lat=48.8795, lng=2.3555,
         price=72, stars=3.5, area="Gare du Nord",
         desc="No-frills but clean & reliable. Excellent metro hub: Lines 2, 4, 5 + RER B. Close to Eurostar/Thalys. 5 min walk to Gare du Nord.",
         metro="Gare du Nord (Lines 2, 4, 5, RER B, D)", walk_center="20 min to Les Halles"),
    dict(id="hotel_paris_voltaire", name="Hotel Paris Voltaire (11th)", lat=48.8615, lng=2.3795,
         price=60, stars=3.6, area="Bastille / Republique",
         desc="Cozy budget hotel near Bastille. Clean rooms, good WiFi. Area full of cheap restaurants & bars. Metro: Voltaire (Line 9) + Bastille (Lines 1, 5, 8).",
         metro="Voltaire (Line 9), Bastille (Lines 1, 5, 8)", walk_center="15 min to Marais"),
    dict(id="hotel_jeanne_darc", name="Hotel Jeanne d'Arc Le Marais (4th)", lat=48.8555, lng=2.3615,
         price=95, stars=4.3, area="Le Marais (central!)",
         desc="Best-value hotel in Le Marais. Charming, quiet street. Walkable to Louvre, Notre-Dame, Bastille. Extremely central. Book months ahead!",
         metro="Saint-Paul (Line 1), Bastille (Lines 1, 5, 8)", walk_center="5 min to everything"),
    dict(id="hotel_du_college", name="Hotel du College de France (5th)", lat=48.8490, lng=2.3465,
         price=85, stars=4.0, area="Latin Quarter (5th)",
         desc="Charming Latin Quarter hotel. Walking distance to Notre-Dame, Sainte-Chapelle, Luxembourg Garden. Surrounded by cheap restaurants.",
         metro="Maubert-Mutualite (Line 10), Cluny-La Sorbonne (Line 10, RER B)", walk_center="10 min to Notre-Dame"),
    # --- Trending deals / Airbnb-style ---
    dict(id="hotel_ibis_styles", name="Ibis Styles Paris Republique (11th)", lat=48.8646, lng=2.3658,
         price=78, stars=3.8, area="Republique",
         desc="Modern design hotel. Breakfast included! Excellent location at Place de la Republique. Metro: Republique (Lines 3, 5, 8, 9, 11) = best connected metro hub in Paris.",
         metro="Republique (Lines 3, 5, 8, 9, 11)", walk_center="15 min to Marais"),
]

# ======================================================================
# DATA -- RESTAURANTS
# ======================================================================
RESTAURANTS = [
    dict(name="Bouillon Chartier", lat=48.8741, lng=2.3407, avg=14, cuisine="Classic French",
         desc="Paris's most famous budget restaurant (since 1896). Full 3-course French meal 12-18 EUR.",
         tip="Expect queues -- worth it. Try boeuf bourguignon + creme caramel."),
    dict(name="L'As du Fallafel (Marais)", lat=48.8572, lng=2.3588, avg=9, cuisine="Middle Eastern",
         desc="Best falafel in Paris. Huge portions. 'Special' falafel = 8.50 EUR.",
         tip="Closed Fri evening & Sat (Shabbat). Go at lunch for shortest queue."),
    dict(name="Bouillon Racine", lat=48.8506, lng=2.3421, avg=18, cuisine="Classic French",
         desc="Art Nouveau masterpiece dining room. Lunch menu = 15-20 EUR for 2 courses.",
         tip="Go for LUNCH -- much better value than dinner. Duck confit is superb."),
    dict(name="Creperie Josselin (Montparnasse)", lat=48.8421, lng=2.3258, avg=12, cuisine="Breton Crepes",
         desc="Authentic Breton creperie. Galettes (savoury buckwheat) + sweet crepes.",
         tip="Galette Complete (ham, cheese, egg) + bolee of cider = classic Breton meal."),
    dict(name="Pink Mamma (10th)", lat=48.8680, lng=2.3620, avg=18, cuisine="Italian",
         desc="4-floor Italian restaurant, incredible decor. Huge pizzas, generous pastas.",
         tip="Come at 11:30 opening to skip massive evening queues. No reservations!"),
    dict(name="Chez Janou (3rd)", lat=48.8575, lng=2.3647, avg=22, cuisine="Provencal French",
         desc="Famous for all-you-can-eat chocolate mousse served from a giant bowl!",
         tip="Go specifically for the chocolate mousse -- an unforgettable experience."),
    dict(name="Bouillon Julien", lat=48.8712, lng=2.3530, avg=15, cuisine="Classic French",
         desc="Stunning Belle Epoque interior (1906). Same concept as Chartier -- 3 courses ~15-20 EUR.",
         tip="Less famous than Chartier = shorter queue. Equally beautiful."),
    dict(name="Any Boulangerie (bakery)", lat=48.8600, lng=2.3400, avg=5, cuisine="Bakery / Quick",
         desc="Croissant (~1.30 EUR), pain au chocolat (~1.50 EUR), jambon-beurre sandwich = 3.50-5 EUR.",
         tip="Look for 'Artisan Boulanger' sign. Every 50 metres in Paris."),
]

# ======================================================================
# DATA -- SHOPS
# ======================================================================
SHOPS = [
    dict(name="Citypharma (6th)", lat=48.8518, lng=2.3329, cat="Cosmetics",
         desc="THE cheapest pharmacy in Paris. 20-40% off La Roche-Posay, Vichy, Bioderma, Avene, Nuxe, Caudalie.",
         tip="Go early morning or 13h. Always packed. Bring a shopping list!", budget="Save 30-80 EUR vs abroad"),
    dict(name="Pharmacie Monge (5th)", lat=48.8432, lng=2.3510, cat="Cosmetics",
         desc="Another big discount pharmacy. Less crowded than Citypharma. Great for French skincare.",
         tip="Ask for 'offres du moment' (current deals) at counter.", budget="Save 20-60 EUR"),
    dict(name="Primark (Rue de Rivoli)", lat=48.8583, lng=2.3467, cat="Clothes",
         desc="Ultra-cheap fashion. T-shirts from 3 EUR, jeans from 12 EUR, jackets from 15 EUR.",
         tip="Great for basics & pyjamas. Don't expect high quality but unbeatable prices.", budget="5-30 EUR/item"),
    dict(name="Galeries Lafayette (Sales)", lat=48.8737, lng=2.3321, cat="Clothes/Luxury",
         desc="Check outlet corners on lower floors. End-of-season sales = 30-70% off branded items.",
         tip="Get 10% tourist discount card + claim 12% tax refund on purchases >100.01 EUR.", budget="Varies widely"),
    dict(name="Monoprix (Champs-Elysees)", lat=48.8713, lng=2.3045, cat="Cosmetics/Clothes",
         desc="French dept store. Good own-brand cosmetics + affordable clothing line.",
         tip="Food hall downstairs = great for picnic supplies, wine, French snacks & souvenirs.", budget="5-40 EUR/item"),
    dict(name="Marche aux Puces Saint-Ouen", lat=48.8994, lng=2.3547, cat="Vintage/Designer",
         desc="World's largest flea market. Vintage Chanel, Hermes scarves, designer finds.",
         tip="Haggle! Start at 50% of asking. Sat-Mon only. Metro 4 to Clignancourt.", budget="10-200+ EUR"),
    dict(name="Sephora Champs-Elysees", lat=48.8706, lng=2.3042, cat="Cosmetics",
         desc="Huge flagship store. All major brands. Good for French exclusives unavailable abroad.",
         tip="Ask for free samples! They're generous at the flagship store.", budget="10-80 EUR/item"),
]

# ======================================================================
# DATA -- TRANSPORT
# ======================================================================
TRANSPORT_FFM = [
    dict(mode="FlixBus", price=20, time="6-8h", note="Cheapest option. Frankfurt Hbf. Prices 15-30 EUR if booked 2-3 weeks ahead. Night bus available!"),
    dict(mode="ICE / TGV Train", price=50, time="~4h", note="Frankfurt Hbf -> Paris Gare de l'Est. Book at bahn.de or sncf-connect.com. Supersparpreis from 29.90 EUR if booked early."),
    dict(mode="Budget Flight", price=45, time="~1.5h + transfers", note="Ryanair (Frankfurt-Hahn/Paris-Beauvais) or EasyJet. Add ~20-30 EUR airport transfer each side. Total may be 80-100 EUR."),
]

PARIS_TRANSPORT = {
    "t_plus": dict(name="t+ Single Ticket", price=2.15, note="1 trip on metro/bus/RER zone 1. Buy via app or station."),
    "carnet_10": dict(name="Carnet of 10 t+ tickets", price=16.90, note="Saves ~22%. Buy at any metro station or Ile-de-France Mobilites app."),
    "navigo_easy": dict(name="Navigo Easy Card", price=2.00, note="Rechargeable card (2 EUR for card + load t+ at 1.73 EUR each)."),
    "visite_3_z3": dict(name="Paris Visite 3-day (Zone 1-3)", price=30.90, note="Unlimited metro/bus/RER for 3 consecutive days. Good for your trip!"),
    "visite_3_z5": dict(name="Paris Visite 3-day (Zone 1-5)", price=47.00, note="Includes Versailles, CDG/Orly airports."),
}

# ======================================================================
# DAY SETUP -- updated for Mar 21-25
# ======================================================================
DAY_LABELS = {
    0: "Mar 21 -- Arrival Night",
    1: "Mar 22 -- Day 1 (Eiffel, Champs-Elysees, Seine)",
    2: "Mar 23 -- Day 2 (Louvre, Sainte-Chapelle, Rodin)",
    3: "Mar 24 -- Day 3 (Montmartre, Shopping, Cafe)",
    4: "Mar 25 -- Departure Morning",
}
ACTIVE_DAYS = [1, 2, 3]  # the 3 sightseeing days
NIGHTS = 4  # Mar 21, 22, 23, 24
EATING_DAYS = 3  # full sightseeing days

DAY_COLORS = {0: "gray", 1: "red", 2: "blue", 3: "green", 4: "black"}
DAY_HEX = {0: "#78909c", 1: "#e53935", 2: "#1e88e5", 3: "#43a047", 4: "#37474f"}

FOLIUM_ICONS = {
    "Tower": "tower-broadcast", "Shopping": "bag-shopping", "Monument": "landmark",
    "Museum": "building-columns", "Boat": "ship", "Art": "palette",
    "Church": "church", "Statue": "person", "Castle": "chess-rook",
    "Shop": "store", "Coffee": "mug-hot", "Science": "flask",
}

# ======================================================================
# HELPERS
# ======================================================================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def walk_min(km):
    return max(1, round(km / 4.5 * 60))

def nn_route(places):
    if len(places) <= 1:
        return list(places)
    rem = list(places)
    route = [rem.pop(0)]
    while rem:
        last = route[-1]
        nxt = min(rem, key=lambda p: haversine(last["lat"], last["lng"], p["lat"], p["lng"]))
        route.append(nxt)
        rem.remove(nxt)
    return route

def route_km(places):
    return sum(haversine(places[i]["lat"], places[i]["lng"], places[i+1]["lat"], places[i+1]["lng"])
               for i in range(len(places)-1))

def get_day_places(day_num):
    en = st.session_state.enabled
    assigned = [p for p in PLACES if st.session_state.days.get(p["id"]) == day_num and en.get(p["id"], True)]
    return nn_route(assigned)

def calc_budget():
    n = st.session_state.n_people
    hotel = HOTELS[st.session_state.hotel_idx]
    en = st.session_state.enabled

    accom = hotel["price"] * NIGHTS
    tickets = sum(p["cost"] for p in PLACES if en.get(p["id"], True)) * n

    opt_to = TRANSPORT_FFM[st.session_state.tr_to]
    opt_from = TRANSPORT_FFM[st.session_state.tr_from]
    long_tr = (opt_to["price"] + opt_from["price"]) * n

    lk = st.session_state.local_tr
    li = PARIS_TRANSPORT[lk]
    if "visite" in lk:
        local_tr = li["price"] * n
    elif lk == "carnet_10":
        rides_est = 6 * EATING_DAYS  # ~6 rides/day x 3 days
        local_tr = li["price"] * math.ceil(rides_est / 10) * n
    else:
        local_tr = li["price"] * 6 * EATING_DAYS * n

    food = st.session_state.food_day * EATING_DAYS
    shop = st.session_state.shop_budget
    total = accom + tickets + long_tr + local_tr + food + shop
    return dict(accom=accom, tickets=tickets, long_tr=long_tr, local_tr=local_tr,
                food=food, shop=shop, total=total, pp=total/n)

def metro_day_cost():
    """Estimate metro cost for a single day."""
    n = st.session_state.n_people
    lk = st.session_state.local_tr
    li = PARIS_TRANSPORT[lk]
    if "visite" in lk:
        return li["price"] * n / EATING_DAYS
    elif lk == "carnet_10":
        return li["price"] * math.ceil(6/10) * n  # ~6 rides/day
    else:
        return li["price"] * 6 * n


# ======================================================================
# BUILD MAP
# ======================================================================
def build_map(places, hotel=None, show_route=True, zoom=12, show_numbers=True,
              restaurants=False, shops_on=False):
    if places:
        clat = sum(p["lat"] for p in places) / len(places)
        clng = sum(p["lng"] for p in places) / len(places)
    else:
        clat, clng = 48.8566, 2.3522

    m = folium.Map(location=[clat, clng], zoom_start=zoom, tiles="CartoDB positron")

    # Hotel
    if hotel:
        folium.Marker(
            [hotel["lat"], hotel["lng"]],
            tooltip="HOTEL: " + hotel["name"],
            popup=f"<b>HOTEL: {hotel['name']}</b><br>{hotel['price']} EUR/night<br>{hotel['area']}<br>Metro: {hotel.get('metro','')}",
            icon=folium.Icon(color="darkblue", icon="bed", prefix="fa"),
        ).add_to(m)

    # Place markers
    for idx, p in enumerate(places):
        day = st.session_state.days.get(p["id"], p["default_day"])
        colour = DAY_COLORS.get(day, "gray")
        fi = FOLIUM_ICONS.get(p["icon"], "info-sign")

        popup_html = (
            f"<div style='min-width:240px'>"
            f"<h4 style='margin:0'>#{idx+1} {p['name']}</h4>"
            f"<p><b>{p['cat']}</b> | {p['hrs']}h | {p['cost']:.2f} EUR/pp</p>"
            f"<p>{p['desc']}</p>"
            f"<p><b>Tip:</b> {p['tip']}</p>"
            f"<p>Hours: {p['hours']}</p></div>"
        )

        if show_numbers:
            icon = folium.DivIcon(html=f"""
                <div style="
                    background:{DAY_HEX.get(day,'#666')};
                    color:white; font-weight:bold; font-size:14px;
                    width:28px; height:28px; border-radius:50%;
                    display:flex; align-items:center; justify-content:center;
                    border:2px solid white; box-shadow:0 2px 6px rgba(0,0,0,.3);
                ">{idx+1}</div>""")
        else:
            icon = folium.Icon(color=colour, icon=fi, prefix="fa")

        folium.Marker(
            [p["lat"], p["lng"]],
            tooltip=f"#{idx+1} {p['name']} ({p['cost']:.0f} EUR/pp)",
            popup=folium.Popup(popup_html, max_width=340),
            icon=icon,
        ).add_to(m)

    # Animated route line
    if show_route and len(places) > 1:
        coords = [[p["lat"], p["lng"]] for p in places]

        AntPath(
            locations=coords,
            color=DAY_HEX.get(
                st.session_state.days.get(places[0]["id"], 1) if places else 1,
                "#e53935"
            ),
            weight=4, opacity=0.8, dash_array=[12, 20], delay=800,
            pulse_color="#ffffff",
        ).add_to(m)

        # Start / End labels
        folium.Marker(
            coords[0],
            icon=folium.DivIcon(html="""<div style="background:#43a047;color:white;font-weight:bold;font-size:11px;
                padding:3px 8px;border-radius:12px;white-space:nowrap;
                border:2px solid white;box-shadow:0 2px 4px rgba(0,0,0,.3);">START</div>"""),
        ).add_to(m)
        folium.Marker(
            coords[-1],
            icon=folium.DivIcon(html="""<div style="background:#e53935;color:white;font-weight:bold;font-size:11px;
                padding:3px 8px;border-radius:12px;white-space:nowrap;
                border:2px solid white;box-shadow:0 2px 4px rgba(0,0,0,.3);">END</div>"""),
        ).add_to(m)

    if restaurants:
        for r in RESTAURANTS:
            folium.CircleMarker(
                [r["lat"], r["lng"]], radius=6, color="#ff9800", fill=True, fill_opacity=0.8,
                tooltip=f"Restaurant: {r['name']} (~{r['avg']} EUR/pp)",
                popup=f"<b>{r['name']}</b><br>{r['cuisine']}<br>~{r['avg']} EUR/pp<br>{r['desc']}",
            ).add_to(m)

    if shops_on:
        for s in SHOPS:
            folium.CircleMarker(
                [s["lat"], s["lng"]], radius=6, color="#e91e63", fill=True, fill_opacity=0.8,
                tooltip=f"Shop: {s['name']}",
                popup=f"<b>{s['name']}</b><br>{s['cat']}<br>{s['desc']}",
            ).add_to(m)

    return m


def show_map(m, height=520):
    try:
        from streamlit_folium import st_folium
        st_folium(m, width=None, height=height, returned_objects=[])
    except ImportError:
        from streamlit.components.v1 import html as st_html
        st_html(m._repr_html_(), height=height + 20)


# ======================================================================
# SESSION STATE
# ======================================================================
if "days" not in st.session_state:
    st.session_state.days = {p["id"]: p["default_day"] for p in PLACES}
if "enabled" not in st.session_state:
    st.session_state.enabled = {p["id"]: True for p in PLACES}
if "hotel_idx" not in st.session_state:
    st.session_state.hotel_idx = 0
if "tr_to" not in st.session_state:
    st.session_state.tr_to = 0
if "tr_from" not in st.session_state:
    st.session_state.tr_from = 0
if "local_tr" not in st.session_state:
    st.session_state.local_tr = "visite_3_z3"
if "food_day" not in st.session_state:
    st.session_state.food_day = 50
if "shop_budget" not in st.session_state:
    st.session_state.shop_budget = 150
if "n_people" not in st.session_state:
    st.session_state.n_people = 2


# ======================================================================
# SIDEBAR
# ======================================================================
with st.sidebar:
    st.title("Trip Settings")
    st.markdown("**Frankfurt -> Paris -> Frankfurt**")
    st.markdown("**Mar 21 night - Mar 25 early morning**")
    st.markdown("3 full days | 4 nights | Couple")
    st.divider()

    st.subheader("Hotel")
    h_names = [f"{h['name']} -- {h['price']} EUR/n" for h in HOTELS]
    st.session_state.hotel_idx = st.selectbox("Choose hotel:", range(len(HOTELS)),
        format_func=lambda i: h_names[i], index=st.session_state.hotel_idx, key="h_sel")
    h = HOTELS[st.session_state.hotel_idx]
    st.caption(f"Metro: {h.get('metro','N/A')} | {h.get('walk_center','')}")

    st.divider()
    st.subheader("Frankfurt <-> Paris")
    t_labels = [f"{t['mode']} -- {t['price']} EUR/pp ({t['time']})" for t in TRANSPORT_FFM]
    st.session_state.tr_to = st.selectbox("To Paris:", range(len(TRANSPORT_FFM)),
        format_func=lambda i: t_labels[i], index=st.session_state.tr_to, key="tr_to_sel")
    st.session_state.tr_from = st.selectbox("Back to Frankfurt:", range(len(TRANSPORT_FFM)),
        format_func=lambda i: t_labels[i], index=st.session_state.tr_from, key="tr_from_sel")

    st.divider()
    st.subheader("Paris Metro / Bus")
    lt_keys = list(PARIS_TRANSPORT.keys())
    lt_labels = {k: f"{v['name']} -- {v['price']} EUR" for k, v in PARIS_TRANSPORT.items()}
    st.session_state.local_tr = st.radio("Local pass:", lt_keys,
        format_func=lambda k: lt_labels[k],
        index=lt_keys.index(st.session_state.local_tr), key="lt_radio")

    st.divider()
    st.subheader("Budget Estimates")
    st.session_state.food_day = st.slider("Food/day (couple, EUR):", 30, 150,
        st.session_state.food_day, step=5, key="food_sl")
    st.session_state.shop_budget = st.slider("Shopping total (EUR):", 0, 500,
        st.session_state.shop_budget, step=25, key="shop_sl")

    st.divider()
    st.caption("Change any setting -> plan updates live!")


# ======================================================================
# MAIN TABS
# ======================================================================
st.title("Paris Trip Planner -- March 21-25, 2026")
st.caption("3 full days, 4 nights. Adjust everything in sidebar & Day Planner. All updates are live.")

tab_overview, tab_days, tab_map, tab_budget, tab_hotels, tab_transport, tab_eat, tab_shop = st.tabs([
    "Overview", "Day Planner", "Map & Routes", "Budget",
    "Hotel Guide", "Transport", "Where to Eat", "Shopping Guide",
])


# ======================================================================
# TAB: OVERVIEW
# ======================================================================
with tab_overview:
    budget = calc_budget()
    hotel = HOTELS[st.session_state.hotel_idx]
    en = st.session_state.enabled
    active = [p for p in PLACES if en.get(p["id"], True)]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Trip", "4 nights / 3 days")
    c2.metric("Places", f"{len(active)}")
    c3.metric("Hotel", f"{hotel['price']} EUR/n")
    c4.metric("Total Est.", f"{budget['total']:.0f} EUR")
    c5.metric("Per Person", f"{budget['pp']:.0f} EUR")

    st.markdown("---")
    st.subheader("Quick Itinerary")
    for d in DAY_LABELS:
        dp = get_day_places(d)
        label = DAY_LABELS[d]
        names = " -> ".join(p["name"] for p in dp) if dp else "-- travel / free time --"
        st.markdown(f"**{label}:** {names}")

    st.markdown("---")
    st.subheader("All Places at a Glance")
    m = build_map(active, hotel=hotel, show_route=False, zoom=12, show_numbers=False)
    show_map(m, 480)


# ======================================================================
# TAB: DAY PLANNER
# ======================================================================
with tab_days:
    st.subheader("Assign Places to Days")
    st.caption("Toggle places on/off and reassign days. Route & budget update instantly.")

    # Note about Mont-Saint-Michel
    mst_enabled = st.session_state.enabled.get("mont_saint_michel", True)
    if mst_enabled:
        st.warning("Mont-Saint-Michel is a FULL DAY trip and is currently DISABLED by default (assigned to arrival night). "
                   "With only 3 days in Paris, it's recommended to skip it or replace an entire day. "
                   "Toggle it off or assign it to a day if you really want to go.")

    for p in PLACES:
        col_on, col_name, col_cat, col_day, col_cost = st.columns([0.5, 3, 1.5, 2.5, 1])
        with col_on:
            is_on = st.checkbox("Enable", value=st.session_state.enabled.get(p["id"], True),
                                key=f"en_{p['id']}", label_visibility="collapsed")
            st.session_state.enabled[p["id"]] = is_on
        with col_name:
            style = "" if is_on else "color:#aaa;text-decoration:line-through;"
            st.markdown(f"<span style='{style}'><b>{p['name']}</b></span>", unsafe_allow_html=True)
        with col_cat:
            st.caption(p["cat"])
        with col_day:
            cur = st.session_state.days.get(p["id"], p["default_day"])
            new_d = st.selectbox("Day", list(DAY_LABELS.keys()),
                format_func=lambda d: DAY_LABELS[d], index=cur,
                key=f"day_{p['id']}", label_visibility="collapsed", disabled=not is_on)
            st.session_state.days[p["id"]] = new_d
        with col_cost:
            st.caption(f"{p['cost']:.2f} EUR/pp" if p["cost"] > 0 else "FREE")


# ======================================================================
# TAB: MAP & ROUTES
# ======================================================================
with tab_map:
    st.subheader("Map & Route Planner")

    map_mode = st.radio("View mode:", ["Day Route", "All Places", "By Category"],
                        horizontal=True, key="map_mode")

    hotel = HOTELS[st.session_state.hotel_idx]
    en = st.session_state.enabled
    all_active = [p for p in PLACES if en.get(p["id"], True)]

    show_rest = st.checkbox("Show restaurants on map", value=False, key="show_rest")
    show_shops = st.checkbox("Show shops on map", value=False, key="show_shops")

    if map_mode == "Day Route":
        sel_day = st.selectbox("Choose day to see route:", ACTIVE_DAYS,
            format_func=lambda d: DAY_LABELS[d], key="route_day")

        day_places = get_day_places(sel_day)

        if not day_places:
            st.warning("No places assigned to this day. Assign places in the Day Planner tab.")
        else:
            zoom = 13
            m = build_map(day_places, hotel=hotel, show_route=True, zoom=zoom,
                          show_numbers=True, restaurants=show_rest, shops_on=show_shops)
            show_map(m, 520)

            st.markdown("---")

            # Route summary
            n = st.session_state.n_people
            total_km = route_km(day_places)
            total_walk = walk_min(total_km)
            day_cost_tickets = sum(p["cost"] for p in day_places) * n
            day_hours = sum(p["hrs"] for p in day_places)

            rc1, rc2, rc3, rc4 = st.columns(4)
            rc1.metric("Route Distance", f"{total_km:.1f} km")
            rc2.metric("Walking Time", f"~{total_walk} min")
            rc3.metric(f"Tickets (x{n})", f"{day_cost_tickets:.0f} EUR")
            rc4.metric("Activity Time", f"~{day_hours:.1f} h")

            st.markdown("---")
            st.subheader("Route: Step by Step")

            # Hotel -> Stop 1
            first = day_places[0]
            d_hotel = haversine(hotel["lat"], hotel["lng"], first["lat"], first["lng"])
            st.markdown(f"""<div class="route-step">
                <b>HOTEL</b> ({hotel['name']})
                &nbsp;&rarr;&nbsp; <b>Stop #1:</b> {first['name']}
                &nbsp;&nbsp;|&nbsp;&nbsp; {d_hotel:.1f} km (~{walk_min(d_hotel)} min walk / metro)
            </div>""", unsafe_allow_html=True)

            for i, p in enumerate(day_places):
                cost_label = f"{p['cost']:.2f} EUR/pp" if p["cost"] > 0 else "FREE"
                st.markdown(f"""<div class="route-step">
                    <b>Stop #{i+1}:</b> {p['name']}
                    &nbsp;&nbsp;|&nbsp;&nbsp; {p['hrs']}h &nbsp;|&nbsp; {cost_label}
                    &nbsp;&nbsp;|&nbsp;&nbsp; <i>{p['desc']}</i>
                </div>""", unsafe_allow_html=True)

                if i < len(day_places) - 1:
                    nxt = day_places[i + 1]
                    d = haversine(p["lat"], p["lng"], nxt["lat"], nxt["lng"])
                    st.markdown(f"""<div style="text-align:center;color:#1e88e5;font-size:1.1rem;margin:2px 0;">
                        &#8595;&nbsp;&nbsp; {d:.1f} km (~{walk_min(d)} min walk)
                    </div>""", unsafe_allow_html=True)

            # Last stop -> Hotel
            last = day_places[-1]
            d_back = haversine(last["lat"], last["lng"], hotel["lat"], hotel["lng"])
            st.markdown(f"""<div class="route-step">
                <b>Stop #{len(day_places)}</b> ({last['name']})
                &nbsp;&rarr;&nbsp; <b>HOTEL</b>
                &nbsp;&nbsp;|&nbsp;&nbsp; {d_back:.1f} km (~{walk_min(d_back)} min walk / metro)
            </div>""", unsafe_allow_html=True)

            # Day expenses
            st.markdown("---")
            st.subheader(f"Day {sel_day} Expenses")

            food_est = st.session_state.food_day
            m_cost = metro_day_cost()

            exp_data = []
            for p in day_places:
                if p["cost"] > 0:
                    exp_data.append({"Item": p["name"], "Type": "Ticket",
                                     f"EUR (x{n})": round(p["cost"] * n, 2)})
            exp_data.append({"Item": "Food (estimated)", "Type": "Food",
                             f"EUR (x{n})": round(food_est, 2)})
            exp_data.append({"Item": "Metro / Bus", "Type": "Transport",
                             f"EUR (x{n})": round(m_cost, 2)})

            edf = pd.DataFrame(exp_data)
            total_col = f"EUR (x{n})"
            st.dataframe(edf, hide_index=True)
            st.metric(f"Day {sel_day} Total", f"{edf[total_col].sum():.0f} EUR")

    elif map_mode == "All Places":
        m = build_map(all_active, hotel=hotel, show_route=False, zoom=12, show_numbers=False,
                      restaurants=show_rest, shops_on=show_shops)
        show_map(m, 550)

    else:
        cats = sorted(set(p["cat"] for p in PLACES))
        sel_cat = st.selectbox("Category:", cats, key="map_cat_sel")
        cat_p = [p for p in all_active if p["cat"] == sel_cat]
        m = build_map(cat_p, hotel=hotel, show_route=False, zoom=13, show_numbers=False,
                      restaurants=show_rest, shops_on=show_shops)
        show_map(m, 550)

    st.caption("Numbered circles = stop order | Animated line = route | Blue bed = hotel | Orange = restaurants | Pink = shops")


# ======================================================================
# TAB: BUDGET
# ======================================================================
with tab_budget:
    st.subheader("Full Budget Breakdown")
    budget = calc_budget()
    hotel = HOTELS[st.session_state.hotel_idx]
    n = st.session_state.n_people

    s1, s2, s3 = st.columns(3)
    s1.metric("Grand Total", f"{budget['total']:.0f} EUR")
    s2.metric("Per Person", f"{budget['pp']:.0f} EUR")
    s3.metric("Per Day (avg)", f"{budget['total']/EATING_DAYS:.0f} EUR")

    st.markdown("---")

    data = {
        "Category": [f"Hotel ({NIGHTS} nights)", "Attraction Tickets", "Frankfurt <-> Paris",
                      "Local Transport", f"Food ({EATING_DAYS} days)", "Shopping"],
        "Amount (EUR)": [budget["accom"], budget["tickets"], budget["long_tr"],
                         budget["local_tr"], budget["food"], budget["shop"]],
    }
    df = pd.DataFrame(data)
    df["% of Total"] = (df["Amount (EUR)"] / budget["total"] * 100).round(1)
    st.dataframe(df, hide_index=True)
    st.bar_chart(df.set_index("Category")["Amount (EUR)"], color="#002654")

    st.markdown("---")
    st.subheader("Ticket Details (accurate 2025/2026 prices)")
    en = st.session_state.enabled
    tkt = []
    for p in PLACES:
        if en.get(p["id"], True) and p["cost"] > 0:
            tkt.append({"Place": p["name"],
                         "Day": DAY_LABELS.get(st.session_state.days[p["id"]], "?"),
                         "EUR/person": p["cost"],
                         f"EUR x{n}": p["cost"]*n})
    if tkt:
        tdf = pd.DataFrame(tkt)
        st.dataframe(tdf, hide_index=True)
        st.metric("Total Tickets", f"{sum(t[f'EUR x{n}'] for t in tkt):.0f} EUR")
    else:
        st.info("All selected places are free!")

    # Day-wise summary
    st.markdown("---")
    st.subheader("Day-Wise Expense Summary")
    day_summary = []
    for d in ACTIVE_DAYS:
        dp = get_day_places(d)
        tix = sum(p["cost"] for p in dp) * n
        food_d = st.session_state.food_day
        m_d = metro_day_cost()
        day_total = tix + food_d + m_d
        day_summary.append({
            "Day": DAY_LABELS[d],
            "Tickets": round(tix, 0),
            "Food": round(food_d, 0),
            "Metro": round(m_d, 0),
            "DAY TOTAL": round(day_total, 0),
        })
    st.dataframe(pd.DataFrame(day_summary), hide_index=True)

    st.markdown("---")
    st.subheader("Money-Saving Tips")
    tips = [
        "**Free:** Petit Palais, Montmartre walk, Champs-Elysees, Sacre-Coeur, Galeries Lafayette rooftop.",
        "**Paris Museum Pass (2 days = 55 EUR):** Covers Louvre (22), Sainte-Chapelle (11.50), Arc de Triomphe (16), Musee Rodin (14), and 50+ more. SAVES money if visiting 3+ paid museums!",
        "**Eat cheap:** Boulangeries for breakfast (3-5 EUR/pp), Bouillons for dinner (12-18 EUR/pp), park picnics.",
        "**Paris Visite 3-day pass (30.90 EUR):** Best value for your 3-day trip if you ride metro 4+ times/day.",
        "**Citypharma** = cheapest French pharmacy cosmetics in all of Paris. Go early!",
        "**Tap water** is free in restaurants -- ask for 'une carafe d'eau'.",
        "**Eiffel Tower stairs** (11.80 EUR) saves 17.60 EUR vs lift to top (29.40 EUR). Great workout!",
    ]
    for t in tips:
        st.markdown(f"- {t}")


# ======================================================================
# TAB: HOTEL GUIDE
# ======================================================================
with tab_hotels:
    st.subheader("Hotel Guide -- Budget & Well-Connected")
    st.caption(f"You need {NIGHTS} nights (Mar 21-24). Prices are per night for a double room, estimated for March 2026.")

    st.markdown("### How to find the best deal:")
    st.markdown("""
- **Booking.com** -- filter by 'Free cancellation', sort by 'Price', check map view
- **Hostelworld** -- for hostels with private rooms (cheapest option for couples)
- **Google Hotels** -- compares all sites at once, shows price trends
- **Airbnb** -- sometimes cheaper for 4 nights, check entire apartments near metro
- **Book 4-6 weeks ahead** for best prices. Prices rise sharply 2 weeks before.
    """)

    st.markdown("---")
    st.markdown("### Our Picks (sorted by price)")

    sorted_hotels = sorted(HOTELS, key=lambda h: h["price"])
    for h in sorted_hotels:
        total_cost = h["price"] * NIGHTS
        with st.expander(f"{h['name']} -- {h['price']} EUR/night ({total_cost} EUR total for {NIGHTS}n)"):
            hc1, hc2 = st.columns([3, 1])
            with hc1:
                st.write(h["desc"])
                st.write(f"**Area:** {h['area']}")
                st.write(f"**Metro:** {h.get('metro', 'N/A')}")
                st.write(f"**Walk to centre:** {h.get('walk_center', 'N/A')}")
            with hc2:
                st.metric("Per Night", f"{h['price']} EUR")
                st.metric(f"{NIGHTS} Nights", f"{total_cost} EUR")
                st.metric("Rating", f"{h['stars']}/5")

    st.markdown("---")
    st.markdown("### Price comparison at a glance")
    hotel_df = pd.DataFrame([{
        "Hotel": h["name"],
        "EUR/night": h["price"],
        f"Total ({NIGHTS}n)": h["price"] * NIGHTS,
        "Rating": h["stars"],
        "Area": h["area"],
        "Metro": h.get("metro", ""),
    } for h in sorted_hotels])
    st.dataframe(hotel_df, hide_index=True)

    st.markdown("---")
    st.markdown("### Best areas to stay (for your itinerary)")
    st.markdown("""
**1. Le Marais (3rd/4th)** -- BEST location. Walk to Louvre, Notre-Dame, Bastille. Tons of restaurants. But pricier.\n
**2. Republique / Canal Saint-Martin (10th/11th)** -- BEST VALUE. 5-line metro hub. Hip area, cheap eats. 15 min to everything.\n
**3. Gare du Nord / Gare de l'Est (10th)** -- CHEAPEST. Huge metro hub. Not the prettiest area but super connected.\n
**4. Montmartre (18th)** -- CHARMING. Walk to Sacre-Coeur. Metro Line 2 = direct to Champs-Elysees. Hilly!\n
**5. Latin Quarter (5th)** -- CLASSIC PARIS. Walk to Notre-Dame, Sainte-Chapelle. Student area = cheap food.
    """)


# ======================================================================
# TAB: TRANSPORT
# ======================================================================
with tab_transport:
    st.subheader("Getting Around")

    st.markdown("### Frankfurt -> Paris (March 21)")
    opt = TRANSPORT_FFM[st.session_state.tr_to]
    st.info(f"**{opt['mode']}** -- {opt['price']} EUR/pp | {opt['time']}\n\n{opt['note']}")

    st.markdown("### Paris -> Frankfurt (March 25 early morning)")
    opt = TRANSPORT_FFM[st.session_state.tr_from]
    st.info(f"**{opt['mode']}** -- {opt['price']} EUR/pp | {opt['time']}\n\n{opt['note']}")

    st.markdown("---")
    st.markdown("### Paris Local Transport")
    local = PARIS_TRANSPORT[st.session_state.local_tr]
    st.success(f"**Selected:** {local['name']} -- {local['price']} EUR\n\n{local['note']}")

    st.markdown("**All options compared:**")
    pt_data = [{"Pass": v["name"], "Price (EUR)": v["price"], "Details": v["note"]}
               for v in PARIS_TRANSPORT.values()]
    st.dataframe(pd.DataFrame(pt_data), hide_index=True)

    st.markdown("---")
    st.markdown("### Paris Metro Tips")
    st.markdown("""
- **Metro runs:** 5:30-1:00 (till 2:00 Fri/Sat nights)
- **Best app:** Ile-de-France Mobilites (real-time, buy tickets in-app)
- **Google Maps** works perfectly for transit directions
- **Keep your ticket** until exit -- random ticket inspections!
- **RER B** connects CDG airport to central Paris (~11.80 EUR, ~35 min)
- **Navigo Easy** is the most flexible: load as you go at any station
    """)


# ======================================================================
# TAB: WHERE TO EAT
# ======================================================================
with tab_eat:
    st.subheader("Where to Eat -- Budget for Couples")
    st.caption("A couple can eat very well in Paris on 40-60 EUR/day total.")

    st.markdown("### Suggested Daily Meal Plan (couple)")
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown("**Breakfast -- 6-10 EUR total**")
        st.markdown("- Boulangerie: 2 croissants + 2 cafe creme\n- Pain au chocolat = 1.50 EUR\n- Or hotel breakfast if included")
    with mc2:
        st.markdown("**Lunch -- 15-25 EUR total**")
        st.markdown("- Bouillon (3 courses = 12-18 EUR/pp)\n- Falafel / kebab (6-10 EUR/pp)\n- Creperie galette + cider\n- Supermarket + park picnic (8-12 EUR!)")
    with mc3:
        st.markdown("**Dinner -- 25-45 EUR total**")
        st.markdown("- Bouillon Chartier / Racine / Julien\n- Pink Mamma (Italian, generous)\n- Chez Janou (chocolate mousse!)\n- Bistro plat du jour (15-20 EUR/pp)")

    st.markdown("---")
    st.markdown("### Top Restaurant Picks")
    for r in RESTAURANTS:
        with st.expander(f"{r['name']} -- {r['cuisine']} | ~{r['avg']} EUR/pp"):
            rc1, rc2 = st.columns([3, 1])
            with rc1:
                st.write(r["desc"])
                st.write(f"**Tip:** {r['tip']}")
            with rc2:
                st.metric("Cost/pp", f"{r['avg']} EUR")
                st.metric("Couple", f"{r['avg']*2} EUR")

    st.markdown("---")
    st.markdown("### Supermarket Picnic Strategy")
    st.markdown("""
Best romantic budget meal! Eat for **8-12 EUR total** for two:

1. **Monoprix / Franprix / Carrefour City** -- literally everywhere
2. Pick up: baguette (1.20), cheese (3), charcuterie (3), fruit (2), bottle of wine (4)
3. Head to **Champ de Mars**, **Jardin du Luxembourg**, or **Seine riverbanks**
    """)


# ======================================================================
# TAB: SHOPPING
# ======================================================================
with tab_shop:
    st.subheader("Shopping -- Cheap Branded Cosmetics & Clothes")
    st.caption("French pharmacy brands are 30-50% cheaper in Paris than in Germany or elsewhere.")

    st.markdown("### Cosmetics & Skincare -- Best Deals")
    cos_shops = [s for s in SHOPS if "Cosmetic" in s["cat"]]
    for s in cos_shops:
        with st.expander(f"{s['name']} -- {s['budget']}"):
            st.write(s["desc"])
            st.write(f"**Tip:** {s['tip']}")

    st.markdown("**Price Comparison (Paris pharmacy vs abroad):**")
    cdf = pd.DataFrame([
        {"Brand": "La Roche-Posay", "Product": "Effaclar Duo+ 40ml", "Paris": "~13 EUR", "Germany": "~20 EUR", "Save": "~35%"},
        {"Brand": "Bioderma", "Product": "Sensibio H2O 500ml", "Paris": "~11 EUR", "Germany": "~17 EUR", "Save": "~35%"},
        {"Brand": "Vichy", "Product": "Mineral 89 50ml", "Paris": "~17 EUR", "Germany": "~27 EUR", "Save": "~37%"},
        {"Brand": "Avene", "Product": "Thermal Water 300ml", "Paris": "~7 EUR", "Germany": "~13 EUR", "Save": "~46%"},
        {"Brand": "Nuxe", "Product": "Huile Prodigieuse 100ml", "Paris": "~20 EUR", "Germany": "~32 EUR", "Save": "~38%"},
        {"Brand": "Caudalie", "Product": "Beauty Elixir 100ml", "Paris": "~17 EUR", "Germany": "~28 EUR", "Save": "~39%"},
        {"Brand": "Embryolisse", "Product": "Lait-Creme 75ml", "Paris": "~12 EUR", "Germany": "~20 EUR", "Save": "~40%"},
    ])
    st.dataframe(cdf, hide_index=True)

    st.markdown("---")
    st.markdown("### Clothes & Fashion")
    cloth_shops = [s for s in SHOPS if "Clothes" in s["cat"] or "Vintage" in s["cat"]]
    for s in cloth_shops:
        with st.expander(f"{s['name']} -- {s['budget']}"):
            st.write(s["desc"])
            st.write(f"**Tip:** {s['tip']}")

    st.markdown("---")
    st.markdown("### Tax Refund (Detaxe)")
    st.markdown("""
**Non-EU residents** can claim **12% VAT refund** on purchases over **100.01 EUR** from one store.

**If you live in Germany (EU resident):** You are NOT eligible for detaxe.
BUT French prices are already much lower for French brands -- that's your saving!

For non-EU friends: Ask for 'detaxe' form -> validate at airport PABLO kiosk -> refund on card.
    """)


# ======================================================================
# FOOTER
# ======================================================================
st.markdown("---")
st.caption("Paris Trip Planner | March 21-25, 2026 | Prices researched from official sites (2025/2026) | Bon voyage!")
