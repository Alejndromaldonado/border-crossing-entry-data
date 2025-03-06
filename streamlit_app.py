import streamlit as st
import pandas as pd
import plotly.express as px

# -------------Configuración de la página-------------------------
st.set_page_config(page_title="Border Crossing Dashboard", layout="wide")

# ----------------------Cargar datos------------------------------------------
file_id= "1OpJLbDAxCBT8dDwOBZeBHNSoCAplvkhO"# Ajusta el id del archivo
csv_url= f"https://drive.google.com/uc?id={file_id}" 
df_chunks = pd.read_csv(csv_url, chunksize=10000)    
# Unir los bloques en un solo DataFrame  
df_raw = pd.concat(df_chunks, ignore_index=True) 
df = df_raw.copy()


st.sidebar.image("assets/logo_usa.png", use_container_width=False)
# Sidebar - Filtros
st.sidebar.header("Filters")
selected_years = st.sidebar.slider("Select the range", int(df["Year"].min()), int(df["Year"].max()), (int(df["Year"].min()), int(df["Year"].max())))
selected_border = st.sidebar.multiselect("Select a border", df["Border"].unique(), default=df["Border"].unique())
st.sidebar.markdown("")  
st.sidebar.markdown("") 
st.sidebar.markdown("")  
st.sidebar.markdown("") 
st.sidebar.markdown("")  
st.sidebar.markdown("") 
st.sidebar.markdown("")  
st.sidebar.markdown("")
st.sidebar.markdown("""
Created by:  
**Alejandro Maldonado**  
_Data Analyst_
                    """)
st.sidebar.markdown("""
    <a href="https://www.linkedin.com/in/alejandromaldonadod4t4/" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="20" height="20">
</a>""", unsafe_allow_html=True
)

# Filtrar datos
df_filtered = df[(df["Year"] >= selected_years[0]) & (df["Year"] <= selected_years[1]) & (df["Border"].isin(selected_border))]


# Título
st.title("🇺🇸 Border Crossing Entry Data")
st.markdown("""
### Analysis of Border Traffic Unbundling

This analysis examines the unbundling of traffic at the northern and southern U.S. borders and its variation over time. The data provide insights into different modes of transportation, including trucks, trains, containers, buses, personal vehicles, passengers, and pedestrians.

#### Data Source:
The data are sourced from the **Bureau of Transportation Statistics (BTS)**, which compiles inbound crossing statistics at U.S.-Canada and U.S.-Mexico ports of entry. These data, collected by **U.S. Customs and Border Protection (CBP)**, reflect the number of vehicles, containers, passengers, or pedestrians entering the U.S. However, outbound traffic data are not included.

For more details, visit the official dataset:  
[Border Crossing Entry Data](https://data.bts.gov/Research-and-Statistics/Border-Crossing-Entry-Data/keg4-3bc2/about_data)
""")

st.divider()
# KPIs
col1, col2, col3 = st.columns(3)
col1.markdown(
    f"""
    <div style="
        background-color: white;
        padding: 15px;
        margin: 10px 0px 10px 0px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    ">
        Total Records<br> 
        <span style="font-size: 27px; color: #000000 ;">{df_filtered['Value'].sum():,}</span>
    </div>
    """, 
    unsafe_allow_html=True
)
col2.markdown(
    f"""
    <div style="
        background-color: white;
        padding: 15px;
        margin: 10px 0px 10px 0px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    ">
        Analyzed Borders<br> 
        <span style="font-size: 27px; color: #000000 ;">{len(df_filtered["Border"].unique())}</span>
    </div>
    """, 
    unsafe_allow_html=True
)
col3.markdown(
    f"""
    <div style="
        background-color: white;
        padding: 15px;
        margin: 10px 0px 10px 0px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    ">
        Types of Transport<br> 
        <span style="font-size: 27px; color: #000000 ;">{len(df_filtered["Measure"].unique())}</span>
    </div>
    """, 
    unsafe_allow_html=True
)


# Gráfico 1 - Mapa de tráfico
geo_transport = df_filtered.groupby(["State", "Measure", "Latitude", "Longitude"])["Value"].sum().reset_index()

