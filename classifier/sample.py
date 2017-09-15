import pandas as pd
import models

df = pd.read_csv("data/ionosphere.data", sep=",", header=None)
ionosphere_target = df.iloc[:, -1]
ionosphere_attributes = df.drop(df.columns[len(df.columns) - 1], axis=1)
models.svm(ionosphere_attributes, ionosphere_target)
