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
	'ep_phd_refined_grains': 'Float32',
	'ep_phd_whole_grains': 'Float32',
	'ep_phd_tubers_roots': 'Float32',
	'ep_phd_vegetables': 'Float32',
	'ep_phd_fruits': 'Float32',
	'ep_phd_nuts': 'Float32',
	'ep_phd_legumes': 'Float32',
	'ep_phd_dairy': 'Float32',
	'ep_phd_poultry': 'Float32',
	'ep_phd_fish': 'Float32',
	'ep_phd_eggs': 'Float32',
	'ep_phd_meat': 'Float32',
	'ep_phd_plant_oils_unsaturated': 'Float32',
	'ep_phd_plant_oils_saturated': 'Float32',
	'ep_phd_animal_fats': 'Float32',
	'ep_phd_sugar': 'Float32',
	'ep_phd_none': 'Float32'
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
    meta = {
        'commit_sha': 'local',
        'commit_date': 'local',
        'file_url': 'local',
        'fetched_at': datetime.now(timezone.utc).isoformat()
    }
    from pathlib import Path
    return pd.read_csv(
        Path(__file__).parent.parent.absolute() / 'food_properties.csv',
        index_col='code',
        dtype=FOOD_PROP_DTYPES
    ), meta