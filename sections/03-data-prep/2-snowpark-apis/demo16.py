from snowflake.snowpark import Session

def add_five(session: Session, x: int) -> int:
    return session.sql(f"select {x} + 5").collect()[0][0]