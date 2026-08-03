import subprocess
import os

def update(args):
    if not os.path.isdir(".git"):
        print("Bu klasör bir git reposu değil, güncelleme yapılamıyor.")
        print("Projeyi 'git clone' ile indirdiğinden emin ol.")
        return

    print("Güncellemeler kontrol ediliyor...")
    try:
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("Hata:", result.stderr)
    except FileNotFoundError:
        print("git bulunamadı, sisteminde git kurulu mu?")