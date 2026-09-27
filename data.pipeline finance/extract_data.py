import os
import pdfplumber

def ekstrak_pdf_keuangan(jalur_pdf):
    """
    Mengekstrak teks dan tabel dari PDF laporan keuangan secara rapi.
    """
    print(f"[*] Memulai ekstraksi file: {jalur_pdf}")
    teks_lengkap = ""

    # Membuka file PDF menggunakan pdfplumber agar tabel terjaga
    with pdfplumber.open(jalur_pdf) as pdf:
        for indeks_halaman, halaman in enumerate(pdf.pages):
            # Ekstrak teks biasa dari halaman
            teks_halaman = halaman.extract_text()
            
            # Ekstrak tabel jika ada di halaman tersebut
            tabel_halaman = halaman.extract_tables()
            
            if teks_halaman:
                teks_lengkap += f"\n\n--- HALAMAN {indeks_halaman + 1} ---\n\n"
                teks_lengkap += teks_halaman
            
            # Jika ditemukan struktur tabel, konversi ke format teks terstruktur
            if tabel_halaman:
                teks_lengkap += "\n\n[Struktur Tabel Ditemukan]:\n"
                for tabel in tabel_halaman:
                    for baris in tabel:
                        # Membersihkan data baris dan menyatukannya dengan pemisah '|'
                        baris_bersih = [str(sel).replace('\n', ' ').strip() if sel is not None else "" for sel in baris]
                        teks_lengkap += " | ".join(baris_bersih) + "\n"
                        
    return teks_lengkap

if __name__ == "__main__":
    # Ubah nama file sesuai dengan file laporan keuangan BBCA yang ada di laptop lu
    file_target = "RAG/juni 25 bca.pdf" 
    output_txt = "data/02_extracted/hasil_ekstraksi_bca.txt"
    
    # Memastikan folder output tersedia
    os.makedirs(os.path.dirname(output_txt), exist_ok=True)
    
    if os.path.exists(file_target):
        hasil_teks = ekstrak_pdf_keuangan(file_target)
        
        # Simpan hasil ekstraksi mentah ke folder 02_extracted
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(hasil_teks)
        print(f"[+] Ekstraksi selesai! Data mentah disimpan di: {output_txt}")
    else:
        print(f"[-] Gagal: File {file_target} tidak ditemukan. Pastikan nama file di folder RAG sudah sesuai.")
