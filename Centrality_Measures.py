import networkx as nx
import matplotlib.pyplot as plt
import collections
from termcolor import colored
import community
import igraph as ig
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot, plot
from Language_Network_Analysis import general_analysis
from Sentiment_Analysis import *
import statistics
import networkit as nit

def preliminary_analysis(given_graph):

    if '.graphml' in given_graph:
        graph = nx.read_graphml(given_graph)
        nit_graph = nit.readGraph(given_graph, nit.Format.GraphML)
    else:
        graph = given_graph
        nx.write_graphml(graph, "./util_graph.graphml")
        nit_graph = nit.readGraph("./util_graph.graphml", nit.Format.GraphML)


    print(colored("Average clustering: ", "yellow") + str(nx.algorithms.average_clustering(graph)))

    list_of_all_degrees = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    max_degree_tuple = list_of_all_degrees[0]

    print(colored("Total number of nodes: ", "yellow") + str(nx.number_of_nodes(graph)))
    print(colored("Total number of isolated nodes: ", "yellow") + str(nx.number_of_isolates(graph)))
    print(colored("Total number of edges: ", "yellow") + str(nx.number_of_edges(graph)))

    print(colored("Network's overview: ", "yellow"))
    nit.overview(nit_graph)

    if (nx.is_directed(graph)):
        print(colored("Type of network: directed", "yellow"))

        list_of_all_in_degrees = sorted(graph.in_degree, key=lambda x: x[1], reverse=True)
        max_in_degree_tuple = list_of_all_in_degrees[0]

        maximum_in_list = max_in_degree_tuple[1]

        print("")

        print(colored("Len of in-degree", "yellow") + str(len(list_of_all_in_degrees)))

        in_degree_list = []
        for i in range(0, len(list_of_all_in_degrees)):
            in_degree_list.append(list_of_all_in_degrees[i][1])

        z = sum(in_degree_list)
        average_in_degree = sum(in_degree_list) / nx.number_of_nodes(graph)
        print(colored("Average in-degree: " + str(average_in_degree), "green"))

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

        print(colored("Len of out-degree", "yellow") + str(len(list_of_all_out_degrees)))

        maximum_in_list = max_out_degree_tuple[1]

        out_degree_list = []
        for i in range(0, len(list_of_all_out_degrees)):
            out_degree_list.append(list_of_all_out_degrees[i][1])

        c = sum(out_degree_list)
        average_out_degree = sum(out_degree_list) / nx.number_of_nodes(graph)
        print(colored("Average out-degree: " + str(average_out_degree), "green"))

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

def average_shortes_path(given_graph):


    if '.graphml' in given_graph:
        graph = ig.Graph.Read_GraphML(given_graph)
        graph_util = nx.read_graphml(given_graph)
    else:
        graph = given_graph

    average_sp = ig.GraphBase.average_path_length(graph)

    print(colored("Average path lenght: ", "yellow") + str(average_sp))

def degree_distribution(given_graph):

    if '.graphml' in given_graph:
        graph = nx.read_graphml(given_graph)
    else:
        graph = given_graph

    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    '''
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')
    ax.set_yscale('log')
    plt.title("Degree distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of nodes")
    plt.show()
    '''
    fig, ax = plt.subplots()
    plt.hist(list(degree_sequence))
    ax.set_yscale('log')
    plt.title("degree distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of nodes")
    plt.show()

    if (nx.is_directed(graph)):

        # in-degree


        in_degree_sequence = sorted([d for n, d in graph.in_degree()])  # degree sequence
        print("Average in degree: " + str(statistics.mean(list(in_degree_sequence))))
        #print(in_degree_sequence)
        '''
        print(len(in_degree_sequence))
        in_degreeCount = collections.Counter(in_degree_sequence)
        deg, cnt = zip(*in_degreeCount.items())

        fig, ax = plt.subplots()
        plt.bar(deg, cnt, width=0.80, color='b')
        ax.set_yscale('log')
        plt.title("in-degree distribution")
        plt.xlabel("Degree")
        plt.ylabel("Number of nodes")
        plt.show()
        '''
        fig, ax = plt.subplots()
        plt.hist(list(in_degree_sequence))
        ax.set_yscale('log')
        plt.title("in-degree distribution")
        plt.xlabel("Degree")
        plt.ylabel("Number of nodes")
        plt.show()

        # out-degree
        out_degree_sequence = sorted([d for n, d in graph.out_degree()])  # degree sequence
        print("Average out degree: " + str(statistics.mean(list(out_degree_sequence))))
        #print(out_degree_sequence)
        '''
        print(len(out_degree_sequence))
        out_degreeCount = collections.Counter(out_degree_sequence)
        deg, cnt = zip(*out_degreeCount.items())

        fig, ax = plt.subplots()
        plt.bar(deg, cnt, width=0.80, color='b')
        ax.set_yscale('log')
        plt.title("out-degree distribution")
        plt.xlabel("Degree")
        plt.ylabel("Number of nodes")
        plt.show()
        '''
        fig, ax = plt.subplots()
        plt.hist(list(out_degree_sequence))
        ax.set_yscale('log')
        plt.title("out-degree distribution")
        plt.xlabel("Degree")
        plt.ylabel("Number of nodes")
        plt.show()

