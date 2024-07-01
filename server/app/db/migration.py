from databases import Database
from datetime import datetime
from typing import Callable, Coroutine

MIGRATION_TABLE_NAME = "migration_version"


MigrationFunction = Callable[[Database], Coroutine]

async def apply_migrations(db: Database, migrations: list[MigrationFunction]):
    async with db.transaction():
        migration_table = await db.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name",
            {
                "table_name": MIGRATION_TABLE_NAME,
            },
        )
        if migration_table is None:
            await db.execute(
                """
                   CREATE TABLE migration_version  (
                       version INTEGER PRIMARY KEY,
                       applied_on TEXT NOT NULL
                   )
                """
            )

        migrations_applied = await db.fetch_one(
            "SELECT count(*) as count FROM migration_version"
        )
        assert migrations_applied is not None

        count: int = migrations_applied["count"]

        if count > len(migrations):
            raise Exception(
                "Database has newer migrations applied to it. Your code seems to be older, please deploy newer version."
            )

        for i, migration in enumerate(migrations[count:]):
            await migration(db)
            await db.execute(
                """
                INSERT INTO migration_version (version, applied_on) VALUES (:version, :applied_on)
                """,
                {"version": count + i + 1, "applied_on": datetime.now().isoformat()},
            )

