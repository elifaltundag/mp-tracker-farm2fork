"""
Excel dosyasındaki örnek verilerini mevcut API uzerinden sisteme aktarir.

Kullanim:
    python scripts/import_excel.py path/to/data.xlsx --sheet-name Sayfa1 --dry-run
    python scripts/import_excel.py path/to/data.xlsx --api-url http://localhost:8000/api/v1
"""
from __future__ import annotations

import argparse
import json
import math
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import pandas as pd


FIELD_ALIASES = {
    "ornek_no": [
        "ornek_no",
        "örnek_no",
        "örnek numarası",
        "ornek numarasi",
        "örnek numarasi",
        "ornek numarası",
        "sample_no",
        "saha ornek no",
        "saha örnek no",
    ],
    "ornekleme_tarihi": [
        "ornekleme_tarihi",
        "örnekleme_tarihi",
        "örnekleme tarihi",
        "tarih",
        "sampling_date",
    ],
    "ornek_turu": [
        "ornek_turu",
        "örnek_türü",
        "örnek türü",
        "ornek türü",
        "sample_type",
    ],
    "konum.yerlesim_yeri": [
        "konum.yerlesim_yeri",
        "yerlesim_yeri",
        "yerleşim_yeri",
        "yerleşim yeri",
        "yerlesim yeri",
        "konum",
        "location",
        "ornegin alindigi yer",
        "örnegin alindigi yer",
        "örneğin alındığı yer",
    ],
    "konum.ozel_aciklama": [
        "konum.ozel_aciklama",
        "ozel_aciklama",
        "özel açıklama",
        "saha_notu",
        "saha notu",
        "aciklama",
        "açıklama",
        "detay",
    ],
    "konum.koordinatlar.enlem": [
        "konum.koordinatlar.enlem",
        "enlem",
        "latitude",
        "lat",
    ],
    "konum.koordinatlar.boylam": [
        "konum.koordinatlar.boylam",
        "boylam",
        "longitude",
        "lon",
        "lng",
    ],
    "konum.yukseklik_m": [
        "konum.yukseklik_m",
        "yukseklik_m",
        "yükseklik",
        "rakim",
        "elevation",
        "deniz seviyesinden yukseklik, m",
        "deniz seviyesinden yükseklik, m",
    ],
    "konum.egim_yuzde": [
        "konum.egim_yuzde",
        "egim_yuzde",
        "eğim",
        "eğim_%",
        "slope",
        "egim (%)",
        "eğim (%)",
    ],
    "konum.jeoloji": [
        "konum.jeoloji",
        "jeoloji",
        "geology",
        "jeoloji_mineroloji",
        "jeoloji/mineroloji",
    ],
    "tarim.sulama_turu": [
        "tarim.sulama_turu",
        "sulama_turu",
        "sulama türü",
        "irrigation_type",
    ],
    "tarim.sulama_kaynagi": [
        "tarim.sulama_kaynagi",
        "sulama_kaynagi",
        "sulama kaynağı",
        "irrigation_source",
    ],
    "tarim.sulama_sikligi_gun": [
        "tarim.sulama_sikligi_gun",
        "sulama_sikligi_gun",
        "sulama sıklığı",
        "irrigation_frequency",
    ],
    "tarim.urun_yetisme_turu": [
        "tarim.urun_yetisme_turu",
        "urun_yetisme_turu",
        "ürün yetişme türü",
        "ürün yetiştirme türü",
    ],
    "tarim.plastik_malc": [
        "tarim.plastik_malc",
        "plastik_malc",
        "plastik malç",
        "mulch",
    ],
    "tarim.plastik_kirlilik_gozlemi": [
        "tarim.plastik_kirlilik_gozlemi",
        "plastik_kirlilik_gozlemi",
        "plastik kirlilik gözlemi",
    ],
    "tarim.olasi_mp_kaynaklari": [
        "tarim.olasi_mp_kaynaklari",
        "olasi_mp_kaynaklari",
        "olası mp kaynakları",
        "mp kaynakları",
    ],
    "tarim.mp_kaynagina_mesafe_m": [
        "tarim.mp_kaynagina_mesafe_m",
        "mp_kaynagina_mesafe_m",
        "mp kaynağına mesafe",
    ],
    "ornek.planlama_ornek_no": [
        "ornek.planlama_ornek_no",
        "planlama_ornek_no",
        "planlama örnek no",
        "planlanan örnek no",
        "planlama ornek no",
    ],
    "ornek.planlanan_detay": [
        "ornek.planlanan_detay",
        "planlanan_detay",
        "planlanan detay",
        "ürün",
        "urun",
    ],
    "ornek.tur": [
        "ornek.tur",
        "alinan_ornek_turu",
        "örnek türü detayı",
        "toprak/su/gübre/bitki",
        "planlanan ornek turu",
        "planlanan örnek türü",
    ],
    "ornek.ozellik": [
        "ornek.ozellik",
        "alinan_ornek_ozelligi",
        "örnek özelliği",
        "derinlik",
        "ornek derinligi (cm) [1]",
        "örnek derinliği (cm) [1]",
        "ornek derinligi (cm) [2]",
        "örnek derinliği (cm) [2]",
    ],
    "fizikokimyasal.ph": ["fizikokimyasal.ph", "ph"],
    "fizikokimyasal.ec": ["fizikokimyasal.ec", "ec"],
    "fizikokimyasal.organik_madde": [
        "fizikokimyasal.organik_madde",
        "organik_madde",
        "organik madde",
    ],
    "fizikokimyasal.seluloz": ["fizikokimyasal.seluloz", "seluloz", "selüloz"],
    "fizikokimyasal.hemiseluloz": [
        "fizikokimyasal.hemiseluloz",
        "hemiseluloz",
    ],
    "fizikokimyasal.lignin": ["fizikokimyasal.lignin", "lignin"],
    "fizikokimyasal.ekstraktif": ["fizikokimyasal.ekstraktif", "ekstraktif"],
    "mp_analiz.yontem": ["mp_analiz.yontem", "analiz_yontemi", "analiz yöntemi"],
}


