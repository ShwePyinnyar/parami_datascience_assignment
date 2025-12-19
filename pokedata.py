import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

st.set_page_config(page_title="Pokemon Stats Dashboard", layout="wide")
st.title("Gen 1-9 Pokemon Stats Interactive Dashboard")

# ------------------------
# Load Data
# ------------------------
df = pd.read_csv("pokedata.csv")
df = df.drop(['Capture_Rate', 'Base_Happiness', 'Is_Baby', 'Egg_Cycles', 'Past_Type'], axis=1)

# ------------------------
# Sidebar Filters
# ------------------------
st.sidebar.header("Filter Options")

primary_type = ["All"] + sorted(df['Type_1'].fillna('None').unique())
selected_primary_type = st.sidebar.selectbox("Select Primary Type", primary_type, index=0)

secondary_type = ["All"] + sorted(df['Type_2'].fillna('None').unique())
selected_secondary_type = st.sidebar.selectbox("Select Secondary Type", secondary_type, index=0)

legendary = ["All"] + df['Is_Legendary'].unique().tolist()
selected_legendary = st.sidebar.selectbox("Select Legendary or not", legendary, index=0)

mythical = ["All"] + df['Is_Mythical'].unique().tolist()
selected_mythical = st.sidebar.selectbox("Select Mythical or not", mythical, index=0)

generation = ["All"] + df['Generation'].unique().tolist()
selected_generation = st.sidebar.selectbox("Select Generation", generation, index=0)

# ------------------------
# Apply Filters
# ------------------------
filtered_df = df.copy()

if selected_primary_type != "All":
    filtered_df = filtered_df[filtered_df['Type_1'] == selected_primary_type]
if selected_secondary_type != "All":
    filtered_df = filtered_df[filtered_df['Type_2'] == selected_secondary_type]
if selected_legendary != "All":
    filtered_df = filtered_df[filtered_df['Is_Legendary'] == selected_legendary]
if selected_mythical != "All":
    filtered_df = filtered_df[filtered_df['Is_Mythical'] == selected_mythical]
if selected_generation != "All":
    filtered_df = filtered_df[filtered_df['Generation'] == selected_generation]

# ------------------------
# KPI Metrics
# ------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Pokemons", f"{filtered_df['id'].count()}")
col2.metric("Average Height(m)", f"{filtered_df['Height(m)'].mean():.2f}")
col3.metric("Average Weight(kg)", f"{filtered_df['Weight{kg}'].mean():.2f}")
col4.metric("Average Stats Total", f"{filtered_df['Total_Stats'].mean():.2f}")

st.markdown("---")

# ------------------------
# Descriptive Analysis
# ------------------------
st.subheader("📊 Descriptive Statistics")
st.dataframe(filtered_df[['HP','Attack','Defense','Sp.Atk','Sp.Def','Speed','Total_Stats']].describe().T)

# ------------------------
# Correlation Heatmap
# ------------------------
col1, = st.columns(1)
with col1:
    # ------------------------
    # Heatmap: Day vs Hour Sales
    # ------------------------
    st.subheader("Type and Restrited heatmap")

    filtered_df = filtered_df.copy()  # ensure safe copy for assignment
    filtered_df['Restricted'] = (
        filtered_df['Is_Legendary'] |
        filtered_df['Is_Mythical'] |
        filtered_df['Is_Pseudo_Legendary']
    )

    type1 = filtered_df[['Type_1', 'Restricted', 'id']].rename(columns={'Type_1': 'Type'})
    type2 = filtered_df[['Type_2', 'Restricted', 'id']].rename(columns={'Type_2': 'Type'})
    types_combined = pd.concat([type1, type2], ignore_index=True)
    types_combined = types_combined.dropna(subset=['Type'])

    heatmap_data = types_combined.groupby(['Type','Restricted']).size().reset_index(name='Count')
    heatmap_matrix = heatmap_data.set_index(['Type','Restricted'])['Count'].unstack(fill_value=0).sort_index()
    fig_heatmap = px.imshow(
        heatmap_matrix,
        text_auto=True,
        color_continuous_scale='Blues',
        labels=dict(x="Restricted", y="Type", color="Pokémon Count"),
        title="Pokémon Type vs Restricted Status"
    )

    st.plotly_chart(fig_heatmap)

# ------------------------
# Total Sales Bar Chart by Product Line
# ------------------------
st.subheader("Total Pokemon per Type")
pokemon_per_type = types_combined.groupby("Type").size().reset_index(name='Total_Pokemon')
fig_bar = px.bar(
    pokemon_per_type,
    x="Type",
    y="Total_Pokemon",
    color="Type",
    text="Total_Pokemon",
    title="Total Pokemon per Type"
)
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar)

# ------------------------
# Show Filtered Data
# ------------------------
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df)
