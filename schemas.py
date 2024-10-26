from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ForeignData:
    language: str
    name: str
    faceName: Optional[str] = None
    flavorText: Optional[str] = None
    multiverseId: Optional[int] = None
    text: Optional[str] = None
    type: Optional[str] = None


@dataclass
class Identifiers:
    card_kingdom_id: str
    scryfall_id: str
    card_kingdom_etched_id: Optional[str] = None
    card_kingdom_foil_id: Optional[str] = None
    cardsphere_id: Optional[str] = None
    cardsphere_foil_id: Optional[str] = None
    mcm_id: Optional[str] = None
    mcm_meta_id: Optional[str] = None
    mtg_arena_id: Optional[str] = None
    mtgjson_foil_version_id: Optional[str] = None
    mtgjson_non_foil_version_id: Optional[str] = None
    mtgjson_v4_id: Optional[str] = None
    mtgo_foil_id: Optional[str] = None
    mtgo_id: Optional[str] = None
    multiverse_id: Optional[str] = None
    scryfall_card_back_id: Optional[str] = None
    scryfall_oracle_id: Optional[str] = None
    scryfall_illustration_id: Optional[str] = None
    tcgplayer_product_id: Optional[str] = None
    tcgplayer_etched_product_id: Optional[str] = None


@dataclass
class LeadershipSkills:
    brawl: bool
    commander: bool
    oathbreaker: bool


@dataclass
class Legalities:
    alchemy: Optional[str] = None
    brawl: Optional[str] = None
    commander: Optional[str] = None
    duel: Optional[str] = None
    explorer: Optional[str] = None
    future: Optional[str] = None
    gladiator: Optional[str] = None
    historic: Optional[str] = None
    historicbrawl: Optional[str] = None
    legacy: Optional[str] = None
    modern: Optional[str] = None
    oathbreaker: Optional[str] = None
    oldschool: Optional[str] = None
    pauper: Optional[str] = None
    paupercommander: Optional[str] = None
    penny: Optional[str] = None
    pioneer: Optional[str] = None
    predh: Optional[str] = None
    premodern: Optional[str] = None
    standard: Optional[str] = None
    standardbrawl: Optional[str] = None
    timeless: Optional[str] = None
    vintage: Optional[str] = None


@dataclass
class PurchaseUrls:
    card_kingdom: Optional[str] = None
    card_kingdom_etched: Optional[str] = None
    card_kingdom_foil: Optional[str] = None
    cardmarket: Optional[str] = None
    tcgplayer: Optional[str] = None
    tcgplayer_etched: Optional[str] = None


@dataclass
class RelatedCards:
    reverseRelated: Optional[List[str]]
    spellbook: Optional[List[str]]


@dataclass
class Rulings:
    date: str
    text: str


@dataclass
class SourceProducts:
    foil: List[str]
    nonfoil: List[str]


@dataclass
class Translations:
    ancient_greek: Optional[str] = None
    arabic: Optional[str] = None
    chinese_simplified: Optional[str] = None
    chinese_traditional: Optional[str] = None
    french: Optional[str] = None
    german: Optional[str] = None
    hebrew: Optional[str] = None
    italian: Optional[str] = None
    japanese: Optional[str] = None
    korean: Optional[str] = None
    latin: Optional[str] = None
    phyrexian: Optional[str] = None
    portuguese_brazil: Optional[str] = None
    russian: Optional[str] = None
    sanskrit: Optional[str] = None
    spanish: Optional[str] = None


@dataclass
class BoosterPack:
    set_code: str
    booster_name: str
    booster_index: int
    booster_weight: int
    sheet_name: str
    sheet_picks: str
    booster_weight_ratio: Optional = None


@dataclass
class SheetCard:
    set_code: str
    booster_name: str
    card_uuid: str
    card_weight: int
    sheet_name: str
    sheet_weight: str


@dataclass
class CardSheet:
    foil: bool
    total_weight: int


@dataclass
class CardStats:
    uuid: str
    set_code: str
    boosters: List[BoosterPack]
    sheet: CardSheet
    card_weight: int  # on sheet


@dataclass
class CardSet:
    availability: List[str]
    border_color: str
    color_identity: List[str]
    colors: List[str]
    finishes: List[str]
    frame_version: str
    language: str
    layout: str
    mana_value: float
    name: str
    number: str
    rarity: str
    set_code: str
    subtypes: List[str]
    supertypes: List[str]
    type: str
    types: List[str]
    uuid: str
    boosters: Dict
    sheet_cards: Dict
    artist: Optional[str] = None
    artist_ids: Optional[List[str]] = None
    ascii_name: Optional[str] = None
    attraction_lights: Optional[List[int]] = None
    booster_types: Optional[List[str]] = None
    card_parts: Optional[List[str]] = None
    color_indicator: Optional[List[str]] = None
    defense: Optional[str] = None
    duel_deck: Optional[str] = None
    edhrec_rank: Optional[int] = None
    edhrec_saltiness: Optional[int] = None
    face_flavor_name: Optional[str] = None
    face_mana_value: Optional[float] = None
    face_name: Optional[str] = None
    flavor_name: Optional[str] = None
    flavor_text: Optional[str] = None
    foreign_data: Optional[List] = None
    frame_effects: Optional[List[str]] = None
    hand: Optional[str] = None
    has_alternative_deck_limit: Optional[bool] = None
    has_content_warning: Optional[bool] = None
    is_alternative: Optional[bool] = None
    is_full_art: Optional[bool] = None
    is_funny: Optional[bool] = None
    is_online_only: Optional[bool] = None
    is_oversized: Optional[bool] = None
    is_promo: Optional[bool] = None
    is_rebalanced: Optional[bool] = None
    is_reprint: Optional[bool] = None
    is_reserved: Optional[bool] = None
    is_story_spotlight: Optional[bool] = None
    is_textless: Optional[bool] = None
    is_timeshifted: Optional[bool] = None
    keywords: Optional[List[str]] = None
    life: Optional[str] = None
    loyalty: Optional[str] = None
    mana_cost: Optional[str] = None
    original_printings: Optional[List[str]] = None
    original_release_date: Optional[str] = None
    original_text: Optional[str] = None
    original_type: Optional[str] = None
    other_face_ids: Optional[List[str]] = None
    power: Optional[str] = None
    printings: Optional[List[str]] = None
    promo_types: Optional[List[str]] = None
    rebalanced_printings: Optional[List[str]] = None
    rulings: Optional[List] = None
    security_stamp: Optional[str] = None
    side: Optional[str] = None
    signature: Optional[str] = None
    subsets: Optional[List[str]] = None
    text: Optional[str] = None
    toughness: Optional[str] = None
    variations: Optional[List[str]] = None
    watermark: Optional[str] = None


