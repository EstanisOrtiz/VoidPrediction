import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def LDA_model (df,random_state_value):

    # Within Class Scatter Matrix
    class_feature_means = pd.DataFrame(columns=[0.0, 1.0])
    for c, rows in df.groupby('Void'):
        class_feature_means[c] = rows.mean()

    class_feature_means = class_feature_means.drop(['Void'])

    matrix_size=class_feature_means.shape[0]

    within_class_scatter_matrix = np.zeros((matrix_size, matrix_size))
    for c, rows in df.groupby('Void'):
        rows = rows.drop(['Void'], axis=1)
        s = np.zeros((matrix_size, matrix_size))

    for index, row in rows.iterrows():
        x, mc = row.values.reshape(matrix_size, 1), class_feature_means[c].values.reshape(matrix_size, 1)
        s += (x - mc).dot((x - mc).T)
        within_class_scatter_matrix += s

    X = df.iloc[:, :-1].values
    X_dataset = pd.DataFrame(X)

    feature_means = X_dataset.mean()
    between_class_scatter_matrix = np.zeros((matrix_size, matrix_size))
    for c in class_feature_means:
        n = len(df.loc[df['Void'] == c].index)
        mc, m = class_feature_means[c].values.reshape(matrix_size, 1), feature_means.values.reshape(matrix_size, 1)
        between_class_scatter_matrix += n * (mc - m).dot((mc - m).T)

    eigen_values, eigen_vectors = np.linalg.eig(
        np.linalg.inv(within_class_scatter_matrix).dot(between_class_scatter_matrix))

    pairs = [(np.abs(eigen_values[i]), eigen_vectors[:, i]) for i in range(len(eigen_values))]
    pairs = sorted(pairs, key=lambda x: x[0], reverse=True)
    #print('Pairs:')
    #for pair in pairs:
        #print(pair[0])

    eigen_value_sums = sum(eigen_values)
    #print('------------------')
    #print('Explained Variance')
    #for i, pair in enumerate(pairs):
        #print('Eigenvector {}: {}'.format(i, (pair[0] / eigen_value_sums).real))

    w_matrix = np.hstack((pairs[0][1].reshape(19, 1), pairs[1][1].reshape(19, 1))).real

    X_lda = np.array(X.dot(w_matrix))

    le = LabelEncoder()
    y = le.fit_transform(df['Void'])

    plt.xlabel('LD1')
    plt.ylabel('LD2')
    plt.scatter(
        X_lda[:, 0],
        X_lda[:, 1],
        c=y,
        cmap='rainbow',
        alpha=0.7,
        edgecolors='b'
    )

    plt.show()

    X_train, X_test, y_train, y_test = train_test_split(X_lda, y, random_state=random_state_value)

    dt = RandomForestClassifier()
    dt.fit(X_train, y_train)
    y_pred = dt.predict(X_test)
    cm=confusion_matrix(y_test, y_pred)
    print('CONFUSION MATRIX:')
    print(cm)
    print('Accuracy: ' + str(accuracy_score(y_test, y_pred)))
    print('\n')
    print('Analytic Results:')
    precision_class1 = cm[0][0] / (cm[0][0] + cm[1][0])
    precision_class2 = cm[1][1] / (cm[1][1] + cm[0][1])
    recall_class1 = cm[0][0] / (cm[0][0] + cm[0][1])
    recall_class2 = cm[1][1] / (cm[1][1] + cm[1][0])
    accuracy = (cm[0][0] + cm[1][1]) / (cm[0][0] + cm[0][1] + cm[1][0] + cm[1][1])
    print('Recall score class 1: ' + str(recall_class1))
    print('Recall score class 2: ' + str(recall_class2))
    print('Precision class 1: ' + str(precision_class1))
    print('Precision class 2: ' + str(precision_class2))
    print('Accuracy: ' + str(accuracy))

    return X_lda, y, cm, y_test, y_pred
