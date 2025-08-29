#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BBFS EKOR PRO MAX – 6 Angka Terbaik untuk Tembus 2D Belakang
Author : You
Fitur  : Statistik murni + Pola Historis + Backtest Akurasi
"""

import os
import sys
import time
from collections import Counter
from typing import List, Set

# ──────────────────────────────────────────────────────────────
# Warna & Tampilan
# ──────────────────────────────────────────────────────────────
RESET = "\033[0m"

def colored(text: str, color: str = "white", style: str = "normal") -> str:
    styles = {"normal": 0, "bold": 1, "dim": 2}
    colors = {
        "red": 31, "green": 32, "yellow": 33, "blue": 34,
        "magenta": 35, "cyan": 36, "white": 37,
        "bright_red": 91, "bright_green": 92, "bright_yellow": 93,
        "bright_blue": 94, "bright_magenta": 95, "bright_cyan": 96,
    }
    s = styles.get(style, 0)
    c = colors.get(color, 37)
    return f"\033[{s};{c}m{text}{RESET}"

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# ──────────────────────────────────────────────────────────────
# Banner
# ──────────────────────────────────────────────────────────────
BANNER = colored(r"""
   ____           _       _    ____ _  __
  / ___| ___ _ __| |_ ___| |  / ___| |/ /
 | |  _ / _ \ '__| __/ _ \ | | |   | ' / 
 | |_| |  __/ |  | ||  __/ | | |___| . \ 
  \____|\___|_|   \__\___|_|  \____|_|\_\
                                        
        🔮 BBFS EKOR PRO MAX v3.0
     6 Digit dari Data Nyata, Bukan Tebakan
