import data.real.basic
import analysis.special_functions.exp_log
import _5_The_Physical_Layer.qubit_carriers.quantum_state
import _5_The_Physical_Layer.qubit_carriers.entropy_of_states

---- OPENING REMARKS

/-
This file formalizes the math in https://arxiv.org/pdf/2005.14304.pdf.
The comments and docstrings in quotations are copied directly from the 
text of the paper.
-/

/-
"In this paper, we are interested in computing the maximum entanglement distribution rate (flow). 
Given a quantum network G and a set of demands D, we investigate how to produce a set of paths P_i 
and an end-to-end entanglement generation rate r_i (flow), corresponding to each demand (si, ei, Fi), 
such that the total entanglement generation rate ∑ i ∈ [1,|D|], r_i is maximised."
-/

/-
"We consider the problem of optimising the achievable EPR-pair distribution rate between multiple
source-destination pairs in a quantum internet, where the repeaters may perform a probabilistic
bell-state measurement and we may impose a minimum end-to-end fidelity as a requirement.

1- We construct an efficient linear programming formulation that computes the maximum total achievable
entanglement distribution rate, satisfying the end-to-end fidelity constraint in polynomial time (in
the number of nodes in the network).

2- We also propose an efficient algorithm that takes the output of the linear programming solver as an 
input and runs in polynomial time (in the number of nodes) to produce the set of paths to be used to 
achieve the entanglement distribution rate.

3- Moreover, we point out a practical entanglement generation protocol which can achieve those rates."
-/




---- DEFINITIONS

/-
Linear program
-/
-- structure maximization_problem_with_constraints : Type :=
-- (problem : Prop)
-- (constraint_1 : Prop)
-- (constraint_2 : Prop)
-- (constraint_3 : Prop)

/-
Node on a network
-/
structure node : Type :=
(id : ℕ) -- we identify each node by a unique natural number

/-
Edge on a network:
represents the physical connections (e.g., optical fibers between the nodes).
-/
structure edge : Type :=
(node1 : node)
(node2 : node)
(cap : ℝ) -- we attach to each edge a real number called the capacity of the edge
-- which represents the maximum rate at which EPR pairs can be distributed 
-- between the two nodes of the edge.

/-
Path
"Corresponding to a demand (si, ei, Fi), if we start generating the EPR-pairs along a path 
p = ((si, u1),(u1, u2), . . . ,(u|p|−1, ei)), then the total number of required entanglement 
swap operations is |p|−1."
-/
structure path' : Type := -- Have to use path' because path is taken by Lean.
(edges : list edge) -- a path is a list of edges.

-- path-length notation
notation `|`p`|` := p.edges.length -- broken

