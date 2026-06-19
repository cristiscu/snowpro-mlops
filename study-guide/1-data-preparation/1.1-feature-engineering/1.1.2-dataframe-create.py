# paste and run as a Streamlit app

import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

session = get_active_session()
conn = session.connection

query = """
select n_name as country, count(c.*) as tot_customers
from snowflake_sample_data.tpch_sf1.nation n
join snowflake_sample_data.tpch_sf1.customer c
on n_nationkey = c_nationkey
where n_name IN ('CANADA', 'BRAZIL', 'CHINA')
group by n_name
order by n_name
"""

# (1) w/ Python Connector (Snowflake Connector for Python) cursor
cur = conn.cursor()
res = cur.execute(query)
st.dataframe(res)

# (2) w/ Python Connector cursor + Pandas dataframe
df = conn.cursor().execute(query).fetch_pandas_all()
st.dataframe(df)

# (3) w/ Pandas dataframe (from Python Connector connection)
df = pd.read_sql(query, conn)
st.dataframe(df)

# (4) w/ Snowpark DataFrame
df = session.sql(query)
st.dataframe(df)
