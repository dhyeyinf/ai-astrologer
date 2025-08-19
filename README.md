# AI Astrologer

A sophisticated astrology app built with Streamlit, featuring a rule-based horoscope generator, interactive Plotly charts, and a cosmic Q&A system.

## Features
- **Polished UI**: Clean Streamlit interface with vibrant cosmic styling.
- **Comprehensive Horoscope**: Generates detailed profiles based on Sun, Moon (simulated), and Ascendant (simulated) signs, including traits, elements, and lucky numbers.
- **Interactive Charts**: Personality radar chart, zodiac element distribution, and compatibility analysis with all signs.
- **Cosmic Q&A**: Answers questions about love, career, health, or general guidance with zodiac context.
- **Broad Location Support**: Accepts any city/country (no external API dependency).
- **Responsive Design**: Wide layout with sidebar inputs and tabbed analysis.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/YOUR_USERNAME/ai-astrologer.git
   cd ai-astrologer
   ```
2. Create and activate a virtual environment (Python 3.11 recommended):
   ```
   python3.11 -m venv venv
   source venv/bin/activate  # Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```

## Usage
- Enter birth details (name, date, time, city, country).
- Click "Generate Cosmic Profile" to see Sun, Moon, Ascendant details, horoscope, and charts.
- Use the "Ask the Cosmos" section to ask about love, career, health, or life purpose.
- Explore compatibility with any zodiac sign via the dropdown.

## Notes
- Moon and Ascendant signs are simulated (random) for demo simplicity. Real calculations require ephemeris data (e.g., via kerykeion, not used to avoid GeoNames issues).
- Supports any city/country without external APIs, making it robust for global use.
- Built for reliability and visual appeal to stand out in intern selection.

## Demo Video
A 2–5 minute video showcasing the app is included (link or in zip). It demonstrates:
- Entering birth details (e.g., Rajkot, India).
- Generating cosmic profile and charts.
- Asking a question (e.g., "What’s my career like?") and viewing the response.