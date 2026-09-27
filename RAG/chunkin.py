import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

def bersihkan_teks(teks_mentah):
    """
    Membersihkan spasi ganda atau enter berlebih dari hasil ekstraksi.
    """
    baris = teks_mentah.split('\n')
    baris_bersih = [b.strip() for b in baris if b.strip() != ""]
    return "\n".join(baris_bersih)

def potong_dan_proses_data(jalur_teks_mentah, folder_output):
    """
    Memotong teks panjang menjadi chunks terstruktur dan menyimpannya dalam format JSON siap pakai.
    """
    print(f"[*] Membaca data mentah dari: {jalur_teks_mentah}")
    
    with open(jalur_teks_mentah, "r", encoding="utf-8") as f:
        konten = f.read()
    
    teks_matang = bersihkan_teks(konten)
    
    # Konfigurasi Pemotongan (Chunking) untuk data keuangan
    # chunk_size=1000 karakter, chunk_overlap=200 karakter agar konteks angka tidak terputus di ujung potongan
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    potongan_teks = splitter.split_text(teks_matang)
    print(f"[+] Teks berhasil dipotong menjadi {len(potongan_teks)} chunks.")
    
    list_json_data = []
    os.makedirs(folder_output, exist_ok=True)
    
    # Mengemas setiap potongan menjadi objek terstruktur siap konsumsi AI
    for indeks, chunk in enumerate(potongan_teks):
        data_chunk = {
            "chunk_id": indeks + 1,
            "source_document": os.path.basename(jalur_teks_mentah),
            "content": chunk
        }
        list_json_data.append(data_chunk)
        
        # Opsi 1: Simpan per file ke folder 03_processed untuk arsitektur RAG privat
        jalur_file_chunk = os.path.join(folder_output, f"chunk_{indeks + 1:03d}.json")
        with open(jalur_file_chunk, "w", encoding="utf-8") as f_out:
            json.dump(data_chunk, f_out, indent=4, ensure_ascii=False)
            
    # Opsi 2: Simpan satu file gabungan besar untuk kebutuhan latihan/review tim
    file_gabungan = os.path.join(folder_output, "all_processed_chunks.json")
    with open(file_gabungan, "w", encoding="utf-8") as f_all:
        json.dump(list_json_data, f_all, indent=4, ensure_ascii=False)
        
    print(f"[+] Seluruh proses backend data selesai! Buka folder: {folder_output}")

if __name__ == "__main__":
    input_mentah = "data/02_extracted/hasil_ekstraksi_bca.txt"
    output_bersih = "data/03_processed/"
    
    if os.path.exists(input_mentah):
        potong_dan_proses_data(input_mentah, output_bersih)
    else:
        print(f"[-] Gagal: Jalankan skrip 'extract_data.py' terlebih dahulu agar file mentah terbentuk.")
