import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

from db import get_connection


def load_embeddings_from_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT embedding, cluster_id
        FROM posts
        WHERE embedding IS NOT NULL
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    embeddings = []
    labels = []

    for emb_json, cluster_id in rows:
        if emb_json is None or cluster_id is None:
            continue

        embedding = json.loads(emb_json)
        embeddings.append(embedding)
        labels.append(cluster_id)

    return np.array(embeddings), np.array(labels)


def visualize_clusters():

    embeddings, labels = load_embeddings_from_db()

    if len(embeddings) == 0:
        print("No embeddings found in database.")
        return

    print(f"Loaded {len(embeddings)} embeddings.")

    # Reduce to 2D
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(embeddings)

    plt.figure(figsize=(10, 7))

    scatter = plt.scatter(
        reduced[:, 0],
        reduced[:, 1],
        c=labels,
        cmap="tab10",
        alpha=0.7
    )

    plt.title("Reddit Post Clusters (PCA 2D)")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")

    legend = plt.legend(
        *scatter.legend_elements(),
        title="Clusters"
    )
    plt.gca().add_artist(legend)

    plt.tight_layout()
    plt.savefig("cluster_visualization.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    visualize_clusters()