@dataclass
class CardToken:
    availability: List[str]
    border_color: str
    color_identity: List[str]
    colors: List[str]
    finishes: List[str]
    frame_version: str
    has_foil: bool
    has_non_foil: bool
    identifiers: Identifiers
    language: str
    layout: str
    name: str
    number: str
    set_code: str
    subtypes: List[str]
    supertypes: List[str]
    type: str
    types: List[str]
    uuid: str
    artist: Optional[str] = None
    artist_ids: Optional[List[str]] = None
    ascii_name: Optional[str] = None
    booster_types: Optional[List[str]] = None
    card_parts: Optional[List[str]] = None
    color_indicator: Optional[List[str]] = None
    face_name: Optional[str] = None
    face_flavor_name: Optional[str] = None
    flavor_text: Optional[str] = None
    frame_effects: Optional[List[str]] = None
    is_full_art: Optional[bool] = None
    is_funny: Optional[bool] = None
    is_online_only: Optional[bool] = None
    is_promo: Optional[bool] = None
    is_reprint: Optional[bool] = None
    is_textless: Optional[bool] = None
    keywords: Optional[List[str]] = None
    loyalty: Optional[str] = None
    orientation: Optional[str] = None
    original_text: Optional[str] = None
    original_type: Optional[str] = None
    other_face_ids: Optional[List[str]] = None
    power: Optional[str] = None
    promo_types: Optional[List[str]] = None
    related_cards: Optional[RelatedCards] = None
    reverse_related: Optional[List[str]] = None
    security_stamp: Optional[str] = None
    side: Optional[str] = None
    signature: Optional[str] = None
    source_products: Optional[List[str]] = None
    subsets: Optional[List[str]] = None
    text: Optional[str] = None
    toughness: Optional[str] = None
    watermark: Optional[str] = None


@dataclass
class CardSetDeck:
    count: int
    uuid: str
    is_foil: Optional[bool] = None


@dataclass
class DeckSet:
    code: str
    main_board: List[CardSetDeck]
    name: str
    type: str
    side_board: List[CardSetDeck]
    release_date: Optional[str] = None
    sealed_product_uuids: Optional[List[str]] = None
    commander: Optional[List[CardSetDeck]] = None


@dataclass
class SealedProductCard:
    name: str
    number: str
    set: str
    uuid: str
    foil: Optional[bool] = None


@dataclass
class SealedProductDeck:
    name: str
    set: str


@dataclass
class SealedProductOther:
    name: str


@dataclass
class SealedProductPack:
    code: str
    set: str


@dataclass
class SealedProductSealed:
    count: int
    name: str
    set: str
    uuid: str


@dataclass
class SealedProductContents:
    card: Optional[List[SealedProductCard]] = None
    deck: Optional[List[SealedProductDeck]] = None
    other: Optional[List[SealedProductOther]] = None
    pack: Optional[List[SealedProductPack]] = None
    sealed: Optional[List[SealedProductSealed]] = None


@dataclass
class SealedProduct:
    identifiers: Identifiers
    name: str
    purchase_urls: PurchaseUrls
    uuid: str
    subtype: Optional[str] = None  # Can be a string or None
    card_count: Optional[int] = None
    category: Optional[str] = None
    contents: Optional[SealedProductContents] = None
    product_size: Optional[int] = None
    release_date: Optional[str] = None


@dataclass
class Set:
    base_set_size: int
    cards: List[CardSet]
    code: str
    is_foil_only: bool
    is_online_only: bool
    keyrune_code: str
    name: str
    release_date: str
    tokens: List[CardToken]
    total_set_size: int
    translations: Translations
    type: str
    block: Optional[str] = None
    cardsphere_set_id: Optional[int] = None
    code_v3: Optional[str] = None
    decks: Optional[List[DeckSet]] = None
    is_foreign_only: Optional[bool] = None
    is_non_foil_only: Optional[bool] = None
    is_paper_only: Optional[bool] = None
    is_partial_preview: Optional[bool] = None
    languages: Optional[List[str]] = None
    mcm_id: Optional[int] = None
    mcm_id_extras: Optional[int] = None
    mcm_name: Optional[str] = None
    mtgo_code: Optional[str] = None
    parent_code: Optional[str] = None
    sealed_product: Optional[List[SealedProduct]] = None
    tcgplayer_group_id: Optional[int] = None
    token_set_code: Optional[str] = None
