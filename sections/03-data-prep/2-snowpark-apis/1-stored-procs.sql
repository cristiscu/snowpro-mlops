use test.public;

-- =================================================================
-- SQL or Snowflake Scripting

-- Snowflake Scripting stored procedure
create or replace procedure procSQL(num float)
    returns string not null
    language sql
as
begin
    return '+' || to_varchar(num);
end;

call procSQL(22.5);
select * from table(result_scan(last_query_id()));

-- Snowflake Scripting Table stored procedure
create or replace procedure procSQLT(s string)
    returns table(out varchar)
    language sql
as
begin
    LET rs RESULTSET := (select :s union all select :s);
    RETURN TABLE(rs);
end;

call procSQLT('abc');
select * from table(procSQLT('abc'));

-- SQL UDF
create or replace function udfSQL(num float) returns string
as 'select ''+'' || to_varchar(num)';

select udfSQL(22.5);

-- SQL UDTF
create or replace function udtfSQL(s string)
    returns table(out varchar)
as $$
    select s
    union all
    select s
$$;

select * from table(udtfSQL('abc'));

-- =================================================================
-- JavaScript

-- JavaScript stored procedure
create or replace procedure procJS(num float)
    returns string not null
    language javascript
    strict
as $$
    return '+' + NUM.toString();
$$;

call procJS(22.5);
select * from table(result_scan(last_query_id()));

-- JavaScript UDF
create or replace function udfJS(num float)
    returns string not null
    language javascript
    strict
as 'return \'+\' + NUM.toString()';

select udfJS(22.5);

-- JavaScript UDTF
create or replace function udtfJS(s string)
    returns table(out varchar)
    language javascript
    strict
as $$
{
    processRow: function f(row, rowWriter, context)
    {
        rowWriter.writeRow({OUT: row.S});
        rowWriter.writeRow({OUT: row.S});
    }
}
$$;

select * from table(udtfJS('abc'));

-- =================================================================
-- Python

-- Python stored procedure (only w/ Snowpark!)
create or replace procedure procPython(num float)
    returns string
    language python
    runtime_version = '3.10'
    packages = ('snowflake-snowpark-python')
    handler = 'proc1'
as $$
import snowflake.snowpark as snowpark

def proc1(session: snowpark.Session, num: float):
    query = f"select '+' || to_char({num})"
    return session.sql(query).collect()[0][0]
$$;

call procPython(22.5);

-- Python UDF
create or replace function udfPython(num float)
    returns string
    language python
    runtime_version = '3.10'
    handler = 'proc1'
as $$
def proc1(num: float):
    return '+' + str(num)
$$;

select udfPython(22.5);

-- Python UDTF
create or replace function udtfPython(s string)
    returns table(out varchar)
    language python
    runtime_version = '3.10'
    handler = 'MyClass'
as $$
class MyClass:
    def process(self, s: str):
        yield (s,)
        yield (s,)
$$;

select * from table(udtfPython('abc'));
