# The Physical Layer
###### This README is still being written.

## Qubit carriers

Each qubit carrier gets an id when it's created. 

For `Qubit`:

```
class Qubit(object):
    def __init__(self, parent_hardware, ...):
        ...
        self.global_state = global_state_container.state
        self.id = self.global_state.create_qubit(self)
        ...
```

For `Photon`:

```
class Photon(object):
    def __init__(self, ...):
        ...
        self.global_state = global_state_container.state
        self.id = self.global_state.create_qubit(self)
        ...
```

This id corresponds to the index of qubit (photons are currently modelled as qubits) in the global state container [ADD LINK]. We need these ids to tell QuTip on which qubit we want to apply a given gate.

Here is an example: To apply a Y gate on a qubit Q, we do 

```
Y  = ry(90, N=int(math.log2(self.global_state.state.shape[0])), target=Q.id)
new_state = G * old_state * G.dag()
global_state.update_state(new_state)
```

This is how gates are applied in the `EndnodeHardware` class, for example.

----

#### A short story (one possible scenario):

Two parties, Alice and Bob. 

Alice in City A, Bob in City B. City A is 100 km away from City B.

Alice and Bob want to exchange 64 bits of secret key using the BB84 protocol. They want to do it fast! Under one hour would be just fine.

We need to build the hardware that allows them to do that.

The BB84 protocol requires the exchange of qubits.

Alice and Bob can exchange qubits using light: a photon carries a qubit from Alice to Bob, or vice versa. So we know our hardware will include optical fibers (we could also send the photons directly through the air, but air is too lossy a medium). 

Alice and Bob will need detectors, to detect the arriving photons. So we know our hardware will include detectors.

From the applications layer we also know that Alice and Bob will need to be able to change the polarization of the photons (the basis of the qubits). So we know our hardware will include special crystals that do that.


What else do we need?


--------------   So ... can we accomplish the task using this hardware? It depends:


How lossy are the optical fibers? If they are too lossy, then the photons will only rarely make it through 100 km of optical fiber from Alice to Bob. And it will take a long time for Alice and Bob to transmit enough photons so that they end up with 64 bits of secret key. More than the required 1 hour.

How sensitive are the detectors? If they are not sensitive enough, then even the rare photons that do make it accross the fiber are only rarely going to get picked up by the detector. And sharing the secret key will take way more than the required 1 hour.

We also need to take into account the losses due to the other components of our hardware.


-------------- Then clearly we first need to determine precisely how lossy our fiber is, and how sensitive our detectors are, and the other parameters in the rest of the hardware that can affect the transmission of the photons.




