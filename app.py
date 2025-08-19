import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json

# Enhanced zodiac data with compatibility scores
ZODIAC_DATA = {
    "Aries": {
        "symbol": "♈", "element": "Fire", "quality": "Cardinal", "ruler": "Mars",
        "traits": ["energetic", "bold", "pioneering", "competitive"],
        "colors": ["Red", "Orange"], "lucky_numbers": [1, 8, 17],
        "keywords": ["leadership", "initiative", "courage", "independence"],
        "compatibility": {"Aries": 75, "Taurus": 50, "Gemini": 85, "Cancer": 55, "Leo": 90, "Virgo": 60,
                         "Libra": 80, "Scorpio": 70, "Sagittarius": 95, "Capricorn": 65, "Aquarius": 85, "Pisces": 60}
    },
    "Taurus": {
        "symbol": "♉", "element": "Earth", "quality": "Fixed", "ruler": "Venus",
        "traits": ["reliable", "practical", "devoted", "stable"],
        "colors": ["Green", "Pink"], "lucky_numbers": [2, 6, 9],
        "keywords": ["stability", "patience", "luxury", "sensuality"],
        "compatibility": {"Aries": 50, "Taurus": 80, "Gemini": 55, "Cancer": 85, "Leo": 60, "Virgo": 90,
                         "Libra": 75, "Scorpio": 80, "Sagittarius": 50, "Capricorn": 95, "Aquarius": 55, "Pisces": 70}
    },
    "Gemini": {
        "symbol": "♊", "element": "Air", "quality": "Mutable", "ruler": "Mercury",
        "traits": ["curious", "adaptable", "witty", "communicative"],
        "colors": ["Yellow", "Silver"], "lucky_numbers": [5, 7, 14],
        "keywords": ["communication", "versatility", "learning", "networking"],
        "compatibility": {"Aries": 85, "Taurus": 55, "Gemini": 80, "Cancer": 60, "Leo": 85, "Virgo": 70,
                         "Libra": 95, "Scorpio": 50, "Sagittarius": 80, "Capricorn": 55, "Aquarius": 90, "Pisces": 65}
    },
    "Cancer": {
        "symbol": "♋", "element": "Water", "quality": "Cardinal", "ruler": "Moon",
        "traits": ["nurturing", "intuitive", "protective", "emotional"],
        "colors": ["White", "Silver"], "lucky_numbers": [2, 7, 11],
        "keywords": ["family", "emotions", "intuition", "security"],
        "compatibility": {"Aries": 55, "Taurus": 85, "Gemini": 60, "Cancer": 80, "Leo": 65, "Virgo": 75,
                         "Libra": 60, "Scorpio": 95, "Sagittarius": 50, "Capricorn": 80, "Aquarius": 55, "Pisces": 90}
    },
    "Leo": {
        "symbol": "♌", "element": "Fire", "quality": "Fixed", "ruler": "Sun",
        "traits": ["confident", "generous", "creative", "dramatic"],
        "colors": ["Gold", "Orange"], "lucky_numbers": [1, 3, 10],
        "keywords": ["creativity", "leadership", "drama", "generosity"],
        "compatibility": {"Aries": 90, "Taurus": 60, "Gemini": 85, "Cancer": 65, "Leo": 80, "Virgo": 55,
                         "Libra": 85, "Scorpio": 70, "Sagittarius": 95, "Capricorn": 60, "Aquarius": 80, "Pisces": 65}
    },
    "Virgo": {
        "symbol": "♍", "element": "Earth", "quality": "Mutable", "ruler": "Mercury",
        "traits": ["analytical", "practical", "loyal", "hardworking"],
        "colors": ["Navy Blue", "Grey"], "lucky_numbers": [3, 15, 20],
        "keywords": ["perfection", "service", "health", "analysis"],
        "compatibility": {"Aries": 60, "Taurus": 90, "Gemini": 70, "Cancer": 75, "Leo": 55, "Virgo": 80,
                         "Libra": 65, "Scorpio": 85, "Sagittarius": 50, "Capricorn": 95, "Aquarius": 60, "Pisces": 70}
    },
    "Libra": {
        "symbol": "♎", "element": "Air", "quality": "Cardinal", "ruler": "Venus",
        "traits": ["diplomatic", "balanced", "social", "artistic"],
        "colors": ["Blue", "Green"], "lucky_numbers": [4, 6, 13],
        "keywords": ["balance", "justice", "beauty", "relationships"],
        "compatibility": {"Aries": 80, "Taurus": 75, "Gemini": 95, "Cancer": 60, "Leo": 85, "Virgo": 65,
                         "Libra": 80, "Scorpio": 70, "Sagittarius": 85, "Capricorn": 55, "Aquarius": 90, "Pisces": 65}
    },
    "Scorpio": {
        "symbol": "♏", "element": "Water", "quality": "Fixed", "ruler": "Pluto",
        "traits": ["passionate", "resourceful", "brave", "magnetic"],
        "colors": ["Deep Red", "Black"], "lucky_numbers": [8, 11, 18],
        "keywords": ["transformation", "mystery", "intensity", "power"],
        "compatibility": {"Aries": 70, "Taurus": 80, "Gemini": 50, "Cancer": 95, "Leo": 70, "Virgo": 85,
                         "Libra": 70, "Scorpio": 80, "Sagittarius": 55, "Capricorn": 90, "Aquarius": 60, "Pisces": 95}
    },
    "Sagittarius": {
        "symbol": "♐", "element": "Fire", "quality": "Mutable", "ruler": "Jupiter",
        "traits": ["optimistic", "freedom-loving", "jovial", "philosophical"],
        "colors": ["Purple", "Turquoise"], "lucky_numbers": [3, 9, 22],
        "keywords": ["adventure", "philosophy", "travel", "wisdom"],
        "compatibility": {"Aries": 95, "Taurus": 50, "Gemini": 80, "Cancer": 50, "Leo": 95, "Virgo": 50,
                         "Libra": 85, "Scorpio": 55, "Sagittarius": 80, "Capricorn": 60, "Aquarius": 90, "Pisces": 65}
    },
    "Capricorn": {
        "symbol": "♑", "element": "Earth", "quality": "Cardinal", "ruler": "Saturn",
        "traits": ["responsible", "disciplined", "self-control", "ambitious"],
        "colors": ["Black", "Brown"], "lucky_numbers": [4, 8, 13],
        "keywords": ["ambition", "structure", "responsibility", "success"],
        "compatibility": {"Aries": 65, "Taurus": 95, "Gemini": 55, "Cancer": 80, "Leo": 60, "Virgo": 95,
                         "Libra": 55, "Scorpio": 90, "Sagittarius": 60, "Capricorn": 80, "Aquarius": 65, "Pisces": 75}
    },
    "Aquarius": {
        "symbol": "♒", "element": "Air", "quality": "Fixed", "ruler": "Uranus",
        "traits": ["progressive", "original", "independent", "humanitarian"],
        "colors": ["Light Blue", "Silver"], "lucky_numbers": [4, 7, 11],
        "keywords": ["innovation", "friendship", "technology", "rebellion"],
        "compatibility": {"Aries": 85, "Taurus": 55, "Gemini": 90, "Cancer": 55, "Leo": 80, "Virgo": 60,
                         "Libra": 90, "Scorpio": 60, "Sagittarius": 90, "Capricorn": 65, "Aquarius": 80, "Pisces": 70}
    },
    "Pisces": {
        "symbol": "♓", "element": "Water", "quality": "Mutable", "ruler": "Neptune",
        "traits": ["compassionate", "artistic", "intuitive", "gentle"],
        "colors": ["Mauve", "Sea Green"], "lucky_numbers": [3, 9, 12],
        "keywords": ["spirituality", "dreams", "compassion", "creativity"],
        "compatibility": {"Aries": 60, "Taurus": 70, "Gemini": 65, "Cancer": 90, "Leo": 65, "Virgo": 70,
                         "Libra": 65, "Scorpio": 95, "Sagittarius": 65, "Capricorn": 75, "Aquarius": 70, "Pisces": 80}
    }
}

