from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)

map_options = GMapOptions(lat=40, lng=-100, map_type="roadmap", zoom=4)

plot1 = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, \
    plot_width = 1200, width = 1200, plot_height = 700 ,height = 700
)

plot2 = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, \
    plot_width = 1200, width = 1200, plot_height = 700 ,height = 700
)

plot1.title.text = "Expedia Data Visualization: Users who booked a hotel"
plot2.title.text = "Expedia Data Visualization: Users who did not book a hotel"

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:

# Getting API key from external text file
api_key_file = open('google_maps_api_key.txt', 'r')
api_key_file_lines = api_key_file.readlines()
api_key = api_key_file_lines[0]
api_key_file.close()

# Setting API key
plot1.api_key = api_key
plot2.api_key = api_key

# Read columns for lat and long from data.txt file
# MAKE SURE WE CHANGE THIS _SHORT TO THE FULL VERSION WHEN TESTING IS DONE
data_file = open('world_mobile_locations_short.csv', 'r')
csv_lines = data_file.readlines()
header_row = csv_lines[0]
lat_index = header_row.split('\t').index('"user_location_latitude"') + 1
lon_index = header_row.split('\t').index('"user_location_longitude"') + 1
mobile_index = header_row.split('\t').index('"is_mobile"') + 1
booking_index = header_row.split('\t').index('"is_booking"\n') + 1

# Filter out lines in CSV into:
#   1. users who booked a hotel (or package)
#   2. users who did not book a hotel (or package)

lat_array_book = []
lon_array_book = []
lat_array_no_book = []
lon_array_no_book = []
lat_mobile_array_book = []
lon_mobile_array_book = []
lat_mobile_array_no_book = []
lon_mobile_array_no_book = []

for line in csv_lines[1:-1]:
    line = line.split('\t')
    # split the lines into mobile and not mobile
    # 1 if on mobile, 0 otherwise
    if '1' in line[mobile_index].replace('"', ''):
        if '1' in line[booking_index].replace('"', ''):
            lat_mobile_array_book.append(line[lat_index].replace('"', ''))
            lon_mobile_array_book.append(line[lon_index].replace('"', ''))
        else:
            lat_mobile_array_no_book.append(line[lat_index].replace('"', ''))
            lon_mobile_array_no_book.append(line[lon_index].replace('"', ''))

    else:
        if '1' in line[booking_index].replace('"', ''):
            lat_array_book.append(line[lat_index].replace('"', ''))
            lon_array_book.append(line[lon_index].replace('"', ''))
        else:
            lat_array_no_book.append(line[lat_index].replace('"', ''))
            lon_array_no_book.append(line[lon_index].replace('"', ''))

# Define latitude and longitude
source_non_mobile1 = ColumnDataSource(
    data=dict(
        lat=lat_array_book,
        lon=lon_array_book,
    )
)

source_non_mobile2 = ColumnDataSource(
    data=dict(
        lat=lat_array_no_book,
        lon=lon_array_no_book,
    )
)

source_mobile1 = ColumnDataSource(
    data=dict(
        lat=lat_mobile_array_book,
        lon=lon_mobile_array_book,
    )
)

source_mobile2 = ColumnDataSource(
    data=dict(
        lat=lat_mobile_array_no_book,
        lon=lon_mobile_array_no_book,
    )
)

# NON MOBILE
# BLUE
#pink FF72A8
circle1 = Circle(x="lon", y="lat", size=10, fill_color="#FF72A8", fill_alpha=0.3, line_color=None)
# MOBILE
# GREEN
# blue 599ACC
circle2 = Circle(x="lon", y="lat", size=10, fill_color="#599ACC", fill_alpha=0.3, line_color=None)

plot1.add_glyph(source_non_mobile1, circle1)
plot1.add_glyph(source_mobile1, circle2)

plot2.add_glyph(source_non_mobile2, circle1)
plot2.add_glyph(source_mobile2, circle2)

plot1.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
plot2.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")
show(plot1)
show(plot2)