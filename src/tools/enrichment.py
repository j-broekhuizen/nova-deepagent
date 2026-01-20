"""Transaction enrichment tool."""

from langchain_core.tools import tool

from nova.models.transaction import TransactionCategory


# Merchant mapping for enrichment
MERCHANT_MAPPINGS: dict[str, tuple[str, TransactionCategory]] = {
    # Coffee
    "starbucks": ("Starbucks", TransactionCategory.COFFEE),
    "dunkin": ("Dunkin'", TransactionCategory.COFFEE),
    "peet's": ("Peet's Coffee", TransactionCategory.COFFEE),
    "peets": ("Peet's Coffee", TransactionCategory.COFFEE),
    "blue bottle": ("Blue Bottle Coffee", TransactionCategory.COFFEE),
    "philz": ("Philz Coffee", TransactionCategory.COFFEE),
    # Fast food
    "mcdonald's": ("McDonald's", TransactionCategory.FAST_FOOD),
    "mcdonalds": ("McDonald's", TransactionCategory.FAST_FOOD),
    "burger king": ("Burger King", TransactionCategory.FAST_FOOD),
    "wendy's": ("Wendy's", TransactionCategory.FAST_FOOD),
    "wendys": ("Wendy's", TransactionCategory.FAST_FOOD),
    "taco bell": ("Taco Bell", TransactionCategory.FAST_FOOD),
    "chick-fil-a": ("Chick-fil-A", TransactionCategory.FAST_FOOD),
    "chickfila": ("Chick-fil-A", TransactionCategory.FAST_FOOD),
    "chipotle": ("Chipotle", TransactionCategory.FAST_FOOD),
    "five guys": ("Five Guys", TransactionCategory.FAST_FOOD),
    "in-n-out": ("In-N-Out", TransactionCategory.FAST_FOOD),
    "shake shack": ("Shake Shack", TransactionCategory.FAST_FOOD),
    # Delivery
    "uber eats": ("Uber Eats", TransactionCategory.DELIVERY),
    "ubereats": ("Uber Eats", TransactionCategory.DELIVERY),
    "doordash": ("DoorDash", TransactionCategory.DELIVERY),
    "grubhub": ("Grubhub", TransactionCategory.DELIVERY),
    "postmates": ("Postmates", TransactionCategory.DELIVERY),
    "seamless": ("Seamless", TransactionCategory.DELIVERY),
    "instacart": ("Instacart", TransactionCategory.DELIVERY),
    # Dining
    "restaurant": ("Restaurant", TransactionCategory.DINING),
    "cafe": ("Cafe", TransactionCategory.DINING),
    "bar": ("Bar", TransactionCategory.DINING),
    "grill": ("Grill", TransactionCategory.DINING),
    "bistro": ("Bistro", TransactionCategory.DINING),
    # Transportation
    "uber": ("Uber", TransactionCategory.TRANSPORTATION),
    "lyft": ("Lyft", TransactionCategory.TRANSPORTATION),
    "shell": ("Shell", TransactionCategory.TRANSPORTATION),
    "chevron": ("Chevron", TransactionCategory.TRANSPORTATION),
    "exxon": ("Exxon", TransactionCategory.TRANSPORTATION),
    "mobil": ("Mobil", TransactionCategory.TRANSPORTATION),
    "bp": ("BP", TransactionCategory.TRANSPORTATION),
    "arco": ("Arco", TransactionCategory.TRANSPORTATION),
    # Subscriptions
    "netflix": ("Netflix", TransactionCategory.SUBSCRIPTION),
    "spotify": ("Spotify", TransactionCategory.SUBSCRIPTION),
    "hulu": ("Hulu", TransactionCategory.SUBSCRIPTION),
    "disney+": ("Disney+", TransactionCategory.SUBSCRIPTION),
    "amazon prime": ("Amazon Prime", TransactionCategory.SUBSCRIPTION),
    "apple": ("Apple", TransactionCategory.SUBSCRIPTION),
    "hbo max": ("HBO Max", TransactionCategory.SUBSCRIPTION),
    "youtube": ("YouTube Premium", TransactionCategory.SUBSCRIPTION),
    # Shopping
    "amazon": ("Amazon", TransactionCategory.SHOPPING),
    "target": ("Target", TransactionCategory.SHOPPING),
    "walmart": ("Walmart", TransactionCategory.SHOPPING),
    "costco": ("Costco", TransactionCategory.GROCERIES),
    "best buy": ("Best Buy", TransactionCategory.SHOPPING),
    "home depot": ("Home Depot", TransactionCategory.SHOPPING),
    "lowes": ("Lowe's", TransactionCategory.SHOPPING),
    # Groceries
    "whole foods": ("Whole Foods", TransactionCategory.GROCERIES),
    "trader joe": ("Trader Joe's", TransactionCategory.GROCERIES),
    "safeway": ("Safeway", TransactionCategory.GROCERIES),
    "kroger": ("Kroger", TransactionCategory.GROCERIES),
    "publix": ("Publix", TransactionCategory.GROCERIES),
    "aldi": ("Aldi", TransactionCategory.GROCERIES),
    "sprouts": ("Sprouts", TransactionCategory.GROCERIES),
    # Entertainment
    "amc": ("AMC Theatres", TransactionCategory.ENTERTAINMENT),
    "regal": ("Regal Cinemas", TransactionCategory.ENTERTAINMENT),
    "cinemark": ("Cinemark", TransactionCategory.ENTERTAINMENT),
    "ticketmaster": ("Ticketmaster", TransactionCategory.ENTERTAINMENT),
    "stubhub": ("StubHub", TransactionCategory.ENTERTAINMENT),
}


@tool
def enrich_transaction(raw_description: str) -> dict:
    """Enrich a transaction with merchant info and category.

    Takes a raw transaction description and returns normalized merchant name,
    category, and confidence level.

    Args:
        raw_description: The raw merchant description from the transaction
            (e.g., "STARBUCKS #12345 SAN FRANCISCO CA").

    Returns:
        Enriched merchant information with normalized name and category.
    """
    description_lower = raw_description.lower()

    # Check for known merchants
    for keyword, (name, category) in MERCHANT_MAPPINGS.items():
        if keyword in description_lower:
            # Higher confidence if keyword is at the start
            words = description_lower.split()
            confidence = "high" if words and keyword in words[0] else "medium"

            return {
                "normalized_name": name,
                "category": category.value,
                "original_description": raw_description,
                "confidence": confidence,
            }

    # Default fallback - try to clean up the description
    # Remove common suffixes and numbers
    cleaned = raw_description.split("#")[0].strip()
    cleaned = " ".join(word for word in cleaned.split() if not word.isdigit())

    return {
        "normalized_name": cleaned.title() if cleaned else raw_description,
        "category": TransactionCategory.OTHER.value,
        "original_description": raw_description,
        "confidence": "low",
    }