def calculate_zodiac_sign(birth_date):
    """Calculate zodiac sign from birth date"""
    month, day = birth_date.month, birth_date.day
    
    zodiac_ranges = [
        ("Capricorn", [(12, 22, 31), (1, 1, 19)]),
        ("Aquarius", [(1, 20, 31), (2, 1, 18)]),
        ("Pisces", [(2, 19, 29), (3, 1, 20)]),
        ("Aries", [(3, 21, 31), (4, 1, 19)]),
        ("Taurus", [(4, 20, 30), (5, 1, 20)]),
        ("Gemini", [(5, 21, 31), (6, 1, 20)]),
        ("Cancer", [(6, 21, 30), (7, 1, 22)]),
        ("Leo", [(7, 23, 31), (8, 1, 22)]),
        ("Virgo", [(8, 23, 31), (9, 1, 22)]),
        ("Libra", [(9, 23, 30), (10, 1, 22)]),
        ("Scorpio", [(10, 23, 31), (11, 1, 21)]),
        ("Sagittarius", [(11, 22, 30), (12, 1, 21)])
    ]
    
    for sign, ranges in zodiac_ranges:
        for start_month, start_day, end_day in ranges:
            if month == start_month and start_day <= day <= end_day:
                return sign
    return "Capricorn"

