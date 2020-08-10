import analysis.special_functions.exp_log

-- Capacity of Quantum Channels


/-
To transmit quantum information, optical fibers are utilised and these can be modelled as quantum channels. These channels are usually not ideal and lead to information losses. To makes estimates of number of entanglement generation rate and to choose ideal entanglement purification process, it is necessary to study and determine the capacity of the channel. This document consists of information on
1) Basic quantum channel definitions, notations and theorems (without proofs)
2) Optical fiber channels
-/




-- Basic Quantum channel definitions, notations and theorems.


/-
Defintion (quantum channel): A quantum channel is a completely 
positive, trace-preserving linear map.
-/

def positive_semidefinite (M : matrix) :=
∀ e ∈ eigenvalues M, e ≥ 0

structure density_operator : Type :=
(M : matrix)
(positive_semidefinite : positive_semidefinite M)

def positive (map : type1 → type2) : 
∀ (M : matrix) (hM : positive_semidefinite M), positive_semidefinite (map M) 

def identity_map (dim : ℕ) := sorry

def completely_positive (map : type1 → type2) : 
∀ (n : ℕ), positive ((identity_map n) ⊗ map)

structure quantum_channel : Type :=
(map : type1 → type2)
(linear: map(α * XA + β * YA) = α * map(XA) + β * map(XB))
(completely_positive : completely_positive map)
(trace_preserving : trace (map ρ) = trace ρ)

/-
Channels can be mathematically modelled as evolutions of 
the state by an operator, that is usually not unitary. An 
important representation is the Krauss representation.
-/

/-
Theorem (Krauss representation): for any quantum channel 
𝒩 there exists a list of operators Vᵢ such that for any 
density operator ρ, ∑ i, Vᵢ * ρ * Vᵢ† = 𝒩(ρ), and 
∑ i, Vᵢ† * Vᵢ = I
-/
theorem Krauss_representation : 
∀ (𝒩 : quantum_channel), ∃ list V, (∑ i, Vᵢ * ρ * Vᵢ† = 𝒩.map(ρ) ∧ ∑ i, Vᵢ† * Vᵢ = I) :=
sorry


/-
A useful representation that can be directly derived from 
this is the stinespring representation, which is nothing 
but tracing out ancilla state from the purification of the
Krauss representation:
-/

...

/-
Another useful representation is the choi representation 
of the channel, given by:
-/

...

/-
This representation is particularly useful since it allows 
representations to be vectorisation of input and channel 
operators and also directly reflects the channel effect on 
a maximally entangled pair, and this property is used in to 
simplify our proof.
-/




-- Quantum capacity

/-
Capacity of a channel is the maximum rate of information 
(classical or quantum) that can be transmitted such that 
useful information can be received (or decoded) at the 
receiving end.

The reason we use the limit stems arises due to Shannon's 
theories and that, depending on channel, one always has a 
finite chance of failing to transmit information and in 
the infinite limit, this probability goes to zero.

The quantum capacity of a channel, (which is also the same 
as entanglement generation capacity) is given by
-/

...

/-
Intuitively, Coherent information captures the quantum 
information in common to the input and output of the 
channel, similar to mutual information.
-/




-- Complementary channels

...

/-
The closed form quantum capacities of many channel models 
still are not known.
-/




-- Optical fiber channels

/-
For our purposes, the optical quantum channel is modelled 
as a Phase insensitive Gaussian channel. We can possibly 
choose an input state and protocol that is optimal for 
this. So we need to study the channel and it's properties 
so as to determine it's quantum capacity and hence it's 
fidelity with respect to distance.
-/

/-
Optical fibres similar to those currently used in the 
classical internet system can be used to transmit quantum 
states, via photons, which are bosonic in nature. We can 
represent bosonic states by the fock number representation
|n⟩ where n denotes the number of photons and not the 
state of the photon. These are similar to the modes of 
the Quantum Harmonic oscillator.
-/

/-
For QKD systems and any quantum transmission systems, we 
can model it in two ways, using single photon states and 
it's state and polarisation determining the state. This 
requires single photon sources that may not be readily 
available. The photon output can be modelled by a 
poissonic distribution and in the case of multiple 
photons simultaneously emmited, we can show that QKD 
is not computationally secure and eve can just use a 
beam splitter and retain one of the photons. Though one 
can design protocols that are computationally secure 
(Refer Renato Renner's thesis), we can show that for 
realistic quantum networks where there are high loses 
and single photon sources are both hard to create and 
the single photon has a very low probability of 
successfully making it to the receiver in a coherent 
fashion. We use Gaussian states over mulitple modes 
and > 1 average number of photons to model transmission 
and is detailed below. We can also show that since 
optical channels are gaussian, best rates are achieved 
using gaussian states.
-/

/-
A Wigner function is a phase space mapping of a state, 
something like a fourier transform, except into the 
phase space joint space.
-/
def Wigner_function : density_operator →   := sorry

/-
A general bosonic state is given by ρ(μ,V), (μ is the 
mean and the covariance matrix is given by V)
-/
def bosonic_quantum_state : density_operator := sorry


/-
A pure state is Gaussian if and only if it's wigner 
function is positive.
-/
def is_pure : Prop := sorry

theorem (ρ : density_operator) : 
is_pure ρ ↔ positive (Wigner_function ρ) := sorry


/-
A Gaussian channel is nothing but a channel that takes 
a Gaussian state to another Gaussian state.
-/
def Gaussian_channel (η : ℝ) : quantum_channel := sorry




-- Capacity derivation

/-
Defintion (two-way capacity): A function that takes a 
quantum channel 𝒩 and returns a real number. This real 
number is given by ...
-/
def two_way_capacity (𝒩 : quantum_channel) : ℝ := sorry


/-
Definition (σ-stretching): 
-/
def sigma_stretching (𝒩 : quantum_channel) := sorry


/-
Defintion (KL divergence): 
-/
def KL_divergence := sorry


/-
Defintion (relative entanglement entropy): 
-/
def rel_entanglment_entropy := sorry

/-
Defintion (coherent information): 
-/
def I_c (ρ₁ ρ₂ : density_operator) : ℝ := sorry


/-
Definition (reverse coherent information): 
-/
def I_nc (ρ₁ ρ₂ : density_operator) := sorry


/-
The two-way capacity of this lossy channel for any 
repeaterless implementation of the channel can be shown 
to be C = - log(1-η) per mode, where η represents the 
physical channel's transmissivity. η varies with distance 
exponentially with a constant loss (α) in dbm units.
-/
theorem two_way_capacity_Gaussian_channel : 
two_way_capacity Gaussian_channel = - real.log(1-η) :=
begin
    -- One of the main idea of the proof to establish 
    -- bounds is σ-stretching of the channel.
    sorry
end
