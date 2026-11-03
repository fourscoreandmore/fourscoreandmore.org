# Gunicorn settings for Upsun (see web.commands.start in .platform.app.yaml).
# Gunicorn reads this file from the working directory.
import os

bind = f"127.0.0.1:{os.environ.get('PORT', '8000')}"

# Score processing with music21 is CPU-bound, so concurrency comes from
# processes: each sync worker handles one request at a time, and a slow
# request ties up only its own worker. Each uses about 100 MB.
workers = int(os.environ.get("WEB_CONCURRENCY", "3"))

# Restart a worker stuck on a request for longer than this. Working in Harmony
# analyses have their own, shorter limit (WIH_TIME_LIMIT in app/config.py), so
# this is a backstop for anything else.
timeout = 120

accesslog = "-"
