import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import date, datetime
import json
import os
import random
import re
import time

# =============================================================================
# 🛑 GİZLİ SİLAH: KURUMSAL TEMA ZORLAMASI
# =============================================================================
ST_DIR = ".streamlit"
os.makedirs(ST_DIR, exist_ok=True)
with open(os.path.join(ST_DIR, "config.toml"), "w", encoding="utf-8") as f:
    f.write('''
[theme]
base="light"
primaryColor="#1E3A8A"
backgroundColor="#F8FAFC"
secondaryBackgroundColor="#FFFFFF"
textColor="#0F172A"
font="sans serif"
''')

# =============================================================================
# 🔐 SESSİZ DAĞITIM VE GÜVENLİK AYARLARI
# =============================================================================
SISTEM_API_ANAHTARI = "AIzaSyCUTqmftXDcQ2JtBXQmF20b5uBm4Le2dak" 
GIZLI_DAVET_KODU = "MUSTİK0151" 

ONAYLI_KULLANICILAR = [
    "tahsincanocal@gmail.com",
    "bayrampinarzumra@gmail.com",
    "mehmet4773@gmail.com",
    "ipekbirisi321@gmail.com"
]

DERS_LISTESI = [
    "🇹🇷 Türkçe", "📐 Matematik", "🏛️ Tarih", "🌍 Coğrafya", "⚖️ Vatandaşlık",
    "🔺 Geometri", "🧠 Eğitim Bilimleri", "⚛️ Fizik", "🧪 Kimya", "🧬 Biyoloji", "💡 Genel Kültür"
]

OSYM_SINAVLARI = {
    "KPSS Lisans": date(2026, 9, 13), "KPSS Ön Lisans": date(2026, 10, 4),   
    "KPSS Ortaöğretim": date(2026, 11, 22), "YKS (TYT/AYT)": date(2026, 6, 20),
    "ALES": date(2026, 5, 10), "DGS": date(2026, 7, 5)
}

MOTIVASYON_SOZLERI = [
    "Disiplin, hedeflerinizle başarılarınız arasındaki köprüdür.",
    "Zorluklar, yeteneği geliştirir ve karakteri inşa eder.",
    "Bugünün odaklanması, yarının büyük başarılarıdır.",
    "Bilgiye yapılan yatırım, en yüksek karı getirir.",
    "Büyük işler, güce değil, azme dayanır."
]

KRITIK_BILGILER = [
    "📌 Anayasa Mahkemesi 15 üyeden oluşur.",
    "📌 Lale Devri Islahatları askeri içerikli değildir.",
    "📌 Türkiye'nin en yüksek dağı Ağrı Dağı'dır.",
    "📌 TBMM'nin ilk başkanı Mustafa Kemal Atatürk'tür.",
    "📌 Edirne kahramanı Enver Paşadır.",
    "📌 I.Balkan Harbinde olmayıp II. de olan Romanya'dır",
    "📌 Edirne Müdafii Mehmet Şükrü Paşa'dır (160 gün)",
    "📌 Osmanlıdan ayrılan son Balkan ülkesi Arnavutluktur.",
    "📌 İlk yazılı anayasa 1876 Kanun-i Esasi'dir.",
    "📌 Safiye Hüseyin Elbi İlk Türk hemşiredir."
]

