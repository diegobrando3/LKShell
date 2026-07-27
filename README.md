# LKShell

Kendi Python tabanlı, bash'ten ilham alan basit bir terminal/shell projesi. Kendim için, kendi kurallarımla yazıyorum :))

## Özellikler

- **Giriş ekranı** — kullanıcı adı ve şifre ile basit bir oturum açma
- **Genişletilebilir komut sistemi** — her komut bir Python fonksiyonu, `SOZLUK` içine ekleyerek yeni komut tanımlanabiliyor
- Şu an desteklenen komutlar:
  - `say <metin>` — yazdığın metni ekrana geri basar
  - `whoami` — mevcut oturumdaki kullanıcıyı gösterir
  - `opsec` — gizli komut :)
  - `help` — kullanılabilir komutları listeler
  - `exit` — terminalden çıkış

## Kullanım

```bash
python3 sub.py
```

Açılışta kullanıcı adı ve şifre istenir, giriş yapıldıktan sonra `>>$` prompt'u karşılar.

```
>>$ say merhaba dünya
merhaba dünya

>>$ whoami
Test

>>$ help
'say' kendisinden sonra yazılan yazıyı tekrarlar
'exit' terminalden çıkmak için, Ctrl + C'de basabilirsiniz
'whoami' mevcut oturumdaki kullanıcıyı söyler
'opsec' üst seviye güvenlik açar
```

## Yeni komut ekleme

Yeni bir built-in komut eklemek çok basit — bir fonksiyon yaz, `SOZLUK` sözlüğüne ekle:

```python
def selam(args):
    print("Selam! Bu benim özel komutum.")

SOZLUK["selam"] = selam
```

Tüm komut fonksiyonları `(args)` parametresi almalı (kullanmasa bile), çünkü hepsi aynı satırdan (`SOZLUK[cmd](args)`) çağrılıyor.

## Yol haritası

- [ ] `cd`, `pwd`, `ls` gibi temel dosya sistemi komutları
- [ ] Tanınmayan komutları gerçek sistem shell'ine yönlendirme
- [ ] Komut geçmişi (`history`)
- [ ] Daha güvenli giriş akışı (şifre gizleme)

## Neden?

Bash'i taklit ederek nasıl çalıştığını anlamak, kendi terminal mantığımı kurmak için başladığım kişisel bir öğrenme projesi.
