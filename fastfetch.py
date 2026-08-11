import os
import platform
import subprocess
from datetime import timedelta
import psutil
import socket

SHELL_VERSION = "LKShell v0.2"  # elle güncelle

def get_kernel():
    return platform.release()  # zaten OS satırında var ama ayrı satır istersen bu

def get_hostname():
    return socket.gethostname()


def get_username():
    return os.getenv("USER") or os.getenv("LOGNAME") or "Bilinmiyor"


def get_packages():
    system = platform.system()
    if system == "Linux":
        try:
            out = subprocess.check_output(["dpkg", "--get-selections"], text=True)
            count = len(out.strip().splitlines())
            return f"{count} (dpkg)"
        except Exception:
            pass
    return "Bilinmiyor"


def get_terminal():
    return os.getenv("TERM") or "Bilinmiyor"


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Bilinmiyor"


def get_battery():
    try:
        battery = psutil.sensors_battery()
        if battery:
            status = "şarj oluyor" if battery.power_plugged else "şarjda değil"
            return f"%{battery.percent} ({status})"
    except Exception:
        pass
    return None  # laptop değilse veya bilgi yoksa gösterme

def get_uptime():
    boot = psutil.boot_time()
    now = psutil.time.time()
    delta = timedelta(seconds=int(now - boot))
    return str(delta)



def get_cpu_name():
    system = platform.system()
    if system == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if line.startswith("model name"):
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass
    elif system == "Windows":
        try:
            out = subprocess.check_output(
                ["wmic", "cpu", "get", "name"], text=True
            )
            lines = [l.strip() for l in out.splitlines() if l.strip()]
            if len(lines) > 1:
                return lines[1]
        except Exception:
            pass
    elif system == "Darwin":
        try:
            out = subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
            )
            return out.strip()
        except Exception:
            pass
    return platform.processor() or "Bilinmiyor"


def get_cpu():
    freq = psutil.cpu_freq()
    cpu_name = get_cpu_name()
    percent = psutil.cpu_percent(interval=0.3)
    if freq:
        return f"{cpu_name} @ {freq.current:.0f}MHz ({percent}% kullanım)"
    return f"{cpu_name} ({percent}% kullanım)"


def get_gpu():
    system = platform.system()
    gpu_name = "Bilinmiyor"
    usage_info = None

    if system == "Linux":
        try:
            out = subprocess.check_output(["lspci"], text=True)
            gpus = [
                line.split(": ", 1)[1]
                for line in out.splitlines()
                if "VGA" in line or "3D controller" in line
            ]
            if gpus:
                gpu_name = ", ".join(gpus)
        except Exception:
            pass

        # Önce nvidia-smi'nin var olup olmadığını doğrudan dene (isim eşleşmesine güvenme)
        usage_info = get_nvidia_usage()
        if not usage_info:
            usage_info = get_amd_usage()

    elif system == "Windows":
        try:
            out = subprocess.check_output(
                ["wmic", "path", "win32_VideoController", "get", "name"], text=True
            )
            lines = [l.strip() for l in out.splitlines() if l.strip() and l.strip() != "Name"]
            if lines:
                gpu_name = ", ".join(lines)
        except Exception:
            pass

    elif system == "Darwin":
        try:
            out = subprocess.check_output(
                ["system_profiler", "SPDisplaysDataType"], text=True
            )
            for line in out.splitlines():
                if "Chipset Model" in line:
                    gpu_name = line.split(":", 1)[1].strip()
                    break
        except Exception:
            pass

    if usage_info:
        return f"{gpu_name} ({usage_info})"
    return gpu_name


def get_nvidia_usage():
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        util, mem_used, mem_total = out.strip().split(", ")
        return f"%{util} kullanım, {mem_used}MB/{mem_total}MB VRAM"
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        return None
    except Exception:
        return None


def get_amd_usage():
    # Farklı sistemlerde kart index'i card0 olmayabilir, ilk 4'ü dene
    for i in range(4):
        path = f"/sys/class/drm/card{i}/device/gpu_busy_percent"
        try:
            with open(path) as f:
                percent = f.read().strip()
            return f"%{percent} kullanım"
        except FileNotFoundError:
            continue
        except Exception:
            continue
    return None


def get_memory():
    mem = psutil.virtual_memory()
    used_gb = mem.used / (1024 ** 3)
    total_gb = mem.total / (1024 ** 3)
    return f"{used_gb:.1f}GB / {total_gb:.1f}GB ({mem.percent}%)"


def get_disk():
    disk = psutil.disk_usage("/")
    used_gb = disk.used / (1024 ** 3)
    total_gb = disk.total / (1024 ** 3)
    return f"{used_gb:.1f}GB / {total_gb:.1f}GB ({disk.percent}%)"


def get_display():
    """
    Çözünürlük ve yenileme hızı işletim sistemine göre farklı yollarla alınır.
    Otomatik alınamazsa None döner, sen elle girersin.
    """
    system = platform.system()
    try:
        if system == "Linux":
            out = subprocess.check_output(["xrandr"], text=True)
            for line in out.splitlines():
                if "*" in line:  # aktif mod işaretli satır
                    parts = line.split()
                    resolution = parts[0]
                    refresh = [p for p in parts if "*" in p][0].replace("*", "").replace("+", "")
                    return f"{resolution} @ {refresh}Hz"
        elif system == "Windows":
            import ctypes
            user32 = ctypes.windll.user32
            w = user32.GetSystemMetrics(0)
            h = user32.GetSystemMetrics(1)
            return f"{w}x{h}"  # Windows'ta Hz almak için win32api gerekir
        elif system == "Darwin":  # macOS
            out = subprocess.check_output(
                ["system_profiler", "SPDisplaysDataType"], text=True
            )
            return out  # ham çıktı, isteğe göre parse edilebilir
    except Exception:
        pass
    return None

