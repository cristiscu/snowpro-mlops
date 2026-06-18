import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

df = pd.DataFrame({
    'age': [34, 23, 54, 31],
    'city': ['SF', 'NY', 'SF', 'LA'],
    'income': [120000, 95000, 135000, 99000]})

numeric_features = ['age', 'income']
numeric_transformer = StandardScaler()
categorical_features = ['city']
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer(transformers=[
   ('num', numeric_transformer, numeric_features),
   ('cat', categorical_transformer, categorical_features)])

pipeline = Pipeline(steps=[('preprocessor', preprocessor)])
X_processed = pipeline.fit_transform(df)
print(X_processed)
