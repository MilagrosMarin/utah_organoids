import datajoint as dj

schema = dj.schema()
if "custom" not in dj.config:
    dj.config["custom"] = {}

DB_PREFIX = dj.config["custom"].get("database.prefix", "")

schema = dj.schema(DB_PREFIX + "lineage")


@schema
class Induction(dj.Manual):
    definition = """
    induction_id: varchar(8)     # de-identified code
    ---
    family: varchar(8)
    line: varchar(8)
    passage_id: int
    """

@schema
class InductionSequence(dj.Manual):
    definition = """
    -> Induction
    sequence: varchar(8)
    """
