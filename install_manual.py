#!/usr/bin/env python3

import os
import shutil
import subprocess

def install_manual():
    manual_source_path = "phishonthefly.1"
    manual_destination_dir = "/usr/local/man/man1/"
    manual_destination_path = os.path.join(manual_destination_dir, "phishonthefly.1")

    # S'assegura que el directori existeix
    os.makedirs(manual_destination_dir, exist_ok=True)

    # Copia el manual al directori de destí
    shutil.copy(manual_source_path, manual_destination_path)
    print(f"Manual instal·lat a {manual_destination_path}")

    # Actualitza la base de dades del manual
    subprocess.run(["mandb"], check=True)
    print("Base de dades del manual actualitzada amb èxit.")

if __name__ == "__main__":
    install_manual()
