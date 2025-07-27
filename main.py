import streamlit as st
import google.generativeai as genai
import requests
import json
from datetime import datetime
import base64
from PIL import Image
import io
from streamlit_paste_button import paste_image_button

# Fungsi untuk mengkonversi singkatan koin ke nama lengkap
def convert_crypto_symbol(symbol):
    """
    Mengkonversi singkatan koin (BTC, ETH) ke nama lengkap untuk CoinCap API
    """
    # Dictionary mapping singkatan koin ke nama lengkap
    symbol_map = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'BNB': 'binance-coin',
        'SOL': 'solana',
        'XRP': 'xrp',
        'ADA': 'cardano',
        'DOGE': 'dogecoin',
        'DOT': 'polkadot',
        'AVAX': 'avalanche',
        'SHIB': 'shiba-inu',
        'MATIC': 'polygon',
        'LTC': 'litecoin',
        'LINK': 'chainlink',
        'UNI': 'uniswap',
        'ATOM': 'cosmos',
        'XLM': 'stellar',
        'BCH': 'bitcoin-cash',
        'ALGO': 'algorand',
        'NEAR': 'near-protocol',
        'FIL': 'filecoin'
    }
    
    # Cek apakah input adalah singkatan koin
    if symbol.upper() in symbol_map:
        return symbol_map[symbol.upper()]
    
    # Jika bukan singkatan, kembalikan symbol asli
    return symbol

# Fungsi untuk mengambil data crypto dari CoinCap API v3
def get_crypto_data(symbol, api_key="45ce01ec5f1b5a4969727263cdfb3be193e9482d348cb68331b511557b9d5b49"):
    """
    Mengambil data cryptocurrency real-time dari CoinCap API v3
    """
    try:
        # Konversi singkatan koin jika diperlukan
        symbol = convert_crypto_symbol(symbol)
        
        # Konversi symbol ke format CoinCap (lowercase)
        symbol_lower = symbol.lower()
        
        # URL endpoint CoinCap API v3
        url = f"https://rest.coincap.io/v3/assets/{symbol_lower}"
        
        # Headers dengan API key
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        
        # Request data
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                crypto_data = data['data']
                return {
                    'symbol': crypto_data.get('symbol', '').upper(),
                    'name': crypto_data.get('name', ''),
                    'price': float(crypto_data.get('priceUsd', 0)),
                    'change_24h': float(crypto_data.get('changePercent24Hr', 0)),
                    'market_cap': float(crypto_data.get('marketCapUsd', 0)),
                    'volume_24h': float(crypto_data.get('volumeUsd24Hr', 0)),
                    'supply': float(crypto_data.get('supply', 0)),
                    'rank': int(crypto_data.get('rank', 0))
                }
        return None
    except Exception as e:
        st.error(f"Error mengambil data crypto: {e}")
        return None

def format_currency(value):
    """
    Format angka menjadi currency dengan pemisah ribuan
    """
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif value >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

# Konfigurasi halaman
st.set_page_config(
    page_title="TradingView Chart Analyzer",
    page_icon="📈",
    layout="wide"
)

