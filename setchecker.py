import heapq
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Dict, List, Set

import psycopg2
from dotenv import load_dotenv
from psycopg2 import pool, sql

from schemas import BoosterPack, CardSet, CardStats, SheetCard

load_dotenv()

database = os.getenv("DATABASE")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")

my_logger = logging.getLogger("MyLogger")
my_logger.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(
    filename="application.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=1,  # Keep 5 backup files
)

file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# Set up the console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

my_logger.addHandler(file_handler)
my_logger.addHandler(console_handler)


connection_pool = pool.SimpleConnectionPool(
    1, 10, database=database, user=user, password=password, host=host, port=port
)


def read_deck(deck_file: str):
    """
    reads the deck file and checks for inconsistencies, Returns a list with tuples of count and card name.
    """

    assert deck_file.endswith(".txt"), "The file must be a text file (.txt)"

    if not os.path.isfile(deck_file):
        raise FileNotFoundError(f"The file {deck_file} does not exist.")

    card_data = []

    with open(deck_file, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            parts = line.split(" ", 1)

            if not parts[0].isdigit():
                raise ValueError(f"Invalid count '{parts[0]}' in line: {line}")

            count = int(parts[0])
            card_name = parts[1]

            card_data.append((count, card_name))

    return card_data


def _fetch_query(query: str, parameters=None):
    """
    Fetch query shell aiming at concurrency.
    """
    conn = connection_pool.getconn()
    cursor = conn.cursor()

    cursor.execute(sql.SQL(query), parameters)
    result = cursor.fetchall()

    cursor.close()
    connection_pool.putconn(conn)

    return result


def fetch_copies(card_name: str) -> List[CardSet]:
    """
    Fetches card data based on it's name and puts the data into an instance of the Card class
    """

    card_data = _fetch_query("SELECT * FROM cards WHERE cards.name = %s", [card_name])
    cardset_list = []
    for card in card_data:
        cardset = CardSet(
            availability=card[5].split(","),
            border_color=card[7],
            color_identity=card[9].split(",") if card[9] else [],
            colors=card[11].split(",") if card[11] else [],
            finishes=card[20].split(","),
            frame_version=card[24],
            language=card[44],
            layout=card[45],
            mana_value=card[50],
            name=card[51],
            number=card[52],
            rarity=card[21],
            set_code=card[65],
            subtypes=card[70].split(",") if card[70] else [],
            supertypes=card[71].split(",") if card[71] else [],
            type=card[74],
            types=card[75].split(","),
            uuid=card[76],
            boosters=fetch_boosters(card[65], card[76]),
            sheet_cards=fetch_sheetcards(card[65], card[76]),
        )

        cardset_list.append(cardset)

    return cardset_list


def filter_cards(cardset_list: List[CardSet], filters: Set[str]):
    """
    Removes card sets from cardset_list that match any of the filter types.
    """
    filtered_cardset_list = [
        cardset for cardset in cardset_list if not filters & set(cardset.types)
    ]
    return filtered_cardset_list


def count_sets(
    card_copies: List[CardSet],
    sets: Dict,
):
    """
    Populates a Dict with set names as keys and a count as values.
    """
    for card in card_copies:
        if card.set_code in sets:
            sets[card.set_code]["Count"] += 1
            sets[card.set_code]["Cards"].append(card)
        else:
            sets[card.set_code] = {"Count": 1, "Cards": [card]}

    return sets


def fetch_boosters(set_code: str, uuid: str):
    """
    Fetches booster types and their respective weights.
    """

    total_booster_weight = _fetch_query(
        """
        SELECT boostername, SUM(boosterweight) as total_booster_weight FROM setboostercontentweights WHERE setboostercontentweights.setcode = %s
        GROUP BY boostername
        """,
        [set_code],
    )

    booster_join = _fetch_query(
        """
        SELECT sbsc.*, sbc.boosterindex, sheetpicks, boosterweight
        FROM public.setboostersheetcards as sbsc
        LEFT JOIN setboostercontents as sbc
            ON sbc.setcode = sbsc.setcode 
                AND sbc.sheetname = sbsc.sheetname
                AND sbc.boostername = sbsc.boostername
        LEFT JOIN setboostercontentweights as sbcw
            ON sbcw.setcode = sbsc.setcode 
                AND sbcw.boostername = sbsc.boostername
                AND sbcw.boosterindex = sbc.boosterindex
        WHERE carduuid = %s AND sbsc.setcode = %s
        """,
        [uuid, set_code],
    )

    total_weight_lookup = {
        weight_row[0]: weight_row[1] for weight_row in total_booster_weight
    }

    booster_dict = {}

    for booster in booster_join:
        booster_index = booster[6]
        booster_name = booster[1]

        booster_pack = BoosterPack(
            set_code=booster[3],
            booster_name=booster_name,
            booster_index=booster_index,
            sheet_name=booster[5],
            sheet_picks=booster[7],
            booster_weight=booster[8],
        )

        if booster_pack.booster_name in booster_dict:
            booster_dict[booster_pack.booster_name]["BoosterPacks"].append(booster_pack)
        else:
            total_weight = total_weight_lookup.get(booster_name, None)
            booster_dict[booster_pack.booster_name] = {
                "TotalBoosterWeight": total_weight,
                "BoosterPacks": [booster_pack],
            }

    return booster_dict


def fetch_sheetcards(set_code: str, uuid: str):
    """
    Fetches card weight on sheet and the respective total sheet weight.
    """
    card_weights = _fetch_query(
        """
        SELECT * FROM setboostersheetcards WHERE setboostersheetcards.setcode = %s AND setboostersheetcards.carduuid = %s
        """,
        [set_code, uuid],
    )

    total_sheet_weights = _fetch_query(
        """
        SELECT setboostersheetcards.sheetname, setboostersheetcards.boostername, SUM(cardweight) as total_weight 
        FROM setboostersheetcards 
        WHERE setboostersheetcards.setcode = %s 
        GROUP BY setboostersheetcards.sheetname, setboostersheetcards.boostername
        """,
        [set_code],
    )

    weight_lookup = {
        (weight_row[0], weight_row[1]): weight_row[2]
        for weight_row in total_sheet_weights
    }

    sheet_dict = {}

    for card in card_weights:
        sheet_name = card[5]
        booster_name = card[1]

        weight = weight_lookup.get((sheet_name, booster_name), None)

        sheet_card = SheetCard(
            set_code=card[4],
            booster_name=booster_name,
            sheet_name=sheet_name,
            card_uuid=card[2],
            card_weight=card[3],
            sheet_weight=weight,
        )

        sheet_dict[(sheet_card.booster_name, sheet_card.sheet_name)] = sheet_card

    return sheet_dict


def fetch_cardstats(uuid: str, boosters, sheet):
    """
    Fetches weightings of a card based on uuid.
    """
    weight_data = _fetch_query(
        "SELECT * FROM setboostersheetcards WHERE setboostersheetcards.carduuid = %s",
        [uuid],
    )
    cardweight_list = []
    for card in weight_data:
        cardweight = CardStats(
            set_code=card[4],
            uuid=card[2],
            card_weight=card[3],
            boosters=boosters,
            sheet=sheet,
        )

        cardweight_list.append(cardweight)

    return cardweight_list


def main(file_path):
    deck_data = read_deck(file_path)
    set_counts = {}
    for card in deck_data:
        _, card_name = card
        copies = fetch_copies(card_name)
        filtered_copies = filter_cards(copies, {"Land"})
        count_sets(filtered_copies, set_counts)

    sorted_set_counts = heapq.nlargest(
        10, set_counts.items(), key=lambda item: item[1]["Count"]
    )

    for set_code, value in sorted_set_counts:
        print(f"{set_code}: {value['Count']}")
        for card in value.get("Cards", []):
            print(f" - {card.name} - {card.finishes} - {card.border_color}")
            print(f" - {card.uuid}")
            for _, sheet_card in card.sheet_cards.items():
                print(
                    f"    - sheet name: {sheet_card.sheet_name} \n      - card weight: {sheet_card.card_weight} \n      - sheet weight: {sheet_card.sheet_weight} \n"
                )
            for booster_name, booster_details in card.boosters.items():
                print(f"    * Booster Name: {booster_name}")
                print(
                    f"      Total Booster Weight: {booster_details.get('TotalBoosterWeight', 'N/A')}"
                )
                for booster_pack in booster_details.get("BoosterPacks", []):
                    print(f"       - Booster Index: {booster_pack.booster_index}")
                    print(f"       - Sheet Name: {booster_pack.sheet_name}")
                    print(f"       - Sheet Picks: {booster_pack.sheet_picks}")
                    print(f"       - Booster Weight: {booster_pack.booster_weight} \n")


if __name__ == "__main__":
    main("example_deck.txt")
