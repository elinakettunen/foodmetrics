import requests
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Tuple, Optional

__version__ = "0.1.0"

REPO_OWNER = "elinakettunen"
REPO_NAME = "foodmetrics"
FILE_PATH = "food_properties.csv"

FOOD_PROP_DTYPES = {
    'code': 'str',
    'animal_proportion': 'Float32',
    'fao_subgroup_code': 'Int64',
    'has_fish': 'boolean',
    'has_meat_or_poultry': 'boolean',
    'has_seafood': 'boolean',
    'name': 'str',
	'cereals': 'Float32',
	'whole_grain': 'Float32',
	'tubers_roots': 'Float32',
	'vegetables': 'Float32',
	'fruits': 'Float32',
	'nuts': 'Float32',
	'legumes': 'Float32',
	'dairy': 'Float32',
	'poultry': 'Float32',
	'fish': 'Float32',
	'eggs': 'Float32',
	'meat': 'Float32',
	'plant_oils_unsaturated': 'Float32',
	'plant_oils_saturated': 'Float32',
	'animal_fats': 'Float32',
	'sugar': 'Float32',
	'none': 'Float32'
}

def get_latest_version_info() -> Dict[str, str]:
    """
    Get version information for the latest commit of the food properties file.
    
    Returns:
        Dict with commit_sha, commit_date, and file_url
    """
    api_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits'
    params = {'path': FILE_PATH, 'page': 1, 'per_page': 1}
    
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    
    latest_commit = response.json()[0]
    commit_sha = latest_commit['sha']
    commit_date = latest_commit['commit']['committer']['date']
    
    versioned_url = (
        f'https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/'
        f'{commit_sha}/{FILE_PATH}'
    )
    
    return {
        'commit_sha': commit_sha,
        'commit_date': commit_date,
        'file_url': versioned_url,
        'fetched_at': datetime.now(timezone.utc).isoformat()
    }


def get_food_properties(
    commit_sha: Optional[str] = None
) -> Tuple[pd.DataFrame, Dict[str, str]] | pd.DataFrame:
    """
    Fetch the food properties CSV from GitHub.
    
    Args:
        commit_sha: Specific commit SHA to fetch. If None, fetches latest.    
    Returns:
        Tuple of (DataFrame, metadata dict)
    """
    if commit_sha is None:
        metadata = get_latest_version_info()
        commit_sha = metadata['commit_sha']
    else:
        versioned_url = (
            f'https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/'
            f'{commit_sha}/{FILE_PATH}'
        )
        metadata = {
            'commit_sha': commit_sha,
            'file_url': versioned_url,
            'fetched_at': datetime.utcnow().isoformat()
        }
    
    df = pd.read_csv(
        metadata['file_url'],
        index_col='code',
        dtype=FOOD_PROP_DTYPES
    )
    
    return df, metadata

def get_food_properties_local():
    from pathlib import Path
    return pd.read_csv(
        Path(__file__).parent.parent.absolute() / 'food_properties.csv',
        index_col='code',
        dtype=FOOD_PROP_DTYPES
    )