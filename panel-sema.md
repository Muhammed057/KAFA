# Panel şeması

Panel linki:

```
https://vibekafasi.github.io/kafa/#k=<base64url(deflate-raw(JSON))>
```

`#k=` sıkıştırılmış, `#j=` sıkıştırılmamış base64url JSON'dur. `#k=` tercih edilir.

Link `scripts/panel_link.py` ile üretilir; elle base64 hesaplanmaz:

```
python3 scripts/panel_link.py '{"ad":"Ayşe","isler":[{"t":"Kargo firmasını ara","e":"cuma"}]}'
python3 scripts/panel_link.py veri.json
cat veri.json | python3 scripts/panel_link.py
```

Doğrulama:

```
python3 scripts/panel_link.py --decode '<link>'
```

## Alanlar

| Alan | Tip | En fazla | Panelde nerede |
|---|---|---|---|
| `ad` | string | 24 | Başlık ("Günaydın Ayşe") |
| `selam` | string | 20 | Karşılama. Boşsa saate göre otomatik |
| `odak` | string | 120 | Başlığın altındaki tek satır |
| `isler` | dizi | 5 | Bugünün işleri |
| `hedef` | nesne | — | Hedef kartı |
| `bekleyen` | dizi | 3 | Bekleyenler |
| `projeler` | dizi | 4 | Projelerim |
| `notlar` | dizi | 4 | Son notlar |

### `isler` — bugünün işleri

Her öğe `{"t": "iş metni", "e": "etiket"}` ya da düz string.

```json
"isler": [
  {"t": "Zeynep hanımın 2 kutu siparişi", "e": "Cuma kargo · önemli"},
  {"t": "En iyi reels'i seç ve paylaş", "e": "15 dk"}
]
```

`e` seçenekli; yazılırsa sağda etiket olarak görünür.

### `hedef` — hedef kartı

```json
"hedef": {"t": "Ayda 100 sipariş", "y": 38, "a": "0 / 100 · kalan 21 gün"}
```

- `t`: hedef adı (60)
- `y`: yüzde, 0–100 (progress bar)
- `a`: alt satır (60). Boşsa `t` varsa "0 / …" görünür.

### `bekleyen` — bekleyenler

```json
"bekleyen": [{"t": "Kargo firmasına fiyat sor", "e": "2 gün geçti"}]
```

En fazla 3; `e` sağda görünür (24).

### `projeler` — projelerim

```json
"projeler": [
  {"t": "Instagram sayfam", "a": "3 reels hazır · sıradaki: paylaş", "d": "y"},
  {"t": "Yeni ürün paketleri", "a": "tasarım bitti", "d": "s"}
]
```

- `t`: proje adı (50)
- `a`: kısa durum (70)
- `d`: durum rengi — `y` yeşil, `s` sarı, `k` kırmızı

### `notlar` — son notlar

```json
"notlar": [{"t": "Un: Mehmet bey, 25 kg 900 TL, perşembe", "tarih": "09.11"}]
```

`tarih` seçenekli; `GG.AA` formatında.

## Örnek

```json
{
  "ad": "Ayşe",
  "selam": "Günaydın",
  "odak": "Ayda 100 sipariş",
  "isler": [
    {"t": "Zeynep hanımın 2 kutu siparişi", "e": "Cuma kargo · önemli"},
    {"t": "En iyi reels'i seç ve paylaş", "e": "15 dk"},
    {"t": "Muhasebe defterine ilk satır", "e": "7 gündür bekliyor"}
  ],
  "hedef": {"t": "Ayda 100 sipariş", "y": 38, "a": "0 / 100 · kalan 21 gün"},
  "bekleyen": [{"t": "Kargo firmasına fiyat sor", "e": "2 gün geçti"}],
  "projeler": [{"t": "Instagram sayfam", "a": "3 reels hazır", "d": "y"}],
  "notlar": [{"t": "Un: Mehmet bey, 25 kg 900 TL, perşembe", "tarih": "09.11"}]
}
```

## Notlar

- Sadece dolu alanları gönder; boş dizi gönderme.
- Uzun metinler panelde zaten kırpılır; script de aynı limitleri uygular.
- Veri değişince linki yeniden üret. Eski link eski veriyi gösterir.
- Linkin içinde bilgiler vardır, sunucuya gitmez; kullanıcıya paylaşmamasını hatırlat.
