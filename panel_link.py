#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KAFA panel linki üretir.

Kullanım:
  python3 panel_link.py '{"ad":"Ayşe","isler":[{"t":"Kargo firmasını ara"}]}'
  python3 panel_link.py veri.json
  cat veri.json | python3 panel_link.py
  python3 panel_link.py --decode 'https://vibekafasi.github.io/kafa/#k=...'

Çıktı: panel linki (tek satır).
"""

import base64
import json
import sys
import zlib

PANEL = "https://vibekafasi.github.io/kafa/"

LIMITS = {"isler": 5, "bekleyen": 3, "projeler": 4, "notlar": 4}
TEXT_LIMITS = {"ad": 24, "selam": 20, "odak": 120, "t": 60, "a": 70, "e": 40, "tarih": 12}


def _b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64u_coz(text: str) -> bytes:
    text = text.replace("-", "+").replace("_", "/")
    while len(text) % 4:
        text += "="
    return base64.b64decode(text)


def _kirp(value, limit):
    if value is None:
        return None
    text = " ".join(str(value).split())
    return text[:limit]


def normalize(data):
    """Panelin beklediği şekle getirir; fazlalığı keser."""
    if not isinstance(data, dict):
        raise ValueError("JSON bir nesne ({...}) olmalı.")
    out = {}
    for key, limit in TEXT_LIMITS.items():
        if key in data and data[key] is not None:
            out[key] = _kirp(data[key], limit)

    for key, cap in LIMITS.items():
        items = data.get(key)
        if not isinstance(items, list):
            continue
        cleaned = []
        for item in items[:cap]:
            if isinstance(item, str):
                cleaned.append({"t": _kirp(item, TEXT_LIMITS["t"])})
            elif isinstance(item, dict):
                row = {}
                for field, limit in (("t", 60), ("e", 40), ("a", 70), ("d", 1), ("tarih", 12)):
                    if item.get(field) not in (None, ""):
                        row[field] = _kirp(item[field], limit)
                if row:
                    cleaned.append(row)
        out[key] = cleaned

    hedef = data.get("hedef")
    if isinstance(hedef, dict):
        row = {}
        if hedef.get("t"):
            row["t"] = _kirp(hedef["t"], 60)
        if hedef.get("a"):
            row["a"] = _kirp(hedef["a"], 60)
        try:
            row["y"] = max(0, min(100, round(float(hedef.get("y", 0)))))
        except (TypeError, ValueError):
            pass
        out["hedef"] = row

    return out


def encode(data) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    comp = zlib.compressobj(9, zlib.DEFLATED, -15)
    raw = comp.compress(payload) + comp.flush()
    return PANEL + "#k=" + _b64u(raw)


def decode(url: str):
    hash_part = url.split("#", 1)[1] if "#" in url else url
    kind, _, body = hash_part.partition("=")
    if kind not in ("k", "j"):
        raise ValueError("Link #k=... ya da #j=... içermeli.")
    blob = _b64u_coz(body)
    if kind == "k":
        blob = zlib.decompress(blob, -15)
    return json.loads(blob.decode("utf-8"))


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("-")]
    flags = [a for a in argv[1:] if a.startswith("-")]

    if "--decode" in flags:
        target = args[0] if args else sys.stdin.read().strip()
        print(json.dumps(decode(target), ensure_ascii=False, indent=2))
        return 0

    if args and args[0].strip().startswith("{"):
        raw = args[0]
    elif args:
        with open(args[0], encoding="utf-8") as handle:
            raw = handle.read()
    else:
        raw = sys.stdin.read()

    if not raw.strip():
        print("JSON verilmedi.", file=sys.stderr)
        return 2

    data = json.loads(raw)
    print(encode(normalize(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
