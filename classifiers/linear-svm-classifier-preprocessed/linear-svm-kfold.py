import pickle
import numpy as np
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
# Genres
genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

# Load features and labels
trainFileName = '../../features/train-features.txt'
with open(trainFileName, 'r') as f:
    X = f.readlines()
X = [x.strip().split(',') for x in X]
y = np.array([genres.index(x.pop()) for x in X])
X = np.array(X, dtype=float)

# pre processing
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

# Define classifier
clf = svm.SVC(kernel='linear', C=1.0)

score = []
rates = []
# KFold
kf = KFold(n_splits=10, shuffle=True)
for train_index, test_index in kf.split(X):
    # Split data to train and test set
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # Train
    clf.fit(X_train, y_train)

    # Print accuracy
    score.append(clf.score(X_test, y_test))
    print("Accuracy: \t" + str(clf.score(X_test, y_test)))

    # I make the predictions
    predicted = clf.predict(X_test)

    # I obtain the confusion matrix
    cm = confusion_matrix(y_test, predicted)

    # rate calculation
    tp_rate = []
    i = 0
    for row in cm:
        current = 0
        TP = 0
        FP = 0
        for g in row:
            if current == i:
                TP = g
            else:
                FP = FP + g
            current = current + 1
        tp_rate.append(TP / (TP + FP))
        i = i + 1
    rates.append(tp_rate)

rates = np.round(np.mean(rates, axis=0), 3)
print("")
print("accuracy mean:", np.mean(score))
i = 0
for r in rates:
    print(genres[i], r)
    i = i + 1