def generate_ai_horoscope(sun_sign, moon_sign, ascendant, birth_date, user_name):
    """Generate comprehensive rule-based horoscope"""
    zodiac = ZODIAC_DATA[sun_sign]
    moon_data = ZODIAC_DATA[moon_sign]
    asc_data = ZODIAC_DATA[ascendant]
    
    # Calculate days until next birthday
    today = datetime.now().date()
    next_birthday = birth_date.replace(year=today.year)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)
    days_to_birthday = (next_birthday - today).days
    
    horoscope = f"""
    🌟 **Cosmic Profile for {user_name}** 🌟
    
    **Solar Essence ({sun_sign} {zodiac['symbol']})**
    Your core being radiates {zodiac['element']} energy, making you naturally {', '.join(zodiac['traits'][:2])}. 
    As a {zodiac['quality']} sign ruled by {zodiac['ruler']}, you approach life with {zodiac['traits'][2]} determination.
    
    **Lunar Emotions ({moon_sign} {moon_data['symbol']})**
    Your emotional landscape is colored by {moon_data['element']} energy, creating {', '.join(moon_data['traits'][:2])} responses to life's experiences.
    
    **Rising Persona ({ascendant} {asc_data['symbol']})**
    Others perceive you as {asc_data['traits'][0]} and {asc_data['traits'][1]}, drawn to your {asc_data['element']} energy.
    
    **Today's Cosmic Weather:**
    The universe aligns to support your {zodiac['keywords'][0]} endeavors. Your {zodiac['element']} nature 
    harmonizes beautifully with current planetary transits, especially favoring {zodiac['keywords'][1]} and {zodiac['keywords'][2]}.
    
    **Personal Power Colors:** {', '.join(zodiac['colors'])}
    **Lucky Numbers:** {', '.join(map(str, zodiac['lucky_numbers']))}
    **Days until your Solar Return:** {days_to_birthday} days
    """
    
    return horoscope