""", "cyan", "bold")

HISTORY_FILE = "history.txt"

# ──────────────────────────────────────────────────────────────
# Load & Save Histori
# ──────────────────────────────────────────────────────────────
def load_history() -> List[str]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return [line.strip() for line in f if line.strip().isdigit() and len(line.strip()) == 4]
    except:
        return []

def save_history(history: List[str]) -> None:
    with open(HISTORY_FILE, "w") as f:
        f.write("\n".join(history))

# ──────────────────────────────────────────────────────────────
# Prediksi BBFS 6 Digit (Berdasarkan Statistik 2D Belakang)
# ──────────────────────────────────────────────────────────────
def generate_bbfs_from_ekor_stats(history: List[str]) -> List[str]:
    if len(history) < 5:
        # Jika belum ada data, kembalikan default kuat
        return ["1", "2", "4", "5", "7", "8"]  # angka umum kuat

    # Ambil semua 2D belakang
    ekors: List[str] = [res[2:] for res in history]

    # Hitung frekuensi tiap digit di posisi PULUHAN (d3) dan SATUAN (d4)
    freq_puluhan = Counter([e[0] for e in ekors])
    freq_satuan = Counter([e[1] for e in ekors])

    # Gabungkan frekuensi total
    freq_total = Counter()
    for d in "0123456789":
        freq_total[d] += freq_puluhan[d] + freq_satuan[d]

    # Ambil 6 digit dengan frekuensi tertinggi
    top_6 = [item[0] for item in freq_total.most_common(6)]
    return sorted(top_6, key=lambda x: int(x))

# ──────────────────────────────────────────────────────────────
# Backtest: Berapa kali 2D MASUK BBFS?
# ──────────────────────────────────────────────────────────────
def backtest_bbfs(history: List[str]) -> None:
    if len(history) < 2:
        print(colored("\n❌ Butuh minimal 2 data!", "red"))
        input(colored("Enter...", "dim"))
        return

    tembus = 0
    total = len(history) - 1

    print(colored(f"\n🔍 BACKTEST: Apakah 2D MASUK BBFS?", "bright_yellow", "bold"))

    for i in range(total):
        prev_batch = history[:i+1]
        actual = history[i+1]
        ekor = actual[2:]  # d3 dan d4
        d3, d4 = ekor[0], ekor[1]

        bbfs = generate_bbfs_from_ekor_stats(prev_batch)
        bbfs_set = set(bbfs)

        match = d3 in bbfs_set and d4 in bbfs_set
        status = "✅" if match else "❌"

        if match:
            tembus += 1
            print(f"{status} {prev_batch[-1]} → {actual} | 2D: {ekor} | BBFS: {''.join(bbfs)}")
        else:
            print(f"{status} {prev_batch[-1]} → {actual} | ❌ {ekor} | BBFS: {''.join(bbfs)}")

    akurasi = (tembus / total) * 100
    warna = "green" if akurasi >= 80 else "yellow" if akurasi >= 60 else "red"
    print(colored(f"\n🎯 Akurasi Tembus 2D: {tembus}/{total} → {akurasi:.1f}%", warna, "bold"))
    input(colored("\nTekan Enter untuk kembali...", "dim"))

# ──────────────────────────────────────────────────────────────
# Animasi
# ──────────────────────────────────────────────────────────────
def loading_animation():
    for _ in range(15):
        sys.stdout.write("\r" + colored("📊", "cyan") + " Analisis statistik ekor...")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

# ──────────────────────────────────────────────────────────────
# Menu
# ──────────────────────────────────────────────────────────────
def menu():
    history = load_history()
    while True:
        clear_screen()
        print(BANNER)
        print(colored(f"\n📁 Histori: {len(history)} data", "blue", "dim"))
        print(colored("\n [1] Prediksi BBFS 6 Digit (Statistik Ekor)", "bright_green"))
        print(colored(" [2] Tambah Histori", "cyan"))
        print(colored(" [3] Backtest (2D Masuk BBFS?)", "bright_yellow"))
        print(colored(" [4] Hapus Histori", "red"))
        print(colored(" [5] Keluar\n", "bright_red"))

        choice = input(colored("Pilih: ", "yellow")).strip()

        if choice == "1":
            if len(history) < 5:
                print(colored("\n⚠️ Butuh minimal 5 data histori untuk prediksi akurat!", "yellow"))
                print(colored("Tambahkan lebih banyak data di menu [2].", "dim"))
                input(colored("\nEnter...", "dim"))
                continue

            loading_animation()
            bbfs = generate_bbfs_from_ekor_stats(history)
            clear_screen()
            print(BANNER)
            print(colored(f"\n🎯 BBFS 6 DIGIT (Statistik 2D Belakang):", "bright_magenta", "bold"))
            print(" → " + colored("  ".join(bbfs), "bright_yellow", "bold"))
            print(colored(f"\n💡 Catatan:\n   • Berdasarkan frekuensi 2D historis\n   • Semakin banyak data, semakin akurat\n   • Cocok untuk semua pasaran", "dim"))
            input(colored("\n\nEnter untuk kembali...", "dim"))

        elif choice == "2":
            print(colored("\nMasukkan 4D (kosongkan untuk selesai):", "cyan"))
            added = 0
            while True:
                inp = input(f"Hasil {len(history) + added + 1}: ").strip()
                if not inp: break
                if inp.isdigit() and len(inp) == 4:
                    history.append(inp)
                    added += 1
                    print(colored("✓", "green"))
                else:
                    print(colored("✗ Harus 4 digit!", "red"))
            if added > 0:
                save_history(history)

        elif choice == "3":
            backtest_bbfs(history)

        elif choice == "4":
            if input(colored("Hapus semua? (y/t): ", "red")).lower() == 'y':
                history = []
                if os.path.exists(HISTORY_FILE):
                    os.remove(HISTORY_FILE)
                print(colored("🗑️ Histori dihapus", "green"))
                time.sleep(1)

        elif choice == "5":
            print(colored("\nSemoga 2D Anda selalu masuk BBFS! 🍀", "bright_yellow"))
            break

        else:
            print(colored("Pilih 1-5!", "red"))
            input(colored("Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Jalankan
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(colored("\n\nDihentikan.", "red"))
