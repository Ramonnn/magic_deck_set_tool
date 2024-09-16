data[["Count", "Card_Name"]] = data["bulk"].str.extract(RGX_PATTERN)

json_responses = []


def insert_card(card_name):
    try:
        cur.execute(
            sql.SQL(
                """WITH existing AS 
                (SELECT card_id FROM Cards WHERE card_name = %s) 
                INSERT INTO Cards (card_name) 
                SELECT %s 
                WHERE NOT EXISTS (SELECT 1 FROM existing)
                RETURNING card_id;"""
            ),
            [card_name, card_name],
        )
        result = cur.fetchone()
        if result:
            return result[0]
        logging.info(f"Card '{card_name}' was not inserted, likely due to a conflict.")
        return get_card_id(card_name)
    except Exception as e:
        logging.error(f"Error inserting card '{card_name}': {e}")
        raise


def insert_set(set_name):
    try:
        cur.execute(
            sql.SQL(
                """WITH existing AS 
                (SELECT set_id FROM Sets WHERE set_name = %s) 
                INSERT INTO Sets (set_name) 
                SELECT %s 
                WHERE NOT EXISTS (SELECT 1 FROM existing)
                RETURNING set_id;"""
            ),
            [set_name, set_name],
        )
        result = cur.fetchone()
        if result:
            return result[0]  # Extract the card_id
        logging.info(f"Set '{set_name}' was not inserted, likely due to a conflict.")
        return get_set_id(set_name)
    except Exception as e:
        logging.error(f"Error inserting set '{set_name}': {e}")
        raise


def insert_rarity(rarity_name):
    try:
        cur.execute(
            sql.SQL(
                """WITH existing AS 
                (SELECT rarity_id FROM Rarities WHERE rarity_name = %s) 
                INSERT INTO Rarities (rarity_name) 
                SELECT %s 
                WHERE NOT EXISTS (SELECT 1 FROM existing)
                RETURNING rarity_id;"""
            ),
            [rarity_name, rarity_name],
        )
        result = cur.fetchone()
        if result:
            return result[0]  # Extract the card_id
        logging.info(
            f"Rarity '{rarity_name}' was not inserted, likely due to a conflict."
        )
        return get_rarity_id(rarity_name)
    except Exception as e:
        logging.error(f"Error inserting rarity'{rarity_name}': {e}")
        raise


def insert_foil(foil, foil_type):
    try:
        cur.execute(
            sql.SQL(
                """WITH existing AS 
                (SELECT foil_id FROM Foil WHERE foil = %s AND foil_type = %s) 
                INSERT INTO Foil (foil, foil_type) 
                SELECT %s, %s::jsonb 
                WHERE NOT EXISTS (SELECT 1 FROM existing)
                RETURNING foil_id;"""
            ),
            [foil, foil_type, foil, foil_type],
        )
        result = cur.fetchone()
        if result:
            return result[0]  # Extract the card_id
        logging.info(f"Foil '{foil_type}' was not inserted, likely due to a conflict.")
        return get_foil_id(foil, foil_type)
    except Exception as e:
        logging.error(f"Error inserting foil type'{foil_type}': {e}")
        raise


def insert_card_code(card_code):
    try:
        cur.execute(
            sql.SQL(
                """WITH existing AS 
                (SELECT card_code_id FROM CardCode WHERE card_code = %s) 
                INSERT INTO CardCode (card_code) 
                SELECT %s
                WHERE NOT EXISTS (SELECT 1 FROM existing)
                RETURNING card_code_id;"""
            ),
            [card_code, card_code],
        )
        result = cur.fetchone()
        if result:
            return result[0]  # Extract the card_id
        logging.info(
            f"Card code '{card_code}' was not inserted, likely due to a conflict."
        )
        return get_card_code_id(card_code)
    except Exception as e:
        logging.error(f"Error inserting card code'{card_code}': {e}")
        raise


def insert_card_type(card_type):
    try:
        cur.execute(
            sql.SQL(
                """WITH existing AS 
                (SELECT card_type_id FROM CardType WHERE card_type = %s) 
                INSERT INTO CardType (card_type) 
                SELECT %s
                WHERE NOT EXISTS (SELECT 1 FROM existing)
                RETURNING card_type_id;"""
            ),
            [card_type, card_type],
        )
        result = cur.fetchone()
        if result:
            return result[0]  # Extract the card_id
        logging.info(
            f"Card type '{card_type}' was not inserted, likely due to a conflict."
        )
        return get_card_type_id(card_type)
    except Exception as e:
        logging.error(f"Error inserting card code'{card_type}': {e}")
        raise