def answer_cosmic_question(question, sun_sign, moon_sign, ascendant):
    """Rule-based question answering with astrological context"""
    sun_data = ZODIAC_DATA[sun_sign]
    moon_data = ZODIAC_DATA[moon_sign]
    
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["love", "relationship", "romance", "partner", "marriage"]):
        response = f"""💕 **Love & Relationships Guidance:**
        
        Your {sun_sign} sun seeks {sun_data['traits'][0]} partnerships, while your {moon_sign} moon needs {moon_data['traits'][0]} emotional connection. 
        
        **Romantic Advice:** As a {sun_data['element']} sign, you're naturally drawn to {sun_data['keywords'][0]} in relationships. Your {ascendant} rising attracts partners who appreciate your {ZODIAC_DATA[ascendant]['traits'][1]} nature.
        
        **Best Approach:** Combine your {sun_sign} {sun_data['traits'][2]} energy with your {moon_sign} emotional {moon_data['traits'][1]} for authentic connections."""
        
    elif any(word in question_lower for word in ["career", "job", "work", "profession", "money", "finance"]):
        response = f"""💼 **Career & Financial Guidance:**
        
        Your {sun_sign} ambition shines in {sun_data['keywords'][0]}-related fields. The {sun_data['element']} element suggests you excel in dynamic, {sun_data['traits'][0]} environments.
        
        **Career Path:** Your {sun_data['quality']} quality makes you naturally {sun_data['traits'][1]} in professional settings. Consider roles involving {', '.join(sun_data['keywords'][:2])}.
        
        **Financial Wisdom:** Trust your {moon_sign} intuition for investments, but use your {sun_sign} {sun_data['traits'][3]} approach for major decisions."""
        
    elif any(word in question_lower for word in ["health", "wellness", "body", "fitness"]):
        response = f"""🌿 **Health & Wellness Guidance:**
        
        Your {sun_sign} constitution benefits from {sun_data['element']}-balancing activities. As a {sun_data['quality']} sign, you need {sun_data['traits'][0]} exercise routines.
        
        **Wellness Approach:** Focus on activities that honor your {sun_data['traits'][1]} nature while supporting your {moon_sign} emotional well-being.
        
        **Energy Management:** Your {ascendant} rising influences how you present your vitality to the world."""
        
    else:
        response = f"""🔮 **General Cosmic Guidance:**
        
        The stars align to support your {sun_sign} journey. Your {sun_data['element']} essence, guided by {sun_data['ruler']}, opens pathways of {sun_data['keywords'][0]}.
        
        **Cosmic Insight:** Channel your {sun_data['traits'][0]} {sun_sign} energy while honoring your {moon_sign} emotional needs. Your {ascendant} rising helps you navigate this beautifully.
        
        **Universal Message:** Trust in your natural {sun_data['traits'][2]} abilities - the universe supports your authentic path."""
    
    return response

def create_compatibility_chart(user_sign):
    """Create interactive compatibility chart"""
    compatibility_data = []
    user_data = ZODIAC_DATA[user_sign]
    
    for sign, score in user_data['compatibility'].items():
        compatibility_data.append({
            'Sign': f"{ZODIAC_DATA[sign]['symbol']} {sign}",
            'Compatibility': score,
            'Element': ZODIAC_DATA[sign]['element']
        })
    
    df = pd.DataFrame(compatibility_data)
    
    fig = px.bar(df, x='Sign', y='Compatibility', 
                 color='Element',
                 title=f"Compatibility with {user_sign} {user_data['symbol']}",
                 color_discrete_map={
                     'Fire': '#ff6b6b',
                     'Earth': '#4ecdc4', 
                     'Air': '#45b7d1',
                     'Water': '#96ceb4'
                 })
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=20
    )
    
    return fig

