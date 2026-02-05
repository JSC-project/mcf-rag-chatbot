import streamlit as st
from pathlib import Path
import geopandas as gpd
import pydeck as pdk

#With ALOT of help from ChatGpt
st.set_page_config(page_title="Skyddsrumskarta", layout="wide")
st.title("Skyddsrum i Sverige 🛡️")

GPKG_PATH = Path(__file__).parents[2] / "data" / "shelters" / "Skyddsrum_EPSG3006.gpkg"

@st.cache_data
def load_shelters(path: Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    # GeoPackage från MSB är i EPSG:3006 → gör om till lat/lon (EPSG:4326) för webbkarta
    gdf = gdf.to_crs(epsg=4326)
    # plocka ut koordinater
    gdf["lon"] = gdf.geometry.x
    gdf["lat"] = gdf.geometry.y
    return gdf

if not GPKG_PATH.exists():
    st.error(f"Hittar inte filen: {GPKG_PATH}")
    st.stop()

gdf = load_shelters(GPKG_PATH)
st.caption(f"Antal skyddsrum: {len(gdf):,}")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=gdf,
    get_position="[lon, lat]",
    get_radius=20,
    get_fill_color=[255, 0, 0],   # R, G, B
    get_line_color=[255, 255, 255],
)

view_state = pdk.ViewState(latitude=62.0, longitude=15.0, zoom=4.2)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Skyddsrum"},
    ),
    use_container_width=True,
)
