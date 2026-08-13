import curses
import json
import os
import hashlib
import time

ACCOUNTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts.json")

RED = "\033[31m"
RESET = "\033[0m"

MAX_ATTEMPTS = 3
COOLDOWN_SECONDS = 30


def hata(msg):
    print(f"{RED}{msg}{RESET}")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return {}
    try:
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=2, ensure_ascii=False)


def _menu(stdscr, title, options):
    curses.curs_set(0)
    current = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title)
        for i, option in enumerate(options):
            prefix = "> " if i == current else "  "
            stdscr.addstr(i + 2, 0, f"{prefix}{option}")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            current = (current - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            return current


def show_menu(title, options):
    return curses.wrapper(lambda stdscr: _menu(stdscr, title, options))


def cooldown_bekle():
    hata(f"Çok fazla yanlış deneme yaptın. {COOLDOWN_SECONDS} saniye bekleman gerekiyor.")
    for kalan in range(COOLDOWN_SECONDS, 0, -1):
        print(f"\r{RED}Bekleniyor... {kalan}s{RESET}   ", end="", flush=True)
        time.sleep(1)
    print()  # satırı temizlemek için


def giris_yap(accounts):
    denemeler = 0
    while denemeler < MAX_ATTEMPTS:
        username = input("Kullanıcı adı: ")
        password = input("Şifre: ")

        if username in accounts and accounts[username]["password"] == hash_password(password):
            print(f"Hoşgeldin, {username}!")
            return username

        denemeler += 1
        kalan_hak = MAX_ATTEMPTS - denemeler
        if kalan_hak > 0:
            hata(f"Kullanıcı adı veya şifre hatalı. Kalan hak: {kalan_hak}")
        else:
            cooldown_bekle()
            return None  # cooldown sonrası menüye dön

    return None


def hesap_olustur(accounts):
    denemeler = 0
    while denemeler < MAX_ATTEMPTS:
        username = input("Yeni kullanıcı adı: ")

        if not username.strip():
            denemeler += 1
            hata(f"Kullanıcı adı boş olamaz. Kalan hak: {MAX_ATTEMPTS - denemeler}")
            continue
        if username in accounts:
            denemeler += 1
            hata(f"Bu kullanıcı adı zaten alınmış. Kalan hak: {MAX_ATTEMPTS - denemeler}")
            continue

        password = input("Şifre: ")
        password2 = input("Şifre (tekrar): ")
        if password != password2:
            denemeler += 1
            kalan_hak = MAX_ATTEMPTS - denemeler
            if kalan_hak > 0:
                hata(f"Şifreler eşleşmiyor. Kalan hak: {kalan_hak}")
                continue
            else:
                cooldown_bekle()
                return

        security_q = input("Güvenlik sorusu (şifremi unuttum'da sorulacak): ")
        security_a = input("Cevap: ")

        accounts[username] = {
            "password": hash_password(password),
            "security_question": security_q,
            "security_answer": hash_password(security_a.lower().strip()),
        }
        save_accounts(accounts)
        print("Hesap oluşturuldu, şimdi giriş yapabilirsin.")
        return

    cooldown_bekle()


def sifremi_unuttum(accounts):
    denemeler = 0
    while denemeler < MAX_ATTEMPTS:
        username = input("Kullanıcı adı: ")
        if username not in accounts:
            denemeler += 1
            kalan_hak = MAX_ATTEMPTS - denemeler
            if kalan_hak > 0:
                hata(f"Böyle bir kullanıcı yok. Kalan hak: {kalan_hak}")
                continue
            else:
                cooldown_bekle()
                return

        question = accounts[username].get("security_question", "Güvenlik sorusu yok")
        print(f"Soru: {question}")
        answer = input("Cevap: ")

        if hash_password(answer.lower().strip()) == accounts[username].get("security_answer"):
            new_pw = input("Yeni şifre: ")
            accounts[username]["password"] = hash_password(new_pw)
            save_accounts(accounts)
            print("Şifre güncellendi, giriş yapabilirsin.")
            return

        denemeler += 1
        kalan_hak = MAX_ATTEMPTS - denemeler
        if kalan_hak > 0:
            hata(f"Cevap yanlış. Kalan hak: {kalan_hak}")
        else:
            cooldown_bekle()
            return

def hesap_sil(accounts):
    denemeler = 0
    while denemeler < MAX_ATTEMPTS:
        username = input("Silinecek kullanıcı adı: ")

        if username not in accounts:
            denemeler += 1
            kalan_hak = MAX_ATTEMPTS - denemeler
            if kalan_hak > 0:
                hata(f"Böyle bir kullanıcı yok. Kalan hak: {kalan_hak}")
                continue
            else:
                cooldown_bekle()
                return

        password = input("Şifre (onaylamak için): ")
        if accounts[username]["password"] != hash_password(password):
            denemeler += 1
            kalan_hak = MAX_ATTEMPTS - denemeler
            if kalan_hak > 0:
                hata(f"Şifre hatalı. Kalan hak: {kalan_hak}")
                continue
            else:
                cooldown_bekle()
                return

        onay = input(f"'{username}' hesabını silmek istediğine emin misin? (evet/hayır): ")
        if onay.lower() == "evet":
            del accounts[username]
            save_accounts(accounts)
            print("Hesap silindi.")
        else:
            print("İptal edildi.")
        return

def login_flow():
    accounts = load_accounts()

    while True:
        choice = show_menu("LKShell - Hoşgeldin",
                            ["Giriş yap", "Hesap oluştur", "Şifremi unuttum", "Hesap sil", "Çıkış"])

        if choice == 0:
            result = giris_yap(accounts)
            if result:
                return result

        elif choice == 1:
            hesap_olustur(accounts)

        elif choice == 2:
            sifremi_unuttum(accounts)

        elif choice == 3:
            hesap_sil(accounts)

        elif choice == 4:
            print("Görüşürüz!")
            exit(0)