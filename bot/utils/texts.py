WELCOME = (
    "Welcome to our shop! 🛍\n\n"
    "Browse our catalog, add items to your cart, and place orders — all right here.\n\n"
    "Use the menu below or type /help for available commands."
)

HELP = (
    "Available commands:\n\n"
    "/start — Main menu\n"
    "/catalog — Browse products\n"
    "/search — Search products by name\n"
    "/cart — View your cart\n"
    "/orders — Order history\n"
    "/help — This message"
)

CATALOG_EMPTY = "The catalog is empty. Check back later!"
CATEGORIES_TITLE = "Choose a category:"
PRODUCTS_TITLE = "Products in {category}:"
PRODUCT_NOT_FOUND = "Product not found."
CATEGORY_NOT_FOUND = "Category not found."

PRODUCT_CARD = (
    "<b>{name}</b>\n\n"
    "{description}\n\n"
    "💰 Price: <b>${price:.2f}</b>\n"
    "📦 {stock_status}"
)

IN_STOCK = "In stock"
OUT_OF_STOCK = "Out of stock"

ADDED_TO_CART = "✅ {product} added to cart!"
ALREADY_OUT_OF_STOCK = "Sorry, this product is out of stock."

CART_EMPTY = "Your cart is empty.\n\nBrowse /catalog to find something!"
CART_TITLE = "🛒 Your cart:\n\n"
CART_ITEM = "{i}. {name} — ${price:.2f} x {qty} = ${subtotal:.2f}\n"
CART_TOTAL = "\n<b>Total: ${total:.2f}</b>"
ITEM_REMOVED = "Item removed from cart."
QUANTITY_UPDATED = "Quantity updated."

ORDER_CREATED = (
    "✅ Order #{order_id} has been placed!\n\n"
    "Total: <b>${total:.2f}</b>\n"
    "Status: {status}\n\n"
    "Thank you for your order!"
)
ORDER_EMPTY_CART = "Your cart is empty. Add some products first!"
NO_ORDERS = "You have no orders yet."
ORDER_HISTORY_TITLE = "Your orders:\n\n"
ORDER_ITEM_LINE = "  • {name} x{qty} — ${subtotal:.2f}\n"
ORDER_SUMMARY = (
    "📦 <b>Order #{order_id}</b> — {date}\n"
    "Status: {status}\n"
    "{items}"
    "Total: <b>${total:.2f}</b>\n\n"
)

CONFIRM_ORDER = "Place your order?\n\nTotal: <b>${total:.2f}</b>"

SEARCH_PROMPT = "Send me a product name to search for:"
SEARCH_NO_RESULTS = "Nothing found for \"{query}\". Try a different search term."
SEARCH_RESULTS = "Found {count} product(s) for \"{query}\":"
SEARCH_TOO_SHORT = "Please enter at least 2 characters."

# Admin texts
ADMIN_PANEL = "Admin panel. Choose an action:"
ADMIN_ONLY = "This section is for admins only."
ADMIN_ADD_CATEGORY = "Enter the category name:"
ADMIN_CATEGORY_ADDED = "✅ Category '{name}' added."
ADMIN_DELETE_CATEGORY = "Choose a category to delete:"
ADMIN_CATEGORY_DELETED = "Category deleted."
ADMIN_SELECT_CATEGORY = "Select a category for the new product:"
ADMIN_ENTER_NAME = "Enter product name:"
ADMIN_ENTER_DESC = "Enter product description (or send '-' to skip):"
ADMIN_ENTER_PRICE = "Enter price (number):"
ADMIN_ENTER_IMAGE = "Send image URL (or send '-' to skip):"
ADMIN_PRODUCT_ADDED = "✅ Product '{name}' added."
ADMIN_INVALID_PRICE = "Invalid price. Please enter a number."
ADMIN_SELECT_PRODUCT = "Select a product to delete:"
ADMIN_PRODUCT_DELETED = "Product deleted."
ADMIN_PRODUCTS_EMPTY = "No products in this category."
ADMIN_TOGGLE_STOCK = "Select a product to toggle stock status:"
ADMIN_STOCK_TOGGLED = "Stock status for '{name}' changed to: {status}"

ADMIN_STATS_EMPTY = "No orders yet — nothing to show."
ADMIN_STATS_TEXT = (
    "📊 <b>Shop Stats</b>\n\n"
    "Orders: <b>{orders}</b>\n"
    "Revenue: <b>${revenue:.2f}</b>\n"
    "Products: <b>{products}</b>\n"
    "Pending orders: <b>{pending}</b>\n\n"
    "🏆 <b>Top products:</b>\n"
    "{top_products}"
)
