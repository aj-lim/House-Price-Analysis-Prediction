from data_understanding import df
import matplotlib.pyplot as plt
import seaborn as sns
import math
import plotly_express as px
import requests

"""create correlation matrix from all numerical features"""
numerical_columns = ['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view',
                     'condition', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zip']
df_wo_street_city = df[numerical_columns]
correlation_matrix = df_wo_street_city.corr(method='pearson')
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, annot_kws={"size": 6})
plt.xticks(fontsize=8, rotation=45, ha='right')
plt.yticks(fontsize=8, rotation=0)
plt.title('Correlations Between Numerical Features')
plt.show()

"""create histograms for all numerical features"""
num_cols = len(numerical_columns)

# Layout: 5 histograms per row
cols_per_row = 5
rows = math.ceil(num_cols / cols_per_row)

fig, axes = plt.subplots(rows, cols_per_row, figsize=(cols_per_row * 4, rows * 3))
axes = axes.flatten()  # Flatten to 1D array for easy indexing

# Plot each histogram
for i, col in enumerate(numerical_columns):
    axes[i].hist(df_wo_street_city[col], bins=15, color='#86bf91', edgecolor='black')
    axes[i].set_title(col)
    axes[i].grid(axis='y', linestyle='--', alpha=0.7)

# Hide any unused subplots
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

fig.suptitle("Histograms for All Numerical Columns (5 per row)", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

"""create choropleth to show prices across zip codes"""
geojson_url = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/wa_washington_zip_codes_geo.min.json"

try:
    response = requests.get(geojson_url)
    response.raise_for_status()
    wa_zip_geojson = response.json()
except requests.RequestException as e:
    print(f"Error fetching GeoJSON: {e}")
    exit(1)

zip_codes = [feature["properties"]["ZCTA5CE10"] for feature in wa_zip_geojson["features"]]

fig = px.choropleth_mapbox(
    df,
    geojson=wa_zip_geojson,
    locations="zip",
    color="price",
    featureidkey="properties.ZCTA5CE10",  # matches GeoJSON property
    color_continuous_scale="Viridis",
    range_color=[300000, 500000],
    mapbox_style="carto-positron",
    zoom=5.5,
    center={"lat": 47.5, "lon": -120.5},  # Center of Washington State
    opacity=0.6,
    labels={"price": "Price"}
)

fig.update_layout(
    title="Washington State ZIP Code Choropleth",
    margin={"r":0, "t":40, "l":0, "b":0}
)

fig.show()
