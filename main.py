#Entry point aplikasi CLI pengolahan data mahasiswa.

import argparse
from pathlib import Path
import sys

from student_manager import (
    filter_by_min_ipk,
    format_summary_text,
    load_json_data,
    search_students_by_keyword,
    summarize_students,
    write_report_json,
)


def parse_args() -> argparse.Namespace:
    """Mengurai argumen baris perintah."""
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="CLI Pengolahan Data Mahasiswa (UTS Pemrograman Dasar)"
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=base_dir / "data" / "mahasiswa.json",
        help="Path file JSON input",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=base_dir / "data" / "output.json",
        help="Path file JSON output",
    )
    parser.add_argument(
        "--min-ipk",
        type=float,
        default=None,
        help="Opsional: tampilkan mahasiswa dengan IPK >= nilai ini",
    )

    parser.add_argument(
        "--cari",
        type=str,
        default=None,
        help="Opsional: cari mahasiswa berdasarkan potongan NIM atau nama",
    )
    return parser.parse_args()


def main() -> int:
    """Menjalankan alur utama aplikasi CLI."""
    args = parse_args()

    if args.min_ipk is not None and not (0.0 <= args.min_ipk <= 4.0):
        print("Error: --min-ipk harus berada di antara 0.0 dan 4.0.", file=sys.stderr)
        return 1

    try:
        raw_data = load_json_data(args.input)
        summary = summarize_students(raw_data)
        write_report_json(args.output, summary)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Gagal memproses data: {exc}", file=sys.stderr)
        return 1

    print(format_summary_text(summary))

    if args.min_ipk is not None:
        filtered = filter_by_min_ipk(summary["data_valid"], args.min_ipk)
        print(f"\nMahasiswa dengan IPK >= {args.min_ipk:.2f} ({len(filtered)} orang):")
        for mhs in filtered:
            print(f"  - {mhs['nim']} | {mhs['nama']} | IPK: {mhs['ipk']:.2f}")

    if args.cari is not None:
        matches = search_students_by_keyword(summary["data_valid"], args.cari)
        print(f"\nHasil pencarian '{args.cari}' ({len(matches)} ditemukan):")
        for mhs in matches:
            print(f"  - {mhs['nim']} | {mhs['nama']} | {mhs['prodi']} | IPK: {mhs['ipk']:.2f}")

    print(f"\nHasil disimpan ke: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())