def insert_card_set(card_id, set_id, rarity_id, foil_id, card_code_id, card_type_id):
    try:
        logging.info(
            f"Inserting into CardSets: card_id={card_id}, set_id={set_id}, rarity_id={rarity_id}, card_code_id={card_code_id}, card_type_id={card_type_id}"
        )
        cur.execute(
            sql.SQL(
                """WITH existing AS
                (SELECT card_id, set_id, rarity_id, foil_id, card_code_id, card_type_id FROM CardSets 
                WHERE card_id = %s AND set_id = %s AND rarity_id = %s AND foil_id = %s AND card_code_id = %s AND card_type_id = %s)
                INSERT INTO CardSets (card_id, set_id, rarity_id, foil_id, card_code_id, card_type_id)
                SELECT %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (SELECT 1 FROM existing)
                RETURNING id;"""
            ),
            [
                card_id,
                set_id,
                rarity_id,
                foil_id,
                card_code_id,
                card_type_id,
                card_id,
                set_id,
                rarity_id,
                foil_id,
                card_code_id,
                card_type_id,
            ],
        )

        if cur.rowcount == 0:
            logging.warning(
                f"Insert skipped due to conflict: card_id={card_id}, set_id={set_id}, rarity={rarity_id}, foil={foil_id}, card_code={card_code_id}, card_type={card_type_id}"
            )
    except Exception as e:
        logging.error(f"Error inserting a card set for card '{card_type_id}': {e}")
        raise


def get_card_id(card_name):
    cur.execute(
        sql.SQL("SELECT card_id FROM Cards WHERE card_name = %s"),
        [card_name],
    )
    result = cur.fetchone()
    return result[0] if result else None


def get_set_id(set_name):
    cur.execute(
        sql.SQL("SELECT set_id FROM Sets WHERE set_name = %s"),
        [set_name],
    )
    result = cur.fetchone()
    return result[0] if result else None


def get_rarity_id(rarity_name):
    cur.execute(
        sql.SQL("SELECT rarity_id FROM Rarities WHERE rarity_name = %s"),
        [rarity_name],
    )
    result = cur.fetchone()
    return result[0] if result else None


def get_foil_id(foil, foil_type):
    cur.execute(
        sql.SQL("SELECT foil_id FROM Foil WHERE foil = %s AND foil_type = %s"),
        [foil, foil_type],
    )
    result = cur.fetchone()
    return result[0] if result else None


def get_card_code_id(card_code):
    cur.execute(
        sql.SQL("SELECT card_code_id FROM CardCode WHERE card_code = %s"),
        [card_code],
    )
    result = cur.fetchone()
    return result[0] if result else None


def get_card_type_id(card_type):
    cur.execute(
        sql.SQL("SELECT card_type_id FROM CardType WHERE card_type = %s"),
        [card_type],
    )
    result = cur.fetchone()
    return result[0] if result else None


def get_card_name(card_name):
    cur.execute(
        sql.SQL("SELECT card_name FROM Cards WHERE card_name = %s"),
        [card_name],
    )
    result = cur.fetchone()
    return result[0] if result else None


def get_card_sets(card_name):
    cur.execute(
        sql.SQL(
            """
            SELECT set_name 
            FROM CardSets 
            LEFT JOIN Sets ON CardSets.set_id = Sets.set_id
            LEFT JOIN Cards ON CardSets.card_id = Cards.card_id
            WHERE card_name = %s
            """
        ),
        [card_name],
    )
    results = cur.fetchall()

    if results:
        print(f"Card sets for '{card_name}': {results}")
        return [result[0] for result in results]
    else:
        print(f"No card sets found for '{card_name}'")
        return None


def get_sets(card_name):
    # base_url = "https://api.scryfall.com/cards/named"
    # params = {"fuzzy": card_name}

    card_name_perc_enc = card_name.replace(" ", "%21")
    base_url = (
        f"https://api.scryfall.com/cards/search?q=%21{card_name_perc_enc}&unique=prints"
    )
    response = None

    try:
        response = requests.get(base_url, timeout=5)
        response.raise_for_status()
        print(response.url)
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for {card_name}: {e}")
        return None

    except ValueError as e:
        if response is not None:
            logging.error(
                f"Error parsing JSON for {card_name}. Response: {response.text}. Error: {e}"
            )
        else:
            logging.error(f"Error parsing JSON for {card_name}. Error: {e}")
        return None


