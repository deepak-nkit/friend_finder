import pytest
import tempfile
from . import migration
import databases


@pytest.mark.asyncio
async def test_migration():
    db = databases.Database("sqlite:///:memory:", force_rollback=True)
    await db.connect()

    async def migration_01(db: databases.Database):
        print("============= running migration function")
        await db.execute("""
            CREATE TABLE user (
                id INTEGER PRIMARY KEY
            )
        """)


    ############ Step 1: Apply migration 1
    await migration.apply_migrations(db, [migration_01])

    row = await db.fetch_one("""
            SELECT count(*) as count from migration_version
    """)
    assert row is not None
    assert row['count'] == 1


    row = await db.fetch_one("""
           SELECT name FROM sqlite_master WHERE type='table' AND name='user'
    """)
    assert row is not None


    ############ Step 2: Apply migration 1 again (should not give error)
    await migration.apply_migrations(db, [migration_01])

    row = await db.fetch_one("""
            SELECT count(*) as count from migration_version
    """)
    assert row is not None
    assert row['count'] == 1

    row = await db.fetch_one("""
           SELECT name FROM sqlite_master WHERE type='table' AND name='user'
    """)
    assert row is not None

    ############ Step 3: Apply migration 1 and 2 (should not give error)
    async def migration_02(db: databases.Database):
        await db.execute("""
           ALTER TABLE user ADD COLUMN name TEXT NOT NULL; 
        """)

    await migration.apply_migrations(db, [migration_01, migration_02])
    row = await db.fetch_one("""
            SELECT count(*) as count from migration_version
    """)
    assert row is not None
    assert row['count'] == 2

    row = await db.fetch_one("""
           SELECT name, sql FROM sqlite_master WHERE type='table' AND name='user'
    """)
    assert row is not None
    assert 'name' in row['sql']


    ########## Step 4: execute only 1 migration, should throw error as database is newer
    

    with pytest.raises(Exception):
        await migration.apply_migrations(db, [migration_01])



    await db.disconnect()

    
