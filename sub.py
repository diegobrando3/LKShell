import os
import sys
from fastfetch import fastfetch
from update import update

print("Lütfen LKShell'i tam ekranda kullanın!")
User = "Test"
Passwd= 333
while True:
    ask1=input("User: ")
    if ask1==User:
        while True:
            try:
                ask2=int(input("Password: "))
                if ask2==Passwd:
                    break
                else:
                    print("şifre eşleşmedi")
            except:
                print("şifre eşleşmedi")
                continue
        break
    else:
        print(f"kullanıcı bulunamadı: {ask1}")
def cmd_echo(args):
    print(" ".join(args))
def benkimim(args):
    print(User)
def sudoopsec(args):
    print("Mr. Robot sudo opsec haha")
global path
path=os.path.expanduser("~")
def cmd_gir(args):
    if not args:
        path=os.path.expanduser("~")
        UserPath= print(f"{path}")
    else:
        path=args[0]
        UserPath= print(f"{path}")

    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"gir: dizin bulunamadı: {path}")
    except NotADirectoryError:
        print(f"gir: bir dizin değil: {path}")
    except PermissionError:
        print(f"gir: izin reddedildi: {path}")
def cmd_neredeyim(args):
    print(os.getcwd)
def cmd_ls(args):
    target=args[0] if args else "."
    try:
        items=sorted(os.listdir(target))
        for item in items:
            full_path=os.path.join(target, item)
            if os.path.isdir(full_path):
                print(f"{item}/")#klasör ayırt etmek icin /
            else:
                print(item)
    except FileNotFoundError:
        print(f"varmi: bulunamadı: {target}")
    except NotADirectoryError:
        print(f"varmi: bir dizin değil: {target}")

def cmd_mkdir(args):
    if not args:
        print("mkdir: dizin adı gerekli")
        return
    try:
        os.makedirs(args[0])
    except FileExistsError:
        print(f"mkdir: dizin zaten var: {args[0]}")

def cmd_rm(args):
    if not args[0]:
        print("sil: dosya/dizin adı gerekli")
        return
    target=args[0]
    try:
        if os.path.isdir(target):
            os.rmdir(target)
            print("ok")
        else:
            os.remove(target)
            print("ok")
    except FileNotFoundError:
        print(f"sil: bulunamadı {target}")
    except OSError:
        print(f"sil: klasör boş değil, silinemedi {target}")


def helpme(args):
    print("'say' kendisinden sonra yazılan yazıyı tekrarlar")
    print("'exit' terminalden çıkmak için, Ctrl + C'de basabilirsiniz")
    print("'whoami' mevcut oturumdaki kullanıcıyı söyler")
    print("'opsec' üst seviye güvenlik açar")
    print("'lks' fastfetch")
    print("'update' LKShell'i günceller (Yeniden başlatmanız gerekir!)")

def fetch(args):
    fastfetch(args)

#neofetch ekle
SOZLUK = {
    "say": cmd_echo,
    "whoami": benkimim,
    "lks": fetch,
    "opsec": sudoopsec,
    "help": helpme,
    "update": update,
    "sil": cmd_rm,
    "yarat": cmd_mkdir,
    "neredeyim": cmd_neredeyim,
    "varmi": cmd_ls,
    "gir": cmd_gir,
}
print("Yardım için 'help'")



while True:
    UserInput = input(">>$ ")

    if UserInput == "exit":
        break

    parts = UserInput.split()
    if not parts:
        continue

    cmd = parts[0]
    args = parts[1:]

    if cmd in SOZLUK:
        SOZLUK[cmd](args)
    else:
        print(f"komut bulunamadı: {cmd}")