fig1 = px.scatter_map(geo_transport, 
                     lat="Latitude", 
                     lon="Longitude", 
                     size="Value",
                     size_max=70, 
                     color="Measure", 
                     hover_name="State",
                     zoom=2,
                     title="Geographic Distribution of Traffic by Type of Transport",
                     map_style="carto-darkmatter",
                     color_discrete_sequence=px.colors.qualitative.Bold,
                     )
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2 - Tendencia durante los años
year_count = df_filtered.groupby(["Year", "Border"])["Value"].sum().reset_index(name="Value").sort_values(by="Year", ascending=False)

fig2 = px.line(year_count, 
                x="Year", 
                y="Value", 
                color="Border",
                color_discrete_sequence=px.colors.qualitative.Bold,
                title=f"Records between {selected_years[0]}-{selected_years[1]}")

fig2.update_layout(
    paper_bgcolor="White",
    plot_bgcolor="White",
    yaxis_title="Records",
    xaxis_title="Year"
)
fig2.update_traces(mode="lines+markers"
                  )

# Gráfico 3 - Tendencia mensual
month_count = df_filtered.groupby(["Month", "Border"])["Value"].sum().reset_index(name="Value").sort_values(by="Month", ascending=True)
dict_meses = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
month_count["Month"] = month_count["Month"].map(dict_meses)

fig3 = px.line(month_count, 
                x="Month", 
                y="Value", 
                color="Border",
                color_discrete_sequence=px.colors.qualitative.Bold,
                title=f"Monthly trend of border crossing {selected_years[0]}-{selected_years[1]}")
fig3.update_layout(
    paper_bgcolor="White",
    plot_bgcolor="White",
    yaxis_title="Records",
)
fig3.update_traces(mode="lines+markers", 
                  )

col1, col2 = st.columns(2)
col1.plotly_chart(fig2, use_container_width=True)
col2.plotly_chart(fig3, use_container_width=True)

# Gráfico 4 - Puertos de entrada con mayor flujo segun modalida de transporte
bc_ports= df_filtered.groupby(["Measure", "Port Name"])["Value"].sum().reset_index(name="Value").sort_values(by="Value", ascending=False)
most_congested_ports = bc_ports.loc[bc_ports.groupby("Measure")["Value"].idxmax()].sort_values(by="Value", ascending=False)

fig4 = px.bar(most_congested_ports, 
            x="Port Name", 
            y="Value", 
            color="Measure", 
            color_discrete_sequence=px.colors.qualitative.Bold,
            title=f"Ports of Entry with the Highest Traffic Flow by Mode of Transport <br> {selected_years[0]}-{selected_years[1]}",)
fig4.update_layout(
    paper_bgcolor="White",
    plot_bgcolor="White",
    yaxis_title="Records",
)

# Gráfico 5 - Evolución de cruces por año
filter_trucks = df_filtered[df_filtered["Measure"].isin(["Trucks", "Truck Containers Empty", "Truck Containers Loaded"])]
trucks_count = filter_trucks.groupby(["Year", "Border", "Measure"])["Value"].sum().reset_index(name="Value").sort_values(by="Year", ascending=False)
fig5 = px.line(trucks_count, 
                x="Year", 
                y="Value", 
                color="Measure",
                facet_col="Border",
                color_discrete_sequence=px.colors.qualitative.Bold,
                title=f"Evolution of truck traffic between {selected_years[0]}-{selected_years[1]}")
fig5.update_layout(
    paper_bgcolor="White",
    plot_bgcolor="White",
    yaxis_title="Records",
)
fig5.update_traces(mode="lines+markers", 
                  )

col1, col2 = st.columns(2)
col1.plotly_chart(fig4, use_container_width=True)
col2.plotly_chart(fig5, use_container_width=True)



# Notas
st.info("This dashboard is optimized for interactive analysis, allowing users to explore trends, filter data by various criteria, and visualize traffic patterns at the northern and southern U.S. borders over time. It provides dynamic tools to break down information by transportation type, port of entry, and analysis period, facilitating data-driven decision-making.")