BOOL_TRUE_VALUES = {"evet", "true", "1", "var", "yes", "x"}
BOOL_FALSE_VALUES = {"hayir", "hayır", "false", "0", "yok", "no"}
LIST_SEPARATORS = [";", ",", "|"]
JEOLOJI_MAPPING = {
    "kuvarterner aluvyon (a)": "Alüvyon",
    "kuvarterner aluvyon yelpazesi (ay)": "Alüvyon yelpazesi",
    "paleozoik mermer (me)": "Mermer",
    "neojen konglomera kumtasi (ku)": "Konglomera",
    "mesozoik kirectasi bloklu flis": "Ofiyolit",
    "m. kirectasi": "Kireçtaşı",
    "m. andezit": "Andezit",
    "p. metamorfik": "Şist",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Excel dosyasini API uzerinden ice aktar.")
    parser.add_argument("excel_path", type=Path, help="Excel dosya yolu")
    parser.add_argument(
        "--sheet-name",
        dest="sheet_name",
        help="Okunacak sheet adi. Verilmezse ilk sheet kullanilir.",
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000/api/v1",
        help="API base URL. Ornek: http://localhost:8000/api/v1",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout suresi (saniye)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="API'ye gondermeden donusturulmus payload'lari gosterir.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Sadece ilk N satiri isler.",
    )
    return parser.parse_args()


def normalize_key(value: str) -> str:
    normalized = value.strip().lower()
    replacements = str.maketrans(
        {
            "ç": "c",
            "ğ": "g",
            "ı": "i",
            "ö": "o",
            "ş": "s",
            "ü": "u",
        }
    )
    normalized = normalized.translate(replacements)
    normalized = normalized.replace("-", "_").replace("/", "_")
    normalized = normalized.replace(",", " ")
    normalized = normalized.replace("(", " ").replace(")", " ")
    normalized = normalized.replace("[", " ").replace("]", " ")
    normalized = " ".join(normalized.split())
    return normalized


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if pd.isna(value):
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def clean_scalar(value: Any) -> Any:
    if is_empty(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.date().isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return value.strip()
    return value


def parse_bool(value: Any) -> Optional[bool]:
    value = clean_scalar(value)
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = normalize_key(str(value))
    if text in BOOL_TRUE_VALUES:
        return True
    if text in BOOL_FALSE_VALUES:
        return False
    raise ValueError(f"Boolean degeri anlasilmadi: {value}")


def parse_number(value: Any) -> Optional[float]:
    value = clean_scalar(value)
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).replace("%", "").strip()
    if "," in text and "." not in text:
        text = text.replace(",", ".")

    return float(text)


def parse_int(value: Any) -> Optional[int]:
    parsed = parse_number(value)
    if parsed is None:
        return None
    return int(parsed)


def parse_date_value(value: Any) -> Optional[str]:
    value = clean_scalar(value)
    if value is None:
        return None
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt).date().isoformat()
            except ValueError:
                continue
    return clean_scalar(value)