def largest_node(centrality):

    return list(reversed(sorted((value, node)
                                for (node, value) in centrality.items())))

def closeness_centrality(given_graph):

    if '.graphml' in given_graph:
        graph = ig.Graph.Read_GraphML(given_graph)
        graph_util = nx.read_graphml(given_graph)
    else:
        graph_util = given_graph
        nx.write_graphml(graph_util, "./util_graph.graphml")
        graph = ig.Graph.Read_GraphML("./util_graph.graphml")

    closeness = ig.GraphBase.closeness(graph)
    nodes = list(graph_util.nodes)

    my_util_dict = {}

    for i in range(0, len(nodes)):
        my_util_dict[nodes[i]] = closeness[i]

    plt.hist(my_util_dict.values(), color = 'b')
    plt.title("Normalized closeness distribution")
    plt.xlabel("Closeness")
    plt.ylabel("Number of nodes")
    plt.yscale("log")
    plt.show()

    highest_closeness_centralities_list = sorted(my_util_dict.items(), key=lambda x: x[1], reverse=True)
    print(colored("Top ten highest closeness centralities:", "green"))
    for i in range(0, 10):
        print(str((highest_closeness_centralities_list[i])[1]) + "->" +
              str((highest_closeness_centralities_list[i])[0]))

def betweenness_centrality(given_graph):

    if '.graphml' in given_graph:
        graph = ig.Graph.Read_GraphML(given_graph)
        graph_util = nx.read_graphml(given_graph)
    else:
        graph_util = given_graph
        nx.write_graphml(graph_util, "./util_graph.graphml")
        graph = ig.Graph.Read_GraphML("./util_graph.graphml")

    betweenness = ig.GraphBase.betweenness(graph)
    nodes = list(graph_util.nodes)

    my_util_dict = {}

    for i in range (0, len(nodes)):
        my_util_dict[nodes[i]] = betweenness[i]

    plt.hist(my_util_dict.values(), color = 'b')
    plt.title("Betweennes distribution")
    plt.xlabel("betweennes")
    plt.ylabel("Number of nodes")
    plt.xticks(rotation='vertical')
    plt.yscale("log")
    plt.show()

    highest_betweenness_centralities_list = sorted(my_util_dict.items(), key=lambda x: x[1], reverse=True)
    print(colored("Top ten highest betweenness centralities:", "green"))
    for i in range(0, 10):
        print(str((highest_betweenness_centralities_list[i])[1]) + "->" +
              str((highest_betweenness_centralities_list[i])[0]))

