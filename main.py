from bs4 import BeautifulSoup
import requests
import time


foxsports_url = "https://www.foxsports.com"


def main():
    instruction_message = """This program can do one of three things:
    1) Print all WWC 2023 replays.
    2) Search for a specific WWC 2023 replay between two teams.
    3) Repeatedly search site for a specific WWC 2023 replay.
    """
    possible_commands = ["1", "2", "3", "q", "Q"]
    command = ""
    while command not in possible_commands:
        print(instruction_message)
        command = input(
            "Enter which task you'd like to do (1, 2, or 3), or Q to quit: ")

    if command == "Q" or command == "q":
        exit(0)
    if command == "1":
        print("Printing all WWC 2023 replays:\n")
        for replay in get_wwc2023_replays():
            print(replay["title"])
            print(replay["url"])
            print()
    elif command == "2":
        print("Will search for a game between the teams you specify.")
        team1 = input("Team 1: ")
        team2 = input("Team 2: ")
        check_for_replay(team1, team2)
    elif command == "3":
        print(
            "Will repeatedly search for a game between the teams you specify.")
        team1 = input("Team 1: ")
        team2 = input("Team 2: ")

        retry_minutes = 10
        retry_minutes_input = input("Wait (in minutes) between retries: ")
        try:
            retry_minutes = max(float(retry_minutes_input), 0)
        except ValueError:
            print(f"Could not convert {retry_minutes_input} to a number.")

        max_retries = float("inf")
        max_retries_input = input("Max retries: ")
        try:
            max_retries = max(float(max_retries_input), 0)
        except ValueError:
            print(f"Could not convert {retry_minutes_input} to a number.")

        check_until_posted(team1, team2, retry_minutes, max_retries)


def check_until_posted(
        team1,
        team2,
        retry_minutes=10,
        max_retries=float("inf")):
    print(f"Checking for games between {team1} and {team2} "
          f"every {retry_minutes} minutes until game is found or maximum "
          f"of {max_retries} retries is reached.")
    retry_count = 0
    if check_for_replay(team1, team2):
        exit(0)
    while retry_count < max_retries:
        print(f"Retrying in {retry_minutes} minutes...")
        time.sleep(retry_minutes * 60)
        if check_for_replay(team1, team2):
            exit(0)
        retry_count += 1
    print(f"\nReached retry limit of {max_retries} retries.")


def check_for_replay(team1, team2):
    print(f"Checking for games between {team1} and {team2}...")
    wwc2023_replays = get_wwc2023_replays()
    team1 = team1.lower()
    team2 = team2.lower()
    for replay in wwc2023_replays:
        if (team1 in replay["title"].lower()
                and team2 in replay["title"].lower()):
            print("FOUND GAME!!!")
            print(replay["title"])
            print(replay["url"])
            print()
            return True
    print(f"No games found between {team1} and {team2}.")
    return False


def get_wwc2023_replays():
    wwc2023_replays = []

    all_replays = get_fox_replays()

    for replay in all_replays:
        links = replay.find_all("a")
        for link in links:
            title = link.find("h3")
            if title and "2023 FIFA Women's World Cup" in title.text:
                wwc2023_replays.append({
                    "title": link.find("h3").text,
                    "url": foxsports_url + str(link["href"])
                })

    return wwc2023_replays


def get_fox_replays():
    fox_replays_html = requests.get(foxsports_url + "/replays").text
    fox_replays_soup = BeautifulSoup(fox_replays_html, "lxml")

    return fox_replays_soup.find(
        "div", class_="highlight-feed-container").find_all(
        "div", class_="mg-t-25")


if __name__ == "__main__":
    main()
