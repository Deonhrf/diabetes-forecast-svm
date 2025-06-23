import streamlit as st
import pickle
import pathlib

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Pakar",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fungsi untuk membaca CSS
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# Load CSS eksternal
css_path = pathlib.Path('assets/styles.css')
load_css(css_path)

# Fungsi untuk membuat card hasil
def create_result_card(prediction, input_data):
    """Membuat card hasil prediksi"""
    if prediction == 1:
        return '''
        <div class="result-card">
            <h3 class="high-risk-title">⚠️ Risiko Diabetes Tinggi</h3>
            <p class="result-message" style="color: #dc2626;">
                Berdasarkan data yang dianalisis, Anda memiliki risiko tinggi mengalami diabetes.
            </p>
            <div class="warning-result">
                <p class="warning-title">🏥 Rekomendasi:</p>
                <ul class="warning-list">
                    <li>Konsultasi dengan dokter segera</li>
                    <li>Lakukan pemeriksaan darah lengkap</li>
                    <li>Terapkan pola hidup sehat</li>
                    <li>Kontrol asupan gula dan karbohidrat</li>
                    <li>Rutin monitor gula darah</li>
                </ul>
            </div>
        </div>
        '''
    else:
        return '''
        <div class="result-card">
            <h3 class="low-risk-title">✅ Risiko Diabetes Rendah</h3>
            <p class="result-message" style="color: #059669;">
                Berdasarkan data yang dianalisis, risiko Anda mengalami diabetes relatif rendah.
            </p>
            <div class="success-result">
                <p class="success-title">💚 Tetap Jaga Kesehatan:</p>
                <ul class="success-list">
                    <li>Pertahankan pola makan sehat</li>
                    <li>Rutin berolahraga minimal 30 menit/hari</li>
                    <li>Kontrol berat badan ideal</li>
                    <li>Pemeriksaan berkala ke dokter</li>
                    <li>Hindari makanan tinggi gula</li>
                </ul>
            </div>
        </div>
        '''


def create_default_state():
    """Membuat tampilan default state"""
    return '''
    <div class="result-card">
        <h3 class="default-state">🩺 Menunggu Input Data</h3>
        <p class="default-description">
            Silakan lengkapi semua data kesehatan Anda di kolom sebelah kiri, 
            kemudian klik tombol "Analisis Prediksi Diabetes" untuk melihat hasil.
        </p>
        <div style="margin-top: 2rem;">
            <p class="requirements-title">📋 Data yang Diperlukan:</p>
            <ul class="requirements-list">
                <li>Riwayat kehamilan dan usia</li>
                <li>Kadar glukosa darah</li>
                <li>Tekanan darah dan BMI</li>
                <li>Level insulin</li>
                <li>Ketebalan kulit</li>
                <li>Faktor genetik diabetes</li>
            </ul>
        </div>
        <div class="tips-box">
            <p class="tips-text">
                💡 <strong>Tips:</strong> Pastikan data yang dimasukkan akurat untuk hasil prediksi yang optimal.
            </p>
        </div>
    </div>
    '''

# Inisialisasi session state
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
if 'input_summary' not in st.session_state:
    st.session_state.input_summary = None

# # Membaca model

diabetes_model = pickle.load(open('diabetes_model.pkl', 'rb'))
# @st.cache_resource
# def load_model():
#     """Memuat model machine learning"""
#     try:
#         return pickle.load(open('diabetes_model.pkl', 'rb'))
#     except FileNotFoundError:
#         st.error("❌ Model file 'diabetes_model.pkl' tidak ditemukan!")
#         st.info("Pastikan file model berada di direktori yang sama dengan aplikasi.")
#         st.stop()

# diabets_model = load_model()

# Header aplikasi
st.markdown('<h1 class="main-title">🩺 Sistem Pakar Diagnosa Penyakit Diabetes</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Masukkan data kesehatan Anda untuk mendapatkan prediksi risiko diabetes yang akurat</p>', unsafe_allow_html=True)

# Layout dua kolom
input_col, result_col = st.columns([1, 1], gap="large")

