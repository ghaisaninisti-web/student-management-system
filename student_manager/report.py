#modul penyajian laporan CLI dan penyimpanan haasil output.

from pathlib import Path
from typing import Any

from .data_handler import save_json_data


def format_summary_text(summary: dict[str, Any]) -> str:
    """Membentuk ringkasan teks untuk ditampilkan di terminal"""
    lines = [
        "=== RINGKASAN DATA MAHASISWA ===",
        f"Total data input   : {summary['total_input']}",
        f"Data valid         : {summary['total_valid']}",
        f"Data diabaikan     : {summary['total_diabaikan']}",
        f"Prodi unik         : {', '.join(summary['daftar_prodi_unik']) or '-'}",
        "Rata-rata IPK/Prodi:",
    ]
    for prodi, avg_ipk in summary["rata_rata_ipk_prodi"].items():
        lines.append(f"  - {prodi}: {avg_ipk:.2f}")
    return "\n".join(lines)


def write_report_json(output_path: Path, summary: dict[str, Any]) -> Path:
    """Menyimpan objek ringkasan ke file output JSON."""
    return save_json_data(output_path, summary)