def eigenvector_centrality(given_graph):

    if '.graphml' in given_graph:
        graph = ig.Graph.Read_GraphML(given_graph)
        graph_util = nx.read_graphml(given_graph)
    else:
        graph_util = given_graph
        nx.write_graphml(graph_util, "./util_graph.graphml")
        graph = ig.Graph.Read_GraphML("./util_graph.graphml")

    eigenvector = ig.GraphBase.eigenvector_centrality(graph)
    nodes = list(graph_util.nodes)

    my_util_dict = {}

    for i in range (0, len(nodes)):
        my_util_dict[nodes[i]] = eigenvector[i]

    plt.hist(my_util_dict.values(), color = 'b')
    plt.title("Eigenvector distribution")
    plt.xlabel("eigenvector")
    plt.ylabel("Number of nodes")
    plt.xticks(rotation='vertical')
    plt.yscale("log")
    plt.show()

    highest_eigenvector_centralities_list = sorted(my_util_dict.items(), key=lambda x: x[1], reverse=True)
    print(colored("Top ten highest eigenvector centralities:", "green"))
    for i in range(0, 10):
        print(str((highest_eigenvector_centralities_list[i])[1]) + "->" +
              str((highest_eigenvector_centralities_list[i])[0]))

def degree_centrality(given_graph):

    if '.graphml' in given_graph:
        graph = nx.read_graphml(given_graph)
    else:
        graph = given_graph

    degree = nx.degree_centrality(graph)
    plt.hist(degree.values(), color = 'b')
    plt.title("Degree centrality distribution")
    plt.xlabel("degree centrality")
    plt.ylabel("Number of nodes")
    plt.xticks(rotation='vertical')
    plt.yscale("log")
    plt.show()

    highest_degree_centralities_list = largest_node(degree)
    print(colored("Top ten highest degree centralities:", "green"))
    for i in range(0, 10):
        print(str((highest_degree_centralities_list[i])[1]) + "->" +
              str((highest_degree_centralities_list[i])[0]))


def pagerank(given_graph):

    if '.graphml' in given_graph:
        graph = nx.read_graphml(given_graph)
    else:
        graph = given_graph

    pagernk = nx.pagerank(graph)
    plt.hist(pagernk.values(), color='b')
    plt.title("Pagerank distribution")
    plt.xlabel("pagerank")
    plt.ylabel("Number of nodes")
    plt.xticks(rotation='vertical')
    plt.yscale("log")
    plt.show()

    highest_pagernk_centralities_list = largest_node(pagernk)
    print(colored("Top ten highest pagerank centralities:", "green"))
    for i in range(0, 10):
        print(str((highest_pagernk_centralities_list[i])[1]) + "->" +
              str((highest_pagernk_centralities_list[i])[0]))

def connected_component_analysis(given_graph):

    if '.graphml' in given_graph:
        graph = nx.to_undirected(nx.read_graphml(given_graph))
        nx.write_graphml(graph, "./util_graph.graphml")
        nit_graph = nit.readGraph("./util_graph.graphml", nit.Format.GraphML)
    else:
        graph = given_graph
        nx.write_graphml(nx.to_undirected(graph), "./util_graph.graphml")
        nit_graph = nit.readGraph("./util_graph.graphml", nit.Format.GraphML)

    cc = nit.components.ConnectedComponents(nit_graph)
    cc.run()
    compSizes = cc.getComponentSizes()
    numCC = len(compSizes)
    maxCC = max(compSizes.values())

    print("#cc = %d,largest = %d" % (numCC, maxCC))

    plt.hist(compSizes.values(), color="b")
    plt.title("Connected components size distribution")
    plt.xlabel("Size")
    plt.ylabel("Number of connected components")
    plt.xticks(rotation='vertical')
    plt.yscale("log")

    plt.show()

    nit_graph.removeSelfLoops()

    print("Average local cluster coefficient: " + str(nit.globals.ClusteringCoefficient.avgLocal(nit_graph)))