# ===== KOLOM INPUT (KIRI) =====
with input_col:
    # st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📝 Input Data Kesehatan</h2>', unsafe_allow_html=True)
    
    # Form input dengan validasi
    with st.form("diabetes_prediction_form", clear_on_submit=False):
        st.markdown('<p class="section-subtitle">Silahkan Lengkapi Informasi Data Kesehatan Anda</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            Kehamilan = st.text_input(
                '🤱 Jumlah Kehamilan', 
                help='Jumlah total kehamilan yang pernah dialami'
            )
        
        with col2:
            Umur = st.text_input(
                '📅 Umur (tahun)', 
                help='Usia dalam tahun'
            )
        
        with col1:
            Glukosa = st.text_input(
                '🩸 Glukosa (mg/dL)', 
                help='Kadar glukosa dalam darah (normal: 70-100 mg/dL)'
            )
        with col2 :
            Tekanan_Darah = st.text_input(
                '💓 Tekanan Darah (mmHg)', 
                help='Tekanan darah diastolik (normal: 60-80 mmHg)'
            )
        
        with col1:
            Insulin = st.text_input(
                '💉 Insulin (mu U/ml)', 
                help='Level insulin dalam darah'
            )
        with col2:
            BMI = st.text_input(
                '⚖️ BMI (kg/m²)', 
                help='Body Mass Index (normal: 18.5-24.9)'
            )
        
        with col1:
            Ketebalan_Kulit = st.text_input(
                '✋ Ketebalan Kulit (mm)', 
                help='Ketebalan lipatan kulit triceps'
            )
        
        with col2:
            DiabetesPedigreeFunction = st.text_input(
                '🧬 Diabetes Pedigree Function', 
                help='Fungsi silsilah diabetes (0.078-2.42)'
            )
        
        # Tombol prediksi
        submitted = st.form_submit_button('🔍 Analisis Prediksi Diabetes')
        
        if submitted:
            # Validasi input
            input_fields = [Kehamilan, Glukosa, Tekanan_Darah, Ketebalan_Kulit, 
                          Insulin, BMI, DiabetesPedigreeFunction, Umur]
            
            if any(x == '' or x is None for x in input_fields):
                st.error("❌ Semua field harus diisi dengan nilai yang valid!")
            else:
                try:
                    # Konversi dan validasi data
                    input_data = [
                        float(Kehamilan),
                        float(Glukosa),
                        float(Tekanan_Darah),
                        float(Ketebalan_Kulit),
                        float(Insulin),
                        float(BMI),
                        float(DiabetesPedigreeFunction),
                        float(Umur)
                    ]
                    
                    # Validasi rentang nilai
                    if any(x < 0 for x in input_data):
                        st.error("❌ Semua nilai harus berupa angka positif!")
                    elif float(BMI) > 70 or float(Umur) > 120:
                        st.error("❌ Nilai BMI atau umur tidak dalam rentang normal!")
                    else:
                        # Prediksi
                        with st.spinner('🤖 Menganalisis data kesehatan...'):
                            prediction = diabetes_model.predict([input_data])
                            
                            # Simpan hasil ke session state
                            st.session_state.prediction_result = prediction[0]
                            st.session_state.input_summary = {
                                '🤱 Kehamilan': f'{Kehamilan} kali',
                                '🩸 Glukosa': f'{Glukosa} mg/dL',
                                '💓 Tekanan Darah': f'{Tekanan_Darah} mmHg',
                                '✋ Ketebalan Kulit': f'{Ketebalan_Kulit} mm',
                                '💉 Insulin': f'{Insulin} mu U/ml',
                                '⚖️ BMI': f'{BMI} kg/m²',
                                '🧬 Diabetes Pedigree': DiabetesPedigreeFunction,
                                '📅 Umur': f'{Umur} tahun'
                            }
                            st.session_state.show_result = True
                        
                        st.success("✅ Analisis selesai! Lihat hasil di kolom sebelah kanan.")
                        
                except ValueError as e:
                    st.error(f"❌ Format input tidak valid: {str(e)}")
                    st.info("💡 Pastikan semua input berupa angka yang valid.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== KOLOM HASIL (KANAN) =====
with result_col:
    # st.markdown('<div class="result-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📊 Hasil Analisis</h2>', unsafe_allow_html=True)
    
    if not st.session_state.show_result:
        # State default - menunggu input
        default_html = create_default_state()
        st.markdown(default_html, unsafe_allow_html=True)
    
    else:
        # Tampilkan hasil prediksi
        result_html = create_result_card(st.session_state.prediction_result, st.session_state.input_summary)
        st.markdown(result_html, unsafe_allow_html=True)
        
        # # Tampilkan ringkasan data
        # if st.session_state.input_summary:
        #     summary_html = create_data_summary(st.session_state.input_summary)
        #     st.markdown(summary_html, unsafe_allow_html=True)
        
        # Tombol reset
        if st.button('🔄 Analisis Data Baru', key='reset_btn'):
            st.session_state.show_result = False
            st.session_state.prediction_result = None
            st.session_state.input_summary = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)