# =============================================================================
# 🛑 KURUMSAL / PRESTİJLİ UI/UX TASARIMI
# =============================================================================
st.set_page_config(page_title="MUSTİK AKADEMİ", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp, div[data-testid="stAppViewContainer"], .main { background-color: #f1f5f9 !important; background-image: linear-gradient(rgba(241, 245, 249, 0.92), rgba(241, 245, 249, 0.95)), url('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=1920&auto=format&fit=crop') !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important; color: #0f172a !important; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important; }
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.8) !important; backdrop-filter: blur(12px) !important; border-right: 1px solid rgba(226, 232, 240, 0.8) !important; box-shadow: 2px 0 10px rgba(0,0,0,0.03) !important; }
    .premium-card { background: rgba(255, 255, 255, 0.98) !important; border-radius: 12px !important; padding: 25px !important; margin-bottom: 20px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.04) !important; border-left: 5px solid #1E3A8A !important; border-top: 1px solid #f1f5f9 !important; border-right: 1px solid #f1f5f9 !important; border-bottom: 1px solid #f1f5f9 !important; transition: all 0.3s ease !important; color: #1e293b !important; }
    .premium-card:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(0,0,0,0.08) !important; }
    .premium-card h2 { color: #1E3A8A !important; font-size: 2.5rem !important; margin: 0 !important; font-weight: 800 !important; }
    .premium-card b { color: #64748b !important; font-size: 0.9rem !important; text-transform: uppercase !important; letter-spacing: 1.2px !important; }
    
    /* GİRİŞ KUTULARI VE AÇILIR MENÜ (DROPDOWN) DÜZELTMELERİ */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, div[data-baseweb="select"] > div { background-color: #ffffff !important; color: #1e293b !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; padding: 10px 15px !important; font-weight: 500 !important; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02) !important; transition: border-color 0.2s !important; }
    .stTextInput input:focus, .stTextArea textarea:focus, div[data-baseweb="select"] > div:focus-within { border-color: #1E3A8A !important; box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.1) !important; }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div { color: #1e293b !important; } /* AÇILIR MENÜ YAZI RENGİ DÜZELTMESİ */

    h1, h2, h3, h4 { color: #0f172a !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
    h1 { font-size: 2.6rem !important; color: #0f172a !important; border-bottom: 2px solid #e2e8f0 !important; padding-bottom: 10px !important; margin-bottom: 25px !important; }
    
    /* BUTON TASARIMLARI VE YAZI RENGİ ZORLAMASI */
    div.stButton > button { background: #1E3A8A !important; border: 1px solid #1e3a8a !important; border-radius: 6px !important; padding: 0.6rem 1.5rem !important; box-shadow: 0 2px 4px rgba(30, 58, 138, 0.2) !important; transition: all 0.2s ease !important; width: 100% !important; }
    div.stButton > button * { color: #ffffff !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
    div.stButton > button:hover { background: #1e40af !important; box-shadow: 0 4px 8px rgba(30, 58, 138, 0.3) !important; transform: translateY(-1px) !important; }
    
    .timer-card { background: #ffffff; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); margin-bottom: 15px; }
    .timer-card b { color: #b91c1c !important; font-size: 22px !important; font-weight: 800 !important; display: block; margin-top: 5px;}
    .timer-card p { color: #475569 !important; margin: 0 !important; font-size: 14px !important; font-weight: 600 !important;}
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 2px solid #e2e8f0; gap: 20px; padding-bottom: 0px; }
    .stTabs [data-baseweb="tab"] { font-size: 15px !important; font-weight: 600 !important; color: #64748b !important; background: transparent; border: none !important; padding: 10px 5px !important; }
    .stTabs [aria-selected="true"] { color: #1E3A8A !important; border-bottom: 3px solid #1E3A8A !important; background: transparent !important; box-shadow: none !important;}
    p, li, .stMarkdown { color: #334155 !important; font-size: 1.05rem !important; }
    
    /* GÖZE SOKMAYAN KURUCU İMZASI - Opaklık 0.2'ye düşürüldü */
    .kurucu-imza { position: fixed; bottom: 10px; right: 15px; color: #475569; opacity: 0.2; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; z-index: 9999; pointer-events: none; }
    </style>
    <div class="kurucu-imza">KURUCU/DEVELOPER TAHSİN CAN ÖCAL</div>
    """, unsafe_allow_html=True)

# --- VERİTABANI YÖNETİMİ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERI_DOSYASI = os.path.join(BASE_DIR, "akademi_veritabani.json")

def veritabanini_yukle():
    if os.path.exists(VERI_DOSYASI):
        try:
            with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"kullanicilar": {}}
    return {"kullanicilar": {}}

def veritabanini_kaydet(veri):
    try:
        with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Veri kaydetme hatası: {e}")

# --- KURUMSAL EĞİTİM KOÇU KRONOMETRESİ (POMODORO) ---
def egitim_kocu_kronometresi():
    html_kodu = """
    <div style="background: #1E3A8A; background-image: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%); padding: 35px; border-radius: 12px; color: white; text-align: center; font-family: 'Helvetica Neue', Arial, sans-serif; box-shadow: 0 10px 25px rgba(15, 23, 42, 0.2); margin-bottom: 25px; position: relative; overflow: hidden; border: 1px solid #334155;">
        <h3 style="margin-top: 0; font-size: 20px; font-weight: 600; text-transform: uppercase; color: #e2e8f0; letter-spacing: 1px;">Kurumsal Odaklanma Modülü</h3>
        <div id="timerDisplay" style="font-size: 70px; font-weight: 700; margin: 10px 0; font-variant-numeric: tabular-nums; color: #ffffff; letter-spacing: -2px;">25:00</div>
        <p id="statusText" style="font-size: 16px; margin-bottom: 25px; font-weight: 400; color: #cbd5e1; background: rgba(255,255,255,0.1); display: inline-block; padding: 8px 20px; border-radius: 6px;">Lütfen çalışma seansınızı başlatın.</p>
        <br>
        <button onclick="startTimer(25, 'Çalışma')" style="background: #ffffff; border: none; padding: 12px 25px; border-radius: 6px; color: #1E3A8A; font-weight: 700; font-size: 14px; cursor: pointer; margin: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: all 0.2s; text-transform: uppercase;">▶ 25 DK Odaklan</button>
        <button onclick="startTimer(5, 'Mola')" style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); padding: 12px 25px; border-radius: 6px; color: #ffffff; font-weight: 600; font-size: 14px; cursor: pointer; margin: 5px; transition: all 0.2s; text-transform: uppercase;">⏸ 5 DK Mola</button>
        <button onclick="resetTimer()" style="background: transparent; border: 1px solid rgba(255,255,255,0.3); padding: 12px 25px; border-radius: 6px; color: #ffffff; font-weight: 600; font-size: 14px; cursor: pointer; margin: 5px; transition: all 0.2s; text-transform: uppercase;">🔄 Sıfırla</button>

        <!-- Kurumsal Uyarı Penceresi -->
        <div id="modalOverlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.85); z-index:9999; justify-content:center; align-items:center; backdrop-filter: blur(5px);">
            <div style="background: #ffffff; color: #0f172a; padding: 50px 40px; border-radius: 12px; text-align: center; max-width: 600px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border-top: 5px solid #1E3A8A;">
                <h2 id="modalTitle" style="color: #1E3A8A; font-size: 32px; margin-bottom: 15px; font-weight: 800; text-transform: uppercase;">Seans Tamamlandı</h2>
                <p id="modalDesc" style="font-size: 18px; color: #475569; line-height: 1.6; margin-bottom: 35px; font-weight: 400;">Belirlenen süreyi başarıyla tamamladınız. Lütfen yönergelere göre hareket ediniz.</p>
                <button onclick="closeModal()" style="background: #1E3A8A; color: white; border: none; padding: 15px 40px; border-radius: 6px; font-size: 16px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 6px rgba(30, 58, 138, 0.2); text-transform: uppercase;">Onayla ve Kapat</button>
            </div>
        </div>

        <script>
            let timerInterval;
            let timeLeft = 25 * 60;
            let currentMode = "Çalışma";

            function updateDisplay() {
                let m = Math.floor(timeLeft / 60);
                let s = timeLeft % 60;
                document.getElementById('timerDisplay').innerText = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
            }

            function showModal(mode) {
                if(mode === 'Çalışma') {
                    document.getElementById('modalTitle').innerText = "Odaklanma Seansı Bitti";
                    document.getElementById('modalDesc').innerText = "25 dakikalık verimli çalışma seansınızı tamamladınız. Lütfen 5 dakikalık ara vererek dinleniniz.";
                } else {
                    document.getElementById('modalTitle').innerText = "Mola Süresi Doldu";
                    document.getElementById('modalDesc').innerText = "Dinlenme süreniz tamamlanmıştır. Çalışma rutininize dönmeniz tavsiye edilir.";
                }
                document.getElementById('modalOverlay').style.display = 'flex';
            }

            function closeModal() {
                document.getElementById('modalOverlay').style.display = 'none';
            }

            function startTimer(minutes, mode) {
                clearInterval(timerInterval);
                currentMode = mode;
                timeLeft = minutes * 60;
                
                if(mode === 'Çalışma') {
                    document.getElementById('statusText').innerHTML = "<b>Sistem Kayıtta:</b> Odaklanma Seansı Aktif.";
                } else {
                    document.getElementById('statusText').innerHTML = "<b>Sistem Beklemede:</b> Dinlenme Modu Aktif.";
                }
                
                updateDisplay();
                
                timerInterval = setInterval(() => {
                    timeLeft--;
                    updateDisplay();
                    if (timeLeft <= 0) {
                        clearInterval(timerInterval);
                        document.getElementById('statusText').innerText = "SÜRE TAMAMLANDI";
                        showModal(currentMode);
                    }
                }, 1000);
            }

            function resetTimer() {
                clearInterval(timerInterval);
                timeLeft = 25 * 60;
                document.getElementById('statusText').innerText = "Lütfen çalışma seansınızı başlatın.";
                updateDisplay();
            }
        </script>
    </div>
    """
    components.html(html_kodu, height=330)

# --- SESSION DURUMU ---
if 'db' not in st.session_state:
    st.session_state.db = veritabanini_yukle()
if 'aktif_kullanici' not in st.session_state:
    st.session_state.aktif_kullanici = None
if 'sinav_durumu' not in st.session_state:
    st.session_state.sinav_durumu = "bekliyor"
if 'sinav_verisi' not in st.session_state:
    st.session_state.sinav_verisi = None
if 'login_time' not in st.session_state:
    st.session_state.login_time = time.time()

# --- AI CONNECT ---
kullanilacak_model = "gemini-1.5-flash" 
if SISTEM_API_ANAHTARI:
    try:
        genai.configure(api_key=SISTEM_API_ANAHTARI)
        aktif_modeller = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if aktif_modeller:
            if "gemini-1.5-flash" in aktif_modeller: kullanilacak_model = "gemini-1.5-flash"
            elif "gemini-1.5-flash-latest" in aktif_modeller: kullanilacak_model = "gemini-1.5-flash-latest"
            elif "gemini-pro" in aktif_modeller: kullanilacak_model = "gemini-pro"
            else: kullanilacak_model = aktif_modeller[0] 
    except Exception as e:
        pass 

# --- AUTHENTICATION FLOW (SADECE KURUCU GİRİŞİ) ---
if st.session_state.aktif_kullanici is None:
    st.title("MUSTİK AKADEMİ YÖNETİM SİSTEMİ")
    
    t1, t2 = st.tabs(["🔐 Sisteme Giriş", "📝 Davetiyeli Kayıt"])
    
    with t1:
        c, _ = st.columns([1, 2])
        with c:
            st.markdown("<div style='background:white; padding:25px; border-radius:10px; border:1px solid #e2e8f0; box-shadow:0 4px 10px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#1E3A8A; margin-top:0;'>🛡️ Kullanıcı Girişi</h3>", unsafe_allow_html=True)
            
            m_in = st.text_input("Kurumsal E-Posta:", key="l_m")
            p_in = st.text_input("Güvenlik Şifresi:", type="password", key="l_p")
            st.write("")
            
            if st.button("Sisteme Giriş Yap", key="l_btn"):
                if m_in in st.session_state.db.get("kullanicilar", {}):
                    if st.session_state.db["kullanicilar"][m_in]["sifre"] == p_in:
                        st.session_state.aktif_kullanici = m_in
                        st.session_state.login_time = time.time()
                        st.rerun()
                    else:
                        st.error("Girdiğiniz şifre hatalı!")
                else:
                    st.error("Bu e-posta sistemde kayıtlı değil. Önce kayıt olmalısınız.")
            st.markdown("</div>", unsafe_allow_html=True)
            
    with t2:
        c, _ = st.columns([1, 2])
        with c:
            st.markdown("<div style='background:white; padding:25px; border-radius:10px; border:1px solid #e2e8f0; box-shadow:0 4px 10px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#1E3A8A; margin-top:0;'>📝 Yeni Kayıt</h3>", unsafe_allow_html=True)
            st.info("Sadece onaylı e-postalar ve davet kodu ile kayıt olunabilir.")
            
            n_in = st.text_input("Ad ve Soyad:", key="r_n")
            m_in = st.text_input("Onaylı E-Posta:", key="r_m")
            p_in = st.text_input("Şifre Belirleyin:", type="password", key="r_p")
            i_in = st.text_input("Gizli Davet Kodu:", type="password", key="r_i")
            st.write("")
            
            if st.button("Kaydı Tamamla ve Giriş Yap", key="r_btn"):
                if m_in not in ONAYLI_KULLANICILAR:
                    st.error("Bu e-posta adresi sisteme giriş için onaylanmamış!")
                elif i_in != GIZLI_DAVET_KODU:
                    st.error("Gizli davet kodu hatalı!")
                elif m_in in st.session_state.db.get("kullanicilar", {}):
                    st.error("Bu hesap zaten kayıtlı. Lütfen giriş yapın.")
                else:
                    if "kullanicilar" not in st.session_state.db:
                        st.session_state.db["kullanicilar"] = {}
                        
                    st.session_state.db["kullanicilar"][m_in] = {
                        "isim": n_in, "sifre": p_in, "sayaclar": [], 
                        "kutuphane": [], "hedefler": "", "activity_log": [],
                        "stats": {"soru": 0, "dogru": 0, "yanlis": 0, "konu": 0, "dakika": 0},
                        "ders_programi": {g: "" for g in ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]},
                        "calisma_plani": [], "dersler": []
                    }
                    veritabanini_kaydet(st.session_state.db)
                    st.success("Kayıt başarılı! Sisteme alınıyorsunuz...")
                    time.sleep(1)
                    
                    st.session_state.aktif_kullanici = m_in
                    st.session_state.login_time = time.time()
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

else:
    user_data = st.session_state.db["kullanicilar"][st.session_state.aktif_kullanici]
    
    eksik_alanlar = {
        "stats": {"soru": 0, "dogru": 0, "yanlis": 0, "konu": 0, "dakika": 0},
        "activity_log": [], "ders_programi": {g: "" for g in ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]},
        "calisma_plani": [], "hedefler": "", "dersler": [], "kutuphane": [], "sayaclar": []
    }
    for key, val in eksik_alanlar.items():
        if key not in user_data: user_data[key] = val
            
    now = time.time()
    elapsed = int((now - st.session_state.login_time) / 60)
    if elapsed > 0:
        user_data["stats"]["dakika"] += elapsed
        st.session_state.login_time = now
        veritabanini_kaydet(st.session_state.db)

    # --- SIDEBAR (KURUMSAL BİLGİ PANELİ) ---
    with st.sidebar:
        
        # YETKİLİ PROFİL KONTROLÜ (Sadece tahsincanocal@gmail.com için yazacak)
        rol_etiketi = '<p style="color:#64748b; font-size:12px; font-weight:700; text-transform:uppercase; margin-bottom:5px;">YETKİLİ PROFİL</p>' if st.session_state.aktif_kullanici == "tahsincanocal@gmail.com" else ''
        
        st.markdown(f"""
        <div style="background:#ffffff; padding:20px; border-radius:10px; border:1px solid #e2e8f0; text-align:center; box-shadow: 0 2px 5px rgba(0,0,0,0.02); margin-bottom:20px;">
            {rol_etiketi}
            <h3 style="color:#1E3A8A; font-weight:800; margin:0;">{user_data['isim']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        t_q, d_q = user_data["stats"]["soru"], user_data["stats"]["dogru"]
        ratio = int((d_q / t_q * 100)) if t_q > 0 else 0
        st.markdown(f"**Genel Sınav Başarısı: %{ratio}**")
        st.progress(ratio / 100)
        st.metric("Sistemde Geçen Süre", f"{user_data['stats']['dakika']} Dk")
        st.divider()
        st.markdown("### 📌 Yönetim Notu")
        st.info(random.choice(MOTIVASYON_SOZLERI))
        st.divider()
        st.markdown("### 🔎 Akademik Bilgi")
        st.warning(random.choice(KRITIK_BILGILER))
        st.divider()
        
        if st.button("Oturumu Kapat"):
            st.session_state.aktif_kullanici = None
            st.rerun()

    st.title(f"MUSTİK AKADEMİ'ye Hoş Geldiniz, {user_data['isim'].split()[0]}")
    
    # En üstte Kurumsal Kronometre
    egitim_kocu_kronometresi()
    
    # --- SINAV SAYAÇLARI ---
    st.markdown("<h4 style='color:#334155;'>Sınav Takvimi</h4>", unsafe_allow_html=True)
    timer_cols = st.columns(len(OSYM_SINAVLARI))
    for i, (name, s_date) in enumerate(OSYM_SINAVLARI.items()):
        days_left = (s_date - date.today()).days
        with timer_cols[i]:
            st.markdown(f"""
                <div class="timer-card">
                    <p>{name}</p>
                    <b>{days_left} GÜN</b>
                </div>
            """, unsafe_allow_html=True)

    tabs = st.tabs(["Gelişim Raporu", "Yapay Zeka Destek", "Değerlendirme Sınavı", "Ders Programı", "Görev Planlayıcı", "Akademik Arşiv"])
    
    # TAB 1: DURUM
    with tabs[0]:
        st.markdown("### Akademik İstatistikler")
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='premium-card'><b>Toplam Soru</b><br><h2>{t_q}</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='premium-card'><b>Doğru / Yanlış</b><br><h2>{d_q} <span style='color:#b91c1c; font-size:1.5rem;'>/ {user_data['stats']['yanlis']}</span></h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='premium-card'><b>Tamamlanan Konu</b><br><h2>{user_data['stats']['konu']}</h2></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='premium-card'><b>Aktif Süre</b><br><h2>{user_data['stats']['dakika']} dk</h2></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Hedef ve Strateji Bildirimi")
        h_v = st.text_area("Yıllık akademik hedeflerinizi bu alana kaydedebilirsiniz:", value=user_data.get("hedefler", ""), height=150, key="m_h_area")
        if st.button("Hedefleri Güncelle", key="h_btn"):
            user_data["hedefler"] = h_v
            veritabanini_kaydet(st.session_state.db)
            st.success("Strateji bildiriminiz başarıyla sisteme kaydedildi.")

    # TAB 2: AI 
    with tabs[1]:
        st.subheader("Akıllı Ders Asistanı")
        st.markdown("Eksik olduğunuz konularda detaylı akademik destek alabilirsiniz.")
        ai_c1, ai_c2 = st.columns([1, 2])
        
        ai_d = ai_c1.selectbox("Ders Kategorisi:", DERS_LISTESI, key="ai_lesson")
        ai_i = ai_c1.radio("İşlem Türü:", ["Konu Özeti Oluştur", "Detaylı Anlatım Sağla", "Örnek Soru Hazırla"], key="ai_task")
        
        ai_k = ai_c2.text_area("İncelenecek Konu veya Soru:", key="ai_content", height=200, placeholder="Örn: Kurtuluş Savaşı Muharebeleri...")
        
        if ai_c2.button("Sorguyu Başlat", key="ai_run") and ai_k:
            with st.spinner("Akademik veritabanı taranıyor..."):
                try:
                    model = genai.GenerativeModel(kullanilacak_model)
                    res = model.generate_content(f"Ders: {ai_d}. Konu: {ai_k}. Lütfen bana bu konu hakkında profesyonel bir dille {ai_i}.").text
                    user_data["stats"]["konu"] += 1
                    user_data["activity_log"].append(f"[{datetime.now().strftime('%H:%M')}] AI Asistan ile {ai_d} analizi yapıldı.")
                    user_data["kutuphane"].append({"tarih": str(date.today()), "ders": ai_d, "baslik": ai_k[:30], "icerik": res})
                    veritabanini_kaydet(st.session_state.db)
                    st.markdown("<div style='background:white; padding:25px; border-radius:10px; border:1px solid #e2e8f0; box-shadow:0 2px 4px rgba(0,0,0,0.02);'>", unsafe_allow_html=True)
                    st.markdown(res)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Sistem sunucularıyla iletişim kurulamadı. Lütfen ağ bağlantınızı kontrol ediniz.\n\nDetay: {e}")

    # TAB 3: SINAV
    with tabs[2]:
        if st.session_state.sinav_durumu == "bekliyor":
            st.subheader("Değerlendirme Modülü")
            
            ex_d = st.selectbox("Test Edilecek Ders:", DERS_LISTESI, key="ex_lesson")
            
            c_s1, c_s2 = st.columns(2)
            ex_s = c_s1.slider("Soru Miktarı:", 5, 20, 10, key="ex_count")
            ex_k = c_s2.text_input("Spesifik Konu Filtresi:", key="ex_topic", placeholder="Tüm üniteler için boş bırakınız.")
            
            if st.button("Testi Başlat", key="ex_start"):
                with st.spinner("ÖSYM standartlarında sorular derleniyor..."):
                    try:
                        model = genai.GenerativeModel(kullanilacak_model)
                        konu_metni = f"özellikle {ex_k} konusunda" if ex_k else "genel karma konulardan"
                        p = f"{ex_d} dersi için {konu_metni} {ex_s} adet akademik seviye çoktan seçmeli test sorusu hazırla. JSON formatında ver: [{{'soru':'...','secenekler':['A)...','B)...','C)...','D)...','E)...'],'cevap':'A)...'}}]"
                        r = model.generate_content(p).text
                        m = re.search(r'\[.*\]', r, re.DOTALL)
                        if m:
                            st.session_state.sinav_verisi = {"tur": "Test", "sorular": json.loads(m.group(0)), "ders": ex_d, "konu": ex_k or "Genel Deneme"}
                            st.session_state.sinav_durumu = "cozuyor"
                            st.rerun()
                        else:
                            st.error("Veri formatında hata oluştu. Lütfen işlemi tekrarlayınız.")
                    except Exception as e:
                        st.error(f"Sistem Hatası.\n\nDetay: {e}")
                        
        elif st.session_state.sinav_durumu == "cozuyor":
            v = st.session_state.sinav_verisi
            st.markdown(f"### {v['ders']} - {v['konu']} Değerlendirmesi")
            with st.form("exam_form"):
                ans = {}
                for i, q in enumerate(v["sorular"]):
                    st.markdown(f"<div style='background:white; padding:20px; border-radius:8px; border:1px solid #e2e8f0; margin-bottom:15px; box-shadow:0 1px 3px rgba(0,0,0,0.02);'><b>Soru {i+1}:</b> {q['soru']}</div>", unsafe_allow_html=True)
                    ans[i] = st.radio("Cevabınız:", q["secenekler"], index=None, key=f"q_{i}", label_visibility="collapsed")
                if st.form_submit_button("Sınavı Tamamla"):
                    st.session_state.sinav_verisi["cevaplar"] = ans
                    st.session_state.sinav_durumu = "bitti"
                    st.rerun()
                    
        elif st.session_state.sinav_durumu == "bitti":
            v = st.session_state.sinav_verisi
            d, y, rap = 0, 0, ""
            for i, q in enumerate(v["sorular"]):
                o = v["cevaplar"].get(i)
                if o == q["cevap"]: d += 1
                else: y += 1
                icon = '✅' if o == q["cevap"] else '❌'
                rap += f"**Soru {i+1}:** {q['soru']}\n> **Sizin Cevabınız:** {o} | **Doğru Yanıt:** {q['cevap']} ({icon})\n\n---\n"
            
            user_data["stats"].update({"soru": user_data["stats"]["soru"]+len(v["sorular"]), "dogru": user_data["stats"]["dogru"]+d, "yanlis": user_data["stats"]["yanlis"]+y})
            user_data["activity_log"].append(f"[{datetime.now().strftime('%H:%M')}] {v['ders']} Sınavı Tamamlandı. Sonuç: {d} Doğru, {y} Yanlış.")
            
            st.success(f"Değerlendirme Sonucu: {d} Doğru / {y} Yanlış")
            st.markdown(f"<div style='background:white; padding:25px; border-radius:10px; border-left:4px solid {'#16a34a' if d>y else '#dc2626'}; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
            st.markdown(rap)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            c_btn1, c_btn2 = st.columns(2)
            if c_btn1.button("Sonuç Raporunu Arşivle", key="ex_save"):
                user_data["kutuphane"].append({"tarih": str(date.today()), "ders": v["ders"], "baslik": f"Sınav: {v['konu']}", "icerik": rap})
                veritabanini_kaydet(st.session_state.db)
                st.session_state.sinav_durumu = "bekliyor"
                st.rerun()
            if c_btn2.button("Yeni Değerlendirme Başlat", key="ex_reset"):
                st.session_state.sinav_durumu = "bekliyor"
                st.rerun()

    # TAB 4: DERS PROGRAMI
    with tabs[3]:
        st.subheader("Haftalık Akademik Takvim")
        st.markdown("Müfredat planlamanızı aşağıdan organize edebilirsiniz.")
        cols = st.columns(7)
        gnl = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        for i, gun in enumerate(gnl):
            user_data["ders_programi"][gun] = cols[i].text_area(f"{gun}", value=user_data["ders_programi"].get(gun, ""), height=300, key=f"prog_{gun}")
        if st.button("Takvimi Sisteme Kaydet", key="prog_save"):
            veritabanini_kaydet(st.session_state.db)
            st.success("Akademik takviminiz başarıyla güncellendi.")

    # TAB 5: PLAN
    with tabs[4]:
        st.subheader("Günlük Görev Yöneticisi")
        c_todo1, c_todo2 = st.columns([4, 1])
        n_t = c_todo1.text_input("Yeni görev tanımı giriniz:", key="new_task_input")
        if c_todo2.button("Listeye İlave Et", key="task_add") and n_t:
            user_data["calisma_plani"].append({"task": n_t, "done": False})
            veritabanini_kaydet(st.session_state.db)
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        for i, item in enumerate(user_data["calisma_plani"]):
            cc1, cc2 = st.columns([12, 1])
            v = cc1.checkbox(f"{item['task']}", value=item["done"], key=f"check_{i}")
            if v != item["done"]:
                user_data["calisma_plani"][i]["done"] = v
                veritabanini_kaydet(st.session_state.db)
                st.rerun()
            if cc2.button("Sil", key=f"task_del_{i}"):
                user_data["calisma_plani"].pop(i)
                veritabanini_kaydet(st.session_state.db)
                st.rerun()

    # TAB 6: AJANDA
    with tabs[5]:
        st.subheader("Sistem Kayıtları ve Doküman Arşivi")
        
        c_arsiv1, c_arsiv2 = st.columns(2)
        with c_arsiv1:
            st.markdown("#### Aktivite Dökümü")
            for log in reversed(user_data["activity_log"][-10:]):
                st.markdown(f"<div style='background:white; border-left:3px solid #1E3A8A; padding:12px; margin-bottom:8px; border-radius:6px; font-size:13px; color:#475569; box-shadow:0 1px 2px rgba(0,0,0,0.02);'>{log}</div>", unsafe_allow_html=True)
                
        with c_arsiv2:
            st.markdown("#### Kayıtlı Dokümanlar")
            for i, item in enumerate(reversed(user_data["kutuphane"])):
                with st.expander(f"📄 {item['tarih']} | {item.get('ders', 'Genel')} | {item.get('baslik', 'Bilinmiyor')}"):
                    st.markdown(item["icerik"])
                    if st.button("Belgeyi Sil", key=f"arch_del_{i}"):
                        user_data["kutuphane"].remove(item)
                        veritabanini_kaydet(st.session_state.db)
                        st.rerun()