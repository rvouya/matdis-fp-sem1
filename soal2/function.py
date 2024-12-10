import pandas as pd
import itertools
import time

def load_data(filename):
    # Memuat data CSV dan mengonversi kolom yang diperlukan
    df = pd.read_csv(filename)
    df["mmr"] = pd.to_numeric(df["mmr"], errors="coerce")
    rank_mapping = {"Iron": 1, "Silver": 2, "Gold": 3, "Platinum": 4}
    df["rank_numeric"] = df["rank"].map(rank_mapping)
    df["latency"] = pd.to_numeric(df["latency"], errors="coerce")
    df["region"] = df["region"].fillna('NA')
    return df.to_dict("records")

def get_allowed_ranks(rank):
    # Menentukan rank yang diperbolehkan berdasarkan rank dasar
    allowed_rank_map = {
        1: [1, 2],
        2: [1, 2, 3],
        3: [2, 3, 4],
        4: [3, 4],
    }
    return allowed_rank_map.get(rank, [])

def filter_players_by_rank(players, base_rank):
    # Memfilter pemain berdasarkan rank yang diperbolehkan
    allowed_ranks = get_allowed_ranks(base_rank)
    return [player for player in players if player["rank_numeric"] in allowed_ranks]

def calculate_team_score(team):
    # Menghitung total MMR dari sebuah tim
    return sum(player["mmr"] for player in team)

def backtrack_matchmaking(players, base_rank, team_size, match_count):
    start_time = time.time()
    matches_found = 0
    results = []
    used_players = set()

    # Filter pemain berdasarkan rank dasar
    players = filter_players_by_rank(players, base_rank)

    # Cek apakah cukup pemain untuk membentuk dua tim
    if len(players) < 2 * team_size:
        print("Tidak cukup pemain untuk membentuk dua tim!")
        return []

    # Pembentukan kombinasi tim
    for team1 in itertools.combinations(players, team_size):
        if any(player["username"] in used_players for player in team1):
            continue

        remaining_players = [p for p in players if p not in team1]
        if len(remaining_players) < team_size:
            continue

        for team2 in itertools.combinations(remaining_players, team_size):
            if any(player["username"] in used_players for player in team2):
                continue

            score1 = calculate_team_score(team1)
            score2 = calculate_team_score(team2)
            skill_diff = abs(score1 - score2)

            results.append((team1, team2, skill_diff))
            matches_found += 1

            used_players.update(player["username"] for player in team1)
            used_players.update(player["username"] for player in team2)

            # Jika jumlah pertandingan yang ditemukan sudah mencukupi
            if matches_found >= match_count:
                elapsed_time = time.time() - start_time
                print(f"Processed {matches_found} matches in {elapsed_time:.2f} seconds")
                return results

    return results

def display_matches(matches):
    # Menampilkan hasil pertandingan
    for i, (team1, team2, skill_diff) in enumerate(matches, 1):
        print(f"\nMatch {i}:")
        print("Tim 1:")
        for player in team1:
            print(f"Name: {player['username']}, MMR: {player['mmr']}, Region: {player['region']}, Rank: {player['rank']}")
        print("\nTim 2:")
        for player in team2:
            print(f"Name: {player['username']}, MMR: {player['mmr']}, Region: {player['region']}, Rank: {player['rank']}")
        print(f"Skill Tim 1: {calculate_team_score(team1)}, Skill Tim 2: {calculate_team_score(team2)}, Selisih: {skill_diff}")

def menurank():
    # Menampilkan pilihan rank
    return ("-- MENU RANK --\nRank 1 : Iron\nRank 2 : Silver \nRank 3 : Gold\nRank 4: Platinum")

if __name__ == "__main__":
    data = load_data("dataset.csv")  # Pastikan path file CSV sesuai
    match_count = int(input("Masukkan jumlah pertandingan yang ingin dihitung: "))
    print(menurank())
    base_rank = int(input("Masukkan rank dasar untuk matchmaking (1-4): "))
    team_size = 5
    matches = backtrack_matchmaking(data, base_rank, team_size, match_count)
    display_matches(matches)
