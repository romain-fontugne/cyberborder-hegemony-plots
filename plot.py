from neo4j import GraphDatabase
import networkx as nx
from matplotlib import pylab as plt

COUNTRY_CODE = 'IR'
TIER1 = [5511, 6461, 7018, 6830, 6453, 701, 3356, 2914, 12956, 3491, 3257, 6762, 3320, 1299, 174]

# Query 
query = f"""
MATCH (a:AS)-[ra:RANK]->(:Ranking {{name: 'IHR country ranking: Total AS ({COUNTRY_CODE})'}})<-[rb:RANK]-(b:AS)
WHERE ra.rank < 20
    AND rb.rank < 20
MATCH (b)-[pw:PEERS_WITH {{reference_name: 'bgpkit.as2rel_v4'}}]-(a)
MATCH (a)-[:COUNTRY {{reference_org:'NRO'}}]-(ca:Country)
MATCH (b)-[:COUNTRY {{reference_org:'NRO'}}]-(cb:Country)
WHERE pw.rel = 0 // Peer-to-peer
RETURN  a.asn AS anode, b.asn AS bnode, ca.country_code AS acc, cb.country_code AS bcc
"""

URI = 'neo4j://localhost:7687'
AUTH = ('neo4j', 'password')

# URI = 'neo4j://iyp-bolt.ihr.live:7687'
# AUTH = None
db = GraphDatabase.driver(URI, auth=AUTH)

links = []
node_in = []
node_tier1 = []
node_out = []

records, _, _ = db.execute_query(query)
for r in records:
    links.append([r['anode'], r['bnode']])
    if r['anode'] in TIER1:
        node_tier1.append(r['anode'])
    elif r['acc'] == COUNTRY_CODE:
        node_in.append(r['anode'])
    else:
        node_out.append(r['anode'])

    if r['bnode'] in TIER1:
        node_tier1.append(r['bnode'])
    elif r['bcc'] == COUNTRY_CODE:
        node_in.append(r['bnode'])
    else:
        node_out.append(r['bnode'])

db.verify_connectivity()
db.close()


# plot the graph

G = nx.Graph()
G.add_edges_from(links)
pos = nx.forceatlas2_layout(G)
nx.draw(G, pos=pos)

# nodes
options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 1}
nx.draw_networkx_nodes(G, pos, nodelist=set(node_in), node_color="tab:orange", **options)
nx.draw_networkx_nodes(G, pos, nodelist=set(node_tier1), node_color="tab:red", **options)
nx.draw_networkx_nodes(G, pos, nodelist=set(node_out), node_color="tab:blue", **options)

# edges
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

# some math labels
# labels = {}
# labels[0] = r"$a$"
# labels[1] = r"$b$"
# labels[2] = r"$c$"
# labels[3] = r"$d$"
# labels[4] = r"$\alpha$"
# labels[5] = r"$\beta$"
# labels[6] = r"$\gamma$"
# labels[7] = r"$\delta$"
# nx.draw_networkx_labels(G, pos, labels, font_size=22, font_color="whitesmoke")

plt.tight_layout()
plt.axis("off")
plt.show()
