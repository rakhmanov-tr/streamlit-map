import streamlit as st
import pandas as pd
import numpy as np

# Загрузка данных
@st.cache_resource
def load_data():
    data = pd.read_csv('data/data.tsv', sep='\t')
    return data

df = load_data()

st.title('🗂️Data display')

# Фильтрация данных
st.sidebar.header('Filters')

# Функция для фильтрации данных по выбранной колонке и значению
def filter_column_like_geo(column, values):
    if values and values != 'Select':
        if isinstance(values, list):  # если values - список
            return df[df[column].isin(values)]
        else:  # если values - одиночное значение
            return df[df[column] == values]
    return df

def filter_column_like_depth(df, column_name, display_name=None):
    # Если display_name не предоставлено, используем column_name
    display_name = display_name or column_name
    
    min_value = df[column_name].replace(['None', 'unknown'], np.nan).dropna().astype(float).min()
    max_value = df[column_name].replace(['None', 'unknown'], np.nan).dropna().astype(float).max()
    selected_values = st.sidebar.slider(display_name, float(min_value), float(max_value), (float(min_value), float(max_value)))

    include_none = st.sidebar.checkbox(f'Include None in {display_name}', value=True)
    include_unknown = st.sidebar.checkbox(f'Include unknown in {display_name}', value=True)

    condition = (df[column_name].replace(['None', 'unknown'], np.nan).astype(float) >= selected_values[0]) & \
                (df[column_name].replace(['None', 'unknown'], np.nan).astype(float) <= selected_values[1])

    if include_none:
        condition = condition | (df[column_name] == 'None')
    if include_unknown:
        condition = condition | (df[column_name] == 'unknown')

    return df[condition]

def filter_column_like_api(df, column_name, display_name=None):
    # Если display_name не предоставлено, используем column_name
    display_name = display_name or column_name
    
    # Преобразование в числовой формат, где это возможно
    df_temp = df[column_name].replace(['None', 'unknown'], np.nan).dropna()
    df_temp = pd.to_numeric(df_temp, errors='coerce')
    
    min_value = int(df_temp.min())
    max_value = int(df_temp.max())

    selected_values = st.sidebar.slider(display_name, min_value, max_value, (min_value, max_value))

    include_none = st.sidebar.checkbox(f'Include None in {display_name}', value=True)
    include_unknown = st.sidebar.checkbox(f'Include unknown in {display_name}', value=True)

    condition = (pd.to_numeric(df[column_name], errors='coerce') >= selected_values[0]) & \
                (pd.to_numeric(df[column_name], errors='coerce') <= selected_values[1])

    if include_none:
        condition = condition | (df[column_name] == 'None')
    if include_unknown:
        condition = condition | (df[column_name] == 'unknown')

    return df[condition]

# Функция для склонения слова
def get_declension_word(n):
    return 'sample' if n == 1 else 'samples'


# publication_year - slider
min_year = int(df['publication_year'].min())
max_year = int(df['publication_year'].max())
selected_years = st.sidebar.slider('Year of publication', min_year, max_year, (min_year, max_year))
df = df[(df['publication_year'] >= selected_years[0]) & (df['publication_year'] <= selected_years[1])]

# geo_loc_name - multiselect
locations = sorted(df['geo_loc_name'].dropna().unique().tolist())
selected_locations = st.sidebar.multiselect('Country where samples were taken', locations)
df = filter_column_like_geo('geo_loc_name', selected_locations)

# study_primary_focus - multiselect
focuses = sorted(df['study_primary_focus'].dropna().unique().tolist())
selected_focus = st.sidebar.multiselect('Focus of the research', focuses)
df = filter_column_like_geo('study_primary_focus', selected_focus)

# study_process - multiselect
processes = sorted(df['study_process'].dropna().unique().tolist())
selected_process = st.sidebar.multiselect('Biochemical process that is studied', processes)
df = filter_column_like_geo('study_process', selected_process)

# depth likely - slider and checkboxes
df = filter_column_like_depth(df, 'depth', 'Sampling depth')
df = filter_column_like_depth(df, 'temp', 'Temperature')
df = filter_column_like_depth(df, 'pH')
df = filter_column_like_depth(df, 'salinity', 'Salinity')

# API - slider and checkboxes
df = filter_column_like_api(df, 'API', 'API gravity')

# depth likely - slider and checkboxes
df = filter_column_like_depth(df, 'NO3-', 'Concentration of NO₃⁻')
df = filter_column_like_depth(df, 'PO43-', 'Concentration of PO₄³⁻')
df = filter_column_like_depth(df, 'SO42-', 'Concentration of SO₄²⁻')
df = filter_column_like_depth(df, 'Ca2+', 'Concentration of Ca²⁺')
df = filter_column_like_depth(df, 'Mg2+', 'Concentration of Mg²⁺')
df = filter_column_like_depth(df, 'Na+', 'Concentration of Na⁺')
df = filter_column_like_depth(df, 'K+', 'Concentration of K⁺')
df = filter_column_like_depth(df, 'Cl-', 'Concentration of Cl⁻')
df = filter_column_like_depth(df, 'HCO3-', 'Concentration of HCO₃⁻')
df = filter_column_like_depth(df, 'acetate', 'Concentration of acetate')

# feature - multiselect
processes = sorted(df['feature'].dropna().unique().tolist())
selected_process = st.sidebar.multiselect('Medium description', processes)
df = filter_column_like_geo('feature', selected_process)

# material - multiselect
processes = sorted(df['material'].dropna().unique().tolist())
selected_process = st.sidebar.multiselect('Sample type for DNA isolation', processes)
df = filter_column_like_geo('material', selected_process)

# collection_date - slider and checkboxes
df = filter_column_like_api(df, 'collection_date', 'Date of sample collection')

# archive - multiselect
processes = sorted(df['archive'].dropna().unique().tolist())
selected_process = st.sidebar.multiselect('Archive of library data', processes)
df = filter_column_like_geo('archive', selected_process)

# Вывод количества отобранных строк
n_samples = len(df)  # Используется df вместо filtered_data
verb = "was" if n_samples == 1 else "were"
st.write(f'{n_samples} {get_declension_word(n_samples)} {verb} selected')

# Отображение данных
st.dataframe(df)

st.download_button(
    label="Download data",
    data=df.to_csv(sep='\t', index=False).encode(),
    file_name="data.tsv",
    mime="text/tab-separated-values"
)