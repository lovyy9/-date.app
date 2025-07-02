import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import base64

# Konfigurasi halaman
st.set_page_config(
    page_title="+date.png", 
    layout="centered",
    page_icon="🖋️"
)

st.title("🖋️ Tambahkan Tanggal ke Gambarmu")
st.markdown("---")

# === STEP 1: Upload Gambar ===
st.subheader("📁 Step 1: Unggah Gambar")
uploaded_file = st.file_uploader(
    "Pilih file gambar stempel", 
    type=["png", "jpg", "jpeg"],
    help="Format yang didukung: PNG, JPG, JPEG"
)

if uploaded_file:
    st.success("✅ Gambar berhasil diunggah!")
    # Preview gambar asli
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(uploaded_file, caption="Gambar Asli", use_column_width=True)

st.markdown("---")

# === STEP 2: Pilih Tanggal ===
st.subheader("📅 Step 2: Pilih Tanggal")

tanggal_opsi = st.radio(
    "Pilih opsi tanggal:",
    ["Tanggal Hari Ini", "Tanggal Manual"],
    help="Pilih apakah ingin menggunakan tanggal hari ini atau memasukkan tanggal manual"
)

if tanggal_opsi == "Tanggal Hari Ini":
    tanggal_dipilih = datetime.now().strftime("%d %B %Y")
    st.info(f"📅 Tanggal yang akan digunakan: **{tanggal_dipilih}**")
else:
    tanggal_input = st.text_input(
        "Masukkan tanggal manual:", 
        placeholder="Contoh: 02 Juli 2025",
        help="Format bebas, contoh: 02 Juli 2025, 15 Desember 2024, dll."
    )
    tanggal_dipilih = tanggal_input.strip()
    if tanggal_dipilih:
        st.info(f"📅 Tanggal yang akan digunakan: **{tanggal_dipilih}**")

st.markdown("---")

# === STEP 3: Pengaturan Tambahan ===
st.subheader("⚙️ Step 3: Pengaturan Teks")

# Pengaturan otomatis
ukuran_font = 75  # Fixed font size
jarak_bawah = 70  # Fixed spacing

col1, col2 = st.columns(2)
with col1:
    warna_teks = st.selectbox(
        "Warna Teks:",
        ["Merah", "Hitam", "Biru", "Hijau"],
        index=0
    )
    
with col2:
    st.info("📏 **Pengaturan Otomatis:**\n- Ukuran Font: 75px\n- Jarak dari Bawah: 70px")

# Mapping warna
color_map = {
    "Merah": (255, 0, 0, 255),
    "Hitam": (0, 0, 0, 255),
    "Biru": (0, 0, 255, 255),
    "Hijau": (0, 128, 0, 255)
}

st.markdown("---")

# === STEP 4: Proses Gambar ===
st.subheader("🖨️ Step 4: Proses Gambar")

if st.button("🚀 Tambahkan Tanggal ke Stempel", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("❌ Silakan unggah gambar terlebih dahulu!")
    elif not tanggal_dipilih:
        st.error("❌ Silakan masukkan tanggal terlebih dahulu!")
    else:
        with st.spinner("⏳ Sedang memproses gambar..."):
            try:
                # Buka dan konversi gambar
                gambar = Image.open(uploaded_file).convert("RGBA")
                
                # Buat layer teks transparan
                txt_layer = Image.new("RGBA", gambar.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(txt_layer)
                
                # Coba gunakan font yang lebih baik dan BOLD
                try:
                    # Coba beberapa font BOLD yang umum tersedia
                    font_paths = [
                        "arialbd.ttf",  # Arial Bold
                        "Arial-Bold.ttf", 
                        "/System/Library/Fonts/Arial Bold.ttf",  # macOS
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
                        "C:/Windows/Fonts/arialbd.ttf",  # Windows Arial Bold
                        "C:/Windows/Fonts/calibrib.ttf",  # Windows Calibri Bold
                        "arial.ttf",  # Fallback ke Arial regular
                    ]
                    
                    font = None
                    for font_path in font_paths:
                        try:
                            font = ImageFont.truetype(font_path, ukuran_font)
                            break
                        except:
                            continue
                    
                    if font is None:
                        # Jika tidak ada font yang ditemukan, gunakan default dengan size lebih besar
                        font = ImageFont.load_default()
                        
                except Exception as e:
                    font = ImageFont.load_default()
                
                # Hitung posisi teks dengan spacing yang lebih baik
                bbox = draw.textbbox((0, 0), tanggal_dipilih, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                width, height = gambar.size
                x = (width - text_width) // 2  # Center horizontal
                y = height - text_height - jarak_bawah  # Bottom dengan margin yang bisa diatur

                # Pastikan teks tidak keluar dari gambar
                if y < 0:
                    y = 10  # Minimal 10px dari atas
                
                # Gambar teks dengan outline yang lebih tebal untuk visibility yang lebih baik
                # Gambar teks dengan outline putih untuk semua warna (termasuk hitam)
                outline_color = (255, 255, 255, 255)  # Selalu putih untuk semua warna

                # Gambar outline yang lebih tebal
                outline_thickness = 3
                for adj_x in range(-outline_thickness, outline_thickness + 1):
                    for adj_y in range(-outline_thickness, outline_thickness + 1):
                        if adj_x != 0 or adj_y != 0:  # Skip center position
                            draw.text((x + adj_x, y + adj_y), tanggal_dipilih, font=font, fill=outline_color)

                # Gambar teks utama
                draw.text((x, y), tanggal_dipilih, font=font, fill=color_map[warna_teks])
                
                # Gabungkan layer
                hasil_image = Image.alpha_composite(gambar, txt_layer)
                
                # Simpan hasil ke session state
                st.session_state.hasil_image = hasil_image
                st.session_state.tanggal_digunakan = tanggal_dipilih
                
                st.success("✅ Gambar berhasil diproses!")
                
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {str(e)}")

# === STEP 5: Tampilkan Hasil dan Download ===
if 'hasil_image' in st.session_state:
    st.markdown("---")
    st.subheader("🎉 Hasil Akhir")
    
    # Tampilkan gambar hasil
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(st.session_state.hasil_image, caption=f"Stempel dengan tanggal: {st.session_state.tanggal_digunakan}", use_column_width=True)
    
    # Persiapkan file untuk download
    img_buffer = io.BytesIO()
    st.session_state.hasil_image.save(img_buffer, format="PNG", quality=100)
    img_buffer.seek(0)
    
    # Tombol download
    st.markdown("### 📥 Download Hasil")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.download_button(
            label="📥 Download PNG",
            data=img_buffer.getvalue(),
            file_name=f"stempel_dengan_tanggal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png",
            type="primary",
            use_container_width=True
        )
    
    # Info tambahan
    st.info("💡 **Tips**: Klik tombol 'Download PNG' untuk menyimpan gambar ke komputer Anda.")
    
    # Opsi untuk memproses gambar lain
    if st.button("🔄 Proses Gambar Lain", use_container_width=True):
        # Clear session state
        if 'hasil_image' in st.session_state:
            del st.session_state.hasil_image
        if 'tanggal_digunakan' in st.session_state:
            del st.session_state.tanggal_digunakan
        st.rerun()

# === Footer ===
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        🖋️ Tambahkan tanggal pada gambarmu~
    </div>
    """, 
    unsafe_allow_html=True
)
