import json
import networkx as nx
from matplotlib import pylab as plt

TIER1 = [5511, 6461, 7018, 6830, 6453, 701, 3356, 2914, 12956, 3491, 3257, 6762, 3320, 1299, 174]


def plot(data):
    links = []
    node_in = []
    node_tier1 = []
    node_out = []

    for r in data['links']:
        links.append([r['node0'], r['node1']])
        if r['node0'] in TIER1:
            node_tier1.append(r['node0'])
        elif r['country0'] == data['country_code']:
            node_in.append(r['node0'])
        else:
            node_out.append(r['node0'])

        if r['node1'] in TIER1:
            node_tier1.append(r['node1'])
        elif r['country1'] == data['country_code']:
            node_in.append(r['node1'])
        else:
            node_out.append(r['node1'])



    # plot the graph

    G = nx.Graph()
    G.add_edges_from(links)
    pos = nx.forceatlas2_layout(G,  gravity=2, seed=1)
    nx.draw(G, pos=pos)

    # nodes
    options = {"edgecolors": "tab:gray", "node_size": 1200, "alpha": 1}
    nx.draw_networkx_nodes(G, pos, nodelist=set(node_in), node_color="tab:orange", **options)
    nx.draw_networkx_nodes(G, pos, nodelist=set(node_tier1), node_color="tab:purple", **options)
    nx.draw_networkx_nodes(G, pos, nodelist=set(node_out), node_color="tab:blue", **options)

    # edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

    # add labels
    labels = {}
    for n in G.nodes():
        labels[n] = n
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="black")

    plt.tight_layout()
    plt.axis("off")
    plt.savefig(f'AS_graph_{data['country_code']}.png')
    plt.savefig(f'AS_graph_{data['country_code']}.pdf')
    plt.show()


def main():
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description="Plot the given AS graph")

    # Add arguments
    parser.add_argument("data", type=str, help="Json file containing the AS graph")

    # Parse arguments
    args = parser.parse_args()

    with open(args.data, 'r') as fp:
        as_graph = json.load(fp)
        plot(as_graph)


if __name__ == '__main__':
    main()
