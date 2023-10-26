# Imports
import customtkinter
from PIL import Image, ImageTk
import subprocess

# Configurações
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=5, padx=5, fill="both", expand=True)

# Imagens
def load(image_path, size=(50, 50)):
    image = Image.open(image_path)
    resized_image = image.resize(size)
    return ImageTk.PhotoImage(resized_image)

apps = load("img/apps.png")
icones = load("img/icones.png")
switch = load("img/switch.png")
host = load("img/host.png")
pasta = load("img/pasta.png")

# Pacotes
packages = {
    "remove": [
        "gnome-sudoku",
        "gnome-calculator",
        "gnome-screenshot",
        "gnome-characters",
        "gnome-contacts",
        "gnome-dictionary",
        "gnome-maps",
        "gnome-mahjongg",
        "gnome-weather",
        "gnome-mines",
        "gnome-logs",
        "gnome-clocks",
        "gnome-chess",
        "gnome-extensions",
        "bijiben",
        "system-config-printer",
        "seahorse",
        "iagno",
        "swell-foop",
        "transmission-gtk",
        "totem",
        "pidgin",
        "polari",
        "yelp",
        "vinagre",
        "quadrapassel",
        "simple-scan",
        "lightsoff",
        "dosbox",
        "evolution",
        "evince",
        "gimp",
        "opensuse-welcome",
        "cheese",
        "baobab",
        "gpk-update-viewer",
        "tigervnc",
        "PackageKit",
    ],
    "install": [
        "bleachbit",
        "zsh",
        "steam",
        "htop",
        "lutris",
        "neofetch",
        "gamemode",
        "gamemoded",
        "libgamemode-devel",
        "libgamemode0",
        "libgamemode0-32bit",
        "libgamemodeauto0",
        "libgamemodeauto0-32bit",
        "easyeffects",
        "sublime-text",
        "gh",
        "discord",
        "sysconfig-netconfig",
        # Pacotes flatpak
        "com.vysp3r.ProtonPlus",
        "com.mattjakeman.ExtensionManager",
        "org.videolan.VLC",
        "org.gabmus.hydrapaper",
    ]
}

#Array de Funçoes   
def handle_packages(action):
    if action not in packages:
        return

    command = "sudo zypper {} -y ".format("install" if action == "install" else "remove")

    for package in packages[action]:
        if package.startswith(("org.", "com.")):
            # Use flatpak para pacotes que começam com "org." ou "com."
            flatpak_command = "sudo flatpak install -y {}".format(package)
            subprocess.run(flatpak_command, shell=True, executable="/bin/bash")
        else:
            # Use zypper para outros pacotes
            zypper_command = command + package
            subprocess.run(zypper_command, shell=True, executable="/bin/bash")

def aplicar_tema():
    tema = 'Catppuccin-Mocha-Standard-Lavender-Dark'
    icones = 'Tela-dracula'
    cursor = 'Win-8.1-S'

    commands = [
        f'gsettings set org.gnome.desktop.interface gtk-theme "{tema}"',
        f'gsettings set org.gnome.desktop.interface icon-theme "{icones}"',
        f'gsettings set org.gnome.desktop.interface cursor-theme "{cursor}"',
        f'flatpak --user override --filesystem=/usr/share/icons/:ro',
        f'flatpak --user override --filesystem=/home/$USER/.icons/:ro',
        f'sudo flatpak override --env=GTK_THEME=Catppuccin-Mocha-Standard-Lavender-Dark',
        f'sudo flatpak override --filesystem=$HOME/.themes',
        f'dconf load /org/gnome/shell/extensions/ < extensao.conf',
    ]
    
    for cmd in commands:
        subprocess.run(cmd, shell=True, executable="/bin/bash")

def aplicar_keybinds():
    microfone= 'Page_down'
    mudar_janelas = '<Alt>Tab'
    fechar_janelas = '<Alt>4'
    prints = 'Page_up'

    commands = [
        f'gsettings set org.gnome.settings-daemon.plugins.media-keys mic-mute "[\'{microfone}\']"',
        f'gsettings set org.gnome.desktop.wm.keybindings switch-windows "[\'{mudar_janelas}\']"',
        f'gsettings set org.gnome.desktop.wm.keybindings close "[\'{fechar_janelas}\']"',
        f'gsettings set org.gnome.shell.keybindings show-screenshot-ui "[\'{prints}\']"',
    ]

    for cmd in commands:
        subprocess.run(cmd, shell=True, executable="/bin/bash")

