from data_understanding import data_clean
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10
from bokeh.io import output_file
import numpy as np
import pandas as pd

"""create dataframe from the columns needed in the graph"""
price_sqft_living = ['price', 'sqft_living', 'bedrooms']
df = data_clean[price_sqft_living]

"""specify the dataframe as the source for Bokeh"""
source = ColumnDataSource(df)

"""sort bedroom categories numerically"""
bedroom_categories = sorted(df["bedrooms"].unique())

"""output to HTML file"""
output_file("scatter_price_sqft_bedrooms_sorted.html")

"""create figure"""
p = figure(
    title="House Price vs. Living Area (Bedrooms Sorted Ascending)",
    x_axis_label="Living Area (sqft)",
    y_axis_label="Price (USD)",
    tools="pan,wheel_zoom,box_zoom,reset,save",
    sizing_mode="stretch_width",
    height=500
)

"""assign colors from palette"""
palette = Category10[max(3, len(bedroom_categories))]

"""plot each bedroom category separately to control legend order"""
for i, b in enumerate(bedroom_categories):
    subset = df[df["bedrooms"] == b]
    source = ColumnDataSource(subset)
    p.scatter(
        x="sqft_living",
        y="price",
        size=8,
        color=palette[i % len(palette)],
        alpha=0.7,
        source=source,
        legend_label=str(b)  # Legend label as string
    )

"""add hover tooltips"""
hover = HoverTool(tooltips=[
    ("Sqft Living", "@sqft_living"),
    ("Price", "@price{$0,0}"),
    ("Bedrooms", "@bedrooms")
])
p.add_tools(hover)

"""style legend"""
p.legend.title = "Bedrooms"
p.legend.location = "top_left"
p.legend.click_policy = "hide"  # Allow toggling categories

"""show plot"""
show(p)

"""replaces year built with the decade the property was built"""
data_clean['yr_built'] = (data_clean['yr_built'] // 10 * 10).astype(str) + 's'

print(data_clean['yr_built'])

"""define bins and labels"""
bins = [-np.inf, 1, 2, 3, 4, np.inf]
labels = [
    "x ≤ 1",
    "1 < x ≤ 2",
    "2 < x ≤ 3",
    "3 < x ≤ 4",
    "x > 4"
]

"""replace values with category labels"""
data_clean['number of bathrooms'] = pd.cut(data_clean['bathrooms'], bins=bins, labels=labels, right=True)

print(data_clean['number of bathrooms'])

"""count occurrences per decade and bathroom count"""
counts = data_clean.groupby(["yr_built", "number of bathrooms"]).size().unstack(fill_value=0)

"""make sure of consistent order of decades"""
decades = sorted(counts.index.tolist())

"""prepare Bokeh data source"""
source = ColumnDataSource(data=dict(
    decade=decades,
    **{str(b): counts[b].tolist() for b in counts.columns}
))

"""bathroom categories as list of strings"""
bathroom_categories = [str(b) for b in counts.columns]

"""create figure"""
p = figure(
    x_range=decades,
    height=400,
    width=600,
    title="Stacked Bar Chart: Count by Decade and Number of Bathrooms",
    toolbar_location=None,
    tools="hover",
    tooltips="$name: @$name"
)

"""stack bars"""
p.vbar_stack(
    bathroom_categories,
    x='decade',
    width=0.8,
    color=Category10[len(bathroom_categories)],
    source=source,
    legend_label=[f"{b} bathrooms" for b in bathroom_categories]
)

"""adjust"""
p.y_range.start = 0
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "vertical"

"""show plot"""
show(p)
