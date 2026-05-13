class Artist:
    def __init__(self, id: str, name: str, genre: str, popularity_score: float):
        self.id = id
        self.name = name
        self.genre = genre
        self.popularity_score = popularity_score


class User:
    def __init__(self, id: str, name: str, listening_history: list):
        self.id = id
        self.name = name
        self.listening_history = listening_history

    def get_preferences(self):
        return self.listening_history


class MusicGraph:
    def __init__(self):
        self.artists = []
        self.relationships = {}

    def add_artist(self, artist):
        self.artists.append(artist)
        self.relationships[artist] = []

    def add_relationship(self, artist1, artist2):
        if artist1 in self.relationships:
            self.relationships[artist1].append(artist2)
        if artist2 in self.relationships:
            self.relationships[artist2].append(artist1)

    def get_related_artists(self, artist):
        return self.relationships.get(artist, [])


class RecommendationEngine:
    def __init__(self, graph):
        self.graph = graph

    def generate_recommendations(self, user):
        scores = {}
        for artist in user.get_preferences():
            neighbors = self.graph.get_related_artists(artist)
            for neighbor in neighbors:
                if neighbor not in scores:
                    scores[neighbor] = 0
                scores[neighbor] += 1
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [a for a, s in ranked]

    def generate_biased_recommendations(self, user, top_k=5):
        scores = {}
        for artist in user.get_preferences():
            neighbors = self.graph.get_related_artists(artist)
            for neighbor in neighbors:
                if neighbor not in scores:
                    scores[neighbor] = 0
                scores[neighbor] += 1
        ranked = sorted(
            scores.items(),
            key=lambda x: x[1] + (2.0 * x[0].popularity_score),
            reverse=True
        )
        return [a for a, s in ranked[:top_k]]


class PopularityBiasAnalyzer:
    def detect_bias(self, recommendations):
        if not recommendations:
            return 0
        return sum(a.popularity_score for a in recommendations) / len(recommendations)


class DiversityStrategy:
    def apply_diversity(self, recommendations, top_k=5, max_popular=1, popularity_threshold=0.8):
        emerging = [a for a in recommendations if a.popularity_score < popularity_threshold]
        popular  = [a for a in recommendations if a.popularity_score >= popularity_threshold]
        final = emerging[:(top_k - max_popular)] + popular[:max_popular]
        return final[:top_k]


def build_graph():
    # Mainstream artists
    taylor   = Artist("1",  "Taylor Swift",     "Pop",       0.95)
    ariana   = Artist("2",  "Ariana Grande",    "Pop",       0.93)
    justin   = Artist("3",  "Justin Bieber",    "Pop",       0.92)
    ed       = Artist("4",  "Ed Sheeran",       "Pop",       0.90)
    billie   = Artist("5",  "Billie Eilish",    "Alt Pop",   0.91)
    harry    = Artist("15", "Harry Styles",     "Pop",       0.92)
    olivia_r = Artist("16", "Olivia Rodrigo",   "Pop",       0.90)
    sabrina  = Artist("17", "Sabrina Carpenter","Pop",       0.88)
    charli   = Artist("18", "Charli XCX",       "Pop",       0.85)

    # Emerging artists 
    addison     = Artist("7",  "Addison Rae",     "Pop",       0.50)
    chappell    = Artist("8",  "Chappell Roan",   "Pop",       0.45)
    lizzy       = Artist("9",  "Lizzy McAlpine",  "Indie",     0.40)
    gracie      = Artist("10", "Gracie Abrams",   "Indie Pop", 0.55)
    tate        = Artist("11", "Tate McRae",      "Pop",       0.65)
    conan       = Artist("12", "Conan Gray",      "Indie Pop", 0.60)
    beabadoobee = Artist("13", "Beabadoobee",     "Indie",     0.50)
    raye        = Artist("14", "RAYE",            "R&B",       0.58)
    pink        = Artist("19", "PinkPantheress",  "Alt Pop",   0.65)
    malcolm     = Artist("20", "Malcolm Todd",    "Indie",     0.45)
    royel       = Artist("21", "Royel Otis",      "Indie Rock",0.50)
    olivia_d    = Artist("22", "Olivia Dean",     "Soul",      0.55)
    clairo      = Artist("23", "Clairo",          "Indie",     0.60)

    graph = MusicGraph()
    all_artists = [
        taylor, ariana, justin, ed, billie, harry, olivia_r, sabrina, charli,
        addison, chappell, lizzy, gracie, tate, conan, beabadoobee, raye,
        pink, malcolm, royel, olivia_d, clairo
    ]
    for artist in all_artists:
        graph.add_artist(artist)

    # Mainstream connections 
    graph.add_relationship(taylor, ariana)
    graph.add_relationship(taylor, ed)
    graph.add_relationship(ariana, justin)
    graph.add_relationship(justin, ed)
    graph.add_relationship(billie, taylor)
    graph.add_relationship(billie, ariana)
    graph.add_relationship(harry, taylor)
    graph.add_relationship(olivia_r, taylor)
    graph.add_relationship(sabrina, ariana)
    graph.add_relationship(charli, billie)

    # Emerging and mainstream connections 
    graph.add_relationship(chappell, taylor)
    graph.add_relationship(lizzy, billie)
    graph.add_relationship(gracie, taylor)
    graph.add_relationship(conan, ariana)
    graph.add_relationship(tate, justin)
    graph.add_relationship(raye, ariana)
    graph.add_relationship(addison, taylor)
    graph.add_relationship(pink, billie)
    graph.add_relationship(clairo, taylor)
    graph.add_relationship(olivia_d, ariana)

    # Emergering connections
    graph.add_relationship(gracie, lizzy)
    graph.add_relationship(conan, beabadoobee)
    graph.add_relationship(clairo, lizzy)
    graph.add_relationship(clairo, beabadoobee)
    graph.add_relationship(pink, charli)
    graph.add_relationship(royel, malcolm)
    graph.add_relationship(olivia_d, raye)
    graph.add_relationship(gracie, clairo)
    graph.add_relationship(royel, conan)

    return graph, all_artists