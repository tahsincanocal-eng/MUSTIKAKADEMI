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
    "mehmetkurt4773998@gmail.com",
    "ipekbirisi321@gmail.com"
]

# Üniversite dersleri seçeneği listeye eklendi
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
# 🛑 KURUMSAL / PRESTİJLİ UI/UX TASARIMI (HATASIZ VE TEMİZ)
# =============================================================================
st.set_page_config(page_title="AKADEMİ", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<meta name="robots" content="noindex, nofollow" />
<style>
    .stApp, div[data-testid="stAppViewContainer"], .main { 
        background-color: #f1f5f9 !important; 
        background-image: linear-gradient(rgba(241, 245, 249, 0.92), rgba(241, 245, 249, 0.95)), url('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=1920&auto=format&fit=crop') !important; 
        background-size: cover !important; 
        background-position: center !important; 
        background-attachment: fixed !important; 
    }
    [data-testid="stSidebar"] { 
        background-color: rgba(255, 255, 255, 0.8) !important; 
        backdrop-filter: blur(12px) !important; 
        border-right: 1px solid rgba(226, 232, 240, 0.8) !important; 
        box-shadow: 2px 0 10px rgba(0,0,0,0.03) !important; 
    }
    .premium-card { 
        background: rgba(255, 255, 255, 0.98) !important; 
        border-radius: 12px !important; 
        padding: 25px !important; 
        margin-bottom: 20px !important; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.04) !important; 
        border-left: 5px solid #1E3A8A !important; 
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input, div[data-baseweb="select"] > div { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        border: 1px solid #cbd5e1 !important; 
    }
    div[data-baseweb="select"] * {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    div.stButton > button { 
        background: #1E3A8A !important; 
        border: 1px solid #1e3a8a !important; 
        color: white !important;
    }
    div.stButton > button:hover { 
        background: #1e40af !important; 
    }
    .timer-card { 
        background: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center; 
        border: 1px solid #e2e8f0; 
    }
    .kurucu-imza { 
        position: fixed; 
        bottom: 10px; 
        right: 15px; 
        color: #475569; 
        opacity: 0.1; 
        font-size: 10px; 
        z-index: 9999; 
        pointer-events: none; 
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

# --- KRONOMETRE MODÜLÜ ---
def egitim_kocu_kronometresi():
    html_kodu = """
    <div style="background: #1E3A8A; padding: 35px; border-radius: 12px; color: white; text-align: center; font-family: sans-serif;">
        <h3 style="margin-top: 0; font-size: 20px; text-transform: uppercase;">Akademik Odaklanma Modülü</h3>
        <div id="timerDisplay" style="font-size: 70px; font-weight: 700; margin: 10px 0;">25:00</div>
        <p id="statusText" style="font-size: 16px; margin-bottom: 25px; color: #cbd5e1; background: rgba(255,255,255,0.1); display: inline-block; padding: 8px 20px; border-radius: 6px;">Lütfen çalışma seansınızı başlatın.</p>
        <br>
        <button onclick="startTimer(25, 'Çalışma')" style="background: white; border: none; padding: 12px 25px; border-radius: 6px; color: #1E3A8A; font-weight: 700; cursor: pointer; margin: 5px;">25 DK ODAKLAN</button>
        <button onclick="startTimer(5, 'Mola')" style="background: rgba(255,255,255,0.15); border: 1px solid white; padding: 12px 25px; border-radius: 6px; color: white; cursor: pointer; margin: 5px;">5 DK MOLA</button>
        <button onclick="resetTimer()" style="background: transparent; border: 1px solid white; padding: 12px 25px; border-radius: 6px; color: white; cursor: pointer; margin: 5px;">SIFIRLA</button>
        <div id="modalOverlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:9999; justify-content:center; align-items:center;">
            <div style="background: white; color: #0f172a; padding: 50px 40px; border-radius: 12px; text-align: center;">
                <h2 id="modalTitle" style="color: #1E3A8A;">SEANS TAMAMLANDI</h2>
                <p id="modalDesc">Lütfen yönergelere göre hareket ediniz.</p>
                <button onclick="closeModal()" style="background: #1E3A8A; color: white; border: none; padding: 15px 40px; border-radius: 6px; cursor: pointer; font-weight: 700;">TAMAM</button>
            </div>
        </div>
        <script>
            let timerInterval;
            let timeLeft = 25 * 60;
            function updateDisplay() {
                let m = Math.floor(timeLeft / 60);
                let s = timeLeft % 60;
                document.getElementById('timerDisplay').innerText = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
            }
            function showModal(mode) {
                document.getElementById('modalTitle').innerText = mode === 'Çalışma' ? "ODAKLANMA BİTTİ" : "MOLA BİTTİ";
                document.getElementById('modalDesc').innerText = mode === 'Çalışma' ? "Harika bir seanstı. Şimdi 5 dakika mola verin." : "Dinlenme bitti. Tekrar masaya dönme zamanı!";
                document.getElementById('modalOverlay').style.display = 'flex';
            }
            function closeModal() { document.getElementById('modalOverlay').style.display = 'none'; }
            function startTimer(minutes, mode) {
                clearInterval(timerInterval);
                timeLeft = minutes * 60;
                document.getElementById('statusText').innerText = mode + " Modu Aktif";
                updateDisplay();
                timerInterval = setInterval(() => {
                    timeLeft--;
                    updateDisplay();
                    if (timeLeft <= 0) { clearInterval(timerInterval); showModal(mode); }
                }, 1000);
            }
            function resetTimer() { clearInterval(timerInterval); timeLeft = 25 * 60; updateDisplay(); document.getElementById('statusText').innerText = "Başlatılmaya hazır."; }
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

# --- AI ASİSTAN ---
kullanilacak_model = "gemini-1.5-flash" 
if SISTEM_API_ANAHTARI:
    try:
        genai.configure(api_key=SISTEM_API_ANAHTARI)
        aktif_modeller = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if aktif_modeller:
            if "gemini-1.5-flash" in aktif_modeller: kullanilacak_model = "gemini-1.5-flash"
            elif "gemini-pro" in aktif_modeller: kullanilacak_model = "gemini-pro"
    except: pass 

# --- GİRİŞ VE KAYIT AKIŞI ---
if st.session_state.aktif_kullanici is None:
    st.title("AKADEMİ")
    t1, t2 = st.tabs(["🔐 Sisteme Giriş", "📝 Davetiyeli Kayıt"])
    
    with t1:
        c, _ = st.columns([1, 2])
        with c:
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            m_in = st.text_input("Kurumsal E-Posta:", key="l_m")
            p_in = st.text_input("Güvenlik Şifresi:", type="password", key="l_p")
            if st.button("Giriş Yap", key="l_btn"):
                if m_in in st.session_state.db.get("kullanicilar", {}):
                    if st.session_state.db["kullanicilar"][m_in]["sifre"] == p_in:
                        st.session_state.aktif_kullanici = m_in
                        st.session_state.login_time = time.time()
                        st.rerun()
                    else: st.error("Hatalı şifre.")
                else: st.error("Kayıt bulunamadı.")
            st.markdown("</div>", unsafe_allow_html=True)
            
    with t2:
        c, _ = st.columns([1, 2])
        with c:
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            n_in = st.text_input("Ad Soyad:", key="r_n")
            m_in = st.text_input("Onaylı E-Posta:", key="r_m")
            p_in = st.text_input("Şifre Belirleyin:", type="password", key="r_p")
            i_in = st.text_input("Davet Kodu:", type="password", key="r_i")
            if st.button("Kaydı Tamamla", key="r_btn"):
                if m_in not in ONAYLI_KULLANICILAR: st.error("E-posta onaylı listede değil!")
                elif i_in != GIZLI_DAVET_KODU: st.error("Davet kodu hatalı!")
                elif m_in in st.session_state.db.get("kullanicilar", {}): st.error("Zaten kayıtlı.")
                else:
                    if "kullanicilar" not in st.session_state.db: st.session_state.db["kullanicilar"] = {}
                    st.session_state.db["kullanicilar"][m_in] = {
                        "isim": n_in, "sifre": p_in, "stats": {"soru": 0, "dogru": 0, "yanlis": 0, "konu": 0, "dakika": 0},
                        "ders_programi": {g: "" for g in ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]},
                        "calisma_plani": [], "kutuphane": [], "ozel_sinavlar": []
                    }
                    veritabanini_kaydet(st.session_state.db)
                    st.success("Kayıt başarılı!")
            st.markdown("</div>", unsafe_allow_html=True)

else:
    user_data = st.session_state.db["kullanicilar"][st.session_state.aktif_kullanici]
    
    # Yeni özellikler için veri yapısı kontrolü (Migration)
    if "ozel_sinavlar" not in user_data:
        user_data["ozel_sinavlar"] = []
    
    now = time.time()
    elapsed = int((now - st.session_state.login_time) / 60)
    if elapsed > 0:
        if "stats" in user_data: user_data["stats"]["dakika"] += elapsed
        st.session_state.login_time = now
        veritabanini_kaydet(st.session_state.db)

    with st.sidebar:
        yetki = '<p style="color:#1E3A8A; font-weight:700; margin-bottom:0;">YETKİLİ PROFİL</p>' if st.session_state.aktif_kullanici == "tahsincanocal@gmail.com" else ''
        st.markdown(f"<div style='text-align:center;'>{yetki}<h3>{user_data['isim']}</h3></div>", unsafe_allow_html=True)
        st.divider()
        if st.button("Oturumu Kapat"):
            st.session_state.aktif_kullanici = None
            st.rerun()

    st.title(f"Hoş Geldiniz, {user_data['isim'].split()[0]}")
    egitim_kocu_kronometresi()
    
    # --- SINAV GERİ SAYIM MERKEZİ ---
    st.subheader("🗓️ Sınav Takvimi")
    
    # Tüm sınavları birleştir (Sabit OSYM + Kullanıcının eklediği Üniversite sınavları)
    active_exams = list(OSYM_SINAVLARI.items())
    for item in user_data.get("ozel_sinavlar", []):
        try:
            ex_date = datetime.strptime(item["tarih"], "%Y-%m-%d").date()
            active_exams.append((item["ad"], ex_date))
        except: pass
        
    tcols = st.columns(len(active_exams) if len(active_exams) > 0 else 1)
    for i, (name, s_date) in enumerate(active_exams):
        days = (s_date - date.today()).days
        if days >= 0:
            with tcols[i % len(tcols)]:
                st.markdown(f"<div class='timer-card'><p>{name}</p><b>{days} GÜN</b></div>", unsafe_allow_html=True)

    tabs = st.tabs(["Rapor", "AI Asistan", "Sınav Merkezi", "Ders Programı", "Görevler", "Arşiv"])
    
    # TAB 1: GELİŞİM & SINAV YÖNETİMİ
    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='premium-card'><b>Soru</b><h2>{user_data['stats']['soru']}</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='premium-card'><b>Doğru/Yanlış</b><h2>{user_data['stats']['dogru']}/{user_data['stats']['yanlis']}</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='premium-card'><b>Konu</b><h2>{user_data['stats']['konu']}</h2></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='premium-card'><b>Dakika</b><h2>{user_data['stats']['dakika']}</h2></div>", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("🎓 Üniversite Sınavlarımı Yönet")
        st.info("Kendi vize, final veya diğer sınavlarını buraya ekleyebilirsin. En üstteki takvimde görünecektir.")
        
        sm1, sm2 = st.columns([1, 2])
        with sm1:
            with st.form("uni_sinav_form"):
                u_ad = st.text_input("Sınav Adı:", placeholder="Örn: Matematik Vizesi")
                u_tarih = st.date_input("Sınav Tarihi:", min_value=date.today())
                if st.form_submit_button("Sınavı Listeye Ekle"):
                    if u_ad:
                        user_data["ozel_sinavlar"].append({"ad": u_ad, "tarih": str(u_tarih)})
                        veritabanini_kaydet(st.session_state.db)
                        st.success(f"{u_ad} eklendi!")
                        st.rerun()
        
        with sm2:
            st.write("**Ekli Üniversite Sınavların:**")
            for idx, ex in enumerate(user_data.get("ozel_sinavlar", [])):
                cx1, cx2 = st.columns([4, 1])
                cx1.write(f"📌 {ex['ad']} - {ex['tarih']}")
                if cx2.button("Sil", key=f"del_ex_{idx}"):
                    user_data["ozel_sinavlar"].pop(idx)
                    veritabanini_kaydet(st.session_state.db)
                    st.rerun()

    # TAB 2: AI (Üniversite Dersleri buradaki listeye eklendi)
    with tabs[1]:
        st.subheader("Akıllı Ders Asistanı")
        ai_c1, ai_c2 = st.columns([1, 2])
        ders = ai_c1.selectbox("Ders Seçimi:", DERS_LISTESI, key="ai_lesson")
        gorev = ai_c1.radio("İşlem:", ["Özetle", "Anlat", "Soru Hazırla"])
        konu = ai_c2.text_area("İncelenecek Konu:", placeholder="Örn: Trablusgarp Savaşı nedenleri veya Diferansiyel Denklemler...")
        if ai_c2.button("Sorgula") and konu:
            with st.spinner("Analiz yapılıyor..."):
                model = genai.GenerativeModel(kullanilacak_model)
                res = model.generate_content(f"Ders: {ders}. Konu: {konu}. {gorev} yap.").text
                st.markdown(res)
                user_data["kutuphane"].append({"tarih": str(date.today()), "baslik": konu[:30], "icerik": res})
                veritabanini_kaydet(st.session_state.db)

    # TAB 3: SINAV
    with tabs[2]:
        if st.session_state.sinav_durumu == "bekliyor":
            st.subheader("Yeni Sınav")
            ex_ders = st.selectbox("Ders:", DERS_LISTESI, key="ex_lesson")
            ex_sayi = st.slider("Soru Sayısı:", 5, 20, 10)
            ex_konu = st.text_input("Konu:", key="ex_konu")
            if st.button("Sınavı Başlat"):
                with st.spinner("Sorular hazırlanıyor..."):
                    model = genai.GenerativeModel(kullanilacak_model)
                    p = f"{ex_ders} dersi {ex_konu} konusu için {ex_sayi} test sorusu. JSON: [{{'soru':'...','secenekler':['A)','B)','C)','D)','E)'],'cevap':'A)'}}]"
                    r = model.generate_content(p).text
                    m = re.search(r'\[.*\]', r, re.DOTALL)
                    if m:
                        st.session_state.sinav_verisi = {"sorular": json.loads(m.group(0)), "ders": ex_ders}
                        st.session_state.sinav_durumu = "cozuyor"
                        st.rerun()
        elif st.session_state.sinav_durumu == "cozuyor":
            v = st.session_state.sinav_verisi
            with st.form("ex_form"):
                ans = {}
                for i, q in enumerate(v["sorular"]):
                    st.write(f"**Soru {i+1}:** {q['soru']}")
                    ans[i] = st.radio("Seç:", q["secenekler"], index=None, key=f"q_{i}", label_visibility="collapsed")
                if st.form_submit_button("BİTİR"):
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
                rap += f"**Soru {i+1}:** {q['soru']}\n> Sen: {o} | Doğru: {q['cevap']}\n\n"
            user_data["stats"]["soru"] += len(v["sorular"])
            user_data["stats"]["dogru"] += d
            user_data["stats"]["yanlis"] += y
            st.success(f"Sonuç: {d} Doğru / {y} Yanlış")
            st.markdown(rap)
            if st.button("Sıfırla"):
                st.session_state.sinav_durumu = "bekliyor"
                st.rerun()

    # TAB 4: PROGRAM
    with tabs[3]:
        st.subheader("Akademik Takvim")
        pcols = st.columns(7)
        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        for i, gun in enumerate(gunler):
            user_data["ders_programi"][gun] = pcols[i].text_area(gun, user_data["ders_programi"].get(gun, ""), height=250)
        if st.button("Kaydet"):
            veritabanini_kaydet(st.session_state.db)
            st.success("Güncellendi.")

    # TAB 5: GÖREVLER
    with tabs[4]:
        st.subheader("Görevler")
        nt = st.text_input("Yeni Görev:")
        if st.button("Ekle") and nt:
            user_data["calisma_plani"].append({"task": nt, "done": False})
            veritabanini_kaydet(st.session_state.db)
            st.rerun()
        for i, task in enumerate(user_data["calisma_plani"]):
            c1, c2 = st.columns([10, 1])
            v = c1.checkbox(task["task"], task["done"], key=f"t_{i}")
            if v != task["done"]:
                user_data["calisma_plani"][i]["done"] = v
                veritabanini_kaydet(st.session_state.db)
                st.rerun()
            if c2.button("🗑️", key=f"d_{i}"):
                user_data["calisma_plani"].pop(i)
                veritabanini_kaydet(st.session_state.db)
                st.rerun()

    # TAB 6: ARŞİV
    with tabs[5]:
        st.subheader("Dokümanlar")
        for i, item in enumerate(reversed(user_data["kutuphane"])):
            with st.expander(f"📄 {item['tarih']} - {item['baslik']}"):
                st.markdown(item["icerik"])
                if st.button("Sil", key=f"arch_{i}"):
                    user_data["kutuphane"].remove(item)
                    veritabanini_kaydet(st.session_state.db)
                    st.rerun()
