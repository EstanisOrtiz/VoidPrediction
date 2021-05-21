import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score

from modules import cm_analysis as cm_analysis

def LDA_model_command(df):
    # Split data into X and y
    X = df.drop('Void', axis=1)
    y = df['Void']

    # Training and Test set 90-10%. Always Random
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.10, random_state=None)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # LDA transform
    lda = LDA(n_components=1)
    X_train = lda.fit_transform(X_train, y_train)   # X_lda
    X_test = lda.transform(X_test)                  # X_lda_pred

    # Classifier Random Foreset Classifier
    classifier = RandomForestClassifier(max_depth=10, random_state=0) # Depth
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print('CONFUSION MATRIX:')
    print(cm)
    print('Accuracy: ' + str(accuracy_score(y_test, y_pred)))

    cm_analysis.cm_analysis(y_test, y_pred)

    return cm

