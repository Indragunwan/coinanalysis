# 🚀 Crypto Analysis & Trading Recommendation AI

Aplikasi Python untuk analisis teknikal dan rekomendasi trading cryptocurrency menggunakan AI. Aplikasi ini dapat menganalisis melalui chat interaktif atau upload screenshot dari TradingView.

## ✨ Fitur Utama

- 💬 **Chat Analysis**: Analisis interaktif melalui chat dengan AI
- 📸 **Image Analysis**: Upload screenshot TradingView untuk analisis visual
- 📊 **Real-time Data**: Data cryptocurrency terkini dari CoinCap API
- 🤖 **AI-Powered**: Menggunakan Gemini AI untuk analisis teknikal
- 📈 **Trading Recommendations**: Rekomendasi long/short dengan entry, TP, dan SL
- 🎯 **Professional Format**: Output analisis dalam format profesional

## 🛠️ Instalasi

### 1. Clone atau Download Project
```bash
cd "c:\Python313\Project APP\crypto analisys"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
streamlit run main.py
```

## 🔧 Konfigurasi API

Aplikasi sudah dikonfigurasi dengan API keys:
- **Gemini AI API**: Untuk analisis AI
- **CoinCap API**: Untuk data cryptocurrency real-time

## 📱 Cara Penggunaan

### Mode Chat Analysis
1. Masukkan symbol cryptocurrency (contoh: BTC, ETH, SYN)
2. Pilih "💬 Chat Analysis"
3. Tulis pertanyaan atau permintaan analisis
4. Klik "🔍 Analisis" untuk mendapatkan rekomendasi

### Mode Image Analysis
1. Masukkan symbol cryptocurrency
2. Pilih "📸 Image Analysis"
3. Upload screenshot chart dari TradingView
4. Tambahkan pertanyaan opsional
5. Klik "🔍 Analisis Gambar"

## 📊 Format Output

Aplikasi menghasilkan analisis dalam format:

```
🧩 Analisa Teknikal [SYMBOL] — Per [Tanggal]

📉 Kondisi Saat Ini
[Analisis kondisi harga dan tren]

🔍 Level Penting
[Support dan resistance levels]

📊 Strategi Trading Aman
🚫 BELI (Long Position)?
✅ JUAL (Short Position)?
⏸️ HOLD?

🧠 Strategi Rekomendasi
[Detail strategi trading]

⚠️ Kesimpulan & Saran
[Kesimpulan dan saran trading]
```

## 🎯 Contoh Penggunaan

### Chat Analysis
**Input**: "Bagaimana analisis teknikal BTC untuk trading hari ini?"

**Output**: Analisis lengkap dengan rekomendasi long/short, level entry, TP, SL

### Image Analysis
**Input**: Screenshot TradingView + "Fokus pada timeframe 1H untuk scalping"

**Output**: Analisis visual chart + rekomendasi berdasarkan pola yang terlihat

## ⚠️ Disclaimer

- Analisis ini hanya untuk tujuan edukasi
- Selalu lakukan riset sendiri sebelum melakukan trading
- Trading cryptocurrency memiliki risiko tinggi
- Tidak ada jaminan keuntungan dalam trading

## 🆘 Troubleshooting

### Error "Module not found"
```bash
pip install -r requirements.txt
```

### Error API
- Pastikan koneksi internet stabil
- Cek apakah symbol cryptocurrency valid

### Error Upload Gambar
- Pastikan format gambar PNG/JPG/JPEG
- Ukuran file tidak terlalu besar (< 10MB)

## 📞 Support

Jika mengalami masalah, pastikan:
1. Python 3.8+ terinstall
2. Semua dependencies terinstall
3. Koneksi internet stabil
4. Symbol cryptocurrency valid

---

**Happy Trading! 🚀📈**