def copiar_arquivos():
    commands = [
        f'cp -r ./arquivos/.icons /home/$USER/', # Tema
        f'cp -r ./arquivos/.themes /home/$USER/', # Icones
        f'cp -r ./arquivos/rich\ presence/* /home/$USER/.config/autostart', # Rich Presence
        f'ln -s -v -r ./arquivos/Lutris/lutris/ /home/$USER/.local/share', # Lutris
        f'ln -s -v -r ./arquivos/Lutris/.config/lutris /home/$USER/.config', # Lutris 2
        f'cp -r ./arquivos/Terminal/.bashrc /home/$USER/', # config Bash
        f'cp -r ./arquivos/Terminal/.zshrc /home/$USER/', # config Zsh
        f'mkdir -p /home/$USER/.config/easyeffects', # Criando dir do easyeffects
        f'cp -r ./arquivos/Equalizadores/* /home/$USER/.config/easyeffects/', # Eq
        f'mkdir -p /home/$USER/.config/BetterDiscord', # Dir BD 
        f'cp -r ./arquivos/BetterDiscord/ /home/$USER/.config/', # Plugins e tema
        f'sudo cp -r ./arquivos/WOL/* /etc/systemd/system', # Wake on lan
        f'sudo chmod 644 /etc/systemd/system/wol.service', # Perms para WOL
        f'sudo systemctl enable wol.service', # Habilitar WOL
        f'sudo systemctl start wol.service', # Iniciar WOL
        
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True, executable="/bin/bash")

def repositorios():
    commands = [
        f'sudo zypper ar -cfp 90 https://ftp.gwdg.de/pub/linux/misc/packman/suse/openSUSE_Tumbleweed/ packman',
        f'sudo zypper refresh',
        f'sudo zypper dup --from packman --allow-vendor-change',
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True, executable="/bin/bash")

# Botões
buttons = [
    {
        "text": "Instalar Pacotes",
        "image": apps,
        "command": lambda: handle_packages("install")
    },
    {
        "text": "Aplicar Tema",
        "image": icones,
        "command": aplicar_tema
    },
    {
        "text": "Repositorios",
        "image": icones,
        "command": repositorios
    },
    {
        "text": "Keybinds",
        "image": switch,
        "command": aplicar_keybinds
    },
    {
        "text": "Copiar arquivos",
        "image": pasta,
        "command": copiar_arquivos
    },
    {
        "text": "Remover Pacotes",
        "image": apps,
        "command": lambda: handle_packages("remove")
    }
]

# Cria os botões
for button_data in buttons:
    button = customtkinter.CTkButton(
        master=frame,
        text=button_data["text"],
        image=button_data["image"],
        corner_radius=6,
        command=button_data["command"]
    )
    button.pack(pady=10, padx=10)

def host_name():
    new_hostname = hostname_entry.get()

    if " " in new_hostname:
        print("Nome de host inválido. O nome do host não pode conter espaços.")
    else:
        command = f"sudo hostnamectl set-hostname {new_hostname}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao definir o nome do host: {e}")

# Cria uma moldura para o botão e a entrada
hostname_frame = customtkinter.CTkFrame(frame)
hostname_frame.pack(fill="both", expand=True)

# Adiciona a caixa de entrada para o nome do host
hostname_label = customtkinter.CTkLabel(hostname_frame, image=host)
hostname_label.grid(row=0, column=0)

hostname_entry = customtkinter.CTkEntry(hostname_frame)
hostname_entry.grid(row=0, column=1)

# Cria o botão de alteração de hostname com imagem à esquerda
change_button = customtkinter.CTkButton(hostname_frame, text="Alterar Hostname", command=host_name)
change_button.grid(row=1, column=1)

# Inicia a janela
root.mainloop()