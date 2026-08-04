# LKShell

Kendi Python tabanlı, bash'ten ilham alan basit bir terminal/shell projesi. Kendim için, kendi kurallarımla yazıyorum :))

## Özellikler

- **Giriş ekranı** — kullanıcı adı ve şifre ile basit bir oturum açma
- **Genişletilebilir komut sistemi** — her komut bir Python fonksiyonu, `SOZLUK` içine ekleyerek yeni komut tanımlanabiliyor
- Şu an desteklenen komutlar:
  - `say <metin>` — yazdığın metni ekrana geri basar
  - `whoami` — mevcut oturumdaki kullanıcıyı gösterir
  - `opsec` — gizli komut :)
  - `fastfetch` — sistem bilgisini (OS, CPU, GPU, RAM, disk, uptime, ekran) logoyla birlikte gösterir
  - `update` — `git pull` ile projeyi GitHub'daki son sürüme günceller
  - `help` — kullanılabilir komutları listeler
  - `exit` — terminalden çıkış

## Kullanım

```bash
git clone https://github.com/diegobrando3/LKShell.git
~/LKShell
python3 sub.py
```

Açılışta kullanıcı adı ve şifre istenir, giriş yapıldıktan sonra `>>$` prompt'u karşılar.

```
>>$ say merhaba dünya
merhaba dünya

>>$ whoami
Test

>>$ fastfetch
 _      _  __ ____  _        OS:        Linux 6.x
| |    | |/ /|  _ \| |       Shell:     LKShell v0.1
| |    | ' / | |_) | |__     Uptime:    0:42:10
| |    |  <  |  __/| '_ \    CPU:       ...
| |____| . \ | |   | | | |   GPU:       ...
|______|_|\_\|_|   |_| |_|   Memory:    ...
Örnektir! ASCII art böyle değil.

>>$ update
Güncellemeler kontrol ediliyor...
Already up to date.
```

## Güncelleme

Projeyi bir kez `git clone` ile indirdikten sonra, yeni sürümleri almak için shell içinden:

```
>>$ update
```

yazman yeterli. Kaydedilmemiş yerel değişikliklerin varsa `update` seni uyarır ve işlemi durdurur — önce commit veya stash yapman gerekir. Güncelleme sonrası değişikliklerin etkili olması için shell'i yeniden başlatman gerekir (`python3 sub.py`).

> Not: `update` komutu yalnızca `git clone` ile indirilen kopyalarda çalışır. Projeyi zip olarak indirdiysen bu komut çalışmaz.

## Yeni komut ekleme

Yeni bir built-in komut eklemek çok basit — bir fonksiyon yaz, `SOZLUK` sözlüğüne ekle:

```python
def selam(args):
    print("Selam! Bu benim özel komutum.")

SOZLUK["selam"] = selam
```

Tüm komut fonksiyonları `(args)` parametresi almalı (kullanmasa bile), çünkü hepsi aynı satırdan (`SOZLUK[cmd](args)`) çağrılıyor.

## Gereksinimler

```bash
pip install psutil --break-system-packages
git
```

## Yol haritası

- [ ] `cd`, `pwd`, `ls` gibi temel dosya sistemi komutları
- [ ] Tanınmayan komutları gerçek sistem shell'ine yönlendirme
- [ ] Komut geçmişi (`history`)
- [ ] Daha güvenli giriş akışı (şifre gizleme)
- [ ] `fastfetch` çıktısında renk (ANSI) desteği

## Neden?

Bash'i taklit ederek nasıl çalıştığını anlamak, kendi terminal mantığımı kurmak için başladığım kişisel bir öğrenme projesi.
