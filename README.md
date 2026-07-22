# everyone_tg_bot

A Telegram bot for group chats that tags everyone with one command: `/all`.

## How it works

Telegram doesn't let bots fetch a group's full member list (privacy restriction).
Instead, this bot remembers everyone who sends a message while it's running, and
`/all` mentions all of them. The list is stored in a local SQLite file (`bot.db`,
created automatically) so it survives restarts.

## Setup

1. **Create a bot token**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow the prompts
   - Copy the token it gives you

2. **Install and configure**
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   ```
   Paste your token into `.env` as `BOT_TOKEN=...`

3. **Run it**
   ```bash
   python bot.py
   ```

4. **Add it to your group**
   - Add the bot to your group chat
   - Make it an **admin** (any permissions, even none, are fine) — this is required
     so Telegram lets it see all messages instead of only commands

That's it. Let people chat normally, then send `/all` to tag everyone the bot
has seen so far.

## Notes

- Only tags people who've sent at least one message since the bot first joined.
- Seen-users data persists across restarts in `bot.db` (not committed to git).
- Keep `bot.py` running continuously (on your machine, a spare PC, or a server)
  for it to keep tracking messages — Telegram doesn't host bot code for you.
