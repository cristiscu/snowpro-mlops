from snowflake.ml.feature_store import Entity

entity = Entity(name="MY_ENTITY", join_keys=["UNIQUE_ID"], desc="my entity")
fs.register_entity(entity)

fs.list_entities().show()

entity = fs.get_entity(name="MY_ENTITY")
print(entity.join_keys)

fs.update_entity(name="MY_ENTITY", desc="NEW DESCRIPTION")
fs.delete_entity(name="MY_ENTITY")