def parse_list(value: Any) -> Optional[list[str]]:
    value = clean_scalar(value)
    if value is None:
        return None
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    text = str(value)
    separator = next((sep for sep in LIST_SEPARATORS if sep in text), None)
    if separator is None:
        return [text.strip()]
    return [item.strip() for item in text.split(separator) if item.strip()]


def parse_text(value: Any) -> Optional[str]:
    value = clean_scalar(value)
    if value is None:
        return None
    return str(value)


def parse_jeoloji(value: Any) -> Optional[str]:
    text = parse_text(value)
    if text is None:
        return None

    normalized = normalize_key(text)
    if normalized in JEOLOJI_MAPPING:
        return JEOLOJI_MAPPING[normalized]

    return text


FIELD_PARSERS = {
    "ornekleme_tarihi": parse_date_value,
    "konum.koordinatlar.enlem": parse_number,
    "konum.koordinatlar.boylam": parse_number,
    "konum.yukseklik_m": parse_number,
    "konum.egim_yuzde": parse_number,
    "tarim.sulama_sikligi_gun": parse_int,
    "tarim.plastik_malc": parse_bool,
    "tarim.olasi_mp_kaynaklari": parse_list,
    "tarim.mp_kaynagina_mesafe_m": parse_number,
    "fizikokimyasal.ph": parse_number,
    "fizikokimyasal.ec": parse_number,
    "fizikokimyasal.organik_madde": parse_number,
    "fizikokimyasal.seluloz": parse_number,
    "fizikokimyasal.hemiseluloz": parse_number,
    "fizikokimyasal.lignin": parse_number,
    "fizikokimyasal.ekstraktif": parse_number,
    "ornek_no": parse_text,
    "ornek_turu": parse_text,
    "konum.yerlesim_yeri": parse_text,
    "konum.ozel_aciklama": parse_text,
    "konum.jeoloji": parse_jeoloji,
    "ornek.planlama_ornek_no": parse_text,
    "ornek.planlanan_detay": parse_text,
    "ornek.tur": parse_text,
    "ornek.ozellik": parse_text,
}


def build_alias_lookup() -> Dict[str, str]:
    lookup: Dict[str, str] = {}
    for target_field, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            lookup[normalize_key(alias)] = target_field
    return lookup


ALIAS_LOOKUP = build_alias_lookup()


def set_nested_value(payload: Dict[str, Any], dotted_key: str, value: Any) -> None:
    parts = dotted_key.split(".")
    current = payload
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    current[parts[-1]] = value


