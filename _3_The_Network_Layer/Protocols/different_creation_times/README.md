## Link Creation Times

As described in the link layer interface, we expect the functionality of creating an entangled pair between adjacent nodes from the link layer. The reference [1] assumes that it takes different amount of time for creation of such a link between each pair of nodes. Choosing the lowest latency path for a given number of demands for link creation is modeled as an LP formulation here. The LP is solved globally for the entire network, which means that each node must have information about the entire network, which might be impractical in a large setting.

## Fidelity

A threshold distance between nodes for achieving desired fidelity is calculated using the known fidelity of link creation and entanglement swapping success probability. Nodes farther apart than this distance from one of the nodes are not considered during path discovery which helps us easily tackle the fidelity constraints of link creation.


## References
1. Entanglement Distribution in a Quantum Network, a Multi-Commodity Flow-Based Approach, *Chakraborty et al*, https://arxiv.org/pdf/2005.14304.pdf