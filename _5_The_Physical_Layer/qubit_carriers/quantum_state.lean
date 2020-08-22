import data.real.basic
import common.matrix_ops

-- variables {n m : ℕ}
variables (n m : ℕ)

---- STATES IN FINITE DIMENSIONAL HILBERT SPACE

/-
Definition (density operator): A quantum state/density operator is 
a positive semi-definite matrix with trace 1.
-/
structure density_operator (n : ℕ) : Type :=
(dim : ℕ)
(M : matrix (fin n) (fin n) ℂ)
(positive_semidefinite : positive_semidefinite M)
(trace_one : Tr(M) = 1)




---- STATES IN INFINITE DIMENSIONAL HILBERT SPACE

-- structure infinite_dim_density_operator : Type := 
-- ()
-- (positive_semidefinite : )
-- (trace_one : )




---- PURE STATES

/-
Definition (pure states): A quantum state is pure when ...
-/
def purity (ρ : density_operator n) : ℝ := Tr(ρ.M† * ρ.M)

def is_pure (ρ : density_operator n) : Prop := purity ρ = 1

/-
Theorem
-/
theorem is_pure_unit_vec (ρ : density_operator n) : 
is_pure ρ ↔ ∃ (ψ : unit_vector), ρ = ∣ψ⟩⟨ψ∣ := 
begin
    sorry
end

/-
Theorem (purity unitary invariant): Purity is conserved under
unitary evolutions.
-/
theorem purity_unitary_invariant {U : matrix (fin n) (fin n) ℂ} {hU : is_unitary U} : 
∀ (ρ : density_operator n), purity(U*ρ*U†) = purity(ρ) :=
begin
    sorry
end

/-
Definition (purification of a density operator)
-/
def is_purification (ρ : density_operator n) (∣ψ⟩ : pure_state) : 
Prop := Tr_E(∣ψ⟩⟨ψ∣) = ρ




---- ENTANGLED STATES

/-
Definition (maximally entangled state with a given dimension)
-/
def maximally_entangled_state (dim : ℕ) : density_operator dim :=
⟨(∑ᵢ ∣i⟩∣i⟩)*(∑ᵢ ∣i⟩∣i⟩)† , _ , _ ⟩ 




---- TENSOR PRODUCT OF DENSITY OPERATORS

/- 
Lemma: The tensor product of two positive semidefinite 
matrices is a positive semi-definite matrix.
-/
lemma tensor_states_pos_semidef 
(M₁ : matrix (fin n) (fin n) ℂ) 
(M₂ : matrix (fin m) (fin m) ℂ) 
(hM : (positive_semidefinite M₁) ∧ (positive_semidefinite M₂)) : 
positive_semidefinite (M₁ ⊗ M₂) :=
begin
    sorry
end

/-
Lemma: The tensor product of two matrices with trace 1 is a matrix with 
trace 1.
-/
lemma tensor_trace_one (M₁ : matrix (fin n) (fin n) ℂ) 
(M₂ : matrix (fin m) (fin m) ℂ) : 
Tr(M₁) = 1 ∧ Tr(M₂) = 1 → Tr(M₁ ⊗ M₂) = 1 :=
begin
    sorry
end

/-
Definition (tensor product of states)
-/
def tensor_states (ρ₁ : density_operator n) (ρ₂ : density_operator m) 
: density_operator (n*m) := ⟨ρ₁.M ⊗ ρ₂.M , _ , _ ⟩




---- CLASSICAL-QUANTUM STATES

/-
Definition (classical-quantum states)
-/
def is_classical_quantum (ρ : density_operator n) : Prop := sorry




---- WIGNER FUNCTION

/-
Definition (Wigner function): A Wigner function is a phase space 
mapping of a state,something like a fourier transform, except into 
the phase space joint space.
-/
-- def Wigner_function : density_operator →   := sorry

/-
A pure state is Gaussian if and only if it's wigner 
function is positive.
-/
-- theorem pure_state_Wigner_function (ρ : density_operator) : 
-- is_pure ρ ↔ positive (Wigner_function ρ) := sorry




---- EXAMPLE STATES

/-
Definition (maximally mixed state): A maximally mixed state of 
dimension n is the state whose matrix is given by the I/n.
-/
def maximally_mixed_state (dim : ℕ) : density_operator dim := 
⟨1/dim • id_matrix dim , _ , _ ⟩ 

-- notation `π_` d := maximally_mixed_state d

/-
Definition (zero state)
-/
def zero_state (dim : ℕ) : density_operator dim := sorry

/-
Definition (one state)
-/
def one_state (dim : ℕ) : density_operator dim := sorry

/-
Definition (bosonic state): A general bosonic state is given by ρ(μ,V), (μ is the 
mean and the covariance matrix is given by V)
-/
-- def bosonic_state : density_operator := sorry