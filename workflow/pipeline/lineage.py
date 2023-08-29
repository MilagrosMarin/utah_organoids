import datajoint as dj

if "custom" not in dj.config:
    dj.config["custom"] = {}

DB_PREFIX = dj.config["custom"].get("database.prefix", "")

schema = dj.schema(DB_PREFIX + "lineage")


@schema
class Storage(dj.Manual):
    definition = """
    induction_id: varchar(8)     # de-identified code (e.g. hmau001)
    ---
    storage_position: enum(1,2,3,4,5)
    stand: int unsigned
    rack: int unsigned
    box_position: int unsigned
    frozen_date: date
    family: varchar(8)
    line: varchar(8)
    passage: int unsigned
    lineage_note='': varchar(256)
    """


@schema
class Sequence(dj.Manual):
    definition = """
    -> Storage
    sequence: varchar(32)
    """
