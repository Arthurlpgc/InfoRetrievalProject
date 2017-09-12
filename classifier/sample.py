import pandas as pd
import models

class_name = "whether he/she donated blood in March 2007"
transfusion = pd.read_csv("data/transfusion.data", sep=",")
transfusion_attributes = transfusion.drop(class_name, 1)
transfusion_target = transfusion[class_name]
models.svm(transfusion_attributes, transfusion_target)
