import pandas as pd
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import kendalltau
from sklearn.ensemble import RandomForestRegressor


pd.set_option('display.max_columns', None)
db = pd.read_csv('NLSY97_subset.csv')
db['Mean_ASVAB'] = db[['ASVABAR','ASVABMK', 'ASVABC4','ASVABC','ASVABMV', 'ASVABNO', 'VERBAL', 'ASVABPC', 'ASVABWK']].mean(axis=1)

# LOOKING FOR VARIABLES WITH CORRELATIONS WITH EARNINGS
db.dropna(inplace=True)
potential_corr = abs(db.corr()['EARNINGS'])
print(potential_corr.sort_values(ascending=False).head(30))
sns.heatmap(db.corr())
plt.show()

# SEARCHING FOR CORRELATIONS:
corr_db = pd.DataFrame(columns=['Variable', 'Pearson', 'Spearman', 'Kendalltau'])
linear_correlations1 = []
nonlinear_correlations2 = []
nonlinear_correlations3 = []
for c in db.columns:
    corr1, _ = pearsonr(db['EARNINGS'], db[c])
    corr2, _ = spearmanr(db['EARNINGS'], db[c])
    corr3, _ = kendalltau(db['EARNINGS'], db[c])
    linear_correlations1.append(corr1)
    nonlinear_correlations2.append(corr2)
    nonlinear_correlations3.append(corr3)
corr_db['Variable'] = db.columns
corr_db['Pearson'] = linear_correlations1
corr_db['Spearman'] = nonlinear_correlations2
corr_db['Kendalltau'] = nonlinear_correlations3
corr_db.dropna(inplace=True)
print(corr_db.sort_values('Pearson').tail(20))


# CREATING A MULTIVARIABLE MODEL USING LINEAR REGRESSION
# The following potential variables were identified: 'S', 'ASVABMK', 'HHINC97', 'POVRAT97', 'EDUCMAST', 'SF', 'SMR'
regression = LinearRegression()
X = db[['S', 'ASVABMK', 'HHINC97', 'POVRAT97', 'EDUCMAST', 'SF', 'SMR']]
Y = db['EARNINGS']
regression.fit(X, y=Y)
print(f'Regression score using data: {round(regression.score(X, Y), 3)}')
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
model = LinearRegression().fit(X_train, Y_train)
print(f'Model interception (x=0): {model.intercept_}')
print(f"Model coefficients per variables ('S', 'ASVABMK', 'HHINC97', 'POVRAT97', 'EDUCPROF', 'SF', 'SMR'): {model.coef_}")
print(f'Model regression score using train values: {round(model.score(X_train, Y_train),3)}')
print(f'Model regression score using test values: {round(model.score(X_test, Y_test),3)}')
prediction = model.predict(X_test)
plt.figure(figsize=(6,6))
plt.scatter(Y_test, prediction, c='crimson')
p1 = max(max(prediction), max(Y_test))
p2 = min(min(prediction), min(Y_test))
plt.plot([p1, p2], [p1, p2], 'b-')
plt.xlabel('True Values', fontsize=10)
plt.ylabel('Predictions', fontsize=10)
plt.axis('equal')
plt.show()



# CREATING A MULTIVARIABLE MODEL USING RANDOM FOREST REGRESSION
# The following potential variables were identified: 'S', 'ASVABMK', 'HHINC97', 'POVRAT97', 'EDUCPROF', 'SF', 'SMR'
VARIABLES = ['S', 'ASVABMK', 'HHINC97', 'POVRAT97', 'EDUCPROF', 'SF', 'SMR']

# for i in range(len(VARIABLES)):
#     X = db[VARIABLES[0:i+1]]
#     Y = db['EARNINGS']
#     X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
X = db[VARIABLES]
Y = db['EARNINGS']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
rfr = RandomForestRegressor()
model = rfr.fit(X_train, Y_train)
print(rfr.score(X_train, Y_train))
Y_pred = rfr.predict(X_test)
print(model.feature_names_in_)
print(model.feature_importances_)
x_ax = range(len(Y_test))
plt.plot(x_ax, Y_test, linewidth=1, label="original")
plt.plot(x_ax, Y_pred, linewidth=1.1, label="predicted")
plt.title("y-test and y-predicted data")
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend(loc='best',fancybox=True, shadow=True)
plt.grid(True)
plt.show()