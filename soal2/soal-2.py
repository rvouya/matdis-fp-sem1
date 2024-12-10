import pandas as pd
import itertools
import time

# **1. Baca dataset**
df = pd.read_csv("soal-2_dataset.csv")

# Pastikan tipe data konsisten
df["mmr"] = pd.to_numeric(df["mmr"], errors="coerce")
rank_mapping = {"Bronze": 1, "Silver": 2, "Gold": 3, "Platinum": 4, "Diamond": 5}  # Mapping rank ke nilai numerik
df["rank_numeric"] = df["rank"].map(rank_mapping)
df["latency"] = pd.to_numeric(df["latency"], errors="coerce")
df["region"] = df["region"].astype(str)

# Konversi data ke dictionary
data = df.to_dict("records")

# **2. Fungsi untuk filter rank yang berdekatan**
def get_allowed_ranks(rank):
    """
    Mendapatkan daftar rank yang diizinkan bermain bersama berdasarkan rank input.
    """
    allowed_rank_map = {
        1: [1, 2],        # Iron
        2: [1, 2, 3],     # Silver
        3: [2, 3, 4],     # Gold
        4: [3, 4],        # Platinum
    }
    return allowed_rank_map.get(rank, [])

def filter_players_by_rank(players, base_rank):
    """
    Filter pemain berdasarkan rank yang diperbolehkan.
    """
    allowed_ranks = get_allowed_ranks(base_rank)
    return [player for player in players if player["rank_numeric"] in allowed_ranks]

# **3. Sorting manual (mergesort)**
def merge_sort(arr, keys):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left, keys)
        merge_sort(right, keys)

        i = j = k = 0
        while i < len(left) and j < len(right):
            for key in keys:
                left_value = str(left[i][key]) if isinstance(left[i][key], str) else left[i][key]
                right_value = str(right[j][key]) if isinstance(right[j][key], str) else right[j][key]
                if left_value < right_value:
                    arr[k] = left[i]
                    i += 1
                    break
                elif left_value > right_value:
                    arr[k] = right[j]
                    j += 1
                    break
            else:
                arr[k] = left[i]
                i += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

# **4. Backtracking terbatas berdasarkan jumlah match dan rank**
def calculate_team_score(team):
    return sum(player["mmr"] for player in team)

def backtrack_matchmaking(players, base_rank, team_size=5, match_count=1):
    start_time = time.time()
    matches_found = 0
    results = []
    used_players = set()  # Set untuk melacak pemain yang sudah digunakan

    # Filter pemain berdasarkan rank
    players = filter_players_by_rank(players, base_rank)

    # Pastikan ada cukup pemain untuk membentuk dua tim
    if len(players) < 2 * team_size:
        print("Tidak cukup pemain untuk membentuk dua tim!")
        return []

    # Gunakan itertools.combinations sebagai generator untuk menghemat memori
    for team1 in itertools.combinations(players, team_size):
        # Pastikan pemain dalam team1 belum digunakan
        if any(player["username"] in used_players for player in team1):
            continue

        remaining_players = [p for p in players if p not in team1]
        if len(remaining_players) < team_size:
            continue

        for team2 in itertools.combinations(remaining_players, team_size):
            # Pastikan pemain dalam team2 belum digunakan
            if any(player["username"] in used_players for player in team2):
                continue

            # Tambahkan tim ke hasil
            score1 = calculate_team_score(team1)
            score2 = calculate_team_score(team2)
            skill_diff = abs(score1 - score2)

            results.append((team1, team2, skill_diff))
            matches_found += 1

            # Tandai pemain dalam kedua tim sebagai "digunakan"
            used_players.update(player["username"] for player in team1)
            used_players.update(player["username"] for player in team2)

            # Hentikan jika sudah mencapai jumlah pertandingan yang diinginkan
            if matches_found >= match_count:
                elapsed_time = time.time() - start_time
                print(f"Processed {matches_found} matches in {elapsed_time:.2f} seconds")
                return results

    return results

# **5. Input jumlah pertandingan yang ingin dihitung**
match_count = int(input("Masukkan jumlah pertandingan yang ingin dihitung: "))
base_rank = int(input("Masukkan rank dasar untuk matchmaking (1-4): "))  # Menambahkan input rank dasar
team_size = 5
matches = backtrack_matchmaking(data, base_rank, team_size=team_size, match_count=match_count)

# **6. Tampilkan hasil**
for i, (team1, team2, skill_diff) in enumerate(matches, 1):
    print(f"\nMatch {i}:")
    print("Tim 1:")
    for player in team1:
        print(f"Name: {player['username']}, MMR: {player['mmr']}, Region: {player['region']}, Rank: {player['rank']}")

    print("\nTim 2:")
    for player in team2:
        print(f"Name: {player['username']}, MMR: {player['mmr']}, Region: {player['region']}, Rank: {player['rank']}")

    print(f"Skill Tim 1: {calculate_team_score(team1)}, Skill Tim 2: {calculate_team_score(team2)}, Selisih: {skill_diff}")
