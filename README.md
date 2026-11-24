# Sistem Manajemen Data Mahasiswa (CLI)
Aplikasi pengolahan data mahasiswa berbasis *command line* menngunakan VSCode berbasis Python

## Fitur Utama
1. Validasi data mahasiswa (kelengkapan field, tipe data, rentan IPK 0'0 - 4'0, dan SKS tidak negatif) serta deteksi/penghapusan duplikasi NIM.
2. Pengelompokan data mahasiswa berdasarkan program studi dan perhitungan rata-rata IPK per prodi.
3. Penyaringan mahasiswa berdasarkan batas minimum IPK (--min-ipk) dan pencarian berdasarkan kata kunci NIM/nama (--cari).
4. Penyimpanan hasil pemrosesan dan rekapitulasi ke file JSON keluaran.

## Struktur Proyek
1. main.py : *Entry point* CLI, *parsing* argumen, dan alur eksekusi utama.
2. student_manager/__init__.py : Inisialisasi *package* dan ekspos fungsi utama.
3. student_manager/data_handler.py : Pembacaan dan penyimpanan file JSON beserta *exception handling*.
4. student_manager/student.py : Validasi, pemrosesan struktur data (list, dict, set), *comprehension*, filter, pencarian, dan rekapitulasi.
5. student_manager/report.py : Pemformatan ringkasan teks di terminal dan penulisan laporan JSON.
6. data/mahasiswa.json : Contoh file data input.
7. data/output.json : Contoh file hasil keluaran.

## Dependency & Package
1. Menggunakan **Python 3** dan **Python Standard Library** saja (argparse, json, pathlib, sys, typing) tanpa *third-party library* eksternal.

## Cara Menjalankan Aplikasi
Pastikan posisi terminal berada di folder  *StudentManagementSystem* :

1. Menjalankan dengan file input dan output default : python main.py

2. Menjalankan dengan filter IPK minimum : python main.py --min-ipk 3.5

3. Menjalankan dengan kata kunci (NIM dan nama) : python main.py --cari "Arya Pratama"

4. Menjalankan dengan path file input/output kustom : python main.py --input data/mahasiswa.json --output data/output.json