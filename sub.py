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