import pandas as pd
data = pd.DataFrame({"Toán":[5], "Văn":[5], "TB":[5]})
data.to_csv("data_diem.csv", index=False)