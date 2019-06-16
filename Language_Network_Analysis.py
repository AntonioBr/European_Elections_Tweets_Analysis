import networkx as nx
import matplotlib.pyplot as plt
from termcolor import colored

def general_analysis(given_graph):

    if '.graphml' in given_graph:
        graph = nx.read_graphml(given_graph)
    else:
        graph = given_graph

    languages_list = []
    nodes_language_list = []
    plotting_dict = {}

    for node in nx.nodes(graph):

        nodes_language_list.append(graph.node[node]["language"])

        if graph.node[node]["language"] not in languages_list:

            languages_list.append(graph.node[node]["language"])

    print(colored("List of all detected languages: ", "yellow") + str(languages_list))
    print(colored("Total number of detected languages: ", "yellow") + str(len(languages_list)))

    for i in range(0, len(languages_list)):
        print(colored(("Number of nodes with language " + languages_list[i] + ": "), "yellow") +
              str(nodes_language_list.count(languages_list[i])))

        plotting_dict[languages_list[i]] = nodes_language_list.count(languages_list[i])

    lists = sorted(plotting_dict.items())  # sorted by key, return a list of tuples

    x, y = zip(*lists)  # unpack a list of pairs into two tuples

    plt.bar(x, y, color = "b")
    plt.yscale("log")
    plt.xticks(rotation='vertical')
    plt.title("Languages distribution")
    plt.xlabel("Languages")
    plt.ylabel("Number of users")
    plt.show()

#general_analysis("./mentions_network_language.graphml")