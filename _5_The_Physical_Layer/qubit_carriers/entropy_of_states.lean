import data.real.basic
import analysis.special_functions.exp_log
import _5_The_Physical_Layer.qubit_carriers.quantum_state
import _5_The_Physical_Layer.optical_fiber.quantum_channel
import common.shannon_theory

notation `|` x `|` := abs x

variables {n m : ℕ}

noncomputable theory

---- QUANTUM ENTROPY

/-
Definition (Quantum entropy):
"Suppose that Alice generates a quantum state ∣ψy⟩ in her 
lab according to some probability density p_Y(y), corresponding
to a random variable Y. Suppose further that Bob has not yet 
received the state from Alice and does not know which one she sent.
The expected density operator from Bob’s point of view is then
σ =  𝐄_Y{∣ψY⟩⟨ψY∣} = ∑ y, p_Y(y) • ∣ψy⟩⟨ψy∣.
The interpretation of the entropy H(σ) is that it quantifies Bob’s 
uncertainty about the state Alice sent — his expected information 
gain is H(σ) qubits upon receiving and measuring the state that 
Alice sends."
https://arxiv.org/pdf/1106.1445.pdf
-/
def quantum_entropy (ρ : density_operator n) : ℝ := 
- Tr(ρ.M * matrix_log(ρ.M)).re

notation `H(` ρ `)` := quantum_entropy ρ

/-
Definition (quantum entropy of spectral decomposition)
-/
-- def quantum_entropy_of_spectral_decomposition : 

/-
Theorem (quantum entropy of state and shannon entropy of prob dist)
-/
theorem quantum_entropy_eq_shannon_entropy_of_prob_dist
{ρ : density_operator n} 
{prob_dist : multiset ℝ} :
-- {hρ : ρ = ∑ i, prob_dist i • ∣i▸dim⟩⟨i▸dim∣} : 
H(ρ) = shannon_entropy(prob_dist) :=
begin
    unfold quantum_entropy,
    unfold shannon_entropy,
    sorry
end

/-
Theorem (non-negativity): Quantum entropy is non-negative.
-/
theorem quantum_entropy_nonneg {n : ℕ} : 
∀ (ρ : density_operator n), H(ρ) ≥ 0 :=
begin
    intro ρ,
    -- This follows from non-negativity of Shannon entropy
    -- rw quantum_entropy_eq_shannon_entropy_of_prob_dist,
    -- exact shannon_entropy_nonneg,
    sorry
end

/-
Theorem (minimum value): The minimum value of quantum entropy is 
zero and occurs when the state is pure.
-/
theorem minimum_value_quantum_entropy : 
∀ (ρ : density_operator n), is_pure ρ → H(ρ) = 0 := sorry

/-
Theorem (maximum value): The maximum value of quantum entropy is 
log d and occurs when the state is the maximally mixed state.
-/
theorem maximum_value_quantum_entropy {ρ : density_operator} : 
H(ρ) ≤ real.log ρ.dim :=
begin
    sorry
end

/-
Theorem (additivity for tensor states)
-/
theorem additive_quantum_entropy_tensor_states :
∀ (ρ₁ : density_operator n) (ρ₂ : density_operator m), H(ρ₁ ⊗ ρ₂) = H(ρ₁) + H(ρ₂) := 
begin
    sorry
end

/-
Theorem (Araki-Lieb triangle inequality)
-/
theorem Araki_Lieb {ρ : density_operator} : 
|H(A)_ρ - H(B)_ρ| ≤ H(AB)_ρ := 
begin
    sorry
end

/-
Theorem (strong subadditivity)
Page 345 here https://arxiv.org/pdf/1106.1445.pdf.
-/
theorem strong_subadditivity {ρ : density_operator} :
H(AC)_ρ + H(BC)_ρ ≥ H(ABC)_ρ + H(C)_ρ :=
begin
    have : I(A;B|C)_ρ = H(AC)_ρ + H(BC)_ρ - H(ABC)_ρ - H(C)_ρ, {sorry},
    have : I(A;B|C)_ρ = H(B|C)_ρ - H(B|AC)_ρ, {sorry},
    have : -H(B|AC)_ρ = D(ρ∥I⊗Tr_B(ρ)), {sorry},
    have : H(B|C)_ρ =  -D(Tr_A(ρ)∥I⊗Tr_AB(ρ)), {sorry},
    have : D(ρ∥I_B⊗Tr_B(ρ)) ≥ D(Tr_A(ρ)∥I_B⊗Tr_AB(ρ)), {sorry},
    sorry
end

/-
Theorem (unital channels increase entropy)
-/
theorem unital_channels_increase_entropy 
{ρ : density_operator} {𝒩 : quantum_channel} {h𝒩 : is_unital(𝒩)} : 
H(𝒩(ρ)) ≥ H(ρ) :=
begin
    sorry
end




---- CONDITIONAL QUANTUM ENTROPY

/-
Definition (conditional quantum entropy)
-/
def cond_quantum_entropy (ρ : density_operator n) : ℝ := H(ρ) - H(Tr_A(ρ))

notation `H(` A `|` B `)_` ρ := cond_quantum_entropy(ρ)

/-
Theorem (conditioning does not increase entropy)
-/
theorem cond_entropy_leq_entropy (ρ : density_operator n) : 
H(A)_ρ ≥ H(A|B)_ρ := 
begin
    sorry
