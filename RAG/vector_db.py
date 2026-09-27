import os
import json
import chromadb

def simpan_ke_vector_database(jalur_file_vektor, folder_db_lokal):
    """
    Memasukkan data koordinat angka (embeddings) ke dalam database vektor terisolasi.
    """
    print(f"[*] Membuka data koordinat angka dari: {jalur_file_vektor}")
    
    # 1. Buka file koordinat hasil dari embadings.py tadi
    with open(jalur_file_vektor, "r", encoding="utf-8") as f:
        data_vektor = json.load(f)
        
    print(f"[*] Menginisialisasi Vector Database (ChromaDB) di: {folder_db_lokal}")
    
    # 2. Membuat koneksi ke database lokal privat milik perusahaan lu
    client = chromadb.PersistentClient(path=folder_db_lokal)
    
    # 3. Membuat "Brankas/Koleksi" khusus untuk data BCA (Isolated Client Database)
    # Ini implementasi taktik multi-tenant kita, tiap klien dapet koleksi terpisah!
    koleksi_bca = client.get_or_create_collection(name="koleksi_keuangan_bca")
    
    print(f"[*] Memasukkan {len(data_vektor)} data tervektor ke dalam brankas database...")
    
    # 4. Memasukkan data ke dalam kolom database
    for item in data_vektor:
        koleksi_bca.add(
            embeddings=[item["embedding"]],    # Koordinat angka dari AI
            documents=[item["content"]],        # Teks asli laporan keuangan
            metadatas=[{"source": item["source_document"]}], # Sumber file
            ids=[f"id_chunk_{item['chunk_id']}"] # ID unik baris data
        )
        
    print(f"[+] BRANKAS TERKUNCI! {len(data_vektor)} data resmi tersimpan aman di database korporat.")

if __name__ == "__main__":
    file_input_vektor = "data/03_processed/bca_vector_data.json"
    lokasi_database_perusahaan = "data/vector_database_storage"
    
    if os.path.exists(file_input_vektor):
        simpan_ke_vector_database(file_input_vektor, lokasi_database_perusahaan)
    else:
        print("[-] Gagal: File bca_vector_data.json belum dibuat. Jalankan embadings.py dulu, bro.")
