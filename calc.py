import streamlit as st
import os

# הגדרת עמוד RTL ועיצוב מותאם למובייל ולמחשב
st.set_page_config(page_title="מחשבון אירועים - EM Group", page_icon="🎵", layout="centered")

# עיצוב CSS מקיף: רקע אפור עדין + יישור ימין מלא (RTL) + מסגרות סגולות
st.markdown("""
    <style>
    /* רקע אפור עדין לכל האפליקציה */
    .stApp {
        background-color: #F4F5F7 !important;
    }
    
    /* יישור ימין כללי */
    div[data-testid="stAppViewContainer"] { text-align: right; direction: rtl; }
    div[data-baseweb="select"] { direction: rtl; }
    .stCheckbox { text-align: right; }
    .stRadio { text-align: right; }
    .stNumberInput { direction: rtl; text-align: right; }
    div[data-testid="stNotification"] { text-align: right; direction: rtl; }
    div[data-testid="stMarkdownContainer"] { text-align: right; direction: rtl; }

    /* מסגרת סגולה בולטת וקבועה לתיבות הבחירה ושדות המספרים */
    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInput"] > div > div {
        border: 2px solid #8E24AA !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }

    /* שינוי צבע המסגרת בלחיצה/פוקוס (סגול כהה עם הילה) */
    div[data-baseweb="select"] > div:focus-within,
    div[data-testid="stNumberInput"] > div > div:focus-within {
        border-color: #4A148C !important;
        box-shadow: 0 0 6px rgba(142, 36, 170, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# הצגת לוגו (אם קיים קובץ logo.png במאגר)
if os.path.exists("logo.png"):
    col1, col2 = st.columns([1, 2])
    with col2:
        st.image("logo.png", width=200)

# כותרות פתיחה
st.title("🎧 מחשבון תמחור אירועים – EM Group")
st.caption("מערכת תמחור פנימית עבור מנהלת המשרד: מירב מימוני")
st.markdown("---")

# 1. כללי ונסיעות
st.header("1. כללי ונסיעות")
client_type = st.radio("סוג לקוח:", ["לקוח רגיל / פרטי", "בית ספר / מוסד (10% הנחה)"])
is_school = client_type == "בית ספר / מוסד (10% הנחה)"

travel_option = st.selectbox("מרחק הגעה:", [
    "מקומי / קרוב (0 ₪)",
    "מרחק בינוני - עד שעה (+500 ₪)",
    "מרוחק - עד שעה וחצי (+1,000 ₪)"
])
travel_cost = 0
if "עד שעה (+500" in travel_option:
    travel_cost = 500
elif "עד שעה וחצי (+1,000" in travel_option:
    travel_cost = 1000

# 2. חבילת בסיס
st.header("2. חבילת בסיס")
st.info("חבילת בסיס (2,800 ₪): מערכת הגברה מותאמת עד 500 איש, מיקסר, מוניטור במה, 2 מיקרופונים אלחוטיים, איש צוות אחד, אירוע של עד 3 שעות בשטח.")
base_price = 2800

# 3. צוות, ציוד ותוספות
st.header("3. צוות, ציוד ותוספות")

extra_hours = st.number_input("שעות חזרה גנרלית / המתנה נוספות (350 ₪/שעה):", min_value=0, max_value=12, value=0)
extra_hours_price = extra_hours * 350

extra_staff = st.number_input("תוספת אנשי צוות (איש צוות 1 כלול בבסיס, 400 ₪ לכל איש צוות נוסף):", min_value=0, max_value=10, value=0)
staff_price = extra_staff * 400

total_mics = st.number_input("סה\"כ מיקרופונים אלחוטיים (2 כלולים בבסיס, 150 ₪ לכל נוסף):", min_value=2, max_value=20, value=2)
extra_mics = max(0, total_mics - 2)
mics_price = extra_mics * 150

extra_monitors = st.number_input("תוספת מוניטורים לבמה (1 כלול בבסיס, 150 ₪ לכל נוסף):", min_value=0, max_value=10, value=0)
monitors_price = extra_monitors * 150

has_dj = st.checkbox("תוספת שירותי DJ / מוסיקה למופע (1,000 ₪)")
dj_price = 1000 if has_dj else 0

has_projector = st.checkbox("מקרן + מסך (500 ₪)")
has_led = st.checkbox("2 מסכי LED 65 אינץ' על סטנדים (1,000 ₪)")
video_price = (500 if has_projector else 0) + (1000 if has_led else 0)

has_light_basic = st.checkbox("תאורת במה בסיסית - 8 פנסים (600 ₪)")
has_light_truss = st.checkbox("גשר תאורה (1,400 ₪)")
has_light_follow = st.checkbox("פולו ספוט + מפעיל ייעודי (650 ₪)")
lighting_price = (600 if has_light_basic else 0) + (1400 if has_light_truss else 0) + (650 if has_light_follow else 0)

has_band = st.checkbox("חיבור להקה / נגנים (1,200 ₪)")
band_price = 1200 if has_band else 0

has_early_local = st.checkbox("פיצול יום / הקמה מוקדמת - אירוע מקומי (400 ₪)")
has_early_out = st.checkbox("הקמה מוקדמת / שהייה ארוכה - אירוע חוץ/מרוחק (600 ₪)")
early_price = (400 if has_early_local else 0) + (600 if has_early_out else 0)

# חישוב סכומים
subtotal = (base_price + travel_cost + extra_hours_price + staff_price + mics_price + 
            monitors_price + dj_price + video_price + lighting_price + band_price + early_price)
discount = subtotal * 0.10 if is_school else 0
final_before_vat = subtotal - discount
vat = final_before_vat * 0.18
final_with_vat = final_before_vat + vat

# סיכום הצעת מחיר
st.markdown("---")
st.subheader("📋 סיכום הצעת מחיר")
st.write(f"• **חבילת בסיס (מערכת הגברה עד 500 איש, מיקסר, מוניטור, 2 אלחוטיים, איש צוות, עד 3 שעות):** {base_price:,} ₪")
if travel_cost > 0: st.write(f"• **נסיעות:** {travel_cost:,} ₪")
if extra_hours > 0: st.write(f"• **חזרה/המתנה ({extra_hours} שעות):** {extra_hours_price:,} ₪")
if extra_staff > 0: st.write(f"• **אנשי צוות נוספים ({extra_staff}):** {staff_price:,} ₪")
if extra_mics > 0: st.write(f"• **מיקרופונים נוספים ({extra_mics}):** {mics_price:,} ₪")
if extra_monitors > 0: st.write(f"• **מוניטורים נוספים ({extra_monitors}):** {monitors_price:,} ₪")
if dj_price > 0: st.write(f"• **שירותי DJ:** {dj_price:,} ₪")
if video_price > 0: st.write(f"• **וידאו/מסכים:** {video_price:,} ₪")
if lighting_price > 0: st.write(f"• **תאורה:** {lighting_price:,} ₪")
if band_price > 0: st.write(f"• **חיבור להקה:** {band_price:,} ₪")
if early_price > 0: st.write(f"• **הקמה מוקדמת/פיצול:** {early_price:,} ₪")

st.markdown("---")
st.write(f"**סה\"כ מחירון:** {subtotal:,.0f} ₪")
if is_school:
    st.write(f"**הנחת מוסד (10%):** -{discount:,.0f} ₪")

st.success(f"### מחיר לפני מע\"מ: {final_before_vat:,.0f} ₪")
st.write(f"מע\"מ (18%): {vat:,.0f} ₪")
st.subheader(f"סה\"כ כולל מע\"מ: {final_with_vat:,.0f} ₪")
