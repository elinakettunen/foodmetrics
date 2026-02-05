# Food Properties Database

This [database of foods and drinks](https://raw.githubusercontent.com/elinakettunen/foodmetrics/refs/heads/main/food_properties.csv) contains information about their attributes. Each food is identified by their code in a food database, mostly from [Fineli](https://fineli.fi/fineli/en/index), the database by Finnish Institute for Health and Welfare.

The attributes include:
- energy proportion of animal-source foods
- energy proportion by food category in the Eat Lancet Planetary Health Reference Diet

This database is work in progress, maintained and updated by Elina Kettunen, a doctoral researcher at the Department of Food and Nutrition at the University of Helsinki. Timestamps of public versions and the changes made are visible in the [commit log](https://github.com/elinakettunen/foodmetrics/commits/main/).

# Python package
Python code is included for reading the database into pandas and noting the exact version used at the same time.

To edit the database clone the repository to your workstation. In that case you can also make the python code available to other projects with  `pip install -e .`. After that you can use the package `foodmetrics` in your code like this:

```python
from foodmetrics import get_food_properties, FOOD_PROP_DTYPES

df, metadata = get_food_properties()
print(metadata['commit_sha'])
df.head()
```
---

**License**  
`foodmetrics` © 2025-2026 by Elina Kettunen is licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).
