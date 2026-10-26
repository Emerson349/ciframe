# Persist custom chord sequences in SQLite on a Docker volume

The app kept its catalog of "famous" chord sequences hardcoded: six entries in
`main.py` and four different entries in the AngularJS controller. Adding a
sequence required editing code and redeploying, and the frontend could not even
show all six sequences the backend already knew. The new feature lets any
visitor register a sequence and search songs by it, so the catalog became
mutable data that must survive a server restart. Songs and genres are still
loaded from `data/top/dataset_final.csv` into memory; only the sequence catalog
needs persistence.

We introduced a single SQLite database using Python's standard `sqlite3`
module. The file lives at `/data/sequencias.db` by default, can be overridden
with the `DB_PATH` environment variable, and falls back to `sequencias.db` in
the project directory when `/data` does not exist (plain virtualenv
development). The `sequencias` table stores an auto-incremented `id`, the
comma-separated `acordes` text with a `UNIQUE` constraint, and `criada_em`.
On startup the table is created if missing and the six original sequences are
inserted only when the table is empty, so repeated restarts do not duplicate
them.

SQLite was chosen because it satisfies ADR 0001: it is embedded, needs no
external service or extra container, and adds no dependency beyond the Python
standard library. It also gives us transactions and a `UNIQUE` constraint,
which a JSON or TinyDB file does not provide safely under concurrent writes;
in the research step, four concurrent writers produced 200 valid inserts, 200
duplicates rejected by the constraint, and one existing row. The alternative of
storing a pre-computed song list per sequence was discarded because a full
real-time scan takes about 123 ms and would have to be rebuilt whenever the CSV
changes.

The main consequence is operational: the database only survives `docker rm`
and container recreation when `/data` is backed by a named volume, so the
`Dockerfile` declares `VOLUME ["/data"]` and the documented run command uses
`-v ciframe-data:/data`. Without a volume, the data lives in an anonymous
volume or is lost with the container. The schema is created at application
startup, so there is no separate migration step; future schema changes will
need explicit migration code. Backups and any future retention policy are now
the responsibility of whoever owns that volume. Sequence creation remains open
and anonymous as required, with invalid input rejected as 400 and duplicates
as 409; rate limiting and spam protection are still out of scope.
