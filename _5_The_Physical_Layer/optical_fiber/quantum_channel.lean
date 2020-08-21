import common.matrix_ops
import _5_The_Physical_Layer.qubit_carriers.quantum_state

-- Basic Quantum channel definitions, notations and theorems.

variables {n m k l : ℕ}


---- QUANTUM CHANNEL BETWEEN STATES IN FINITE DIM HILBERT SPACE

/-
Defintion (quantum channel): A quantum channel is a completely 
positive, trace-preserving linear map.
-/
structure quantum_channel (in_dim : ℕ) (out_dim : ℕ) : Type :=
(map : matrix (fin in_dim) (fin in_dim) ℂ → matrix (fin out_dim) (fin out_dim) ℂ)
(linear: linear map)
(completely_positive : completely_positive map)
(trace_preserving : trace_preserving map)




---- QUANTUM CHANNEL BETWEEN STATES IN INFINITE DIM HILBERT SPACE

-- structure infinite_dim_quantum_channel : Type :=
-- (map : )




---- TENSOR PRODUCT OF CHANNELS

/-
Definition (tensor product of channels)
-/
def tensor_channel (𝒩 : quantum_channel n m) (ℳ : quantum_channel k l) : 
quantum_channel (n*k) (m*l):= sorry

notation 𝒩 `⊗_c` ℳ := tensor_channel 𝒩 ℳ -- note the prime

/-
Definition (tensor power of channels)
-/
def tensor_pow_channel 
(𝒩 : quantum_channel n m) (p : ℕ) : quantum_channel (n^p) (m^p) := sorry

notation 𝒩 `⊗.` p `.⊗` 𝒩 :=  tensor_pow_channel 𝒩 p

-- looks like this when applied: 𝒩⊗.p.⊗𝒩




---- KRAUSS REPRESENTATION OF A CHANNEL

/-
Theorem (Krauss representation): for any quantum channel 
𝒩 there exists a list of operators Vᵢ such that for any 
density operator ρ, ∑ i, Vᵢ * ρ * Vᵢ† = 𝒩(ρ), and 
∑ i, Vᵢ† * Vᵢ = I
-/
theorem Krauss_representation : 
∀ (𝒩 : quantum_channel n m), 
    ∃ list V, 
        (∑ i, Vᵢ * ρ * Vᵢ† = 𝒩.map(ρ) ∧ ∑ i, Vᵢ† * Vᵢ = I) :=
begin
    sorry
end




---- DEGRADABLE CHANNELS

/-
Definition (degradable quantum channels)
https://youtu.be/a8Rgt8VvVeo
-/
def is_degradable (𝒩 : quantum_channel n m) (ℳ := complementary_channel 𝒩) := 
∃ (𝒟 : quantum_channel), ∀ (ρ : density_operator), 𝒟(𝒩(ρ)) = ℳ(ρ)

/-
Theorem (Hadamard channel is degradable)
-/
theorem quantum_Hadamard_channel_is_degradable : 
is_degradable (quantum_Hadamard_channel) := 
begin
    sorry
end




---- EXAMPLE CHANNELS

/-
A Gaussian channel is nothing but a channel that takes 
a Gaussian state to another Gaussian state.
-/
def gaussian_channel (η : ℝ) : quantum_channel := sorry

/-
Definition (phase-insensitive channels): Any phase-insensitive 
channel NPI is completely characterized by its a loss/gain 
parameter τ and noise parameter ν.
https://arxiv.org/pdf/1511.08710.pdf
-/
structure phase_insensitive_quantum_channel : Type :=
(gain : ℝ)
(noise : ℝ)
(h : noise ≥ ∣1 - gain|)

/-
Theorem (phase insensitive channels are entanglement-breaking)
https://arxiv.org/pdf/1312.6225.pdf
-/
theorem phase_insensitive_entanglement_breaking (𝒩 : phase_insensitive_quantum_channel) : 
𝒩.noise ≥ 𝒩.gain + 1 → is_entanglement_breaking (𝒩) :=
begin
    sorry
end