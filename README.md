# Telegram Shop Bot

A Telegram e-commerce bot for small online shops built with **aiogram 3.x**, **SQLAlchemy**, and **SQLite**.

## Features

- **Product Catalog** — browse products organized by categories with inline navigation
- **Shopping Cart** — add/remove items, change quantities, view totals
- **Order System** — place orders, view order history with detailed info
- **Admin Panel** — manage products and categories (add, edit, delete) via bot interface
- **Async Database** — fully asynchronous SQLite via aiosqlite + SQLAlchemy

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

### 1. Clone the repository

```bash
git clone https://github.com/qorexdev/telegram-shop-bot.git
cd telegram-shop-bot
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your values:
- `BOT_TOKEN` — get it from [@BotFather](https://t.me/BotFather)
- `ADMIN_ID` — your Telegram user ID (get it from [@userinfobot](https://t.me/userinfobot))

### 5. Run the bot

```bash
python -m bot.main
```

## Project Structure

```
telegram-shop-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Entry point, dispatcher setup
│   ├── config.py             # Settings from environment
│   ├── database/
│   │   ├── models.py         # SQLAlchemy models
│   │   └── engine.py         # Async engine and session
│   ├── handlers/
│   │   ├── __init__.py       # Router registration
│   │   ├── user.py           # Catalog browsing, product view
│   │   ├── cart.py           # Cart management
│   │   ├── order.py          # Order placement and history
│   │   └── admin.py          # Admin panel
│   ├── keyboards/
│   │   ├── inline.py         # Inline keyboards
│   │   └── reply.py          # Reply keyboards
│   ├── middlewares/
│   │   └── db.py             # Database session middleware
│   └── utils/
│       └── texts.py          # Bot message constants
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Tech Stack

- [aiogram 3.x](https://docs.aiogram.dev/) — async Telegram Bot framework
- [SQLAlchemy 2.x](https://www.sqlalchemy.org/) — ORM with async support
- [aiosqlite](https://github.com/omnilib/aiosqlite) — async SQLite driver
- [python-dotenv](https://github.com/theskumar/python-dotenv) — environment configuration

## License

MIT