LOGO = r"""
                                                                                                    
                                                                                                    
                                                                        @@%%%%%%@@                  
                                                                   @@%#############%@@              
                                                                @%####################%@            
                                                              @%########################%@          
                                                            @@############################@         
                                                           @@########=#####################@@       
 @@##@@                                                   @%########*#####@#################@       
   @*.  -@@@                                             @##########=###%.-#################@       
     @: .  ..:=*@@                                     @@##########=##%:.  %################%@      
      @=.        ..=#%@@@                             @=#########*=%#..    @################%@      
       @*.           ..   ...:-+@@            . @@#-+@.=#######%+:.      . @################%@      
        @#                                    .  ..:*.-@##@@#+. .          %################@       
         @#.                                   ..*+. .@##::::..           .#################@       
          @*.                            ....:#-..  .+#::::..            +#################%@       
           @:   .        .         ...::::::...    .-*:::..          ..-%##################@        
            @    .             . ::::::::....      .#::..           .-...:@###############@         
            @+.               ..:::::::......     .*:...      .         .. ##############%@         
             @.                ::::::.. .        .*.           .-       .   #############%          
              #               .::::..           .*.         .  .=+:.        %###########@           
              @.  .            ......   ..    .-=..:-.::.     :+...*.. ..=. ###########@            
              @%                             .=-....*++-*.    ...:=-=:..-..+##########@             
               @                   .        .+.   .=++++*:*.    .=@%+.+.  .##########@              
               @%.       .-..             .=-..   .=-:::*-..+:.+@@@@@@#:-   :#######@@              
               @@.      :+.    .     .   .+.. .. .+-::::.=.  .-@@@@@@@@@#.   %:####%@               
               @@....+=-...          ..+=-=...-..*:::.....=...*@@@@@@@@@*.   .#-##@@                
              @@@=*..       .....:=**:.....  ::-=:....:*@%#:..*@@@@@@@@@@.     #+#                  
              @=.    ..+*%@@@@-::. .        .=+..:%@@*... --+=-@@@@@@@@@@:   . *@.                  
            @=:*#%######%@@@*::@...         .#@@@@@@.  ..=-::::=+@@@@@@@@.     .%                   
          @@@#######%@@@@@@@@#*=           .#@@@@@@-...+:.-. .-:..:#%%#:*.      *                   
         @%#########%#%@@@@@@@@-.  .        :--:++==:... .=..*..       .-.     :@                   
        @############%@@@@@@@%@@..          -.. ..      ..*+.    .    .++.    .%                    
       @#################@@@@@@@@@-..       -.          ......:==*....:@@.  ..%                     
      @###################@@@%@@@@@*.       =.    .     .=-#+=+=*.  .#%*@.  =@                      
      @####################@%##@@@@-.      .*.  .           .:=:. .*@*-:= .%                        
      @#######################%@@@@=.       *.                ..-@+%@:.@ +                          
      @####################@@@@@@@@@.      .*=..... ......:+#@@@#+::% @:@                           
      @%######################%%##@@@...    *@@@@#####*=:..........: @%                             
      @@#############################@-.   .+......               .#                                
       @################################.   :-            ..--.   .*@                               
        @###############################-*-..+.       .-*=..:=+..:. .@                              
        @@#############################%....=%*=.=-=-:+:*::**-......-                               
         @@############################%=.      .....:::-+=+==-..   .%                              
           @%###########################.             .+.=....-.*.   .@                             
             @%########################:.     .        .:----==-..  ...@                            
               @@%################%@@ =..                             .=                            
                                     @.         .                      .%                           
                                     =.                           .     .@                          
                                    +..                                  .                          
                                    :.  .             .   .  ...      . . *                         
                                   @.                                .     %                        
                                   -.                                       @                       
                                  @..                 .                     .@                      
                                  =.                                         :@                     
                                 @:      .            .      ..               :@                    
                                 %.  .        .  .  .                 .        -@                                                     
"""

def fastfetch(args):
    display = get_display()
    battery = get_battery()

    info_lines = [
        f"OS:        {platform.system()} {platform.release()}",
        f"Kernel:    {get_kernel()}",
        f"Hostname:  {get_hostname()}",
        f"Kullanıcı: {get_username()}",
        f"Shell:     {SHELL_VERSION}",
        f"Terminal:  {get_terminal()}",
        f"Uptime:    {get_uptime()}",
        f"Paketler:  {get_packages()}",
        f"CPU:       {get_cpu()}",
        f"GPU:       {get_gpu()}",
        f"Memory:    {get_memory()}",
        f"Disk (/):  {get_disk()}",
        f"IP:        {get_local_ip()}",
    ]
    if battery:
        info_lines.append(f"Batarya:   {battery}")
    if display:
        info_lines.append(f"Display:   {display}")

    logo_lines = LOGO.strip("\n").splitlines()
    max_lines = max(len(logo_lines), len(info_lines))
    for i in range(max_lines):
        left = logo_lines[i] if i < len(logo_lines) else ""
        right = info_lines[i] if i < len(info_lines) else ""
        print(f"{left:<40}  {right}")