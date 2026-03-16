<p align="center">
  <h1 align="center">Telegram Shop Bot</h1>
  <p align="center">A Telegram e-commerce bot for small online shops with product catalog, shopping cart, orders, and admin panel.</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=flat&logo=telegram&logoColor=white" alt="aiogram">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=flat&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/SQLite-async-003B57?style=flat&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="License">
</p>

---

## Features

- **Product Catalog** — browse products organized by categories with inline navigation
- **Shopping Cart** — add/remove items, change quantities, view totals
- **Order System** — place orders, view order history with detailed info
- **Admin Panel** — manage products and categories (add, edit, delete) via bot interface
- **Async Database** — fully asynchronous SQLite via aiosqlite + SQLAlchemy
- **Modular Architecture** — clean separation of handlers, keyboards, and data layers

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show main menu |
| `/help` | Show help message |
| `/catalog` | Browse product catalog |
| `/cart` | View shopping cart |
| `/orders` | View order history |
| `/admin` | Admin panel (admin only) |

## Setup

### 1. Clone and install

```bash
git clone https://github.com/qorexdev/telegram-shop-bot.git
cd telegram-shop-bot

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your values:

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Get it from [@BotFather](https://t.me/BotFather) |
| `ADMIN_ID` | Your Telegram user ID ([@userinfobot](https://t.me/userinfobot)) |

### 3. Run the bot

```bash
python -m bot.main
```

## Project Structure

```
telegram-shop-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py                # Entry point, dispatcher setup
│   ├── config.py              # Settings from environment
│   ├── database/
│   │   ├── models.py          # SQLAlchemy models (Product, Category, Order, Cart)
│   │   └── engine.py          # Async engine and session factory
│   ├── handlers/
│   │   ├── __init__.py        # Router registration
│   │   ├── user.py            # Catalog browsing, product view
│   │   ├── cart.py            # Cart management
│   │   ├── order.py           # Order placement and history
│   │   └── admin.py           # Admin panel handlers
│   ├── keyboards/
│   │   ├── inline.py          # Inline keyboards (catalog, cart, etc.)
│   │   └── reply.py           # Reply keyboards (main menu)
│   ├── middlewares/
│   │   └── db.py              # Database session middleware
│   └── utils/
│       └── texts.py           # Bot message templates
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Tech Stack

| Component | Technology |
|---|---|
| Bot Framework | [aiogram 3.x](https://docs.aiogram.dev/) |
| ORM | [SQLAlchemy 2.x](https://www.sqlalchemy.org/) (async) |
| Database | SQLite via [aiosqlite](https://github.com/omnilib/aiosqlite) |
| Config | [python-dotenv](https://github.com/theskumar/python-dotenv) |

## License

MIT

---

<p align="center">
  <sub>developed by <a href="https://github.com/qorexdev">qorex</a></sub>
  <br>
  <sub>
    <a href="https://github.com/qorexdev">GitHub</a> · <a href="https://t.me/qorexdev">Telegram</a>
  </sub>
</p>