/-
Entanglement distribution rate through a path
-/
def rate_of_path (p : path') : ℝ := sorry

/-
"In a quantum internet, we abstract the entire network as a graph G = (V, E, C), where V represents 
the set of repeaters as well as the set of end nodes, and the set of edges, E, abstracts the physical 
communication links."
-/
-- variable {F : ℝ} {hF : F > 0.5}

structure quantum_internet : Type := 
(V : list node) -- V is a list of nodes
(E : list edge) -- E is a list of edges.
-- (C : list (edge → ℝ)) -- C is a list of functions that each eat an edge and spit out a real number.
-- WE DEFINE THIS ABOVE AS A PROPERTY OF EDGES.
-- (hF : 
--     ∀ (u v : node) {u ∈ V ∧ v ∈ V},
--             ⟨u,v⟩ ∈ E → ⟨u,v⟩.fidelity ≥ F
-- ) 

/-
Demand
"Depending on the applications, the end nodes may need to generate EPR pairs with a certain fidelity. 
Keeping the analogy with the classical internet, here we refer to such requirement as a demand 
(commodity) and it consists of four items, a source s ∈ V , a destination e ∈ V , end-to-end desired 
entanglement distribution rate r and an end-to-end fidelity requirement F_end."
-/
-- variable {qInternet : quantum_internet}

structure demand : Type :=
(source : node)
(dest : node)
-- (rate : ℝ)
(min_fid : ℝ)  -- minimum fidelity required




---- ASSUMPTIONS

/-
"In this paper we assume that all the mixed entangled states in the network are Werner states. The main 
reason is that Werner states can be written as mixing with isotropic noise and hence form the worst case 
assumption."
-/
variables {n : ℕ} {ρ : Werner_state n}

/-
"We assume that the fidelity of all the EPR-pairs, generated between any two
nodes u, v ∈ V such that (u, v) ∈ E, is the same (say F)."
-/
variable {F : ℝ} -- F is the elementary link fidelity of all elementary links

/-
I think the Bell-state measurement success probability is assumed to be the same 
for all measurements.
-/
variables {q : ℝ} {hq : q > 0.5} -- BSM success probability

/-
I think the elementary link creation probability is assumed to be 1
throughout.
-/




---- PATH LENGTH CONSTRAINT

/-
Length-constraint of a demand:
computed from the minimum fidelity

"For the routing algorithms, one possible way to guarantee the end-to-end fidelity is to put an upper 
bound on the discovered path-lengths."
-/

/-
"In a quantum network, the fidelity of the EPR pairs drops with each entanglement swap 
operation. The fidelity of the output state after a successful swap operation depends on 
the fidelity of the two input states. 

If a mixed state ρ has fidelity F with respect to an EPR pair, say |Ψ⁺⟩ = 1/√2(|00⟩+|11⟩, 
then the corresponding Werner state [32] with parameter W can be written as
    ρ = W * |Ψ⁺⟩⟨ψ⁺| + (1 - W)/4 * I_4, 
where I_4 is the identity matrix with dimension 4.

The fidelity of this state is (1 + 3*W)/4    [Write Lean theorems about this stuff].

For the Werner states, if a node performs a noise-free entanglement swap operation between 
two EPR-pairs with fidelities F, then the fidelity of the resulting state is (1 + 3*W^2)/4, 
which is equal to 1 + 3/4*((4*F - 1) / 3)^2 [33]."
-/
theorem Werner_state_fidelity_after_k_swaps {n : ℕ} {ρ : density_operator n} (k : ℕ) (ws := Werner_state(ρ)): 
fidelity swap_gate_channel^k ws |ψ⁺⟩⟨ψ⁺| = (1 + 3*W)/4 :=
begin
    sorry
end

/-
The goal is to have 
1 + 3/4* ((4*F - 1) / 3)^(|p|) ≥ Fᵢ, 
where Fᵢ is the minimum fidelity required in a given demand.
-/
def satisfies_fidelity_constraint_of_demand (p : path') (d : demand) : Prop :=
1 + 3/4* ((4*F - 1) / 3)^(p.edges.length) ≥ d.min_fid

/-
"From this relation, we get the following constraint on the length of the p: 
|p| ≤ floor( real.log ((4*Fᵢ - 1) / 3) / real.log ((4*F - 1) / 3)  )."
-/
theorem max_path_length_of_fidelity (p : path') (D : list demand) :
∀ (d : demand) {hd : d ∈ D}, satisfies_fidelity_constraint_of_demand p d →
p.edges.length ≤ floor( real.log ((4*d.min_fid - 1) / 3) / real.log ((4*F - 1) / 3) ) :=
begin
    sorry
end

/-
"For the entanglement distribution rate, here we let the achievable rate between two along a 
repeater chain (a path) p be any real number rₚ such that 
rₚ ≤ q^(|p| - 1) * min{C(⟨s,u1⟩), C(⟨u1,u2⟩), ..., C(⟨u*|p|-1,e⟩)},
where C(⟨u,v⟩) denotes the capacities of the edges on the path and q is the success probability 
of the Bell-state measurements."
-/
def is_achievable_rate (r : ℝ) (p : path') : Prop := 
r ≤ q^(p.edges.length - 1) * min{p.edges[0].cap, p.edges[1].cap, ..., p.edges[p.edges.length-1].cap}




---- GRAPH MODIFICATION

/-
"In this paper, we borrow ideas from the length-constrained multi-commodity flow [22] to handle 
this problem. In order to implement the length constraint we need to modify the network graph
G as well as the demand set D."
-/

/-
Proposition 1
The run-time helper proposition.
I am going to ignore the run-time proofs for the first pass.
-/
theorem Proposition_1 : 
|P i j| ≤ |E| * |V| :=
begin
    sorry
end

/-
Theorem 1
-/
theorem Theorem_1 : 
algorithm1.runtime ≤ |D| * |V| * |E| :=
begin
    sorry
end




---- EDGE-BASED IS AT LEAST AS GOOD AS PATH-BASED

/-
Proposition 2
-/
def g_tilde (e : edge) : ℝ := sorry

theorem Proposition_2 : 
∀ (e' ∈ extended_network.edges),
    ∑_i=1^k ∑_j=1^lᵢ ∑_p∈Pᵢⱼ rₚ = ∑_i=1^k ∑_j=1^lᵢ q^(j-1) * ∑_v¹:(sᵢ⁰,v¹)∈E' g_tilde(⟨s_i⁰,v¹⟩) :=
begin
    -- According to the definition of ˜gij in equation ...
    unfold g_tilde,
    -- This implies, 
    rw mul_iff_div,
    -- sum over the two intervals and done
    rw sum_eq_sum,
    sorry
end

/-
Proposition 3
-/
theorem Proposition_3 : 
∀ ... ,
    ∑_i=1^k ∑_j=1^lᵢ ∑_t=0^{l_max-1} g_tilde i j ⟨u(t),v(t+1)⟩ ≤ C(⟨u,v⟩) :=
begin
    unfold g_tilde,
    sorry
end

/-
Proposition 4
-/
theorem Proposition_4 : 
∀ ... ,
    ∑  g_tilde i j ⟨u',v'⟩ = ∑  g_tilde i j ⟨v',w'⟩ :=
begin
    unfold g_tilde,
    sorry
end




---- PATH-BASED IS AT LEAST AS GOOD AS EDGE-BASED

/-
Proposition 5
-/
theorem Proposition_5 : 
∀ e' ∈ extended_network.edges,
    F i j m e' ≥ 0 :=
begin
    sorry
end

/-
Proposition 6
Depends on stuff in algorithm 3.
-/
theorem Proposition_6 : 
∀ ... ,
 |P i j| ≤ extended_network.edges.length :=
begin
    sorry
end

/-
Proposition 7
-/
theorem Proposition_7 : 
∀ ... ,
    ∑  F i j m ⟨u',v'⟩ = ∑  F i j m ⟨v',w'⟩ :=
begin
    sorry
end

/-
Proposition 8
-/
def P : list (list path') := sorry

def F (i j m : ℕ) (e : edge) : ℝ := sorry

theorem F_recursion_relation (i j m : ℕ) : -- should this be a theorem?
∀ e' ∈ extended_network.edges, 
    F i j m e' = F i j (m-1) e' - (r_tilde ()) / q^(j-1)
begin
    sorry
end

def r_tilde (p : path') (j m : ℕ) : ℝ := 
q^(j-1) * min_{e ∈ (p j m).edges} {F i j m e}

theorem Proposition_8 : 
∀ e ∈ network.edges ,
    ∑ i ∈ finset.range(k), 
    ∑ j ∈ finset.range(l[i]),
    ∑ t ∈ finset.range(l.max),
    ∑ (r_tilde p j m) / q^(j-1) ≤ e.cap :=
begin
    sorry
end

/-
Proposition 9
-/
theorem Proposition_9 : 
∀ ... ,
    ∑ ∑ q^(j-1) ∑  g i j ⟨sᵢ⁰,v¹⟩ = ∑ ∑ ∑  r_tilde p :=
begin
    sorry
end




---- PREPARE AND SWAP

/-
"We point out that there exists a practical entanglement distribution protocol along a path, called the 
prepare and swap protocol, which achieves the rates (asymptotically) proposed by path extraction algorithm."
-/

/-
Theorem (Lemma 3 in Appendix D in the paper)
"In a repeater chain network with n + 1 repeaters {u0, u1, . . . , un}, if the probability of generating
an elementary pair per attempt is one and the probability of a successful BSM is (q) and the capacity of 
an elementary link (ui, ui+1) (for 0 ≤ i ≤ n − 1) is denoted by Ci and if the repeaters follow the prepare 
and swap protocol for generating EPR-pairs, then the expected end-to-end entanglement generation rate r
is ... "
-/
theorem prepare_and_swap_rate (stuff) : 
r = q^(n-1) * min{C₀, ..., C_n} :=
begin
    sorry
end




---- EDGE-BASED FORMULATION

def edge_based_maximization_problem : maximization_problem_with_constraints :=
⟨
    ∑ ∑ q^(j-1) * ∑ g i j ⟨sᵢ⁰,v¹⟩,

    ∀ ..., 
        g i j ⟨u(t),v(t+1)⟩,

    ∀ ...,
        ∑ ∑ ∑ g i j ⟨u(t),v(t+1)⟩ ≤ C ⟨u,v⟩,

    ∀ ..., 
        g i j ⟨u',v'⟩ = g i j ⟨v',w'⟩   
⟩




---- PATH-BASED FORMULATION

/-
Path-based problem on the original network
-/
def path_based_maximization_problem : maximization_problem_with_constraints :=
⟨ 
    ∑ ∑ rₚ,

    ∑ ∑ rₚ / q^(|p|-1) ≤ C ⟨u,v⟩,

⟩

/-
Path-based problem on the modified network
-/
def path_based_maximization_problem : maximization_problem_with_constraints :=
⟨ 
    ∑ ∑ ∑ rₚ,

    ∑ ∑ ∑ ∑ rₚ / q^(|p|-1) ≤ C ⟨u,v⟩,

⟩




---- SOLUTION TO EDGE-BASED PROBLEM IFF SOLUTION TO PATH-BASED PROBLEM




---- PATH EXTRACTION ALGORITHM

/-
"we provide an algorithm, called the path extraction algorithm, which takes the solutions of the
edge-based formulation and for each of the commodities it extracts the set of paths to be used and
the corresponding entanglement distribution rate along that path."
-/




---- CLOSING REMARKS

/-
"One can use any entanglement generation protocol for distributing EPR-pairs across the paths that are discovered 
by the path-extraction algorithm."

"Some repeater technologies are unable to perform such quantum operations (for instance, the atomic ensemble-based 
quantum repeaters). Hence, for such cases, one can achieve the end-to-end fidelity requirement only by increasing 
the fidelity F of the elementary pairs and reducing the length of the discovered path."

But if you can do distillation you can increase the fidelity of the end-to-end links:
"One can enhance the end-to-end fidelity using entanglement distillation."
-/

/-
"There exists a practical protocol, called prepare and swap protocol, which can be implemented using atomic ensemble 
based repeaters and if one uses this protocol for distributing entanglement across each of the paths, then one can 
generate EPR-pairs with the rate proposed by our path-extraction algorithm."
-/

/-
"In this paper, we focus on maximising the end-to-end entanglement generation rate. However, one can easily extend 
our results for other objective functions, like minimising the weighted sum of congestion at edges."
-/

/-
"In future work, it would be interesting to include the more realistic parameters like the bounded storage capacity, 
time to perform the swap operation, etc., in our model and modify our current formulations to come up with more 
sophisticated routing algorithms."
-/

/-
Where the authors took inspiration from: "Our algorithm is inspired by multi-commodity flow optimisation which is a 
very  well-studied subject and has been used in many optimisation problems, including classical internet routing [13]."
-/




---- SCRATCH WORK AND NOTES

/-
"Don't make a new structure for the linear programs. Just prove the theroems 
about them and use the PuLP implementation in Kaushik's Github."
-/