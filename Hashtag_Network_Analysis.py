import networkx as nx
import matplotlib.pyplot as plt
import collections
from termcolor import colored
import community
import igraph as ig
from Centrality_Measures import *

def general_hashtag_analysis(given_graph):

    if ".graphml" in given_graph:

        graph = nx.to_undirected(nx.read_graphml(given_graph))

    else:

        graph = given_graph

    preliminary_analysis(graph)

def centralities_hashtag_analysis(given_graph):

    if ".graphml" in given_graph:

        graph = nx.to_undirected(nx.read_graphml(given_graph))

    else:

        graph = given_graph

    preliminary_analysis(graph)
    degree_distribution(graph)
    closeness_centrality(graph)
    betweenness_centrality(graph)
    eigenvector_centrality(graph)
    degree_centrality(graph)
    pagerank(graph)
    connected_component_analysis(graph)
    cliques_per_node_analysis(graph)

#general_hashtag_analysis("./hashtags_network.graphml")
centralities_hashtag_analysis("./hashtags_network.graphml")

