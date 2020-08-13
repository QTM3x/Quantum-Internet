import _5_The_Physical_Layer.qubit_carriers.quantum_state

-- Basic Quantum channel definitions, notations and theorems.

variables {n m : ℕ}


def linear (map : matrix (fin n) (fin n) ℂ → matrix (fin m) (fin m) ℂ) :=
map(α * XA + β * YA) = α * map(XA) + β * map(XB)

def positive (map : matrix (fin n) (fin n) ℂ → matrix (fin m) (fin m) ℂ) := 
∀ (M : matrix) (hM : positive_semidefinite M), positive_semidefinite (map M) 

def completely_positive (map : matrix (fin n) (fin n) ℂ → matrix (fin m) (fin m) ℂ) :=
∀ (n : ℕ), positive ((identity_map n) ⊗ map)

def trace_preserving (map : matrix (fin n) (fin n) ℂ → matrix (fin m) (fin m) ℂ) := trace (map ρ) = trace ρ

/-
Defintion (quantum channel): A quantum channel is a completely 
positive, trace-preserving linear map.
-/
structure quantum_channel : Type :=
(in_dim : ℕ)
(out_dim : ℕ)
(map : matrix (fin in_dim) (fin in_dim) ℂ → matrix (fin out_dim) (fin out_dim) ℂ)
(linear: linear map)
(completely_positive : completely_positive map)
(trace_preserving : trace_preserving map)

/-
Definition (tensor product of channels)
-/
def tensor_channel (𝒩 : quantum_channel) (ℳ : quantum_channel) : 
quantum_channel := sorry

notation 𝒩 `⊗` ℳ := tensor_channel 𝒩 ℳ

/-
Definition (tensor power of channels)
-/
def tensor_pow_channel (𝒩 : quantum_channel) (n : ℕ) : quantum_channel := sorry


/-
Theorem (Krauss representation): for any quantum channel 
𝒩 there exists a list of operators Vᵢ such that for any 
density operator ρ, ∑ i, Vᵢ * ρ * Vᵢ† = 𝒩(ρ), and 
∑ i, Vᵢ† * Vᵢ = I
-/
theorem Krauss_representation : 
∀ (𝒩 : quantum_channel), ∃ list V, (∑ i, Vᵢ * ρ * Vᵢ† = 𝒩.map(ρ) ∧ ∑ i, Vᵢ† * Vᵢ = I) :=
sorry




---- EXAMPLE CHANNELS

/-
A Gaussian channel is nothing but a channel that takes 
a Gaussian state to another Gaussian state.
-/
def Gaussian_channel (η : ℝ) : quantum_channel := sorry

