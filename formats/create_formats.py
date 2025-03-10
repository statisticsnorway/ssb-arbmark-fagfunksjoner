# ## As of 12.02.2025 the SsbFormat-class is not yet published in ssb-fagfunksjoner. Code in this notebook is therefore run on the kernal built from the ssb-fagfunksjoner repo and the 'formats' branch. 

from fagfunksjoner import SsbFormat
from fagfunksjoner.formats import store_format, get_format

# ### Age formats from ssb-arbmark-fagfunksjoner/src/arbmark/groups/age.py

# +
alder = {
    "16-19": "16-19 år",
    "20-24": "20-24 år",
    "25-29": "25-29 år",
    "30-34": "30-34 år",
    "35-39": "35-39 år",
    "40-44": "40-44 år",
    "45-49": "45-49 år",
    "50-54": "50-54 år",
    "55-59": "55-59 år",
    "60-64": "60-64 år",
    "65-66": "65-66 år",
    "67": "67 år",
    "68": "68 år",
    "69": "69 år",
    'other': None
    }

alder_5grp = {
    "low-24": "-24",
    "25-39": "25-39",
    "40-54": "40-54",
    "55-66": "55-66",
    "67-high": "67+",
    'other': None
    }
# -

# ### Company size formats from src/arbmark/groups/company_size.py

virk_str_8grp = {
    "0": "Ingen ansatte",
    "1-4": "1-4 ansatte",
    "5-9": "5-9 ansatte",
    "10-19": "10-19 ansatte",
    "20-49": "20-49 ansatte",
    "50-99": "50-99 ansatte",
    "100-249": "100-249 ansatte",
    "250-high": "250 ansatte og over",
    'other': None
    }
