import pandas as pd
import math

def dijkstra(graph, start_node, end_node):
    nodes = sorted(graph.keys())
    dist = {node: math.inf for node in nodes}
    prev = {node: None for node in nodes}
    dist[start_node] = 0
    unvisited = nodes.copy()

    table_data = []

    while unvisited:
        current = min((node for node in unvisited), key=lambda node: dist[node])
        if dist[current] == math.inf:
            break
        unvisited.remove(current)

        row = {}
        for node in nodes:
            if dist[node] == math.inf:
                row[node] = '∞'
            else:
                parent = prev[node] if prev[node] else node
                row[node] = f"{int(dist[node])}{parent}"
        row['v'] = current
        table_data.append(row)

        for neighbor, weight in graph[current].items():
            alt = dist[current] + weight
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = current

        if current == end_node:
            break

    df = pd.DataFrame(table_data)
    df = df[['v'] + nodes]

    # --- Susun path ---
    path = []
    current = end_node
    while current:
        path.append(current)
        current = prev[current]
    path.reverse()  # dari start ke end

    return df, path


# Graf
graph = {
    'Balige': {'Parapat': 80, 'Siantar': 133, 'Tebing': 209},
    'Parapat': {'Balige': 80, 'Siantar': 126, 'Raya': 38},
    'Raya': {'Parapat': 38, 'Siantar': 101, 'Pardagangaan': 166},
    'Siantar': {'Balige': 133, 'Parapat': 126, 'Raya': 101, 'Tebing': 100, 'Pardagangaan': 59},
    'Tebing': {'Siantar': 100, 'Pardagangaan': 53, 'Medan': 78, 'Binjai': 98},
    'Binjai': {'Tebing': 98, 'Medan': 21},
    'Medan': {'Tebing': 78, 'Binjai': 21, 'Pardagangaan': 126, 'Asahan': 88},
    'Pardagangaan': {'Raya': 166, 'Siantar': 59, 'Tebing': 53, 'Medan': 126, 'Sipirok': 49, 'Asahan': 86},
    'Sipirok': {'Pardagangaan': 49, 'Tanjung': 23, 'Asahan': 78},
    'Tanjung': {'Sipirok': 23, 'Asahan': 81, 'Kisaran': 118},
    'Asahan': {'Pardagangaan': 86, 'Medan': 88, 'Sipirok': 78, 'Tanjung': 81, 'Kisaran': 66},
    'Kisaran': {'Asahan': 66, 'Tanjung': 118}
}


# save ke CSV
edges = []
for node, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
        if {node, neighbor} not in [{e[0], e[1]} for e in edges]:  # Hindari duplikat
            edges.append([node, neighbor, weight])

df_edges = pd.DataFrame(edges, columns=['From', 'To', 'Distance'])
df_edges.to_csv("graph_output.csv", index=False)  # Simpan ke CSV

# ====== JALANKAN DIJKSTRA DAN TAMPILKAN TABEL ======
df_dijkstra, shortest_path = dijkstra(graph, start_node='Balige', end_node='Kisaran')
df_dijkstra.to_csv("dijkstra SOAL 1.csv", index=False)
df_dijkstra.to_excel("dijkstra SOAL 1.xlsx", index=False)
print("\nShortest path : ")
print(" → ".join(shortest_path))
