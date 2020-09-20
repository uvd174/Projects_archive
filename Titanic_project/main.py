import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from catboost import Pool, CatBoostClassifier


train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

print(f'train shape: {train.shape}, test shape {test.shape}')

# col = 'Embarked'
col = 'Sex'
pd.concat([train[col].value_counts(), train[col].value_counts() / train.shape[0] * 100,
           test[col].value_counts(), test[col].value_counts() / test.shape[0] * 100],
          axis=1, keys=['train', '%', 'test', '%'], sort=False)

print('NaN in the data sets')
nans = pd.concat([train.isnull().sum(), test.isnull().sum()],
                 axis=1, keys=['Train Dataset', 'Test Dataset'], sort=False)
print(nans[nans.sum(axis=1) > 0])

# one feature vs target
# col = 'Sex'
col = 'Pclass'
target = 'Survived'
print(train[[col, target]].groupby([col], as_index=False).mean().sort_values(by=col))


def fill_na_by_median(df_, col_):
    df_[col_].fillna(df_[col_].median(), inplace=True)


full_dataset = [train, test]
for df in full_dataset:
    fill_na_by_median(df, 'Age')
    fill_na_by_median(df, 'Fare')

    df['Embarked'].fillna('S', inplace=True)
    df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).astype(int)
    df['Sex'] = df['Sex'].map({'male': 1, 'female': 2}).astype(int)

for data in full_dataset:
    # classify Cabin by fare
    data['Cabin'] = data['Cabin'].fillna('X')
    data['Cabin'] = data['Cabin'].apply(lambda x: str(x)[0])
    data['Cabin'] = data['Cabin'].replace(['A', 'D', 'E', 'T'], 'M')
    data['Cabin'] = data['Cabin'].replace(['B', 'C'], 'H')
    data['Cabin'] = data['Cabin'].replace(['F', 'G'], 'L')
    data['Cabin'] = data['Cabin'].map({'X': 0, 'L': 1, 'M': 2, 'H': 3}).astype(int)

for df in full_dataset:
    df.drop(['Name', 'Ticket'], axis=1, inplace=True)

y = train['Survived']
X = train.drop('Survived', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.12, random_state=2019)

# Scaling the train and test feature set

train_dataset = Pool(data=X_train, label=y_train)
eval_dataset = Pool(data=X_test, label=y_test)

# Initialize CatBoostClassifier
model = CatBoostClassifier(iterations=50)
# Fit model
model.fit(train_dataset)
# Get predicted classes
preds_class = model.predict(eval_dataset)
# Get predicted probabilities for each class
preds_proba = model.predict_proba(eval_dataset)
# Get predicted RawFormulaVal
preds_raw = model.predict(eval_dataset,
                          prediction_type='RawFormulaVal')

print(f'accuracy_cb = {accuracy_score(y_test, preds_class)}')

feature_importances = list(zip(model.feature_names_, model.feature_importances_))
feature_importances.sort(key=lambda x: -x[1])
print(*feature_importances, sep='\n')

y_pred = model.predict(test)
submission = pd.DataFrame({
        'PassengerId': test['PassengerId'],
        'Survived': y_pred.astype('int')
    })
submission.to_csv('titanic_cb.csv', index=False)