def greedy_modularity_communities_detection(given_graph):

    if '.graphml' in given_graph:
        graph = nx.to_undirected(nx.read_graphml(given_graph))
        nx.write_graphml(graph, "./util_graph.graphml")
        nit_graph = nit.readGraph("./util_graph.graphml", nit.Format.GraphML)
    else:
        graph = given_graph
        nx.write_graphml(nx.to_undirected(graph), "./util_graph.graphml")
        nit_graph = nit.readGraph("./util_graph.graphml", nit.Format.GraphML)

    communities = nit.community.detectCommunities(nit_graph)

    mod_communities = []
    for i in range(0, len(communities)):
        mod_communities.append(list(communities.getMembers(i)))

    mod_communities.sort(key=len, reverse=True)

    util_dict = {}
    k = 0
    list_graph_nodes = list(graph.nodes)
    for i in range(0, len(list_graph_nodes)):

        util_dict[list_graph_nodes[i]] = k
        k += 1

    comm_list = []
    for i in range(0, 3):
        for j in range(0, len(mod_communities[i])):
            (mod_communities[i])[j] = [name for (name, age) in util_dict.items() if age == (mod_communities[i])[j]][0]

        comm_list.append((mod_communities[i]))


    sizes = communities.subsetSizes()
    plt.hist(sizes)
    plt.title("Communities size distribution")
    plt.ylabel("Number of communities")
    plt.xlabel("Community size")
    plt.yscale("log")
    plt.show()

    community_plotting(comm_list, graph)

def community_plotting(communities, graph):

    communities_to_study_counter = 3

    for x in communities:

        sub = nx.subgraph(graph, x)
        my_dataframe = pd.DataFrame(columns=["username", "text"])

        #### Sentiment analysis over communities

        nodeDict = dict(graph.nodes(data=True))
        for l in range(0, len(x)):
            for key, value in nodeDict.items():
                if key == x[l]:
                    try:
                        inserting_dict = {"username": key, "text": value["text"]}
                        my_dataframe = my_dataframe.append(inserting_dict,  ignore_index=True)
                    except:
                        pass

        basic_preprocessed_tweets = initial_text_preprocessing(my_dataframe["text"])
        tweets = refined_text_preprocessing(basic_preprocessed_tweets["text"], "english")
        print(words_counter(tweets))

        my_stopwords = ['’', '...', '…', 'rt', '“', '”', '…', 'u', ':/']
        tweets = refined_processing(tweets, my_stopwords)
        print(words_counter(tweets))

        cloud_visualization(tweets)
        histogram_visualization(tweets)
        afinn_visualization(basic_preprocessed_tweets)
        NRC_visualization(basic_preprocessed_tweets["text"])

        ####


        preliminary_analysis(sub)
        degree_distribution(sub)
        closeness_centrality(sub)
        betweenness_centrality(sub)
        eigenvector_centrality(sub)
        degree_centrality(sub)
        pagerank(sub)
        #connected_component_analysis(sub)
        #cliques_per_node_analysis(sub)
        try:
            general_analysis(sub)
        except:
            pass

        print("")
        print("---------------------------------------------------------------------------------------------")
        print("---------------------------------------------------------------------------------------------")

def cliques_per_node_analysis(given_graph):

    if '.graphml' in given_graph:
        graph = nx.to_undirected(nx.read_graphml(given_graph))
    else:
        graph = given_graph

    maximal_cliques = nx.algorithms.clique.number_of_cliques(graph)
    maximal_cliques = sorted(maximal_cliques.items(), key=lambda x: x[1], reverse = True)

    print(colored("Top ten number of maximal cliques per node: ", "yellow"))
    if len(maximal_cliques) > 10:

        for i in range (0, 10):
            print(maximal_cliques[i])

    else:
        for i in range (0, len(maximal_cliques)):
            print(maximal_cliques[i])

    x, y = zip(*maximal_cliques)  # unpack a list of pairs into two tuples

    plt.bar(x, y, color="b")
    plt.yscale("log")
    #plt.xticks(rotation='vertical')
    plt.xticks([])
    plt.title("Number of maximal cliques per node distribution")
    plt.xlabel("Node")
    plt.ylabel("Nuber of maximal cliques per node")
    plt.show()

preliminary_analysis("./mentions_network_language.graphml")
#degree_distribution("./mentions_network_language.graphml")
#closeness_centrality("./mentions_network_language.graphml")
#betweenness_centrality("./mentions_network_language.graphml")
#eigenvector_centrality("./mentions_network_language.graphml")
#degree_centrality("./mentions_network_language.graphml")
#average_shortes_path("./mentions_network_language.graphml")
#pagerank("./mentions_network_language.graphml")
#connected_component_analysis("./mentions_network_language.graphml")
#greedy_modularity_communities_detection("./mentions_network_language.graphml")
#cliques_per_node_analysis("./mentions_network_language.graphml")

