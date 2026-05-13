import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from recommendation import build_graph, User, RecommendationEngine, PopularityBiasAnalyzer, DiversityStrategy

st.set_page_config(page_title="Music Recommendation System", page_icon="🎵")

st.title("Music Recommendation System")
st.caption("PTIA Project — Daniel Rayo, Ángela Gómez")
st.markdown("This system reduces **popularity bias** in music recommendations using an artist graph and a diversity strategy.")

graph, all_artists = build_graph()
artist_dict = {a.name: a for a in all_artists}

st.sidebar.header("🎧 Your music profile")
selected_names = st.sidebar.multiselect(
    "Select the artists you listen to:",
    options=sorted(artist_dict.keys()),
    default=["Taylor Swift", "Ariana Grande"]
)

if not selected_names:
    st.warning("Select at least one artist from the left panel.")
    st.stop()

selected_artists = [artist_dict[name] for name in selected_names]
user = User(id="u1", name="User", listening_history=selected_artists)

engine   = RecommendationEngine(graph)
analyzer = PopularityBiasAnalyzer()
strategy = DiversityStrategy()

biased     = engine.generate_biased_recommendations(user)
candidates = engine.generate_recommendations(user)
diverse    = strategy.apply_diversity(candidates)

bias_before = analyzer.detect_bias(biased)
bias_after  = analyzer.detect_bias(diverse)

st.subheader("Popularity bias comparison")

col1, col2 = st.columns(2)
col1.metric("Average WITHOUT diversity", f"{bias_before:.3f}")
col2.metric("Average WITH diversity", f"{bias_after:.3f}",
            delta=f"{bias_after - bias_before:.3f}")

st.subheader("Music Recommendations")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Without diversity** (biased)")
    for a in biased:
        st.write(f"- {a.name} — popularity: `{a.popularity_score}`")

with col4:
    st.markdown("**With diversity** (corrected)")
    for a in diverse:
        st.write(f"- {a.name} — popularity: `{a.popularity_score}`")

st.subheader("Artist graph")

G = nx.Graph()
for artist in all_artists:
    G.add_node(artist.name, popularity=artist.popularity_score)
for artist, neighbors in graph.relationships.items():
    for neighbor in neighbors:
        G.add_edge(artist.name, neighbor.name)

node_colors = [
    "red" if next((a for a in all_artists if a.name == n), None).popularity_score > 0.8
    else "steelblue"
    for n in G.nodes()
]

fig, ax = plt.subplots(figsize=(10, 7))
nx.draw(G, with_labels=True, node_color=node_colors,
        node_size=900, font_size=8, ax=ax)
st.pyplot(fig)

st.caption("🔴 Mainstream artists   🔵 Emerging artists")