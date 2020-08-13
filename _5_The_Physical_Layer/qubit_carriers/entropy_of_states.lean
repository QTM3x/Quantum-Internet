import .quantum_state



---- QUANTUM ENTROPY

/-
Definition (Quantum entropy): 
-/
def quantum_entropy (ρ : density_operator) : ℝ := - Tr(ρ * log(ρ))

notation `H(` ρ `)` := quantum_entropy(ρ)



---- PROPERTIES OF QUANTUM ENTROPY

/-
Theorem (non-negativity): Quantum entropy is non-negative.
-/
theorem quantum_entropy_nonnegative : ∀ (ρ : density_operator), H(ρ) ≥ 0 :=
-- proof
begin
    sorry
end


/-
Theorem (minimum value): The minimum value of quantum entropy is 
zero and occurs when the state is pure.
-/
theorem minimum_value_quantum_entropy : 
∀ (ρ : density_operator), is_pure ρ → H(ρ) = 0 := sorry


/-
Theorem (maximum value): The maximum value of quantum entropy is 
log d and occurs when the state is the maximally mixed state.
-/
theorem maximum_value_quantum_entropy := sorry


/-
Theorem (additivity of tensor states)
-/
theorem additive_quantum_entropy_tensor_states :
∀ (ρ₁ : density_operator) (ρ₂ : density_operator), H(ρ₁ ⊗ ρ₂) = H(ρ₁) + H(ρ₂) := sorry



---- CONDITIONAL QUANTUM ENTROPY

/-
Definition (conditional quantum entropy)
-/
def cond_quantum_entropy (ρ : density_operator) : ℝ := sorry



---- COHERENT INFORMATION

/-
Definition (coherent information)
-/
def coherent_information (ρ : density_operator) : ℝ := sorry

/-
Definition (reverse coherent information): 
-/
def reverse_coherent_information (ρ : density_operator) := sorry



---- QUANTUM MUTUAL INFORMATION

/-
Definition (quantum mutual information)
-/
def quantum_mutual_information (ρ : density_operator) : ℝ := sorry



---- HOLEVO INFORMATION

/-
Definition (Holevo information)
-/
def Holevo_information (ρ : density_operator) := sorry



---- ACCESSIBLE INFORMATION

/-
Definition (Accessible information)
-/
def accessible_information := sorry



---- CONDITION QUANTUM MUTUAL INFORMATION

/-
Definition (conditional quantum mutual information)
-/
def cond_quantum_mutual_information := sorry



---- QUANTUM RELATIVE ENTROPY

/-
Definition (quantum relative entropy)
-/
def quantum_relative_entropy (ρ : density_operator) (σ : positive_semidefinite_operator) := sorry

notation `D(` ρ `∥` σ `)` := quantum_relative_entropy(ρ,σ)

