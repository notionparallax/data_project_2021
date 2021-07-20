from shapely.geometry import Point
import geopandas as gpd

pnt1 = Point(80.99456, 7.86795)
pnt2 = Point(80.97454, 7.872174)
points_df = gpd.GeoDataFrame({"geometry": [pnt1, pnt2]}, crs="EPSG:4326")
points_df = points_df.to_crs("EPSG:5234")
points_df2 = points_df.shift()  # We shift the dataframe by 1 to align pnt1 with pnt2
points_df.distance(points_df2)