def process_card(
    card_name, set_name, rarity_name, foil, foil_type, card_code, card_type
):
    card_id = insert_card(card_name)
    set_id = insert_set(set_name)
    rarity_id = insert_rarity(rarity_name)
    foil_id = insert_foil(foil, foil_type)
    card_code_id = insert_card_code(card_code)
    card_type_id = insert_card_type(card_type)

    if card_id and set_id and rarity_id and foil_id and card_code_id and card_type_id:
        insert_card_set(card_id, set_id, rarity_id, foil_id, card_code_id, card_type_id)
    else:
        logging.error(
            f"Failed to process card: {card_name}. Missing ID(s): "
            f"card_id={card_id}, set_id={set_id}, rarity_id={rarity_id}, foil_id={foil_id}, card_code_id={card_code_id}, card_type_id={card_type_id}"
        )


def process_card_data(card_name):
    print(f"Processing card: {card_name}")

    card_variants = get_sets(card_name)

    if card_variants and "data" in card_variants:
        for variant in card_variants.get("data", []):
            card_name = variant.get("name")
            set_name = variant.get("set_name")
            rarity = variant.get("rarity")
            foil = variant.get("foil", False)
            foil_type = variant.get("finishes", [])
            card_code = variant.get("collector_number")
            card_type = variant.get("type_line")

            if not foil_type:
                foil_type = None
                foil = None
            else:
                foil = "foil" in foil_type

            foil_type_json = extras.Json(foil_type) if foil_type else None

            if card_name and set_name and rarity and card_code and card_type:
                process_card(
                    card_name,
                    set_name,
                    rarity,
                    foil,
                    foil_type_json,
                    card_code,
                    card_type,
                )
            else:
                my_logger.error(f"Invalid variant data for {card_name}: {variant}")
    else:
        my_logger.error(f"No valid data found for {card_name}")

    time.sleep(1)


def parse_deck(file_path):
    deck = {}
    with open(file_path, "r") as f:
        for line in f:
            if line.strip():
                quantity, card_name = line.split(maxsplit=1)
                deck[card_name.strip()] = int(quantity)
    print(f"Parsed deck: {deck}")
    return deck


def get_set_data(deck):
    card_set_map = {}
    for card_name in deck:
        if get_card_name(card_name) is None:
            process_card_data(card_name)
            time.sleep(1)  # To avoid hitting rate limits on Scryfall

        card_set_map[card_name] = get_card_sets(card_name)

    return card_set_map


def filter_card_type(card_type, card_set_map):
    filtered_card_set_map = card_set_map.copy()
    for card_name in list(filtered_card_set_map.keys()):
        card_type_like = f"%{card_type}%"
        cur.execute(
            sql.SQL(
                """
                SELECT * FROM CardSets
                LEFT JOIN CardType ON CardType.card_type_id = CardSets.card_type_id
                LEFT JOIN Cards ON CardSets.card_id = Cards.card_id
                WHERE CardType.card_type LIKE %s AND Cards.card_name = %s
                """
            ),
            [card_type_like, card_name],
        )
        result = cur.fetchone()

        if result:
            filtered_card_set_map.pop(card_name)

    return filtered_card_set_map


def calculate_set_distribution(deck, card_set_map):
    set_distribution = {}
    for card_name, sets in card_set_map.items():
        print(f"Calculating set distribution for '{card_name}': {sets}")
        if sets:
            for set_name in sets:
                if set_name not in set_distribution:
                    set_distribution[set_name] = 0
                set_distribution[set_name] += deck[
                    card_name
                ]  # adds the number of cards of that card to the set count
    print(f"Set distribution: {set_distribution}")
    return set_distribution


def recommend_sets(set_distribution):
    sorted_sets = sorted(set_distribution.items(), key=lambda x: x[1], reverse=True)
    return sorted_sets

    # deck = parse_deck(file_path)
    # card_set_map = get_set_data(deck)
    # filtered_card_set_map = filter_card_type("land", card_set_map)
    # set_distribution = calculate_set_distribution(deck, filtered_card_set_map)
    # recommendations = recommend_sets(set_distribution)

    # print("Recommended Sets to Purchase:")
    # for set_name, count in recommendations:
    #    print(f"{set_name}: {count} cards")


conn.commit()
cur.close()
conn.close()
