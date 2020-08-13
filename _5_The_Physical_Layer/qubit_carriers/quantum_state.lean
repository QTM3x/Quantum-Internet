import common.matrix_ops

variables {n m : ℕ}

/-
Definition (density operator): A quantum state/density operator is 
a positive semi-definite matrix with trace 1.
-/
structure density_operator : Type :=
(M : matrix (fin n) (fin n) ℂ)
(positive_semidefinite : positive_semidefinite M)
(trace_one : trace M = 1 )

/-
Definition (pure states): A quantum state is pure when ...
-/
def is_pure (ρ : density_operator) := sorry

/-
Definition (tensor product of states)
-/
def tensor_states (ρ₁ : density_operator) (ρ₂ : density_operator) 
: density_operator := sorry -- use kronecker product 


/-
Deinfition (Wigner function): A Wigner function is a phase space 
mapping of a state,something like a fourier transform, except into 
the phase space joint space.
-/
def Wigner_function : density_operator →   := sorry



/-
A pure state is Gaussian if and only if it's wigner 
function is positive.
-/
theorem pure_state_Wigner_function (ρ : density_operator) : 
is_pure ρ ↔ positive (Wigner_function ρ) := sorry






---- EXAMPLE STATES

/-
Definition (maximally mixed state): A maximally mixed state of 
dimension n is the state whose matrix is given by the I/n.
-/
def maximally_mixed_state : density_operator := sorry

/-
Definition (bosonic state): A general bosonic state is given by ρ(μ,V), (μ is the 
mean and the covariance matrix is given by V)
-/
def bosonic_state : density_operator := sorry
