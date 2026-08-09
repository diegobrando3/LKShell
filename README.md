## LKShell v0.2

Kendi Python tabanlı, Bash'ten ilham alan hafif ve genişletilebilir bir terminal/shell projesi. Sıfırdan kendi kurallarımla, terminal mantığını ve komut satırı araçlarının nasıl çalıştığını anlamak amacıyla geliştiriyorum :))

---

### Özellikler

* **Güvenli Oturum Açma:** Başlangıçta kullanıcı adı ve şifre doğrulaması ile basit bir kimlik doğrulama katmanı.
* **Modüler Sözlük Tabanlı Mimari:** Her komut bağımsız bir Python fonksiyonu olarak tanımlanır ve `SOZLUK` (dispatch dictionary) yapısına kolayca entegre edilir.
* **Yerleşik Komut Desteği:**
  * `say <metin>` — Girilen metni ekrana yazdırır.
  * `whoami` — Mevcut aktif oturumdaki kullanıcı adını gösterir.
  * `opsec` — Gizli ve eğlenceli bir güvenlik modu komutu :)
  * `lks` — Sistem donanım ve yazılım bilgilerini logoyla birlikte (`fastfetch` entegrasyonu) listeler.
  * `update` — Projeyi doğrudan GitHub'daki son sürüme günceller.
  * `help` — Tüm kullanılabilir komutları ve açıklamalarını listeler.
  * `gir <dizin>` — Çalışma dizinini değiştirir (`cd` işlevi).
  * `neredeyim` — Mevcut çalışma dizinini gösterir (`pwd` işlevi).
  * `varmi [dizin]` — Belirtilen dizindeki dosya ve klasörleri listeler (`ls` işlevi, klasörleri `/` uzantısıyla ayırt eder).
  * `yarat <dizin>` — Yeni bir klasör oluşturur (`mkdir` işlevi).
  * `sil <dosya/dizin>` — Belirtilen dosya veya boş klasörü siler (`rm` işlevi).
  * `exit` / `quit` — Shell'den güvenli çıkış yapar.

---

### Kurulum

Projeyi klonlamak ve çalıştırmak için terminalinizde şu adımları takip edin:

```bash
git clone https://github.com/diegobrando3/LKShell.git
cd LKShell
python3 sub.py
```

Açılışta kullanıcı adı (`Test`) ve şifre (`333`) istenir; başarılı girişin ardından `>>$ ` komut istemi sizi karşılar.

---

### Örnek Kullanım

```text
>>$ say merhaba dünya
merhaba dünya

>>$ whoami
Test

>>$ neredeyim
/home/kullanici/LKShell

>>$ varmi
sub.py
README.md
fastfetch.py
update.py

>>$ lks
 _      _  __ ____  _        OS:        Linux 6.x
| |    | |/ /|  _ \| |       Shell:     LKShell v0.2
| |    | ' / | |_) | |__     Uptime:    0:42:10
| |    |  <  |  __/| '_ \    CPU:       ...
| |____| . \ | |   | | | |   GPU:       ...
|______|_|\_\|_|   |_| |_|   Memory:    ...
*(Örnek çıktıdır)*           IP:        ...

>>$ update
Güncellemeler kontrol ediliyor...
Already up to date.
```

---

### Güncelleme

Projeyi `git clone` ile indirdiyseniz, en son güncellemeleri almak için shell içerisinden şu komutu çalıştırmanız yeterlidir:

```text
>>$ update
```

> **Not:** Kaydedilmemiş yerel değişiklikleriniz varsa `update` komutu sizi uyararak işlemi durduracaktır (önce `commit` veya `stash` yapmanız gerekir). Güncelleme sonrasında değişikliklerin aktif olması için shell'i yeniden başlatmanız (`python3 sub.py`) gerekmektedir. Projeyi ZIP olarak indirdiyseniz bu komut çalışmaz.

---

### Yeni Komut Ekleme

LKShell, modüler yapısı sayesinde yeni komutlar eklemeyi oldukça kolaylaştırır. Tek yapmanız gereken bir fonksiyon yazıp bunu `SOZLUK` sözlüğüne kaydetmektir:

```python
def selam(args):
    print("Selam! Bu benim özel komutum.")

# Sözlüğe ekleme:
SOZLUK["selam"] = selam
```

> **İpucu:** Tüm komut fonksiyonları, argümanları işlemeseler dahi zorunlu olarak `args` parametresini almalıdır; çünkü tüm komutlar `SOZLUK[cmd](args)` mantığıyla aynı arayüz üzerinden çağrılır.

---

### Gereksinimler

* `Python 3.x`
* `git` (Güncelleme özelliği için)
* `psutil` (Sistem izleme araçları için)

Gerekli Python kütüphanesini kurmak için:
```bash
pip install psutil --break-system-packages
```

---

### Yol Haritası (Roadmap)

* [x] Temel dosya yönetimi komutları (`gir`, `neredeyim`, `varmi`, `yarat`, `sil`)
* [ ] Tanınmayan komutları sistemin kendi shell'ine (Bash/Zsh) yönlendirme
* [ ] Komut geçmişi (`history` ve ok tuşları desteği)
* [ ] Daha güvenli giriş ekranı (şifreyi yıldızlama / gizleme)
* [ ] `fastfetch` çıktısı için renkli (ANSI) terminal desteği