# CSS untuk styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #1f77b4;
    margin-bottom: 30px;
}
.analysis-box {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}
.metric-card {
    background-color: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 5px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📈 AI Analisa Trading Crypto</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Tanya lewat AI untuk referensi analisis teknikal dari trading crypto</p>', unsafe_allow_html=True)

# Konfigurasi API Keys secara otomatis
api_key = "AIzaSyBLP5MCrHAzjoCSu5qmN-We-XDvxQUcZ4M"
coincap_api_key = "45ce01ec5f1b5a4969727263cdfb3be193e9482d348cb68331b511557b9d5b49"

# Konfigurasi Google AI
genai.configure(api_key=api_key)

# Initialize session state for analysis history
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'selected_analysis' not in st.session_state:
    st.session_state.selected_analysis = None

# Sidebar untuk konfigurasi
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    
    # Status API Keys
    st.success("✅ Google AI API Key: Terkonfigurasi")
    st.success("✅ CoinCap API Key: Terkonfigurasi")
    
    st.divider()
    
    # Riwayat Analisis
    st.subheader("📚 Riwayat Analisis")
    
    if st.session_state.analysis_history:
        st.write(f"💾 {len(st.session_state.analysis_history)} analisis tersimpan")
        
        # Display analysis history
        for i, analysis in enumerate(reversed(st.session_state.analysis_history)):
            actual_index = len(st.session_state.analysis_history) - 1 - i
            
            # Create a preview title
            timestamp = datetime.fromisoformat(analysis['timestamp'])
            preview_title = f"📊 {timestamp.strftime('%d/%m %H:%M')}"
            
            # Add symbol if available
            if 'symbol' in analysis:
                preview_title += f" - {analysis['symbol']}"
            
            # Create button for each analysis
            if st.button(preview_title, key=f"analysis_{actual_index}", use_container_width=True):
                st.session_state.selected_analysis = analysis
        
        # Clear history button
        if st.button("🗑️ Hapus Semua Riwayat", type="secondary", use_container_width=True):
            st.session_state.analysis_history = []
            st.session_state.selected_analysis = None
            st.rerun()
    else:
        st.info("📝 Belum ada analisis tersimpan")
        st.caption("Analisis akan muncul di sini setelah Anda menyimpannya")
    
    st.divider()
    
    # Input Symbol Cryptocurrency
    st.subheader("💰 Data Cryptocurrency")
    
    crypto_symbol = st.text_input(
        "Symbol Cryptocurrency:",
        value="",
        placeholder="Masukkan nama lengkap (contoh: bitcoin, ethereum, solana)",
        help="Masukkan nama lengkap koin (contoh: bitcoin, ethereum, solana)"
    )
    
    if crypto_symbol:
        with st.spinner("📊 Mengambil data real-time..."):
            crypto_data = get_crypto_data(crypto_symbol, coincap_api_key)
            
            if crypto_data:
                st.success(f"✅ Data {crypto_data['symbol']} berhasil dimuat")
                
                # Harga saat ini dengan kondisi bearish/bullish
                price_change = crypto_data['change_24h']
                if price_change > 0:
                    trend_emoji = "🟢"
                    trend_text = "BULLISH"
                    trend_color = "green"
                else:
                    trend_emoji = "🔴"
                    trend_text = "BEARISH"
                    trend_color = "red"
                
                # Display harga dan kondisi
                st.markdown(f"""<div style="text-align: center; padding: 10px; border-radius: 10px; background-color: #f0f2f6;">
                <h3>💰 Harga Saat Ini: ${crypto_data['price']:.4f}</h3>
                <h4 style="color: {trend_color};">{trend_emoji} {trend_text} {abs(price_change):.2f}%</h4>
                </div>""", unsafe_allow_html=True)
                
                st.divider()
                
                # Display crypto data
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        label="Market Cap",
                        value=format_currency(crypto_data['market_cap'])
                    )
                    
                    st.metric(
                        label="Rank",
                        value=f"#{crypto_data['rank']}"
                    )
                
                with col2:
                    st.metric(
                        label="24h Volume",
                        value=format_currency(crypto_data['volume_24h'])
                    )
                    
                    st.metric(
                        label="Supply",
                        value=format_currency(crypto_data['supply'])
                    )
                
                st.caption(f"📈 {crypto_data['name']}")
                
                # Store crypto data in session state for use in analysis
                st.session_state.crypto_data = crypto_data
            else:
                st.error("❌ Gagal mengambil data cryptocurrency")
                st.info("💡 Pastikan symbol benar (contoh: bitcoin, ethereum, cardano)")
    
    st.divider()
    
    # Pengaturan analisis
    st.subheader("📊 Pengaturan Analisis")
    
    analysis_depth = st.selectbox(
        "Kedalaman Analisis:",
        ["Basic", "Intermediate", "Advanced"],
        index=1
    )
    
    include_sentiment = st.checkbox("Analisis Sentimen", value=True)
    include_patterns = st.checkbox("Deteksi Pola Chart", value=True)
    include_indicators = st.checkbox("Analisis Indikator Teknikal", value=True)
    include_recommendations = st.checkbox("Rekomendasi Trading", value=True)

