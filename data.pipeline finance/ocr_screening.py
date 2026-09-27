import os
if __name__ == "__main__":
    # 1. TUNJUK FILE PDF LU YANG ADA DI FOLDER RAG
    # Ganti "nama_file_pdf_bca_lu.pdf" dengan nama asli file PDF lu di folder RAG!
    file_target = "RAG/juni 25 bca.pdf" 
    
    # 2. ALAMAT UNTUK MENYIMPAN HASIL EKSTRAKSI MENTAH (.TXT)
    output_txt = "data/02_extracted/hasil_ekstraksi_bca.txt"
    
    os.makedirs(os.path.dirname(output_txt), exist_ok=True)
    
    if os.path.exists(file_target):
        hasil_teks = (file_target)
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(hasil_teks)
        print(f"[+] Ekstraksi selesai! Data mentah disimpan di: {output_txt}")
    else:
        print(f"[-] Gagal: File '{file_target}' tidak ditemukan.")
        print("[-] Cek kembali apakah nama file dan folder RAG sudah sesuai di komputer lu.")
