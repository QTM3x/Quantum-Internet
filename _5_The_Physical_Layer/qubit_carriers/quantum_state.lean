import common.matrix_ops

-- variables {n m : ℕ}
variables (n m : ℕ)


/-
Definition (density operator): A quantum state/density operator is 
a positive semi-definite matrix with trace 1.
-/
structure density_operator : Type :=
(M : matrix (fin n) (fin n) ℂ)
(positive_semidefinite : positive_semidefinite M)
(trace_one : Tr(M) = 1)




-- PURE STATES

/-
Definition (pure states): A quantum state is pure when ...
-/
def purity (ρ : density_operator n) : ℝ := Tr(ρ.M† * ρ.M)

def is_pure (ρ : density_operator n) : Prop := purity ρ = 1

theorem is_pure_unit_vec (ρ : density_operator n) : 
is_pure ρ ↔ ∃ (ψ : unit_vector), ρ = ∣ψ⟩⟨ψ∣

/-
Theorem (purity unitary invariant): Purity is conserved under
unitary evolutions.
-/
theorem purity_unitary_invariant {U : matrix (fin n) (fin n) ℂ} {hU : is_unitary U} : 
purity(U*ρ*U†) = purity(ρ) := sorry




-- TENSOR PRODUCT OF DENSITY OPERATORS

/- 
Lemma: The tensor product of two positive semidefinite 
matrices is a positive semi-definite matrix.
-/
lemma tensor_states_pos_semidef (M₁ : matrix (fin n) (fin n) ℂ) 
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
(M₂ : matrix (fin m) (fin m) ℂ) (hM : (Tr(M₁) = 1) ∧ (Tr(M₂) = 1)): 
Tr(M₁ ⊗ M₂) = 1 :=
begin
    sorry
end

/-
Definition (tensor product of states)
-/
def tensor_states (ρ₁ : density_operator n) (ρ₂ : density_operator m) 
: density_operator (n*m) := ⟨ρ₁.M ⊗ ρ₂.M , _ , _ ⟩




-- WIGNER FUNCTION

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
def maximally_mixed_state : density_operator n := sorry

/-
Definition (bosonic state): A general bosonic state is given by ρ(μ,V), (μ is the 
mean and the covariance matrix is given by V)
-/
def bosonic_state : density_operator := sorry
