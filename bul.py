import os
import fnmatch

def bul(args):
    if not args:
        print("Kullanım: bul <desen> [dizin]   (örnek: bul *.py, bul rapor* ~/Documents)")
        return

    desen = args[0]
    baslangic = args[1] if len(args) > 1 else "."

    if not os.path.isdir(baslangic):
        print(f"bul: dizin bulunamadı: {baslangic}")
        return

    bulunanlar = []
    for kok, dizinler, dosyalar in os.walk(baslangic):
        for dosya in dosyalar:
            if fnmatch.fnmatch(dosya, desen):
                bulunanlar.append(os.path.join(kok, dosya))

    if bulunanlar:
        for yol in bulunanlar:
            print(yol)
        print(f"\n{len(bulunanlar)} sonuç bulundu.")
    else:
        print("Hiçbir sonuç bulunamadı.")