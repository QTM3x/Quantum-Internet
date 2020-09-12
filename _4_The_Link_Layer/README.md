# The Link Layer
###### This README is still being written.

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


