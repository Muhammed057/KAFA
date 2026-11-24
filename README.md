# KAFA Asistan — Skill Paketi

Claude'a yüklenen kişisel asistan. "Kafa kur" ile kurulur; gün planı, yapılacaklar, notlar, para defteri, müşteri takibi, hedef ve alışkanlık takibi yapar, "Kafa, panelimi aç" deyince kişisel panel linki üretir.

## Kurulum (5 adım, ~5 dakika)

1. **Kodu bulutta çalıştır** — claude.ai → sol altta adın → **Ayarlar** → **Yetenekler** → "Kod yürütme ve dosya oluşturma" başlığının altındaki **Kodu bulutta çalıştır** düğmesi mavi olsun.
2. **Skills** — Ayarlar → **Skills** → **+ Ekle** → **Skill yükle**.
3. **Yükle** — `kafa_asistan.zip`'i gri kutuya bırak (ya da kutuya tıklayıp seç) → **Yükle**. Güvenlik taraması kısa sürer.
4. **Kontrol** — `kafa-asistan` sayfası açılır; sağ üstteki düğme mavi olmalı. Mavi = açık.
5. **Başla** — Yeni sohbet → **Kafa kur** yaz, soruları cevapla.

> Zip'i açma. Claude zip'i olduğu gibi yükler. Bilgisayarın kendiliğinden açtıysa `kafa-asistan` klasörünü sağ tıklayıp yeniden sıkıştır.

## İçindekiler

| Dosya | Ne işe yarar |
|---|---|
| `SKILL.md` | Asistanın davranışı: kurulum, komutlar, kayıt kuralları, panel linki |
| `scripts/panel_link.py` | Defter verisini kişisel panel linkine çevirir |
| `references/komutlar.md` | Her komut için örnek giriş ve beklenen cevap |
| `references/panel-sema.md` | Panelin beklediği JSON alanları ve link formatı |

## Panel linki

Kullanıcı "Kafa, panelimi aç" dediğinde `SKILL.md`'deki adımlar izlenir:

```
python3 scripts/panel_link.py '{"ad":"Ayşe","isler":[{"t":"Kargo firmasını ara","e":"cuma"}]}'
```

Çıktı: `https://vibekafasi.github.io/kafa/#k=...` — link, veriyi kendi içinde taşır; sunucuya gitmez.

Doğrulamak için:

```
python3 scripts/panel_link.py --decode '<link>'
```

## Notlar

- Bu paket resmi `kafa_asistan.zip` değildir; kılavuzdaki komutları ve panel şemasını uygulayan bağımsız bir pakettir.
- Panel linki için Claude'da kod yürütme açık olmalı (Kurulum adımı 1). Kapalıysa kullanıcıya bunu söyle.
- Bilgiler kullanıcının kendi hesabında/klasöründe kalır; paket hiçbir veri göndermez.
- Kamera, el hareketi ve ses özellikleri panel tarafındadır; skill bunları üretmez, sadece linki verir.
