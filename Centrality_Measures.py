import networkx as nx
import matplotlib.pyplot as plt
import collections
from termcolor import colored

def preliminary_analysis(given_graph):

    graph = nx.read_graphml(given_graph)

    list_of_all_degrees = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    max_degree_tuple = list_of_all_degrees[0]

    if (nx.is_directed(graph)):
        print(colored("Type of network: directed", "green"))

        list_of_all_in_degrees = sorted(graph.in_degree, key=lambda x: x[1], reverse=True)
        max_in_degree_tuple = list_of_all_in_degrees[0]

        maximum_in_list = max_in_degree_tuple[1]

        print("")
        print(colored("Nodes with max in-degree: ", "green"))
        for i in range(0, len(list_of_all_in_degrees)):
            if ((list_of_all_in_degrees[i])[1] == maximum_in_list):
                print((list_of_all_in_degrees[i])[0])

        print(colored("Max in-degree: " + str(max_in_degree_tuple[1]), "green"))

        print(colored("Top 10:", "green"))
        for i in range(0, 10):
            print(str((list_of_all_in_degrees[i])[0]) + "->" + str((list_of_all_in_degrees[i])[1]))

        print("")

        list_of_all_out_degrees = sorted(graph.out_degree, key=lambda x: x[1], reverse=True)
        max_out_degree_tuple = list_of_all_out_degrees[0]

        maximum_in_list = max_out_degree_tuple[1]

        print(colored("Nodes with max out-degree: ", "green"))
        for i in range(0, len(list_of_all_out_degrees)):
            if ((list_of_all_out_degrees[i])[1] == maximum_in_list):
                print((list_of_all_out_degrees[i])[0])
        print(colored("Max out-degree: " + str(max_out_degree_tuple[1]), "green"))

        print(colored("Top 10:", "green"))
        for i in range(0, 10):
            print(str((list_of_all_out_degrees[i])[0]) + "->" + str((list_of_all_out_degrees[i])[1]))

        print("")

    else:
        print("Type of network: not directed")

    maximum_in_list = max_degree_tuple[1]
    print(colored("Nodes with max degree: ", "green"))
    for i in range(0, len(list_of_all_degrees)):
        if ((list_of_all_degrees[i])[1] == maximum_in_list):
            print((list_of_all_degrees[i])[0])

    print(colored("Max degree: " + str(max_degree_tuple[1]), "green"))

    print(colored("Top 10:", "green"))
    for i in range(0, 10):
        print(str((list_of_all_degrees[i])[0]) + "->" + str((list_of_all_degrees[i])[1]))

    print("")

    degree_list = []
    for i in range(0, len(list_of_all_degrees)):
        degree_list.append(list_of_all_degrees[i][1])
    average_degree = sum(degree_list) / nx.number_of_nodes(graph)
    print(colored("Average degree: " + str(average_degree), "green"))

def degree_distribution(given_graph):

    graph = nx.read_graphml(given_graph)

    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')
    ax.set_yscale('log')
    plt.title("Degree distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of nodes")
    plt.show()

    if (nx.is_directed(graph)):

        # in-degree
        in_degree_sequence = sorted([d for n, d in graph.in_degree()], reverse=True)  # degree sequence
        in_degreeCount = collections.Counter(in_degree_sequence)
        deg, cnt = zip(*in_degreeCount.items())

        fig, ax = plt.subplots()
        plt.bar(deg, cnt, width=0.80, color='b')
        ax.set_yscale('log')
        plt.title("in-degree distribution")
        plt.xlabel("Degree")
        plt.ylabel("Number of nodes")
        plt.show()

        # out-degree
        out_degree_sequence = sorted([d for n, d in graph.out_degree()], reverse=True)  # degree sequence
        out_degreeCount = collections.Counter(out_degree_sequence)
        deg, cnt = zip(*out_degreeCount.items())

        fig, ax = plt.subplots()
        plt.bar(deg, cnt, width=0.80, color='b')
        ax.set_yscale('log')
        plt.title("out-degree distribution")
        plt.xlabel("Degree")
        plt.ylabel("Number of nodes")
        plt.show()

def largest_node(centrality):

    return list(reversed(sorted((value, node)
                                for (node, value) in centrality.items())))

def closeness_centrality(given_graph):

    graph = nx.read_graphml(given_graph)

    closeness = nx.closeness_centrality(graph)
    plt.hist(closeness.values(), color = 'b')
    plt.title("Normalized closeness distribution")
    plt.xlabel("Closeness")
    plt.ylabel("Number of nodes")
    plt.yscale("log")
    plt.show()

    highest_closeness_centralities_list = largest_node(closeness)
    print(colored("Top ten highest closeness centralities:", "green"))
    for i in range(0, 10):
        print(str((highest_closeness_centralities_list[i])[1]) + "->" +
              str((highest_closeness_centralities_list[i])[0]))

def betweenness_centrality(given_graph):

    graph = nx.read_graphml(given_graph)

    betweenness = nx.betweenness_centrality(graph)
    plt.hist(betweenness.values(), color = 'b')
    plt.title("Normalized betweennes distribution")
    plt.xlabel("betweennes")
    plt.ylabel("Number of nodes")
    plt.xticks(rotation='vertical')
    plt.yscale("log")
    plt.show()

    highest_betweenness_centralities_list = largest_node(betweenness)
    print(colored("Top ten highest betweenness centralities:", "green"))
    for i in range(0, 10):
        print(str((highest_betweenness_centralities_list[i])[1]) + "->" +
              str((highest_betweenness_centralities_list[i])[0]))

def eigenvector_centrality(given_graph):

    graph = nx.read_graphml(given_graph)

    eigenvector = nx.eigenvector_centrality(graph)
    plt.hist(eigenvector.values(), color = 'b')
    plt.title("Normalized eigenvector distribution")
    plt.xlabel("eigenvector")
    plt.ylabel("Number of nodes")
    plt.xticks(rotation='vertical')
    plt.yscale("log")
    plt.show()

    highest_eigenvector_centralities_list = largest_node(eigenvector)
    print(colored("Top ten highest eigenvector centralities:", "green"))
    for i in range(0, 10):
        print(str((highest_eigenvector_centralities_list[i])[1]) + "->" +
              str((highest_eigenvector_centralities_list[i])[0]))


#preliminary_analysis("./mentions_network.graphml")
#degree_distribution("./mentions_network.graphml")
closeness_centrality("./mentions_network.graphml")
betweenness_centrality("./mentions_network.graphml")
eigenvector_centrality("./mentions_network.graphml")
