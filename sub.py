import os
import sys
import subprocess
from fastfetch import fastfetch
from update import update

setautoallowbash=False
############################################################################################################
##################################### GİRİŞ EKRANI #########################################################
############################################################################################################
print("Lütfen LKShell'i tam ekranda kullanın!")
print("Çıkmak için: exit, quit")
User = "Test"
Passwd= 333
while True:
    ask1=input("User: ")
    if ask1=="exit":
        exit()
    elif ask1=="quit":
        exit()
    elif ask1==User:
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

#########BASIC##############
def cmd_echo(args):
    print(" ".join(args))
def benkimim(args):
    print(User)
def sudoopsec(args):
    print("Mr. Robot sudo opsec haha")
############################

############################################################################################################
####################################BASH DENEME#############################################################
############################################################################################################

def autoallow_on(args):
    global setautoallowbash
    if setautoallowbash==True:
        print("Otomatik bash zaten açık.")
    else:
        setautoallowbash=True
        print("Otomatik bash açıldı")

def autoallow_off(args):
    global setautoallowbash
    if setautoallowbash==False:
        print("Otomatik bash zaten kapalı.")
    else:
        setautoallowbash=False
        print("Otomatik bash kapatıldı.")

def bashdene(cmd, args, parts):
    global setautoallowbash
    if setautoallowbash == False:
        answer = input(f"Bu komut LKShell üzerinde bulunamadı: {cmd} \nBash üzerinden göreve devam edilsin mi? (y/n): ")
        if answer.lower() == "y":
            try:
                subprocess.run(parts)
            except FileNotFoundError:
                print(f"bash: bilinmeyen komut: {cmd}")
            except Exception as e:
                print(f"Hata: {e}")
        else:
            print(f"lks: bilinmeyen komut: {cmd}")
    else:
        # otomatik açıksa sormadan direkt çalıştır
        try:
            subprocess.run(parts)
        except FileNotFoundError:
            print(f"bash: komut bulunamadı: {cmd}")
        except Exception as e:
            print(f"Hata: {e}")

############################################################################################################
####################################DOSYALAR################################################################
############################################################################################################
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
        print("ok")
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
############################################################################################################

def helpme(args):
    print("'say' kendisinden sonra yazılan yazıyı tekrarlar")
    print("'exit' terminalden çıkmak için, Ctrl + C'de basabilirsiniz")
    print("'whoami' mevcut oturumdaki kullanıcıyı söyler")
    print("'opsec' üst seviye güvenlik açar")
    print("'lks' fastfetch")
    print("'update' LKShell'i günceller (Yeniden başlatmanız gerekir!)")
    print("'yarat' seçili dizine klasör oluşturur")
    print("'sil' seçili dizini siler")
    print("'neredeyim' olduğun dizini gösterir")
    print("'varmi' seçili dizinin var olduğunu kontrol eder")
    print("'gir' seçilen dizine girer")
    print("'otobash1' LKShell üzerinde bilinmeyen komudu bash'e otomatik yönlendirir (y/n sorusunu atlar)")
    print("'otobash0' LKShell üzerinde bilinmeyen komudu bash'e otomatik yönlendirmeyi kapatır(y/n sorusu sorar)[DEFAULT]")
def fetch(args):
    fastfetch(args)

############################################################################################################
##################################### DICTIONARY ###########################################################
############################################################################################################
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
    "otobash1": autoallow_on,
    "otobash0": autoallow_off,
}
print("Yardım için 'help'")
############################################################################################################
############################################################################################################
##################################### MAIN LOOP ############################################################
############################################################################################################
while True:
    UserInput = input(">>$ ")

    if UserInput.lower() == "exit":
        exit()
    if UserInput.lower()=="quit":
        exit()
    parts = UserInput.split()
    if not parts:
        continue

    cmd = parts[0]
    args = parts[1:]

    if cmd in SOZLUK:
        SOZLUK[cmd](args)
    else:
        bashdene(cmd, args, parts)
