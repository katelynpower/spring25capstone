from sklearn import tree
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import pandas as pd

file_path = 'C:/Users/power/Desktop/Classes/DATS4001/25-spring-KPower/data/cleaned_vaccine_sentiment_data.csv'
df= pd.read_csv(file_path)
df.dropna(inplace=True)
x = df.drop(df.columns[[6, 7, 8, 10, 11, 13]], axis=1)

text_columns = ["vaccine","demo_group","demo_category","indicator_category","indicator_group","month_label","dashboard_type"]
label_encoder = LabelEncoder()
for col in text_columns:
    x[col] = label_encoder.fit_transform(x[col])

x_train = x[df['month_label'] != 'October 2024/November 2024'].drop(columns=['month_label','estimate'])
x_test = x[df['month_label'] == 'October 2024/November 2024'].drop(columns=['month_label','estimate'])
y_train = x[df['month_label'] != 'October 2024/November 2024']['estimate']
y_test = x[df['month_label'] == 'October 2024/November 2024']['estimate']

print(y_train.dtypes)
dt = tree.DecisionTreeRegressor(random_state=33)
dt.fit(x_train, y_train)

y_pred = dt.predict(x_test)

print(mean_squared_error(y_test, y_pred))
print(dt.score(x_test, y_test))
tree.plot_tree(dt)
plt.show()