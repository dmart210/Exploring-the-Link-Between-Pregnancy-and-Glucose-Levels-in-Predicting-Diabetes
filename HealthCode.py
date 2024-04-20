import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv('diabetes.csv')
data['id'] = range(1, len(data) + 1)


def removeOutliers():
    Q1 = data["Pregnancies"].quantile(.25)
    Q3 = data["Pregnancies"].quantile(.75)
    IQR = abs(Q3-Q1)

    lowerBound = Q1 - ( 1.5 * IQR)
    upperBound = Q3 + ( 1.5 * IQR)
    
    outliers = data[(data["Pregnancies"] < lowerBound) | (data["Pregnancies"] > upperBound)]
    cleanedData = data[(data["Pregnancies"] >= lowerBound) & (data["Pregnancies"] <= upperBound)]
    return cleanedData

def clientToDict():
    pregWDiab = [[{}],0]
    pregNoDiab = [[{}],0]
    firstQuery = data.query("Glucose > 129 and Pregnancies > 0")
    secondQuery = data.query("Glucose < 129 and Pregnancies > 0")
    for index,row in firstQuery.iterrows():
        pregWDiab[0].append({'id': row['id'],"Pregnancies": row['Pregnancies'], "Glucose":row['Glucose']})
    for index,row in secondQuery.iterrows():
        pregNoDiab[0].append({'id': row['id'],"Pregnancies": row['Pregnancies'], "Glucose":row['Glucose'] })

    pregWDiab[1]= firstQuery["Pregnancies"].mean()
    pregNoDiab[1] = secondQuery["Pregnancies"].mean()
    return pregWDiab, pregNoDiab


def results(pregnanciesAltered):
    print(f'Mean # of Pregnancies of women with diabetes: {round(pregnanciesAltered[0][1], 2)}')
    print(f'Mean # of Pregnancies of women without diabetes: {round(pregnanciesAltered[1][1],2)}')
    print(f'Using these discoveries we can come up with the hypothesis that:\n')
    print("The more pregnancies a women has, the higher likely she is to become diabetic.")


def visualize(pregnancies):
    # Extracting data
    categories = ['With Diabetes', 'Without Diabetes']
    means = [pregnancies[0][1], pregnancies[1][1]]

    # Creating the bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(categories, means, color=['red', 'green'])
    plt.xlabel('Condition')
    plt.ylabel('Average Number of Pregnancies')
    plt.title('Average Number of Pregnancies vs Diabetes Condition')
    plt.ylim(0, max(means) + 1)  # Set y limit to show all data clearly
    plt.show()


data = removeOutliers()
pregnanciesDivided= clientToDict()
# [0] = Preg & Diab [1] = Preg & W/o Diab
results(pregnanciesDivided)
visualize(pregnanciesDivided)






