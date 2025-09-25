from klass import KlassClassification
import numpy as np
import pandas as pd

vkoder = KlassClassification(545).get_codes(select_level='4').data


# +
landkat = KlassClassification(546)
landkoder = landkat.get_codes().data
levels = np.sort(landkoder['level'].astype(int).unique())

vkoder = KlassClassification(545).get_codes().data
levels = np.sort(landkoder['level'].astype(int).unique())

# -

lev3_dict = landkoder.loc[landkoder['level'] == '3'][['code', 'parentCode']].set_index('code').to_dict()['parentCode']

landkoder = KlassClassification(546).get_codes(select_level='3').data
# lev3_dict = landkoder.loc[landkoder.data['level'] == '3'][['code', 'parentCode']].set_index('code').to_dict()
# lev3_dict

def koble_landbakgrunn_546(df: pd.DataFrame, land_col: str = None) -> pd.DataFrame:
    if not land_col:
        raise ValueError("You need to specify column containing country codes in parameter 'land_col'.")
    landkoder = KlassClassification(546).get_codes(presentation_name_pattern='{code} {name}')

    lev3_dict = landkoder.loc[landkoder.data['level'] == '3'][['code', 'parentCode']].set_index('code').rename(columns={'parentCode' : 'land_3_to_2'}).to_dict()
    df['verdensdel']
    df['landegruppe']



def koble_landbakgrunn_old(df):
    landkat = KlassClassification(546)
    landkoder = landkat.get_codes(presentation_name_pattern='{code} {name}')
    landkoder.data

    land_dict = {}
    max_lev = landkoder.data['level'].astype('int').max()
    for n in range(1,max_lev+1):
        land_dict[f'land_{n}'] = landkat.get_codes(select_level=f'{n}', presentation_name_pattern='{code} {name}').to_dict()
    land_dict

    lev3 = landkoder.data.loc[landkoder.data['level'] == '3']
    lev3_dict = lev3[['code', 'parentCode']].set_index('code').rename(columns={'parentCode' : 'land_3_to_2'}).to_dict()
    lev3_dict['land_3_to_2']

    df['land_2'] = df['la'].map(lev3_dict['land_3_to_2'])

    df['land_1'] = df['land_2'].str[0:2]

    df.rename(columns={'land_2': 'verdensdel', 'land_1': 'landegruppe'}, inplace=True)

    vdel_mapping = {
    'G00': 'Abc', 
    'G11': 'UA',
    'G12': 'UB',
    'G13': 'UCA',
    'G21': 'UCB',
    'G14': 'UD',
    'G15': 'UD',
    'G25': 'UD',
    'G26': 'UD',
    'G23': '400',
    'G22': '2',
    'G24': '600sm'
    }
    df['atte_verdensregion'] = df['verdensdel'].map(vdel_mapping)
    
    # Opprette den nye kolonnen 'to_landgr' med de formaterte verdiene
    df['to_landgr'] = df['landegruppe'].apply(landgr_format)

    df['alle_land'] = "999"
    return df
