#modul pembacaan dan penyimpanan file JSON dengan penanganan error

import json
from pathlib import Path
from typing import Any


def load_json_data(file_path: Path) -> list[dict[str, Any]]:
    """Membaca data list of dict dari file JSON secara aman."""
    if not file_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

    try:
        raw_text = file_path.read_text(encoding="utf-8")
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Format JSON tidak valid pada {file_path}: {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("Struktur JSON harus berupa list objek mahasiswa.")

    return data


def save_json_data(file_path: Path, payload: dict[str, Any]) -> Path:
    """Menyimpan hasil pemrosesan ke file JSON."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return file_path