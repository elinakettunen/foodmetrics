# Food Properties Database

This [database of foods and drinks](https://raw.githubusercontent.com/elinakettunen/foodmetrics/refs/heads/main/food_properties.csv), identified by their codes in the [Fineli](https://fineli.fi/fineli/en/index) database by Finnish Institute for Health and Welfare, contains information about the proportional animal-source content within a food item, among other food item attributes.

This database is maintained and updated by Elina Kettunen, a doctoral researcher at the Department of Food and Nutrition at the University of Helsinki. Timestamps of public versions and the changes made are visible in the [commit log](https://github.com/elinakettunen/foodmetrics/commits/main/).

# Python package
To conveniently access the database from analysis code in python, you can clone this repo to your local machine and run `pip install -e .` in the project root. After that you can use the package `foodmetrics` in your code like this:

```python
from foodmetrics import get_food_properties, FOOD_PROP_DTYPES

df, metadata = get_food_properties()
print(metadata['commit_sha'])
print(df.dtypes)
```
---

**License**  
`foodmetrics` © 2025-2026 by Elina Kettunen is licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).
