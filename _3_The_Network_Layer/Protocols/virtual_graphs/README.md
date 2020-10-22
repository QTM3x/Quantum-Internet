## Virtual Graph

A virtual graph is a connectivity graph with edges denoting the presence of an entangled pair between two nodes. Existence of edges in the virtual graph before the path discovery phase begins can potentially help us connect the required nodes in lesser time. [1] explores this idea in addition to ways for choosing virtual links and analysing advantages from virtual links on different types of graphs. 

It is interesting to note that [1] focusses on local greedy algorithms where nodes only have information about other nearby nodes and not all the nodes in the graph.

## Fidelity

A threshold distance between nodes for achieving desired fidelity is calculated using the known fidelity of link creation and entanglement swapping success probability. Nodes farther apart than this distance from one of the nodes are not considered during path discovery which helps us easily tackle the fidelity constraints of link creation.


## References
1. Distributed Routing in a Quantum Internet, *Chakraborty et al*, https://arxiv.org/pdf/1907.11630.pdf