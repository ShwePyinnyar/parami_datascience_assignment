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

primary_type = ["All"] + sorted(df['Type_1'].unique())
selected_primary_type = st.sidebar.selectbox("Select Primary Type", primary_type, index=0)

secondary_type = ["All"] + sorted(df['Type_2'].unique())
selected_secondary_type = st.sidebar.selectbox("Select Secondary Type", secondary_type, index=0)

legendary = ["All"] + df['Is_Legendary'].unique().tolist()
selected_legendary = st.sidebar.selectbox("Select Legendary or not", legendary, index=0)

mythical = ["All"] + df['Is_Mythical'].unique().tolist()
selected_mythical = st.sidebar.selectbox("Select Mythical or not", mythical, index=0)

genetation = ["All"] + df['Generation'].unique().tolist()
selected_genetation = st.sidebar.selectbox("Select Generation", genetation, index=0)


# ------------------------
# Apply Filters
# ------------------------
filtered_df = df.copy()

if primary_type != "All":
    filtered_df = filtered_df[filtered_df['Type_1'] == primary_type]
if secondary_type != "All":
    filtered_df = filtered_df[filtered_df['Type_2'] == secondary_type]
if legendary != "All":
    filtered_df = filtered_df[filtered_df['Is_Legendary'] == legendary]
if mythical != "All":
    filtered_df = filtered_df[filtered_df['Is_Mythical'] == mythical]
if genetation != "All":
    filtered_df = filtered_df[filtered_df['Generation'] == genetation]


# ------------------------
# KPI Metrics
# ------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Pokemons", f"${filtered_df['id'].count()}")
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

    filtered_df['Restricted'] = (
    (filtered_df['Is_Legendary'] == True) |
    (filtered_df['Is_Mythical'] == True) |
    (filtered_df['Is_Pseudo_Legendary'] == True)
    )
    type1 = filtered_df[['Type_1', 'Restricted', 'id']].rename(columns={'Type_1': 'Type'})
    type2 = filtered_df[['Type_2', 'Restricted', 'id']].rename(columns={'Type_2': 'Type'})
    types_combined = pd.concat([type1, type2], ignore_index=True)
    types_combined = types_combined.dropna(subset=['Type'])

    heatmap_data = types_combined.groupby(['Type','Restricted']).size().reset_index(name='Count')
    heatmap_matrix = ( heatmap_data.set_index(['Type', 'Restricted'])['Count'].unstack(fill_value=0))
    fig_heatmap = px.imshow(heatmap_matrix, text_auto=True, color_continuous_scale='Blues', labels=dict( x="Restricted", y="Type", color="Pokémon Count"), title="Pokémon Type vs Restricted Status")

    st.plotly_chart(fig_heatmap)
    
# ------------------------
# Total Sales Bar Chart by Product Line
# ------------------------
st.subheader("Total Pokemon per Type")
pokemon_per_type = types_combined.groupby("Type").size().reset_index(name='Total_Pokemon')
fig_bar = px.bar(pokemon_per_type, x="Type", y="Total_Pokemon", color="Type", text="Total_Pokemon", title="Total Pokemon per Type")
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar)

# ------------------------
# Show Filtered Data
# ------------------------
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df)





