# Main content area
# Check if there's a selected analysis to display
if st.session_state.selected_analysis:
    st.header("📋 Preview Analisis Tersimpan")
    
    analysis = st.session_state.selected_analysis
    timestamp = datetime.fromisoformat(analysis['timestamp'])
    
    # Display analysis info
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"📅 **Tanggal:** {timestamp.strftime('%d %B %Y, %H:%M:%S')}")
    with col2:
        st.write(f"📊 **Level:** {analysis.get('settings', {}).get('depth', 'N/A')}")
    with col3:
        if st.button("❌ Tutup Preview"):
            st.session_state.selected_analysis = None
            st.rerun()
    
    st.divider()
    
    # Display the analysis content
    st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
    st.markdown("### 📊 Hasil Analisis")
    st.markdown(analysis['analysis'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display settings used
    with st.expander("⚙️ Pengaturan yang Digunakan"):
        settings = analysis.get('settings', {})
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"📊 Kedalaman: {settings.get('depth', 'N/A')}")
            st.write(f"💭 Sentimen: {'✅' if settings.get('sentiment') else '❌'}")
        with col2:
            st.write(f"📈 Pola Chart: {'✅' if settings.get('patterns') else '❌'}")
            st.write(f"📉 Indikator: {'✅' if settings.get('indicators') else '❌'}")
    
    st.divider()
else:
    # Tab utama untuk mode aplikasi
    mode_tab1, mode_tab2 = st.tabs(["💬 Chat Mode", "📊 Image Analysis Mode"])

    with mode_tab1:
        st.header("💬 Chat dengan AI")
        
        if api_key:
            # Input coin untuk chat
            col1, col2 = st.columns([2, 1])
            
            with col1:
                chat_crypto_symbol = st.text_input(
                    "🪙 Pilih Coin untuk Analisis Chat:",
                    value="",
                    placeholder="Masukkan nama lengkap koin (contoh: bitcoin,  ethereum, solana)",
                    help="Masukkan nama lengkap  koin yang ingin dianalisis dalam chat",
                    key="chat_crypto_input"
                )
            
            with col2:
                if st.button("📊 Load Data", type="primary", disabled=not chat_crypto_symbol):
                    if chat_crypto_symbol:
                        with st.spinner("📊 Mengambil data real-time..."):
                            chat_crypto_data = get_crypto_data(chat_crypto_symbol, coincap_api_key)
                            
                            if chat_crypto_data:
                                st.session_state.chat_crypto_data = chat_crypto_data
                                st.success(f"✅ Data {chat_crypto_data['symbol']} berhasil dimuat untuk chat")
                            else:
                                st.error("❌ Gagal mengambil data cryptocurrency")
        
        # Display current crypto data for chat if available
        if 'chat_crypto_data' in st.session_state:
            data = st.session_state.chat_crypto_data
            price_change = data['change_24h']
            trend_emoji = "🟢" if price_change > 0 else "🔴"
            trend_text = "BULLISH" if price_change > 0 else "BEARISH"
            trend_color = "green" if price_change > 0 else "red"
            
            st.markdown(f"""<div style="text-align: center; padding: 8px; border-radius: 8px; background-color: #f8f9fa; margin: 10px 0;">
            <strong>📊 Data Aktif: {data['symbol']} - ${data['price']:.4f} 
            <span style="color: {trend_color};">{trend_emoji} {trend_text} {abs(price_change):.2f}%</span></strong>
            </div>""", unsafe_allow_html=True)
        
        st.divider()
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Tanyakan tentang trading, analisis teknikal, atau crypto..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Sedang berpikir..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        # Create context-aware prompt with real-time data
                        crypto_info = ""
                        if 'chat_crypto_data' in st.session_state:
                            data = st.session_state.chat_crypto_data
                            crypto_info = f"""
                            
                            Data Real-time {data['symbol']}:
                            - Harga saat ini: ${data['price']:.4f}
                            - Perubahan 24h: {data['change_24h']:.2f}%
                            - Market Cap: {format_currency(data['market_cap'])}
                            - Volume 24h: {format_currency(data['volume_24h'])}
                            - Ranking: #{data['rank']}
                            """
                        else:
                            crypto_info = "\n\n⚠️ Belum ada data cryptocurrency yang dimuat. Silakan pilih coin terlebih dahulu di atas."
                        
                        full_prompt = f"""
                        Anda adalah seorang analis cryptocurrency profesional. Jawab pertanyaan berikut dengan format yang terstruktur:
                        
                        Pertanyaan: {prompt}
                        {crypto_info}
                        
                        Format output yang diinginkan (sesuaikan dengan jenis pertanyaan):
                        🧩 Analisa [TOPIK] — Per [TANGGAL]
                        
                        📉 Kondisi Saat Ini
                        [ANALISIS_KONDISI_TERKINI]
                        
                        🔍 Level Penting (jika analisis teknikal)
                        Support Terdekat: [LEVEL_SUPPORT]
                        Resistance Kuat: [LEVEL_RESISTANCE]
                        
                        📊 Strategi Trading Aman (jika relevan)
                        🚫 BELI (Long Position)?
                        [ANALISIS_LONG_POSITION]
                        
                        ✅ JUAL (Short Position)?
                        [ANALISIS_SHORT_POSITION]
                        
                        ⏸️ HOLD?
                        [ANALISIS_HOLD_STRATEGY]
                        
                        🧠 Strategi Rekomendasi
                        [DETAIL_STRATEGI_DAN_REKOMENDASI]
                        
                        ⚠️ Kesimpulan & Saran
                        [KESIMPULAN_SINGKAT_DAN_ACTIONABLE]
                        
                        Berikan analisis yang objektif, profesional, dan mudah dipahami dengan emoji yang sesuai.
                        """
                        
                        response = model.generate_content(full_prompt)
                        response_text = response.text
                        
                        st.markdown(response_text)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                        
                    except Exception as e:
                        error_msg = f"❌ Error: {e}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
        
        if not api_key:
            st.warning("⚠️ Masukkan API Key di sidebar untuk menggunakan chat")

    with mode_tab2:
        st.header("📊 Analisis Gambar Chart")
        
        col1, col2 = st.columns([1, 1])
    
        with col1:
            st.subheader("📤 Upload Chart")
            
            # Tab untuk berbagai metode input
            tab1, tab2 = st.tabs(["📁 Upload File", "📋 Paste dari Clipboard"])
            
            uploaded_file = None
            
            with tab1:
                uploaded_file = st.file_uploader(
                    "Pilih file gambar chart:",
                    type=['png', 'jpg', 'jpeg', 'webp'],
                    help="Drag & drop file atau klik untuk browse"
                )
            
            with tab2:
                st.info("💡 **Cara paste gambar dari clipboard:**")
                st.markdown("""
                1. Screenshot chart TradingView (Ctrl+Shift+S atau Print Screen)
                2. Klik tombol 'Paste Image from Clipboard' di bawah
                3. Gambar akan otomatis ter-paste dari clipboard
                """)
                
                # Tombol paste gambar dari clipboard
                pasted_image = paste_image_button(
                    label="📋 Paste Image from Clipboard",
                    key="paste_image",
                    errors="raise"
                )
                
                if pasted_image is not None:
                    try:
                        # PasteResult adalah PIL Image object langsung
                        if pasted_image.image_data is not None:
                            # Simpan sebagai session state untuk digunakan
                            st.session_state.pasted_image = pasted_image.image_data
                            uploaded_file = "pasted_image"  # Flag untuk menandai gambar dari paste
                            st.success("✅ Gambar berhasil di-paste dari clipboard!")
                        else:
                            st.error("❌ Tidak ada data gambar yang ditemukan")
                    except Exception as e:
                        st.error(f"❌ Error memproses gambar: {e}")
                        st.info("💡 Pastikan Anda copy gambar yang valid ke clipboard")
        
            # Preview gambar
            if uploaded_file is not None:
                try:
                    if uploaded_file == "pasted_image" and "pasted_image" in st.session_state:
                        # Gunakan gambar dari paste
                        image = st.session_state.pasted_image
                        st.image(image, caption="Chart yang akan dianalisis", use_container_width=True)
                        st.info(f"📏 Dimensi: {image.size[0]} x {image.size[1]} pixels")
                    else:
                        # Gunakan gambar dari upload
                        image = Image.open(uploaded_file)
                        st.image(image, caption="Chart yang akan dianalisis", use_container_width=True)
                        st.info(f"📏 Dimensi: {image.size[0]} x {image.size[1]} pixels")
                    
                except Exception as e:
                    st.error(f"❌ Error membuka gambar: {e}")

        with col2:
             st.subheader("🔍 Hasil Analisis")
             
             if uploaded_file is not None and api_key:
                 # Input chat untuk pertanyaan tambahan
                 st.markdown("#### 💬 Pertanyaan Tambahan (Opsional)")
                 additional_question = st.text_area(
                     "Apa yang ingin Anda tanyakan tentang chart ini?",
                     placeholder="Contoh: Apakah ini waktu yang tepat untuk buy? Bagaimana dengan level support/resistance? Apa strategi trading yang cocok?",
                     help="Tambahkan pertanyaan spesifik yang ingin Anda tanyakan tentang analisis chart ini",
                     key="image_analysis_question"
                 )
                 
                 st.divider()
                 
                 if st.button("🚀 Mulai Analisis", type="primary", use_container_width=True):
                     with st.spinner("🔄 Menganalisis chart..."):
                         try:
                             # Ambil gambar berdasarkan sumber
                             if uploaded_file == "pasted_image" and "pasted_image" in st.session_state:
                                 # Gunakan gambar dari paste
                                 image = st.session_state.pasted_image
                             else:
                                 # Reset file pointer jika perlu
                                 if hasattr(uploaded_file, 'seek'):
                                     uploaded_file.seek(0)
                                 # Baca gambar dari upload
                                 image = Image.open(uploaded_file)
                             
                             # Konversi ke RGB jika perlu
                             if image.mode != 'RGB':
                                 image = image.convert('RGB')
                             
                             # Buat prompt berdasarkan pengaturan dengan data real-time
                             prompt_parts = [
                                 "Anda adalah seorang analis cryptocurrency profesional. Analisis gambar chart ini dengan format yang terstruktur:",
                                 "\n\n📊 Template Analisis Chart Pattern:",
                                 "Lihat web trading pattern di web ini: https://medium.com/coinmonks/flag-patterns-9eafb3bdfa54.",
                                 "Analisa gambar nya apakah ada pattern-pattern yang muncul dalam gambar tersebut.",
                                 "Identifikasi chart patterns seperti: Flag, Pennant, Triangle, Head & Shoulders, Double Top/Bottom, Support/Resistance, Trend Lines, dan pattern lainnya."
                                 "Lalu berikan analisis apakah ini waktu yang tepat untuk beli atau jual atau hold? bagaimana dengan level support/ressistance sebelumnya apa strategi trading yang cocok."
                             ]
                       
                             # Tambahkan pertanyaan tambahan jika ada
                             if additional_question.strip():
                                 prompt_parts.append(f"\n\n💬 Pertanyaan Khusus dari User:\n{additional_question}\n\nPastikan untuk menjawab pertanyaan ini dalam analisis Anda.")
                             
                             # Tambahkan data real-time jika tersedia
                             if 'crypto_data' in st.session_state:
                                 data = st.session_state.crypto_data
                                 prompt_parts.append(f"""
                                 
                                 Data Real-time {data['symbol']}:
                                 - Harga saat ini: ${data['price']:.4f}
                                 - Perubahan 24h: {data['change_24h']:.2f}%
                                 - Market Cap: {format_currency(data['market_cap'])}
                                 - Volume 24h: {format_currency(data['volume_24h'])}
                                 - Ranking: #{data['rank']}
                                 """)
                             
                             prompt_parts.append("\nFokus pada:")
                             
                             if include_patterns:
                                 prompt_parts.append("- Pola chart dan formasi teknikal")
                             if include_indicators:
                                 prompt_parts.append("- Indikator teknikal yang terlihat")
                             if include_sentiment:
                                 prompt_parts.append("- Sentimen pasar berdasarkan price action")
                             if include_recommendations:
                                 prompt_parts.append("- Rekomendasi entry/exit dan risk management")
                             
                             # Sesuaikan format output berdasarkan analysis_depth
                             if analysis_depth == "Basic":
                                 format_template = [
                                     "\nFormat output yang diinginkan (Basic):",
                                     "✅ Analisa Chart [SYMBOL] ([TIMEFRAME]) – Per [TANGGAL]",
                                     "Pair: [SYMBOL] | Timeframe: [TIMEFRAME] | Exchange: [EXCHANGE]",
                                     "",
                                     "🧠 🔍 Ringkasan Analisa Teknikal:",
                                     "🟦 1. Trend & Price Action",
                                     "Harga saat ini: $[HARGA_SAAT_INI]",
                                     "[ANALISIS_TREND_DAN_PRICE_ACTION]",
                                     "",
                                     "🔺 2. Chart Pattern",
                                     "[ANALISIS_CHART_PATTERN]",
                                     "",
                                     "📉 Indikator Teknis",
                                     "📍 RSI (Relative Strength Index)",
                                     "RSI: [NILAI_RSI] ➜ [INTERPRETASI_RSI]",
                                     "",
                                     "📍 MACD",
                                     "MACD line ([NILAI_MACD]) [POSISI_TERHADAP_SIGNAL]",
                                     "Histogram [KONDISI_HISTOGRAM] → [INTERPRETASI_MOMENTUM]",
                                     "",
                                     "🔑 Zona Support dan Resistance",
                                     "Level | Keterangan",
                                     "[LEVEL_SUPPORT] | Support jangka pendek (valid)",
                                     "[LEVEL_RESISTANCE] | Resistance kuat / Supply Zone",
                                     "[LEVEL_MINOR] | Minor resistance (pivot lokal)",
                                     "",
                                     "🎯 Strategi Rekomendasi (Scalper & Swing)",
                                     "✅ Untuk Scalper:",
                                     "Buy Entry: [ENTRY_SCALP] (area support)",
                                     "Target Take Profit (TP): [TP_SCALP]",
                                     "Stop-Loss (SL): [SL_SCALP] di bawah swing low",
                                     "",
                                     "📈 Untuk Swing Trader:",
                                     "Entry hanya jika breakout valid di atas [BREAKOUT_LEVEL] dengan volume meningkat.",
                                     "Target swing: [TARGET_SWING] (zona distribusi lama)",
                                     "SL: di bawah [SL_SWING] (struktur bawah patah)",
                                     "",
                                     "⚖️ Apakah Harga Sudah Ketinggian?",
                                     "[ANALISIS_VALUASI_HARGA]",
                                     "",
                                     "📌 Rangkuman Rekomendasi:",
                                     "Saran | Penjelasan",
                                     "🔄 Hold | [KONDISI_HOLD]",
                                     "📉 Sell | [KONDISI_SELL]",
                                     "🛒 Buy | [KONDISI_BUY]",
                                     "",
                                     "📌 Indikator Lanjutan yang Perlu Dipantau:",
                                     "Volume Breakout (Volume Profile)",
                                     "Open Interest (OI) & Funding Rate (untuk melihat tekanan long vs short)",
                                     "Divergence RSI / MACD saat harga uji support"
                                 ]
                             elif analysis_depth == "Intermediate":
                                 format_template = [
                                     "\nFormat output yang diinginkan (Intermediate):",
                                     "🧩 Analisa Teknikal [SYMBOL] ([TIMEFRAME]) — Per [TANGGAL]",
                                     "",
                                     "📈 Chart Pattern Analysis",
                                     "Pattern Teridentifikasi: [NAMA_PATTERN]",
                                     "Deskripsi Pattern: [DETAIL_PATTERN]",
                                     "Validitas Pattern: [TINGKAT_VALIDITAS]",
                                     "",
                                     "📉 Kondisi Saat Ini",
                                     "Harga: [HARGA_SAAT_INI]",
                                     "Tren: [ANALISIS_TREND]",
                                     "[DESKRIPSI_KONDISI_PASAR]",
                                     "",
                                     "🔍 Level Penting",
                                     "Support Terdekat: [LEVEL_SUPPORT]",
                                     "Resistance Kuat: [LEVEL_RESISTANCE]",
                                     "Level Supply Kunci: [LEVEL_KUNCI]",
                                     "",
                                     "📊 Strategi Trading Aman",
                                     "🚫 BELI (Long Position)?",
                                     "[ANALISIS_LONG_POSITION]",
                                     "",
                                     "✅ JUAL (Short Position)?",
                                     "[ANALISIS_SHORT_POSITION]",
                                     "",
                                     "⏸️ HOLD?",
                                     "[ANALISIS_HOLD_STRATEGY]",
                                     "",
                                     "🧠 Strategi Rekomendasi: \"[NAMA_STRATEGI]\"",
                                     "[DETAIL_STRATEGI_DAN_INDIKATOR]",
                                     "",
                                     "⚠️ Kesimpulan & Saran",
                                     "[KESIMPULAN_SINGKAT_DAN_ACTIONABLE]"
                                 ]
                             else:  # Advanced
                                 format_template = [
                                     "\nFormat output yang diinginkan (Advanced):",
                                     "🧩 Analisa Teknikal [SYMBOL] ([TIMEFRAME]) — Per [TANGGAL]",
                                     "",
                                     "📈 Chart Pattern Analysis",
                                     "Pattern Teridentifikasi: [NAMA_PATTERN]",
                                     "Deskripsi Pattern: [DETAIL_PATTERN]",
                                     "Validitas Pattern: [TINGKAT_VALIDITAS]",
                                     "Target Price: [TARGET_HARGA]",
                                     "Stop Loss: [LEVEL_STOP_LOSS]",
                                     "",
                                     "📉 Kondisi Saat Ini",
                                     "Harga: [HARGA_SAAT_INI]",
                                     "Tren: [ANALISIS_TREND]",
                                     "[DESKRIPSI_KONDISI_PASAR]",
                                     "",
                                     "🔍 Level Penting",
                                     "Support Terdekat: [LEVEL_SUPPORT]",
                                     "Resistance Kuat: [LEVEL_RESISTANCE]",
                                     "Level Supply Kunci: [LEVEL_KUNCI]",
                                     "",
                                     "📊 Indikator Teknikal",
                                     "RSI: [NILAI_RSI] - [INTERPRETASI]",
                                     "MACD: [NILAI_MACD] - [INTERPRETASI]",
                                     "Volume: [ANALISIS_VOLUME]",
                                     "Moving Averages: [ANALISIS_MA]",
                                     "",
                                     "📊 Strategi Trading Aman",
                                     "🚫 BELI (Long Position)?",
                                     "[ANALISIS_LONG_POSITION]",
                                     "",
                                     "✅ JUAL (Short Position)?",
                                     "[ANALISIS_SHORT_POSITION]",
                                     "",
                                     "⏸️ HOLD?",
                                     "[ANALISIS_HOLD_STRATEGY]",
                                     "",
                                     "🧠 Strategi Rekomendasi: \"[NAMA_STRATEGI]\"",
                                     "[DETAIL_STRATEGI_DAN_INDIKATOR]",
                                     "",
                                     "⚠️ Risk Management",
                                     "Position Size: [UKURAN_POSISI]",
                                     "Risk/Reward Ratio: [RATIO_RR]",
                                     "Time Horizon: [WAKTU_TRADING]",
                                     "",
                                     "⚠️ Kesimpulan & Saran",
                                     "[KESIMPULAN_SINGKAT_DAN_ACTIONABLE]"
                                 ]
                             
                             prompt_parts.extend(format_template)
                             prompt_parts.append("")
                             prompt_parts.append("Berikan analisis yang objektif, profesional, dan mudah dipahami dengan emoji yang sesuai.")
                             
                             prompt = "\n".join(prompt_parts)
                             
                             # Analisis dengan Gemini
                             model = genai.GenerativeModel('gemini-1.5-flash')
                             response = model.generate_content([prompt, image])
                             
                             # Tampilkan hasil
                             st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
                             st.markdown("### 📊 Hasil Analisis Chart")
                             st.markdown(response.text)
                             st.markdown('</div>', unsafe_allow_html=True)
                             
                             # Timestamp
                             st.caption(f"⏰ Analisis dilakukan pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                             
                             # Tombol untuk save hasil
                             col1, col2 = st.columns(2)
                             
                             with col1:
                                 if st.button("💾 Simpan ke Riwayat", type="primary", use_container_width=True):
                                     # Get symbol from crypto data if available
                                     symbol = None
                                     if 'crypto_data' in st.session_state:
                                         symbol = st.session_state.crypto_data.get('symbol')
                                     
                                     analysis_data = {
                                         "timestamp": datetime.now().isoformat(),
                                         "analysis": response.text,
                                         "symbol": symbol,
                                         "settings": {
                                             "depth": analysis_depth,
                                             "sentiment": include_sentiment,
                                             "patterns": include_patterns,
                                             "indicators": include_indicators,
                                             "recommendations": include_recommendations
                                         }
                                     }
                                     
                                     # Add to session state history
                                     st.session_state.analysis_history.append(analysis_data)
                                     st.success("✅ Analisis berhasil disimpan ke riwayat!")
                                     st.balloons()
                                     # Refresh halaman untuk update sidebar
                                     st.rerun()
                             
                             with col2:
                                 # Download button
                                 analysis_data_download = {
                                     "timestamp": datetime.now().isoformat(),
                                     "analysis": response.text,
                                     "settings": {
                                         "depth": analysis_depth,
                                         "sentiment": include_sentiment,
                                         "patterns": include_patterns,
                                         "indicators": include_indicators,
                                         "recommendations": include_recommendations
                                     }
                                 }
                                 
                                 st.download_button(
                                     label="📥 Download JSON",
                                     data=json.dumps(analysis_data_download, indent=2, ensure_ascii=False),
                                     file_name=f"chart_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                     mime="application/json",
                                     use_container_width=True
                                 )
                             
                         except Exception as e:
                             st.error(f"❌ Error dalam analisis: {e}")
                             st.info("💡 Pastikan gambar valid dan API key benar")
        
        if not api_key:
            st.warning("⚠️ Masukkan API Key di sidebar untuk memulai analisis")
        else:
            st.info("📤 Upload gambar chart untuk memulai analisis")
            
            # Tips penggunaan
            st.markdown("""
            ### 💡 Tips untuk hasil analisis terbaik:
            
            - **Screenshot berkualitas tinggi** dari TradingView
            - **Pastikan timeframe terlihat** jelas di chart
            - **Sertakan indikator** yang ingin dianalisis
            - **Chart tidak terpotong** dan lengkap
            - **Resolusi minimal 800x600** pixels
            """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 50px;">
    <p>🤖 Powered by Google Gemini AI | 📈 TradingView Chart Analyzer</p>
    <p><small>⚠️ Disclaimer: Analisis ini hanya untuk tujuan edukasi. Selalu lakukan riset sendiri sebelum trading.</small></p>
</div>
""", unsafe_allow_html=True)