def create_element_distribution():
    """Create pie chart of zodiac elements"""
    elements = {}
    for sign_data in ZODIAC_DATA.values():
        element = sign_data['element']
        elements[element] = elements.get(element, 0) + 1
    
    fig = go.Figure(data=[go.Pie(
        labels=list(elements.keys()),
        values=list(elements.values()),
        hole=.3,
        marker_colors=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
    )])
    
    fig.update_layout(
        title="Zodiac Elements Distribution",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    return fig

# Streamlit App Configuration
st.set_page_config(
    page_title="AI Astrologer - Cosmic Insights",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Main title with cosmic styling
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 20px; margin-bottom: 2rem;'>
    <h1 style='color: white; font-size: 3rem; margin-bottom: 0.5rem;'>✨ AI Astrologer ✨</h1>
    <p style='color: white; font-size: 1.2rem; opacity: 0.9;'>Discover Your Cosmic Blueprint & Celestial Guidance</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for input
with st.sidebar:
    st.header("🌟 Birth Details")
    
    name = st.text_input("Name", placeholder="Enter your name")
    birth_date = st.date_input("Birth Date", value=datetime.now().date() - timedelta(days=9125))
    birth_time = st.time_input("Birth Time")
    birth_city = st.text_input("Birth City", placeholder="e.g., Rajkot")
    
    country_options = {
        "Afghanistan": "AF", "Albania": "AL", "Algeria": "DZ", "Argentina": "AR", "Australia": "AU",
        "Austria": "AT", "Bangladesh": "BD", "Belgium": "BE", "Brazil": "BR", "Canada": "CA",
        "China": "CN", "Colombia": "CO", "Czech Republic": "CZ", "Denmark": "DK", "Egypt": "EG",
        "Finland": "FI", "France": "FR", "Germany": "DE", "Greece": "GR", "India": "IN",
        "Indonesia": "ID", "Iran": "IR", "Italy": "IT", "Japan": "JP", "Malaysia": "MY",
        "Mexico": "MX", "Netherlands": "NL", "New Zealand": "NZ", "Nigeria": "NG", "Norway": "NO",
        "Pakistan": "PK", "Philippines": "PH", "Poland": "PL", "Portugal": "PT", "Russia": "RU",
        "Saudi Arabia": "SA", "Singapore": "SG", "South Africa": "ZA", "South Korea": "KR",
        "Spain": "ES", "Sweden": "SE", "Switzerland": "CH", "Thailand": "TH", "Turkey": "TR",
        "United Arab Emirates": "AE", "United Kingdom": "GB", "United States": "US"
    }
    birth_country = st.selectbox("Birth Country", options=list(country_options.keys()))
    
    generate_chart = st.button("🚀 Generate Cosmic Profile", type="primary")

# Main content area
if generate_chart and all([name, birth_date, birth_time, birth_city, birth_country]):
    # Calculate zodiac signs
    sun_sign = calculate_zodiac_sign(birth_date)
    # Simulate moon and ascendant calculation (for demo simplicity)
    all_signs = list(ZODIAC_DATA.keys())
    moon_sign = random.choice(all_signs)
    ascendant = random.choice(all_signs)
    
    # Store in session state
    st.session_state.user_profile = {
        'name': name, 'sun_sign': sun_sign, 'moon_sign': moon_sign, 
        'ascendant': ascendant, 'birth_date': birth_date
    }
    
    # Main dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(45deg, #ff6b6b, #ffa500); border-radius: 15px; color: white;'>
            <h2>☀️ Sun Sign</h2>
            <h1 style='font-size: 3rem; margin: 1rem 0;'>{ZODIAC_DATA[sun_sign]['symbol']}</h1>
            <h3>{sun_sign}</h3>
            <p>{ZODIAC_DATA[sun_sign]['element']} • {ZODIAC_DATA[sun_sign]['quality']}</p>
            <p>Ruled by {ZODIAC_DATA[sun_sign]['ruler']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(45deg, #4ecdc4, #44a08d); border-radius: 15px; color: white;'>
            <h2>🌙 Moon Sign</h2>
            <h1 style='font-size: 3rem; margin: 1rem 0;'>{ZODIAC_DATA[moon_sign]['symbol']}</h1>
            <h3>{moon_sign}</h3>
            <p>Emotional Nature</p>
            <p>{ZODIAC_DATA[moon_sign]['element']} Element</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(45deg, #667eea, #764ba2); border-radius: 15px; color: white;'>
            <h2>⬆️ Rising Sign</h2>
            <h1 style='font-size: 3rem; margin: 1rem 0;'>{ZODIAC_DATA[ascendant]['symbol']}</h1>
            <h3>{ascendant}</h3>
            <p>Public Persona</p>
            <p>First Impressions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Personality Analysis", "💕 Compatibility", "🔮 Daily Forecast", "📈 Cosmic Charts"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌟 Core Traits")
            traits_text = ""
            for i, trait in enumerate(ZODIAC_DATA[sun_sign]['traits']):
                traits_text += f"**{trait.title()}:** Your {sun_sign} nature makes you naturally {trait}, "
                traits_text += f"which manifests as {ZODIAC_DATA[sun_sign]['keywords'][i % len(ZODIAC_DATA[sun_sign]['keywords'])]} in daily life.\n\n"
            st.markdown(traits_text)
            
            st.subheader("🎨 Power Elements")
            st.write(f"**Element:** {ZODIAC_DATA[sun_sign]['element']}")
            st.write(f"**Quality:** {ZODIAC_DATA[sun_sign]['quality']}")
            st.write(f"**Ruling Planet:** {ZODIAC_DATA[sun_sign]['ruler']}")
            st.write(f"**Lucky Colors:** {', '.join(ZODIAC_DATA[sun_sign]['colors'])}")
            st.write(f"**Lucky Numbers:** {', '.join(map(str, ZODIAC_DATA[sun_sign]['lucky_numbers']))}")
        
        with col2:
            st.subheader("🧠 Psychological Profile")
            
            # Create personality radar chart
            categories = ['Leadership', 'Creativity', 'Communication', 'Intuition', 'Stability', 'Adventure']
            
            # Generate scores based on zodiac traits
            scores = []
            traits = ZODIAC_DATA[sun_sign]['traits']
            if 'confident' in traits or 'bold' in traits: scores.append(90)
            else: scores.append(60)
            
            if 'creative' in traits or 'artistic' in traits: scores.append(85)
            else: scores.append(50)
            
            if 'communicative' in traits or 'social' in traits: scores.append(80)
            else: scores.append(55)
            
            if 'intuitive' in traits or 'emotional' in traits: scores.append(85)
            else: scores.append(60)
            
            if 'stable' in traits or 'reliable' in traits: scores.append(90)
            else: scores.append(50)
            
            if 'adventurous' in traits or 'freedom-loving' in traits: scores.append(85)
            else: scores.append(45)
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name=f'{sun_sign} Profile',
                line_color='#ff6b6b'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("💕 Zodiac Compatibility Analysis")
        
        # Partner selection
        partner_sign = st.selectbox("Select Partner's Zodiac Sign", 
                                   [""] + list(ZODIAC_DATA.keys()),
                                   format_func=lambda x: f"{ZODIAC_DATA[x]['symbol']} {x}" if x else "Choose a sign...")
        
        if partner_sign:
            compatibility_score = ZODIAC_DATA[sun_sign]['compatibility'].get(partner_sign, 50)
            
            # Compatibility meter
            st.markdown(f"""
            <div style='text-align: center; padding: 2rem; background: linear-gradient(45deg, #667eea, #764ba2); border-radius: 15px; color: white; margin: 1rem 0;'>
                <h2>Compatibility Score</h2>
                <h1 style='font-size: 4rem; margin: 1rem 0;'>{compatibility_score}%</h1>
                <div style='background: rgba(255,255,255,0.2); height: 20px; border-radius: 10px; overflow: hidden;'>
                    <div style='width: {compatibility_score}%; height: 100%; background: linear-gradient(90deg, #ff6b6b, #ffa500, #32cd32); border-radius: 10px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Compatibility analysis
            if compatibility_score >= 85:
                st.success("🔥 **Excellent Match!** You two are cosmically aligned with natural harmony and understanding.")
            elif compatibility_score >= 70:
                st.info("💫 **Great Potential!** Strong cosmic connection with room for beautiful growth together.")
            elif compatibility_score >= 55:
                st.warning("⭐ **Good Match!** With mutual effort and understanding, love can flourish beautifully.")
            else:
                st.error("🌙 **Challenging but Possible!** Opposites can attract - requires patience and compromise.")
            
            # Detailed compatibility breakdown
            st.subheader("🔍 Detailed Analysis")
            user_element = ZODIAC_DATA[sun_sign]['element']
            partner_element = ZODIAC_DATA[partner_sign]['element']
            
            st.write(f"**Elemental Harmony:** {user_element} (You) + {partner_element} (Partner)")
            st.write(f"**Your Traits:** {', '.join(ZODIAC_DATA[sun_sign]['traits'])}")
            st.write(f"**Partner's Traits:** {', '.join(ZODIAC_DATA[partner_sign]['traits'])}")
            
        # Show compatibility chart
        if sun_sign in ZODIAC_DATA:
            fig_compat = create_compatibility_chart(sun_sign)
            st.plotly_chart(fig_compat, use_container_width=True)
    
    with tab3:
        st.subheader("🔮 Your Daily Cosmic Forecast")
        
        # Generate comprehensive horoscope
        horoscope = generate_ai_horoscope(sun_sign, moon_sign, ascendant, birth_date, name)
        st.markdown(horoscope)
        
        # Weekly forecast
        st.subheader("📅 7-Day Cosmic Overview")
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cosmic_energies = ['High', 'Medium', 'Low', 'Very High', 'Medium', 'High', 'Low']
        
        weekly_df = pd.DataFrame({
            'Day': days,
            'Cosmic Energy': [random.choice(['High', 'Medium', 'Very High']) for _ in days],
            'Focus Area': [random.choice(ZODIAC_DATA[sun_sign]['keywords']) for _ in days]
        })
        
        st.dataframe(weekly_df, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌍 Element Distribution")
            fig_elements = create_element_distribution()
            st.plotly_chart(fig_elements, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Your Cosmic Strengths")
            
            # Strength analysis based on sign
            strengths = ZODIAC_DATA[sun_sign]['keywords'] + ZODIAC_DATA[sun_sign]['traits']
            strength_scores = [random.randint(70, 95) for _ in strengths[:6]]
            
            strength_df = pd.DataFrame({
                'Strength': strengths[:6],
                'Score': strength_scores
            })
            
            fig_strength = px.bar(strength_df, x='Score', y='Strength', 
                                 color='Score', color_continuous_scale='viridis')
            fig_strength.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_strength, use_container_width=True)

# Cosmic Q&A Section
st.markdown("---")
st.subheader("🔮 Ask the Cosmos")

question = st.text_input("Ask any question about love, career, life purpose, or your cosmic journey...", 
                        placeholder="e.g., What does my future hold in love?")

if st.button("✨ Get Cosmic Guidance") and question:
    if 'user_profile' in st.session_state:
        profile = st.session_state.user_profile
        
        with st.spinner("🌌 Consulting the celestial wisdom..."):
            # Simulate processing
            import time
            time.sleep(2)
            
            response = answer_cosmic_question(question, profile['sun_sign'], 
                                           profile['moon_sign'], profile['ascendant'])
            
            st.markdown(f"""
            <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;'>
                <h3 style='color: #ffd700; margin-bottom: 1rem;'>🔮 Cosmic Response:</h3>
                {response}
                <p style='margin-top: 1rem; font-style: italic; opacity: 0.8;'>✨ The stars have spoken. Use this wisdom to guide your path forward.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please generate your cosmic profile first!")

# Additional features section
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px;'>
        <h3>🎯 Daily Affirmations</h3>
        <p>Personalized cosmic affirmations based on your astrological profile</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px;'>
        <h3>🌙 Lunar Calendar</h3>
        <p>Track moon phases and their influence on your zodiac sign</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px;'>
        <h3>💎 Crystal Recommendations</h3>
        <p>Discover crystals that amplify your astrological energies</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem; margin-top: 3rem; opacity: 0.7;'>
    <p>✨ Crafted with cosmic love • Rule-Based Astrological Insights ✨</p>
</div>
""", unsafe_allow_html=True)