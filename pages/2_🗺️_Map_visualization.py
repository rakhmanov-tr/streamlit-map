import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.features import CustomIcon

# Загрузка данных
@st.cache_resource
def load_data():
    data = pd.read_csv("data/data.tsv", sep='\t')
    return data

# Функция для фильтрации данных
def filter_column_like_geo(column, values):
    if values and values != 'Select':
        if isinstance(values, list):  # если values - список
            return data[data[column].isin(values)]
        else:  # если values - одиночное значение
            return data[data[column] == values]
    return data

# Функция для склонения слова
def get_declension_word(n):
    return 'sample' if n == 1 else 'samples'

data = load_data()

st.title('🗺️Interactive map')


# Фильтрация данных по глубине
filtered_depth_data = data[(data['depth'] != 'unknown') & (data['depth'] != 'None')]
filtered_depth_data['depth'] = filtered_depth_data['depth'].astype(float)
min_depth, max_depth = st.sidebar.slider(
    'Select the depth range',
    float(filtered_depth_data['depth'].min()),
    float(filtered_depth_data['depth'].max()),
    [float(filtered_depth_data['depth'].min()), float(filtered_depth_data['depth'].max())]
)

# Множественный выбор для процесса исследования
unique_processes = sorted(data['study_process'].dropna().unique().tolist())
selected_processes = st.sidebar.multiselect(
    "Select the research process",
    unique_processes,
    default=unique_processes
)

# Проверка выбора процесса исследования
if not selected_processes:
    selected_processes = unique_processes
    st.warning('At least one research process must be selected.')
    st.experimental_rerun()

# Применение фильтров к данным
filtered_data = filter_column_like_geo('study_process', selected_processes)
filtered_data['depth'] = pd.to_numeric(filtered_data['depth'], errors='coerce')  # Преобразование в числовой формат
filtered_data = filtered_data[(filtered_data['depth'] >= min_depth) & (filtered_data['depth'] <= max_depth)]
filtered_data = pd.concat([filtered_data, data[data['depth'].isin(['unknown', 'None'])]])
filtered_data['latitude'] = pd.to_numeric(filtered_data['latitude'], errors='coerce')
filtered_data['longitude'] = pd.to_numeric(filtered_data['longitude'], errors='coerce')
filtered_data = filtered_data.dropna(subset=['latitude', 'longitude'])

# Вывод количества отобранных строк
n_samples = len(filtered_data)
verb = "was" if n_samples == 1 else "were"
st.write(f'{n_samples} {get_declension_word(n_samples)} {verb} selected')

# Создание карты с folium
m = folium.Map(
    location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()],
    zoom_start=2,
    tiles="http://services.arcgisonline.com/arcgis/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}",
    attr="© OpenStreetMap contributors"
)

# Добавление маркеров на карту
for _, row in filtered_data.iterrows():
    popup_content = f"""
    <div>
        <strong>Archive Project:</strong> {row['archive_project']}<br>
        <a href="https://www.ncbi.nlm.nih.gov/search/all/?term={row['archive_project']}" target="_blank">NCBI Link</a>
    </div>
    """
    popup = folium.Popup(popup_content, max_width=300)
    icon = CustomIcon(
        icon_image="assets/marker/oil_marker.png",  # Замените на URL или локальный путь к вашей картинке маркера
        icon_size=(30, 30)  # Установите размер иконки в зависимости от размеров вашей картинки
    )
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=popup,
        icon=icon
    ).add_to(m)

# Отображение карты в Streamlit
folium_static(m)
