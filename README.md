# Quantum Internet

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/QTM3x/Quantum-Internet/master)

*Click on "launch binder" to run the Python notebooks in this repository in your browser.*

##### CURRENT GOAL ([here](https://github.com/QTM3x/Quantum-Internet/blob/master/1.%20The%20Applications%20Layer/BB84.md)): Design a quantum internet that we can use to implement the BB84 protocol fast enough to share 64-bits of secret key between two parties separated by 100 km in under an hour.

## About

**This repository is setup by the staff members of the QTMx courses by DelftX on edX. In this repository, learners from the edX platform will collaborate on building a description of a quantum internet and developing applications for it. The DelftX staff will provide guidance and moderate changes and additions to the repository.**

#### What is a quantum internet?

There is no agreed upon definition of a quantum Internet. Despite that, let us make an attempt to get ourselves started: A quantum Internet is a network of physically separated quantum computers that can deliver an entangled pair of quantum bits (qubits) on demand to any pair of connected end-node quantum computers. In this quantum internet, entanglement between shared qubits of opposite nodes is the crucial resource, and a lot of coordination and communication is needed to produce entanglement on demand to end-users.

#### What is the Quantum Internet for?

The purpose of a quantum internet is not to replace, improve or outperform the current 'classical' internet; On the contrary, a quantum internet will operate in great synergy with the classical internet.  Regular ‘classical’ communication and applications will continue to run on the internet as we are used to. The quantum internet will only be utilized for specialized applications and subroutines where it outperforms the internet in some way. This is similar to how a quantum computer will likely never replace a classical computer entirely – it will outperform a classical computer only for very specific problems. For some examples of applications of the quantum Internet, see this [blog post](https://blog.qutech.nl/index.php/2019/10/22/Quantum-internet-at-the-verge-of-an-emerging-technology/) by QuTech PhD student Bas Dirkse. For a longer but still very accessible introduction to the quantum internet, see Wojtek242's text [here](https://github.com/Wojtek242/draft-irtf-qirg-principles/blob/c41da3a1603671cd2a1552d550a588c64618f943/draft-irtf-qirg-principles-03.txt).

## Structure

We will structure our description of the quantum internet according to the layers of the quantum network stack (see this [blog post](https://blog.qutech.nl/index.php/2019/05/22/a-Quantum-network-stack/) by QuTech PhD student Axel Dahlberg). In general a software stack consists of multiple layers which work together to realize some service to the user. The core idea for using a stack is that higher layers can make sure of the *service* that a lower layer provides, withough knowing the details of how this is implemented.

#### Classical network stack
In the case of the *classical network stack* in the example below, the physical layer consists of all the hardware, cables etc. and concerns how a string of bits is actually transmitted through for example a cable or the air, and the *link layer* has many implementations such as *Ethernet*, *Wi-fi*, *4G* etc. As an analogy, think of when you send a letter in paper form. You don’t need to know exactly how the mailman will deliver your letter or what route he will take to the destination, you only need to know what service he provides, i.e. the delivery of a letter, and what interface to use, i.e. how you should specify the address on the letter.

<img src="https://blog.qutech.nl/wp-content/uploads/2019/05/classical_stack-768x631.png" width="500">

#### Quantum network stack

The *quantum network stack* is heavily inspired by the classical stack and consists of the same five --- they might increase or decrease later --- layers. As such, this repository is divided into five main sections, each concerned with one of the five layers.

| Layer             | Function |
| -----------------|-------------|
| 1. Applications Layer | The stuff we are actually building the internet to be able to do: Quantum key distribution, Quantum anonymous voting, etc.|
| 2. Transport Layer | A set of protocols that together make sure qubits are reliably transmitted between two end nodes. |
| 3. Network Layer | A set of protocols that together make sure that nodes far away from each other remain connected (entangled) when needed. |
| 4. Link Layer | A set of protocols that together make sure that nodes close to each other remain connected (entangled) when needed. |
| 5. Physical layer | The hardware of the internet: optical fiber cables, Quantum processors, Quantum memories, etc. |


## Approach

Our approach will be to begin from the applications layer: What do we need a quantum internet for? Knowing the answer to this question will help us have a clear idea of the requirements that the other layers must satisfy. We will begin with a specific application, and while trying to design a quantum internet on which to run this application we will find/create solutions for the problems we will face. Example of a problem that we will need to find solution to: how are we going to send qubits over large distances if we will always have losses in the optical fibers --- or whatever other medium --- through which we are sending the qubits?

As a starting point, we will consider our application to be quantum key distribution using the BB84 protocol (see more in the applications layer folder). **CURRENT GOAL**: Design a quantum internet that we can use to implement the BB84 protocol fast enough to share 64-bits of secret key between two parties separated by 100 km in under an hour. This goal might be altered later if it turns out to be too complicated for an initial goal.




## How to contribute

As we have chose GitHub as own platform, we will be using the features provided by git to make edits or to add to our files. The workflow is as follows:

1. Create a fork of the repository
2. Edit the files in the fork to your own liking
3. Create a pull request

We have made a video example of this workflow [here](https://youtu.be/ZvfYAfjzc1M). If you are not familiar with GitHub as a platform, here is a nice introductory [video](https://youtu.be/w3jLJU7DT5E).

All files are written in Markdown, a simple markup language with plain-text-formatting syntax. Check out this [cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) for markdown if you need any help and tips. Furthermore, since markdown does not support equations natively, and we are certain to use equations at some point, we recommend to use the following HTML workaround that supports LaTeX formatting.
```markdown
<img src="https://latex.codecogs.com/svg.latex?\Large&space;x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}"/>
```
<img src="https://latex.codecogs.com/svg.latex?\Large&space;x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}"/>




If you have a question, you may ask it in the form of an issue. To raise an issue, simply go to the issues tab and create a new issue. Try to create an issue only when necessary (see point 1 in the guidelines below!).

If you don't know how to begin contributing, have a look at the open issues and try to help with one of them. In fact, we recommend you start by doing that.




Things that can be contributed to the repository include, but are not limited to, code, explanation text, explanation videos, ideas, and research questions. **The repository is still young and a lot of stuff need to be added, so just contribute what you can!**

## Contribution guidelines

Open source projects with collaboration on the wide-scale we are going for here can become very messy. Surprisingly, they often don't! Good guidlines help maintain order. The following are a few such guidelines (feel free to propose more guidelines):


1.  Help us avoid a mess.

  * a) Be polite and thoughtful of others: Let you aim be to understand the other's person point of view, then to learn from them if they are right or to teach them if they are wrong.

  * b) Write clearly and precisely, and add figures and videos where possible: helping others underst and what's going on quickly helps us all make progress faster.

  * c) Avoid redundancy: avoid adding stuff that has been added before, or working on the same thing that someone else is already working on --- help them instead of starting from scratch.


2.  Do good science.

  * a) Provide evidence.

  * b) Be unusually honest about your work; lean over backwards to convey the truth, [as Feynman would say](https://en.wikipedia.org/wiki/Cargo_cult_science).


3. [Have fun!](https://www.youtube.com/watch?v=uxKmDWDUZ5A)
