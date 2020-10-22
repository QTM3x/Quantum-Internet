# The Link Layer
###### This README is still being written.

## Interface to Network layer

Here we describe the functionality the link layer is expected to provide to the network layer

- **Creation of entangled pairs between adjacent nodes** : The link layer has the information of the nodes it is directly connected to and is tasked with the creation of entangled pairs between adjacent nodes in the network. The transport layer can specify the end-nodes for creating a link between the adjacent nodes.

- **Entanglement swap** : The link layer should provide an interface by which the network layer can specify the two qubits in the memory of the node between which an entanglement swap is to be performed. These qubits can either be specified through their locations in memory or the link-layer ids of the links. Though in a practical situation the link layer will not have information about the end-nodes since there can be entanglement swapping occuring at the end nodes too, it suffices for us to abstract the link-layer ids to the end-nodes.

- **Qubit decoherence** : The network layer protocols need information of whether a pre-existing pair of qubits has decohered beyond what is useful for us. This depends a lot on the fidelity and storage conditions determined at the physical layer

## The `Repeater` and `Endnode` objects

Every instance of `Repeater` contains an instance of `RepeaterHardware`:

```
class Repeater(object):
    def __init__(self, ...):
        ...
        self.hardware = RepeaterHardware(self)
        ...
```

Roughly speaking, the `RepeaterHardware` is the body of a repeater and the `Repeater` is its brain.

The `RepeaterHardware` object worries about which gates to apply, how to apply them to the kind of qubits on board, etc. The `Repeater` object worries about implementing link layer protocols, etc.

Similarly for the `Endnode` object.

## The `Cable` object



## The `Link` object

-----

## Possibly useful resources:

https://datatracker.ietf.org/doc/draft-dahlberg-ll-quantum/

https://arxiv.org/pdf/1903.09778.pdf


