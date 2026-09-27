import os
import json
from sentence_transformers import SentenceTransformer

def buat_vektor_embeddings(jalur_input_json, folder_output_vektor):
    """
    Mengubah teks chunks laporan keuangan menjadi koordinat angka (vektor).
    """
    print(f"[*] Membaca data chunks dari: {jalur_input_json}")
    
    # 1. Load model embedding gratis buatan Alibaba/HuggingFace yang sangat pintar bahasa Indonesia & Inggris
    # Model ini enteng banget, bisa jalan di CPU laptop biasa tanpa GPU
    print("[*] Meload model AI Embeddings (All-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. Buka file chunks hasil olahan skrip chunkin.py tadi
    with open(jalur_input_json, "r", encoding="utf-8") as f:
        list_chunks = json.load(f)
    
    print(f"[*] Memproses vektorisasi untuk {len(list_chunks)} potongan data...")
    
    list_vektor_data = []
    
    for item in list_chunks:
        teks_konten = item["content"]
        
        # Di sinilah proses pengubahan teks menjadi deretan angka koordinat terjadi!
        vektor_angka = model.encode(teks_konten).tolist()
        
        # Gabungkan data teks asli dengan koordinat angkanya
        data_tervektor = {
            "chunk_id": item["chunk_id"],
            "source_document": item["source_document"],
            "content": teks_konten,
            "embedding": vektor_angka # Ini isinya ratusan angka desimal koordinat
        }
        list_vektor_data.append(data_tervektor)
        
    # 3. Simpan hasil koordinat angka ini ke folder processed
    os.makedirs(folder_output_vektor, exist_ok=True)
    file_output = os.path.join(folder_output_vektor, "bca_vector_data.json")
    
    with open(file_output, "w", encoding="utf-8") as f_out:
        json.dump(list_vektor_data, f_out, indent=4, ensure_ascii=False)
        
    print(f"[+] WOW! Sukses total. Teks sudah berubah jadi koordinat angka di: {file_output}")

if __name__ == "__main__":
    # Mengambil file gabungan hasil chunkin.py sebelumnya
    input_chunks = "data/03_processed/all_processed_chunks.json"
    output_folder = "data/03_processed/"
    
    if os.path.exists(input_chunks):
        buat_vektor_embeddings(input_chunks, output_folder)
    else:
        print("[-] Gagal: File all_processed_chunks.json tidak ditemukan. Cek folder data/03_processed/ lu.")
