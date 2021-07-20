#%%
from numpy import NaN  # NaN means not a number
import pandas as pd

#%%
price_df = pd.read_excel(
    "price_history_checks_may2021.xlsx", parse_dates=["PriceUpdatedDate"]
)
price_df.head()

#%%
fuel_codes = price_df.FuelCode.unique()
fuel_codes = [x for x in fuel_codes if type(x) is str]
print(fuel_codes)
#%%
new_column_names = (
    [f"Price_{name}_UpdatedDate" for name in fuel_codes]
    + [f"Price_{name}" for name in fuel_codes]
    + [
        name
        for name in price_df.columns
        if name not in ["FuelCode", "PriceUpdatedDate", "Price"]
    ]
)
new_column_names.sort()
print(new_column_names)

#%%
#%%
new_rows = []
temp_row = pd.Series(index=new_column_names, dtype=object)

for i, row in price_df.head(100).iterrows():
    fc = row.FuelCode
    if row.ServiceStationName is not NaN:
        new_rows.append(temp_row)
        temp_row = pd.Series(index=new_column_names, dtype=object)
        for key, element in row.iteritems():
            if key in temp_row.index:
                temp_row[key] = element
        temp_row[f"Price_{fc}_UpdatedDate"] = row.PriceUpdatedDate
        temp_row[f"Price_{fc}"] = row.Price
    elif row.ServiceStationName is NaN:
        temp_row[f"Price_{fc}_UpdatedDate"] = row.PriceUpdatedDate
        temp_row[f"Price_{fc}"] = row.Price

#%%
reshaped_df = pd.DataFrame(new_rows)
reshaped_df.drop([0], inplace=True)
reshaped_df.head()
