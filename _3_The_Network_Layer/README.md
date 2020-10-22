Here we describe the basic functionality we expect the Network layer to perform. 

## Link Layer interface used

The interface the network layer expects from the link layer is:

- **Creation of entangled pairs between adjacent nodes** 

- **Entanglement swap between specified qubits** 

- **Information about qubit decoherence** 

## Interface to Transport layer

We currently expect the network layer to connect any two nodes in the network provided the minimum fidelity to be achieved in the least time possible.

## Information maintained at Network layer

- **Network Graph** : Let us call it `G(N,E)`. The set `N` consists of all the nodes in the network and the edge set `E` contains the pairs of nodes adjacent to each other. Each edge `e` can have functions defined on it describing the fidelity of a link created across it, number of entangled links it can create per second, etc. For the sake of simplicity of the initial simulation, we assume the fidelity of a newly created link to be `F` and link creation time to be `t` for every edge `e`.

- **Virtual Graph** : Let us call it `Gv(N,Ev)`. Here the edge set `Ev` consists of edges connecting nodes which share an entangled pair at the given moment. Two nodes can have multiple entangled links and hence multiple edges between them. The pre-existence of entangled links in the network reduce the diameter of the graph and aid in the reduction of latency. Refer to [2] for more details.

In a practical scenario no node will have complete information of either the virtual or the network graph. The amount of information a node will have has direct impacts on the protocol used at the network layer and will depend on the final protocol employed.

## Steps taken at network layer

According to [1], the steps followed at the network layer to fulfill a demand of link creation are as follows:

1. **Path Discovery** : This step involves deciding the chain of nodes which will act as repeaters in the link creation process. 
2. **Entanglement Reservation** : This step involves simultaneous generation of entangled links between all adjacent pair of nodes along the discovered path.
3. **Entanglement Distribution** : Entanglement swapping is performed at every intermediate node in the chain to finally yield the requested entangled pair.

Steps 2 and 3 above combined constitute the *Prepare and Swap* protocol for entanglement swapping. It was arrived upon independently in #19 and is also discussed in [1].

## Path Discovery

The papers [1] and [2] talk about different ways of solving the path discovery problem taking different parts into consideration. [1] assumes different link creation times and [2] explores the use of virtual graphs to reduce latency. These are discussed in detail in their respective directories in the Protocols\ directory.

We would ideally like to consider a mix of both the papers' suggestions. We should also take into consideration if there is a difference in link creation time and the inverse of number of links created per second, that is can two adjacent nodes be in the process of generating multiple links in parallel? If not we might also consider low fidelity and low latency paths on which multiple links are created which are later distilled.



One important consideration is that we want to end up with a dynamic network and that the network might change while the path discovery algorithm is running.


## References 

1. Entanglement Distribution in a Quantum Network, a Multi-Commodity Flow-Based Approach, *Chakraborty et al*, https://arxiv.org/pdf/2005.14304.pdf
2. Distributed Routing in a Quantum Internet, *Chakraborty et al*, https://arxiv.org/pdf/1907.11630.pdf
