import numpy as np

years = np.genfromtxt(
    "./Cleaned_Energy_Consumption_Data.csv",
    delimiter=",",
    usecols=(range(4, 66)),
    max_rows=1,
)

data = np.genfromtxt(
    "./Cleaned_Energy_Consumption_Data.csv",
    delimiter=",",
    skip_header=1,
    usecols=(range(4, 66)),
)

mean_year = np.nanmean(data, axis=0)
median_year = np.nanmedian(data, axis=0)
std_year = np.nanstd(data, axis=0)

for k, year in enumerate(years, start=0):
    print(f"Moyenne {year} : ", mean_year[k])
    print(f"Médiane {year} : ", median_year[k])
    print(f"Ecart type {year} : ", std_year[k])

mean_pays = np.nanmean(data, axis=1)
pays = np.genfromtxt(
    "./Cleaned_Energy_Consumption_Data.csv",
    delimiter=",",
    skip_header=1,
    usecols=0,
    encoding="utf-8",
    dtype=str,
)
print(
    "Pays avec la consommation énergétique moyenne la plus basse : ",
    pays[np.nanargmin(mean_pays)],
)
print(
    "Pays avec la consommation énergétique moyenne la plus haute : ",
    pays[np.nanargmax(mean_pays)],
)