def get_by_alias(row: pd.Series, *aliases: str) -> Any:
    normalized_aliases = {normalize_key(alias) for alias in aliases}
    for original_column, raw_value in row.items():
        if normalize_key(str(original_column)) in normalized_aliases:
            return raw_value
    return None


def get_by_position(row: pd.Series, index: int) -> Any:
    if index < 0 or index >= len(row.index):
        return None
    column_name = row.index[index]
    return row[column_name]


def infer_ornek_turu(planlama_ornek_no: Any) -> Optional[str]:
    value = parse_text(planlama_ornek_no)
    if value is None:
        return None
    return "Referans Örnek" if value.strip().upper().endswith("-R") else "Standart Örnek"


def split_planlanan_ornek_turu(raw_value: Any) -> tuple[Optional[str], Optional[str]]:
    text = parse_text(raw_value)
    if text is None:
        return None, None

    text = text.strip()
    if "," in text:
        first_part, remainder = text.split(",", 1)
        return first_part.strip(), remainder.strip() or None

    parts = text.split(None, 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip() or None

    return text, None


def build_ornek_ozellik(depth_1: Any, depth_2: Any) -> Optional[str]:
    depth_1_text = parse_text(depth_1)
    depth_2_text = parse_text(depth_2)

    def format_depth_value(text: str) -> str:
        return text if text == "Su" else f"{text} cm"

    if not depth_1_text and not depth_2_text:
        return None

    if depth_1_text and depth_2_text:
        if depth_1_text == depth_2_text:
            return format_depth_value(depth_1_text)
        return f"{format_depth_value(depth_1_text)}, {format_depth_value(depth_2_text)}"

    if depth_1_text:
        return format_depth_value(depth_1_text)

    return format_depth_value(depth_2_text)


def apply_excel_specific_rules(row: pd.Series, payload: Dict[str, Any]) -> Dict[str, Any]:
    saha_ornek_no = get_by_alias(row, "Saha Örnek No")
    planlama_ornek_no = get_by_alias(row, "Planlama Örnek No")
    planlanan_ornek_turu = get_by_alias(row, "Planlanan Örnek Türü")
    depth_1 = get_by_alias(row, "Örnek Derinliği (cm) [1]", "Örnek Derinliği (cm)")
    depth_2 = get_by_alias(row, "Örnek Derinliği (cm) [2]")

    if is_empty(depth_1):
        depth_1 = get_by_position(row, 10)
    if is_empty(depth_2):
        depth_2 = get_by_position(row, 11)

    ornek_no = parse_text(saha_ornek_no)
    if ornek_no:
        payload["ornek_no"] = ornek_no

    planlama_no = parse_text(planlama_ornek_no)
    if planlama_no:
        set_nested_value(payload, "ornek.planlama_ornek_no", planlama_no)

    inferred_ornek_turu = infer_ornek_turu(planlama_ornek_no)
    if inferred_ornek_turu:
        payload["ornek_turu"] = inferred_ornek_turu

    parsed_tur, parsed_detay = split_planlanan_ornek_turu(planlanan_ornek_turu)
    if parsed_tur:
        set_nested_value(payload, "ornek.tur", parsed_tur)
    if parsed_detay:
        set_nested_value(payload, "ornek.planlanan_detay", parsed_detay)

    ornek_ozellik = build_ornek_ozellik(depth_1, depth_2)
    if ornek_ozellik:
        set_nested_value(payload, "ornek.ozellik", ornek_ozellik)

    return payload


def remove_empty_structures(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned = {
            key: remove_empty_structures(inner_value)
            for key, inner_value in value.items()
        }
        cleaned = {
            key: inner_value
            for key, inner_value in cleaned.items()
            if inner_value not in (None, {}, [])
        }
        return cleaned or None
    if isinstance(value, list):
        cleaned = [remove_empty_structures(item) for item in value]
        cleaned = [item for item in cleaned if item not in (None, {}, [])]
        return cleaned or None
    return value


def map_row_to_payload(row: pd.Series) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}

    for original_column, raw_value in row.items():
        if is_empty(raw_value):
            continue

        normalized_column = normalize_key(str(original_column))
        target_field = ALIAS_LOOKUP.get(normalized_column)

        if target_field is None and "." in normalized_column:
            target_field = normalized_column

        if target_field is None:
            continue

        parser = FIELD_PARSERS.get(target_field, clean_scalar)
        parsed_value = parser(raw_value)

        if parsed_value is None:
            continue

        set_nested_value(payload, target_field, parsed_value)

    payload = apply_excel_specific_rules(row, payload)
    payload = remove_empty_structures(payload) or {}
    validate_payload(payload)
    return payload


def validate_payload(payload: Dict[str, Any]) -> None:
    required_fields = ["ornek_no", "ornek_turu"]
    for field in required_fields:
        if not payload.get(field):
            raise ValueError(f"Zorunlu alan eksik: {field}")

    konum = payload.get("konum") or {}
    if not konum.get("yerlesim_yeri"):
        raise ValueError("Zorunlu alan eksik: konum.yerlesim_yeri")

    koordinatlar = konum.get("koordinatlar") or {}
    has_enlem = "enlem" in koordinatlar
    has_boylam = "boylam" in koordinatlar
    if has_enlem != has_boylam:
        raise ValueError("Koordinatlar icin enlem ve boylam birlikte verilmelidir")


def iter_payloads(dataframe: pd.DataFrame, limit: Optional[int]) -> Iterable[tuple[int, Dict[str, Any]]]:
    rows = dataframe.head(limit) if limit else dataframe
    for excel_index, row in rows.iterrows():
        yield int(excel_index) + 2, map_row_to_payload(row)


def print_summary(success_count: int, skipped_count: int, error_count: int) -> None:
    print("")
    print("Aktarim Ozeti")
    print(f"- Basarili: {success_count}")
    print(f"- Atlanan: {skipped_count}")
    print(f"- Hatali: {error_count}")


def main() -> int:
    args = parse_args()

    if not args.excel_path.exists():
        print(f"Excel dosyasi bulunamadi: {args.excel_path}")
        return 1

    dataframe = pd.read_excel(args.excel_path, sheet_name=args.sheet_name)
    if not isinstance(dataframe, pd.DataFrame):
        print("Birden fazla sheet dondu. Lutfan --sheet-name ile tek bir sheet secin.")
        return 1

    success_count = 0
    skipped_count = 0
    error_count = 0

    client = None
    if not args.dry_run:
        try:
            import httpx
        except ModuleNotFoundError:
            print(
                "httpx modulu bulunamadi. Gercek import icin backend bagimliliklarini kurun "
                "veya script'i backend container icinde calistirin."
            )
            return 1

        client = httpx.Client(base_url=args.api_url.rstrip("/"), timeout=args.timeout)

    try:
        for row_number, payload in iter_payloads(dataframe, args.limit):
            if args.dry_run:
                print(f"[DRY RUN] Satir {row_number}")
                print(json.dumps(payload, ensure_ascii=False, indent=2))
                success_count += 1
                continue

            response = client.post("/samples", json=payload)
            if response.status_code == 201:
                print(f"[OK] Satir {row_number} iceri aktarildi: {payload['ornek_no']}")
                success_count += 1
                continue

            detail = response.text
            if response.headers.get("content-type", "").startswith("application/json"):
                detail = response.json().get("detail", response.text)

            if response.status_code == 400 and "zaten mevcut" in str(detail):
                print(f"[SKIP] Satir {row_number} atlandi: {detail}")
                skipped_count += 1
                continue

            print(f"[ERR] Satir {row_number} aktarilamadi: {detail}")
            error_count += 1
    except Exception as exc:
        print(f"[ERR] Aktarim sirasinda beklenmeyen hata: {exc}")
        return 1
    finally:
        if client is not None:
            client.close()

    print_summary(success_count, skipped_count, error_count)
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
