import threading
import re

RED = "\033[31m"
RESET = "\033[0m"


def _sureyi_saniyeye_cevir(sure_str):
    """'30dk', '1s', '45sn' gibi girdileri saniyeye çevirir."""
    eslesme = re.match(r"^(\d+)(sn|dk|s)$", sure_str)
    if not eslesme:
        return None
    miktar, birim = int(eslesme.group(1)), eslesme.group(2)
    if birim == "sn":
        return miktar
    elif birim == "dk":
        return miktar * 60
    elif birim == "s":
        return miktar * 3600
    return None


def _hatirlat_calistir(mesaj):
    print(f"\n{RED}⏰ HATIRLATMA: {mesaj}{RESET}\n>>$ ", end="", flush=True)


def hatirlat(args):
    if len(args) < 2:
        print("Kullanım: hatirlat <süre> <mesaj>   (örnek: hatirlat 30dk kahve hazır mı)")
        print("Süre formatı: sn (saniye), dk (dakika), s (saat)")
        return

    sure_str = args[0]
    mesaj = " ".join(args[1:])

    saniye = _sureyi_saniyeye_cevir(sure_str)
    if saniye is None:
        print(f"Geçersiz süre formatı: {sure_str} (örnek: 30dk, 1s, 45sn)")
        return

    timer = threading.Timer(saniye, _hatirlat_calistir, args=[mesaj])
    timer.daemon = True  # ana program kapanınca bu da kapansın
    timer.start()
    print(f"Hatırlatma kuruldu: {saniye} saniye sonra '{mesaj}'")