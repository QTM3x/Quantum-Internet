Here we write the simulations we need to test the protocols we develop in the repository.

In our tests we look for the following things: 
- The performance of the protocols in terms of entanglement rate.
- The sensitivity of the protocol performances to changes in the simulation models of the hardware; for example, what happens if we do not assume that all the qubits in a quantum repeater have identical coherence times.

[One way](https://arxiv.org/pdf/1511.08710.pdf) to see if our protocols and repeaters are doing what they should be doing --- increasing the rates at which we can share entanglement or secret key between two nodes on the network --- is to compare these rates with the rates we get when we use direct transmission, or sending the qubits directly to the other node over, say, a single segment of optical fiber.

The rates we get for a single segment of optical fiber can be approximated by the capacities of channels that model an optical fiber, like the ... channel.