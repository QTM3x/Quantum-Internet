# Quantum-Internet

### About
In this repository, we will collaborate on building a quantum internet and developing applications for it. The repository is divided into five main sections, each concerned with one of the five --- they might increase or decrease later --- layers of the quantum internet stack. 

If you're unfamiliar with the internet stack, this [blog post](https://blog.qutech.nl/index.php/2019/05/22/a-quantum-network-stack/) by Axel, a PhD student at QuTech, is a great place to begin. To sum up the blog post, the components of the quantum internet are projected to fall into one of five categories or layers.

* The Applications Layer

    The stuff we are actually building the internet to be able to do: quantum key distribution, quantum anonymous voting, etc. 

* The Transport Layer

    A set of protocols that together make sure qubits are reliably transmitted between two end nodes.

* The Network Layer

    A set of protocols that together make sure that nodes far away from each other remain connected (entangled) when needed.

* The Link Layer

    A set of protocols that together make sure that nodes close to each other remain connected (entangled) when needed.

* The Physical layer

    The hardware of the internet: optical fiber cables, quantum processors, quantum memories, etc.


Our approach will be to begin from the applications layer: what do we need a quantum internet for? Knowing the answer to this question will help us have a clear idea of the requirements that the other layers must satisfy. As a starting point, we will consider our application to be quantum key distribution using the BB84 protocol (see more in the applications layer folder). **Precise initial goal:** design a quantum internet that we can use to implement the BB84 protocol fast enough to share 64-bits of secret key in under an hour.


### How to contribute

Simple: create a fork of the repository, edit the files in the fork, then create a pull request. 


##### Contribution guidelines

Open source projects with collaboration on the wide-scale we are going for here can become very messy. Surprisingly, they often don't! Good guidlines help maintain order. The following are a few such guidelines (feel free to propose more guidelines):


1- Questions. 

  * a) If you have a question, you may ask it in the form of an issue. To raise an issue, simply go to the issues tab and create a new issue. Try to create an issue only when necessary (see point 3 below!). 


2- Help us avoid a mess. 

* a) Be polite and thoughtful of others: Let you aim be to understand the other's person point of view, then to learn from them if they are right, and to teach them if they are wrong.

* b) Write clearly and precisely, and add figures and videos where possible: helping others understand what's going on quickly helps us all make progress faster.

* c) Avoid redundancy: avoid adding stuff that has been added before, or working on the same thing that someone else is already working on --- help them instead of starting from scratch.


3- Do good science.

* a) Provide evidence.

* b) Be unusually honest about your work; lean over backwards to convey the truth, [as Feynman would say](https://en.wikipedia.org/wiki/Cargo_cult_science).


4- [Have fun, and work hard!](https://www.youtube.com/watch?v=uxKmDWDUZ5A)







