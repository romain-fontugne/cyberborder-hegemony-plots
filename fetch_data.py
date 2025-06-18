from neo4j import GraphDatabase
import json

COUNTRY_CODE = 'IR'


def query_iyp(country_code):
    # Query 
    query = f"""
    MATCH (a:AS)-[ra:RANK]->(:Ranking {{name: 'IHR country ranking: Total AS ({country_code})'}})<-[rb:RANK]-(b:AS)
    WHERE ra.rank < 20
        AND rb.rank < 20
    MATCH (b)-[pw:PEERS_WITH {{reference_name: 'bgpkit.as2rel_v4'}}]-(a)
    MATCH (a)-[:COUNTRY {{reference_org:'NRO'}}]-(ca:Country)
    MATCH (b)-[:COUNTRY {{reference_org:'NRO'}}]-(cb:Country)
    WHERE pw.rel = 0 // Peer-to-peer
    RETURN  a.asn AS node0, b.asn AS node1, ca.country_code AS country0, cb.country_code AS country1
    """

    # URI = 'neo4j://iyp-bolt.ihr.live:7687'
    # AUTH = ('neo4j', 'password')

    URI = 'neo4j://localhost:7687'
    AUTH = ('neo4j', 'password')

    db = GraphDatabase.driver(URI, auth=AUTH)

    links = []
    records, _, _ = db.execute_query(query)
    for r in records:
        links.append(dict(r))

    data = {'country_code': country_code, 'links': links}
    print(json.dumps(data))

    db.close()


def main():
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description="Print AS graph for important ASes of the given country")

    # Add arguments
    parser.add_argument("country_code", type=str, help="Two letters country code")

    # Parse arguments
    args = parser.parse_args()

    query_iyp(args.country_code)


if __name__ == '__main__':
    main()
