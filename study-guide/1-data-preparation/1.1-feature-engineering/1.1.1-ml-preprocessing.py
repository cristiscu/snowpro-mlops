from snowflake.snowpark import Session
from snowflake.ml.modeling.preprocessing import StandardScaler
from snowflake.ml.modeling.preprocessing import OneHotEncoder
from snowflake.ml.modeling.pipeline import Pipeline

session = Session.builder.configs(...).create()

df = session.table('CUSTOMER_DATA')

scaler = StandardScaler(input_cols=['AGE', 'INCOME'], output_cols = ['AGE_SCALED', 'INCOME_SCALED'])
encoder = OneHotEncoder(input_cols=['CITY'], output_cols=['CITY_ENCODED'])

pipeline = Pipeline(steps=[('scaling', scaler), ('encoding', encoder)])
result = pipeline.fit_transform(df)
result.show()

# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
# normalize labels

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit(["paris", "paris", "tokyo", "amsterdam"])
list(le.classes_)
le.transform(["tokyo", "tokyo", "paris"])
list(le.inverse_transform([2, 2, 1]))

# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html
# X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
# X_scaled = X_std * (max - min) + min

from sklearn.preprocessing import MinMaxScaler
data = [[-1, 2], [-0.5, 6], [0, 10], [1, 18]]
scaler = MinMaxScaler()
print(scaler.fit(data))
print(scaler.data_max_)
print(scaler.transform(data))
print(scaler.transform([[2, 2]]))

# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html
from sklearn.preprocessing import RobustScaler
X = [[ 1., -2.,  2.],
     [ -2.,  1.,  3.],
     [ 4.,  1., -2.]]
transformer = RobustScaler().fit(X)
transformer
transformer.transform(X)