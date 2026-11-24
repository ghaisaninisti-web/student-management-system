#modul validasi, transformasi, dan analisis data mahasiswa

from typing import Any

def validate_student_record(record: Any) -> tuple[bool, str]:
    """Memvalidasi satu record mahasiswa; mengembalikan (valid, pesan_error)."""
    if not isinstance(record, dict):
        return False, "Record bukan dictionary."

    required_fields = {"nim", "nama", "prodi", "ipk", "sks"}
    if not required_fields.issubset(record.keys()):
        return False, "Field wajib belum lengkap."

    nim = str(record["nim"]).strip()
    nama = str(record["nama"]).strip()
    prodi = str(record["prodi"]).strip()

    if not nim or not nama or not prodi:
        return False, "NIM, nama, atau prodi kosong."

    try:
        ipk = float(record["ipk"])
        sks = int(record["sks"])
    except (TypeError, ValueError):
        return False, "IPK atau SKS bukan angka yang valid."

    if not (0.0 <= ipk <= 4.0):
        return False, f"IPK di luar rentang [0.0, 4.0]: {ipk}"

    if sks < 0:
        return False, f"SKS tidak boleh negatif: {sks}"

    return True, ""


def filter_by_min_ipk(
    students: list[dict[str, Any]], min_ipk: float
) -> list[dict[str, Any]]:
    """Menyaring mahasiswa dengan IPK >= min_ipk menggunakan list comprehension."""
    return [s for s in students if float(s["ipk"]) >= min_ipk]


def group_by_prodi(students: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Mengelompokkan nama mahasiswa berdasarkan prodi."""
    grouped: dict[str, list[str]] = {}
    for student in students:
        prodi = str(student["prodi"]).strip()
        nama = str(student["nama"]).strip()
        grouped.setdefault(prodi, []).append(nama)
    return grouped


def search_students_by_keyword(
    students: list[dict[str, Any]], keyword: str
) -> list[dict[str, Any]]:
    """Mencari mahasiswa berdasarkan kecocokan sebagian pada NIM atau nama."""
    query = keyword.strip().lower()
    if not query:
        return []
    return [
        s
        for s in students
        if query in s["nim"].lower() or query in s["nama"].lower()
    ]


def summarize_students(raw_records: list[Any]) -> dict[str, Any]:
    """Membersihkan duplikasi NIM, memproses list/dict/set, dan membuat rekap."""
    seen_nim: set[str] = set()
    clean_students: list[dict[str, Any]] = []
    invalid_records: list[dict[str, Any]] = []
    prodi_stats: dict[str, dict[str, float]] = {}

    for item in raw_records:
        is_valid, reason = validate_student_record(item)
        if not is_valid:
            invalid_records.append({"data": item, "alasan": reason})
            continue

        nim = str(item["nim"]).strip()
        if nim in seen_nim:
            invalid_records.append({"data": item, "alasan": f"Duplikat NIM: {nim}"})
            continue

        seen_nim.add(nim)
        prodi = str(item["prodi"]).strip()
        ipk = round(float(item["ipk"]), 2)
        sks = int(item["sks"])

        student_clean = {
            "nim": nim,
            "nama": str(item["nama"]).strip(),
            "prodi": prodi,
            "ipk": ipk,
            "sks": sks,
        }
        clean_students.append(student_clean)

        if prodi not in prodi_stats:
            prodi_stats[prodi] = {"total_ipk": 0.0, "jumlah": 0.0}
        prodi_stats[prodi]["total_ipk"] += ipk
        prodi_stats[prodi]["jumlah"] += 1.0

    unique_prodi: set[str] = set(prodi_stats.keys())
    avg_ipk_per_prodi: dict[str, float] = {
        prodi: round(stat["total_ipk"] / stat["jumlah"], 2)
        for prodi, stat in prodi_stats.items()
    }

    return {
        "total_input": len(raw_records),
        "total_valid": len(clean_students),
        "total_diabaikan": len(invalid_records),
        "daftar_prodi_unik": sorted(unique_prodi),
        "rata_rata_ipk_prodi": avg_ipk_per_prodi,
        "kelompok_mahasiswa_prodi": group_by_prodi(clean_students),
        "data_valid": clean_students,
        "catatan_diabaikan": invalid_records,
    }