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
    "🔺 Geometri", "🧠 Eğitim Bilimleri", "⚛️ Fizik", "🧪 Kimya", "🧬 Biyoloji", 
    "🎓 Üniversite Dersleri", "💡 Genel Kültür"
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
# 🛑 KURUMSAL / PRESTİJLİ UI/UX TASARIMI (GÖRSEL HATALAR GİDERİLDİ)
# =============================================================================
st.set_page_config(page_title="AKADEMİ", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <meta name="robots" content="noindex, nofollow" />
    <style>
    .stApp, div[data-testid="stAppViewContainer"], .main { 
        background-color: #f1f5f9 !important; 
        background-image: linear-gradient(rgba(241, 245, 249, 0.92), rgba(241, 245, 249, 0.95)), url('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=1920&auto=format&fit=crop') !important; 
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important; 
        color: #0f172a !important; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important; 
    }
    [data-testid="stSidebar"] { 
        background-color: rgba(255, 255, 255, 0.8) !important; 
        backdrop-filter: blur(12px) !important; 
        border-right: 1px solid rgba(226, 232, 240, 0.8) !important; 
    }
    .premium-card { 
        background: rgba(255, 255, 255, 0.98) !important; 
        border-radius: 12px !important; padding: 25px !important; margin-bottom: 20px !important; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.04) !important; border-left: 5px solid #1E3A8A !important; 
        color: #1e293b !important; 
    }
    .premium-card h2 { color: #1E3A8A !important; font-size: 2.5rem !important; font-weight: 800 !important; }
    
    .stTextInput input, .stTextArea textarea, .stNumberInput input, div[data-baseweb="select"] > div { 
        background-color: #ffffff !important; color: #000000 !important; 
        border: 1px solid #cbd5e1 !important; border-radius: 8px !important; 
    }
    div[data-baseweb="select"] * { color: #000000 !important; font-weight: 600 !important; }

    div.stButton > button { 
        background: #1E3A8A !important; border: 1px solid #1e3a8a !important; 
        border-radius: 6px !important; padding: 0.6rem 1.5rem !important; 
    }
    div.stButton > button * { color: #ffffff !important; font-weight: 600 !important; text-transform: uppercase !important; }
    
    .timer-card { 
        background: #ffffff; padding: 15px; border-radius: 10px; text-align: center; 
        border: 1px solid #e2e8f0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); margin-bottom: 15px; 
    }
    .timer-card b { color: #b91c1c !important; font-size: 22px !important; font-weight: 800 !important; display: block; }
    .timer-card p { color: #475569 !important; font-size: 14px !important; font-weight: 600 !important; margin: 0; }
    
    .kurucu-imza { 
        position: fixed; bottom: 10px; right: 15px; color: #475569; opacity: 0.1; 
        font-size: 10px; font-weight: 700; z-index: 9999; pointer-events: none; 
    }
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

# --- KRONOMETRE ---
def egitim_kocu_kronometresi():
    html_kodu = """
    <div style="background: #1E3A8A; padding: 35px; border-radius: 12px; color: white; text-align: center; font-family: sans-serif;">
        <h3 style="margin-top: 0; font-size: 20px; text-transform: uppercase;">Akademik Odaklanma Modülü</h3>
        <div id="timerDisplay" style="font-size: 70px; font-weight: 700; margin: 10px 0;">25:00</div>
        <p id="statusText" style="font-size: 16px; margin-bottom: 25px; color: #cbd5e1;">Lütfen seansı başlatın.</p>
        <button onclick="startTimer(25, 'Çalışma')" style="background: #ffffff; border: none; padding: 12px 25px; border-radius: 6px; color: #1E3A8A; font-weight: 700; cursor: pointer; margin: 5px;">25 DK ODAKLAN</button>
        <button onclick="startTimer(5, 'Mola')" style="background: rgba(255,255,255,0.15); border: 1px solid white; padding: 12px 25px; border-radius: 6px; color: white; cursor: pointer; margin: 5px;">5 DK MOLA</button>
        <button onclick="resetTimer()" style="background: transparent; border: 1px solid white; padding: 12px 25px; border-radius: 6px; color: white; cursor: pointer; margin: 5px;">SIFIRLA</button>
        <script>
            let timerInterval;
            let timeLeft = 25 * 60;
            function updateDisplay() {
                let m = Math.floor(timeLeft / 60); let s = timeLeft % 60;
                document.getElementById('timerDisplay').innerText = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
            }
            function startTimer(minutes, mode) {
                clearInterval(timerInterval); timeLeft = minutes * 60;
                document.getElementById('statusText').innerText = mode + " seansı aktif.";
                updateDisplay();
                timerInterval = setInterval(() => {
                    timeLeft--; updateDisplay();
                    if (timeLeft <= 0) { clearInterval(timerInterval); alert(mode + " bitti!"); }
                }, 1000);
            }
            function resetTimer() { clearInterval(timerInterval); timeLeft = 25 * 60; updateDisplay(); }
        </script>
    </div>
    """
    components.html(html_kodu, height=330)

# --- SESSION DURUMU ---
if 'db' not in st.session_state: st.session_state.db = veritabanini_yukle()
if 'aktif_kullanici' not in st.session_state: st.session_state.aktif_kullanici = None
if 'sinav_durumu' not in st.session_state: st.session_state.sinav_durumu = "bekliyor"
if 'sinav_verisi' not in st.session_state: st.session_state.sinav_verisi = None
if 'login_time' not in st.session_state: st.session_state.login_time = time.time()

# --- AI CONNECT (HATASIZ MODÜL) ---
kullanilacak_model = "gemini-1.5-flash" 
if SISTEM_API_ANAHTARI:
    try:
        genai.configure(api_key=SISTEM_API_ANAHTARI)
        # Mevcut modelleri listele ve en uygun olanı bul (404 hatasını önler)
        available_models = [m.name.replace("models/", "") for m in genai.list_models()]
        if "gemini-1.5-flash" in available_models: kullanilacak_model = "gemini-1.5-flash"
        elif "gemini-1.5-flash-latest" in available_models: kullanilacak_model = "gemini-1.5-flash-latest"
        elif "gemini-pro" in available_models: kullanilacak_model = "gemini-pro"
    except: pass 

# --- GİRİŞ / KAYIT AKIŞI ---
if st.session_state.aktif_kullanici is None:
    st.title("AKADEMİ YÖNETİM SİSTEMİ")
    t1, t2 = st.tabs(["🔐 Sisteme Giriş", "📝 Davetiyeli Kayıt"])
    
    with t1:
        c, _ = st.columns([1, 2])
        with c:
            st.markdown("<div class='premium-card'>🛡️ <b>Kullanıcı Girişi</b>", unsafe_allow_html=True)
            m_in = st.text_input("Kurumsal E-Posta:", key="l_m")
            p_in = st.text_input("Güvenlik Şifresi:", type="password", key="l_p")
            if st.button("Sisteme Giriş Yap", key="l_btn"):
                if m_in in st.session_state.db.get("kullanicilar", {}):
                    if st.session_state.db["kullanicilar"][m_in]["sifre"] == p_in:
                        st.session_state.aktif_kullanici = m_in
                        st.session_state.login_time = time.time()
                        st.rerun()
                    else: st.error("Hatalı şifre!")
                else: st.error("Bu e-posta kayıtlı değil.")
            st.markdown("</div>", unsafe_allow_html=True)
            
    with t2:
        c, _ = st.columns([1, 2])
        with c:
            st.markdown("<div class='premium-card'>📝 <b>Yeni Kayıt</b>", unsafe_allow_html=True)
            n_in = st.text_input("Ad ve Soyad:", key="r_n")
            m_in = st.text_input("Onaylı E-Posta:", key="r_m")
            p_in = st.text_input("Şifre Belirleyin:", type="password", key="r_p")
            i_in = st.text_input("Gizli Davet Kodu:", type="password", key="r_i")
            if st.button("Kaydı Tamamla", key="r_btn"):
                if m_in not in ONAYLI_KULLANICILAR: st.error("E-posta onaylı değil!")
                elif i_in != GIZLI_DAVET_KODU: st.error("Kod hatalı!")
                else:
                    if "kullanicilar" not in st.session_state.db: st.session_state.db["kullanicilar"] = {}
                    st.session_state.db["kullanicilar"][m_in] = {
                        "isim": n_in, "sifre": p_in, "stats": {"soru": 0, "dogru": 0, "yanlis": 0, "konu": 0, "dakika": 0},
                        "ders_programi": {g: "" for g in ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]},
                        "calisma_plani": [], "kutuphane": [], "ozel_sinavlar": []
                    }
                    veritabanini_kaydet(st.session_state.db)
                    st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
            st.markdown("</div>", unsafe_allow_html=True)

else:
    user_data = st.session_state.db["kullanicilar"][st.session_state.aktif_kullanici]
    if "ozel_sinavlar" not in user_data: user_data["ozel_sinavlar"] = []
    
    # Süre Takibi
    now = time.time()
    elapsed = int((now - st.session_state.login_time) / 60)
    if elapsed > 0:
        if "stats" in user_data: user_data["stats"]["dakika"] += elapsed
        st.session_state.login_time = now
        veritabanini_kaydet(st.session_state.db)

    # --- SIDEBAR ---
    with st.sidebar:
        yetki = '<p style="color:#64748b; font-size:12px; font-weight:700;">YETKİLİ PROFİL</p>' if st.session_state.aktif_kullanici == "tahsincanocal@gmail.com" else ''
        st.markdown(f"<div style='text-align:center;'>{yetki}<h3>{user_data['isim']}</h3></div>", unsafe_allow_html=True)
        st.metric("Çalışılan Süre", f"{user_data['stats']['dakika']} Dk")
        st.divider()
        if st.button("Oturumu Kapat"):
            st.session_state.aktif_kullanici = None
            st.rerun()

    st.title(f"AKADEMİ'ye Hoş Geldiniz, {user_data['isim'].split()[0]}")
    egitim_kocu_kronometresi()
    
    # --- DİNAMİK SINAV TAKVİMİ (ÜNİVERSİTE DERSLERİ DAHİL) ---
    st.subheader("🗓️ Sınav Takvimi")
    active_exams = list(OSYM_SINAVLARI.items())
    for item in user_data.get("ozel_sinavlar", []):
        try:
            d_obj = datetime.strptime(item["tarih"], "%Y-%m-%d").date()
            active_exams.append((item["ad"], d_obj))
        except: pass
        
    tcols = st.columns(len(active_exams) if active_exams else 1)
    for i, (name, s_date) in enumerate(active_exams):
        days = (s_date - date.today()).days
        if days >= 0:
            with tcols[i % len(tcols)]:
                st.markdown(f'<div class="timer-card"><p>{name}</p><b>{days} GÜN</b></div>', unsafe_allow_html=True)

    tabs = st.tabs(["Rapor", "AI Asistan", "Sınav Merkezi", "Ders Programı", "Görevler", "Arşiv"])
    
    # --- TAB 1: RAPOR VE ÜNİVERSİTE SINAV YÖNETİMİ ---
    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='premium-card'><b>Toplam Soru</b><br><h2>{user_data['stats']['soru']}</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='premium-card'><b>Doğru / Yanlış</b><br><h2>{user_data['stats']['dogru']} <span style='color:#b91c1c;'>/ {user_data['stats']['yanlis']}</span></h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='premium-card'><b>Konu</b><br><h2>{user_data['stats']['konu']}</h2></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='premium-card'><b>Dakika</b><br><h2>{user_data['stats']['dakika']}</h2></div>", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("🎓 Üniversite Sınavlarımı Yönet")
        st.info("Kendi vize, final veya sunum tarihlerini ekle, en üstteki geri sayım panelinde görünsün.")
        sm1, sm2 = st.columns([1, 2])
        with sm1:
            with st.form("ozel_sinav_form"):
                u_ad = st.text_input("Sınav Adı:", placeholder="Örn: Psikoloji Vizesi")
                u_tar = st.date_input("Tarih:", min_value=date.today())
                if st.form_submit_button("Takvime İşle"):
                    if u_ad:
                        user_data["ozel_sinavlar"].append({"ad": u_ad, "tarih": str(u_tar)})
                        veritabanini_kaydet(st.session_state.db)
                        st.success("Eklendi!")
                        st.rerun()
        with sm2:
            st.write("**Ekli Üniversite Sınavların:**")
            for idx, ex in enumerate(user_data["ozel_sinavlar"]):
                cx1, cx2 = st.columns([4, 1])
                cx1.write(f"📌 {ex['ad']} ({ex['tarih']})")
                if cx2.button("Sil", key=f"del_ex_{idx}"):
                    user_data["ozel_sinavlar"].pop(idx); veritabanini_kaydet(st.session_state.db); st.rerun()

    # --- TAB 2: AI ASİSTAN ---
    with tabs[1]:
        st.subheader("Akıllı Ders Asistanı")
        ai_c1, ai_c2 = st.columns([1, 2])
        ders = ai_c1.selectbox("Ders Seçimi:", DERS_LISTESI, key="ai_lesson")
        gorev = ai_c1.radio("İşlem:", ["Özetle", "Anlat", "Soru Hazırla"])
        konu = ai_c2.text_area("İncelenecek Konu:", placeholder="Örn: Diferansiyel Denklemler veya Osmanlı Duraklama...")
        if ai_c2.button("Sorgula") and konu:
            with st.spinner("Analiz yapılıyor..."):
                try:
                    model = genai.GenerativeModel(kullanilacak_model)
                    res = model.generate_content(f"Ders: {ders}. Konu: {konu}. {gorev} yap.").text
                    st.markdown(res)
                    user_data["stats"]["konu"] += 1
                    user_data["kutuphane"].append({"tarih": str(date.today()), "baslik": konu[:30], "icerik": res})
                    veritabanini_kaydet(st.session_state.db)
                except Exception as e: st.error(f"Sistem Hatası: {e}")

    # --- TAB 3: SINAV MERKEZİ ---
    with tabs[2]:
        if st.session_state.sinav_durumu == "bekliyor":
            st.subheader("Yeni Sınav")
            ex_ders = st.selectbox("Ders:", DERS_LISTESI, key="ex_lesson")
            ex_sayi = st.slider("Soru Sayısı:", 5, 20, 10)
            if st.button("Sınavı Başlat"):
                with st.spinner("Sorular hazırlanıyor..."):
                    try:
                        model = genai.GenerativeModel(kullanilacak_model)
                        p = f"{ex_ders} için {ex_sayi} test sorusu. JSON: [{{'soru':'...','secenekler':['A)','B)','C)','D)','E)'],'cevap':'A)'}}]"
                        r = model.generate_content(p).text
                        m = re.search(r'\[.*\]', r, re.DOTALL)
                        if m:
                            st.session_state.sinav_verisi = {"sorular": json.loads(m.group(0)), "ders": ex_ders}
                            st.session_state.sinav_durumu = "cozuyor"; st.rerun()
                    except: st.error("AI şu an meşgul, tekrar dene.")
        elif st.session_state.sinav_durumu == "cozuyor":
            v = st.session_state.sinav_verisi
            with st.form("ex_form"):
                ans = {}
                for i, q in enumerate(v["sorular"]):
                    st.write(f"**Soru {i+1}:** {q['soru']}")
                    ans[i] = st.radio("Seç:", q["secenekler"], index=None, key=f"q_{i}", label_visibility="collapsed")
                if st.form_submit_button("BİTİR"):
                    st.session_state.sinav_verisi["cevaplar"] = ans
                    st.session_state.sinav_durumu = "bitti"; st.rerun()
        elif st.session_state.sinav_durumu == "bitti":
            v = st.session_state.sinav_verisi
            d, y = 0, 0
            for i, q in enumerate(v["sorular"]):
                if v["cevaplar"].get(i) == q["cevap"]: d += 1
                else: y += 1
            user_data["stats"]["soru"] += len(v["sorular"])
            user_data["stats"]["dogru"] += d; user_data["stats"]["yanlis"] += y
            st.success(f"Sonuç: {d} Doğru / {y} Yanlış"); veritabanini_kaydet(st.session_state.db)
            if st.button("Yeni Sınav"): st.session_state.sinav_durumu = "bekliyor"; st.rerun()

    # --- TAB 4 & 5 & 6 (PROGRAM, GÖREVLER, ARŞİV) ---
    with tabs[3]:
        pcols = st.columns(7)
        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        for i, gun in enumerate(gunler):
            user_data["ders_programi"][gun] = pcols[i].text_area(gun, user_data["ders_programi"].get(gun, ""), height=250)
        if st.button("Programı Kaydet"): veritabanini_kaydet(st.session_state.db); st.success("Kaydedildi.")

    with tabs[4]:
        nt = st.text_input("Yeni Görev:"); 
        if st.button("Ekle") and nt:
            user_data["calisma_plani"].append({"task": nt, "done": False}); veritabanini_kaydet(st.session_state.db); st.rerun()
        for i, task in enumerate(user_data["calisma_plani"]):
            c1, c2 = st.columns([10, 1])
            v = c1.checkbox(task["task"], task["done"], key=f"t_{i}")
            if v != task["done"]: user_data["calisma_plani"][i]["done"] = v; veritabanini_kaydet(st.session_state.db); st.rerun()
            if c2.button("🗑️", key=f"d_{i}"): user_data["calisma_plani"].pop(i); veritabanini_kaydet(st.session_state.db); st.rerun()

    with tabs[5]:
        for i, item in enumerate(reversed(user_data["kutuphane"])):
            with st.expander(f"📄 {item['tarih']} - {item['baslik']}"):
                st.markdown(item["icerik"])
                if st.button("Sil", key=f"arch_{i}"): user_data["kutuphane"].remove(item); veritabanini_kaydet(st.session_state.db); st.rerun()