end

/-
Theorem (maximum of abs of conditional quantum entropy)
Page 333 here https://arxiv.org/pdf/1106.1445.pdf.
-/
theorem cond_quantum_entropy_max : 
∀ (ρ : density_operator n), |H(A|B)_ρ| ≤ real.log Tr_B(ρ).dim :=
begin
    -- start by rewriting using abs_le

    -- first we prove that H(A|B)_ρ ≤ real.log Tr_B(ρ).dim

    -- then we prove that H(A|B)_ρ ≥ - real.log Tr_B(ρ).dim
    sorry
end

/-
Theorem (The π_A ⊗ π_B state saturates condition quantum entropy)
-/
theorem cond_quantum_entropy_saturated {ρ := π⊗π} : 
H(A|B)_ρ = real.log Tr_B(ρ).dim := 
begin
    sorry
end




---- COHERENT INFORMATION

/-
Definition (coherent information)
-/
def coherent_info (ρ : density_operator n) {hρ : ρ.dim ≥ 4} : ℝ := 
H(pTr(ρ.M , ρ.dim/2)) - H(ρ)

notation `I(` A `⟩` B `)_` ρ := coherent_information(ρ)

/-
Definition (reverse coherent information): 
-/
def reverse_coherent_info (ρ : density_operator n) := sorry

/-
Theorem (coherent information of a maximally entangled state)
-/
theorem coherent_info_max_ent_state 
{ρ : density_operator n} {hρ : is_maximally_entangled} :
I(A⟩B)_ρ = ... := 
begin
    sorry
end

/-
Theorem (coherent information of purification)
"Thus, there is a sense in which the coherent information 
measures the difference in the uncertainty of Bob and the 
uncertainty of the environment."
https://arxiv.org/pdf/1106.1445.pdf
-/
theorem coh_info_purification : 
∀ (ρ : density_operator n), 
    ∃ {∣ψ⟩ : pure_state} {hψ : is_purification ρ ∣ψ⟩}, 
        I(A⟩B)_ρ = H(B)_∣ψ⟩ - H(E)_∣ψ⟩ :=
begin
    sorry
end




---- QUANTUM MUTUAL INFORMATION

/-
Definition (quantum mutual information)
-/
def mut_info (ρ : density_operator n) : ℝ := 
H(A)_ρ + H(B)_ρ - H(AB)_ρ

notation `I(` A `;` B `)_` ρ := mut_info(ρ)

/-
Lemma (rewrite in terms of cond entropy)
-/
lemma mut_info_cond_ent {ρ : density_operator n} :
I(A;B)_ρ = H(A)_ρ - H(A|B)_ρ :=
begin
    sorry
end

/-
Lemma (another rewrite in terms of cond entropy)
-/
lemma mut_info_cond_ent' {ρ : density_operator n} : 
I(A;B)_ρ = H(B)_ρ - H(B|A)_ρ :=
begin
    sorry
end

/-
Lemma (non-negativity)
-/
lemma mut_info_nonneg {ρ : density_operator n} : 
I(A;B)_ρ ≥ 0 :=
begin
    sorry
end




---- HOLEVO INFORMATION

/-
Definition (Holevo information)
-/
def Holevo_info (ρ : density_operator n) := sorry




---- ACCESSIBLE INFORMATION

/-
Definition (accessible information)
-/
def accessible_info := sorry




---- CONDITIONAL QUANTUM MUTUAL INFORMATION

/-
Definition (conditional quantum mutual information)
-/
def cond_mut_info (ρ : density_operator n) : ℝ := 
H(A|C)_ρ + H(B|C)_ρ - H(AB|C)_ρ

notation `I(` A `;` B `|` C `)_` ρ := cond_mut_info ρ

/-
Lemma (quanutm mutual information chain rule)
-/
lemma mut_info_chain_rule {ρ : density_operator n} :
I(A;BC)_ρ = I(A;B)_ρ + I(A;C|B)_ρ :=
begin
    sorry
end

/-
Lemma (non-negativity / a.k.a. strong subadditivity)
-/
lemma cond_mut_info_nonnegative {ρ : density_operator n} : 
I(A;B|C)_ρ ≥ 0 :=
begin
    sorry
end

/-
Lemma ("duality" of condition mutual information)
-/
lemma duality {ρ : density_operator n} {hρ : is_pure ρ} : 
I(A;B|C)_ρ = I(A;B|D)_ρ :=
begin
    sorry
end




---- QUANTUM RELATIVE ENTROPY

/-
Definition (quantum relative entropy)
-/
def quantum_relative_entropy (ρ : density_operator n) (σ : positive_semidefinite_operator) := sorry

notation `D(` ρ `∥` σ `)` := quantum_relative_entropy(ρ,σ)

/-
Theorem (quantum Pinsker inequality)
-/
theorem quantum_pinsker {ρ : density_operator n} {σ : linear_operator} : 
D(ρ∥σ) ≥ 1/(2 * ln 2) * ∥ρ - σ∥₁^2 := 
begin
    sorry
end




---- SQUASHED ENTANGLEMENT

/-
Definition (squashed entanglement of quantum state for a given partition)
-/
def squashed_entanglement (ρ : density_operator n) 
{hρ : ρ.dim > 4} (partition_point : ℕ) : ℝ := sorry