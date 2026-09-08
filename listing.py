import json
import os

TODO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo.json")


def _load():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _save(gorevler):
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(gorevler, f, indent=2, ensure_ascii=False)


def todo(args):
    if not args:
        print("Kullanım: todo ekle <metin> | todo listele | todo tamamla <no> | todo sil <no>")
        return

    alt_komut = args[0]
    gorevler = _load()

    if alt_komut == "ekle":
        if len(args) < 2:
            print("todo ekle: bir görev metni gerekli")
            return
        metin = " ".join(args[1:])
        gorevler.append({"metin": metin, "tamam": False})
        _save(gorevler)
        print(f"Eklendi: {metin}")

    elif alt_komut == "listele":
        if not gorevler:
            print("Görev listen boş.")
            return
        for i, gorev in enumerate(gorevler, 1):
            durum = "[x]" if gorev["tamam"] else "[ ]"
            print(f"{i}. {durum} {gorev['metin']}")

    elif alt_komut == "tamamla":
        if len(args) < 2 or not args[1].isdigit():
            print("todo tamamla: geçerli bir görev numarası gerekli")
            return
        idx = int(args[1]) - 1
        if 0 <= idx < len(gorevler):
            gorevler[idx]["tamam"] = True
            _save(gorevler)
            print(f"Tamamlandı: {gorevler[idx]['metin']}")
            for i, gorev in enumerate(gorevler, 1):
                durum = "[x]" if gorev["tamam"] else "[ ]"
                print(f"{i}. {durum} {gorev['metin']}")

        else:
            print("Böyle bir görev numarası yok.")

    elif alt_komut == "sil":
        if len(args) < 2 or not args[1].isdigit():
            print("todo sil: geçerli bir görev numarası gerekli")
            return
        idx = int(args[1]) - 1
        if 0 <= idx < len(gorevler):
            silinen = gorevler.pop(idx)
            _save(gorevler)
            print(f"Silindi: {silinen['metin']}")
        else:
            print("Böyle bir görev numarası yok.")

    else:
        print(f"Bilinmeyen alt komut: {alt_komut}")