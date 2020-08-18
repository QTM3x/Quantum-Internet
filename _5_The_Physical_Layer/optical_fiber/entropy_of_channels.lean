import analysis.special_functions.exp_log
import _5_The_Physical_Layer.optical_fiber.quantum_channel
import _5_The_Physical_Layer.qubit_carriers.quantum_state
import common.matrix_ops



---- HOLEVO INFORMATION OF CHANNELS

/-
Definition (Holevo information of a quantum channel)
-/
def Holevo_information_channel (𝒩 : quantum_channel) : ℝ := sorry



---- MUTUAL INFORMATION OF CHANNELS

/-
Definition (mutual information of a quantum channel)
-/
def quantum_mutual_information_channel (𝒩 : quantum_channel) : ℝ :=  sorry



---- COHERENT INFORMATION OF CHANNELS

/-
Definition (coherent information of a quantum channel)
-/
def coherent_information_channel (𝒩 : quantum_channel) : ℝ := sorry


/-
Definition (regularized coherent information of a quantum channel)
-/
def reg_coherent_information (𝒩 : quantum_channel) : ℝ := sorry


---- PRIVATE INFORMATION OF CHANNELS

/-
Definition (private information of a quantum channel)
-/
def private_inforamtion (𝒩 : quantum_channel) : ℝ := sorry






-- QUANTUM CAPACITY

/-
Definition (quantum communication code)
-/
structure code : Type :=
(𝒩 : quantum_channel)
(n : ℕ) -- uses of the channel
(ε : ℝ) -- allowed error
(ℰ : quantum_channel) -- encoding channel
(𝒟 : quantum_channel) -- decoding channel
-- output state is within allowed error for all input states
(hε : ∀ (ρ :  density_operator), 
    1/2 * ∥ρ - 𝒟(tensor_pow_channel 𝒩 n (ℰ(ρ)))∥₁ ≤ ε)
(rate_achieved : ℝ := 1/n * log ℰ.in_dim)

/-
Definition (achievable rate using a channel)
-/
def achievable_rate (𝒩 : quantum_channel) (rate : ℝ) :=
∀ (ε δ : ℝ) (hε : ε > 0 ∧ ε < 1) (hδ : δ > 0), 
∃ (c : code), c.rate_achieved ≥ rate - δ ∧ c.ε ≤ ε

/-
Definition (quantum capacity of a quantum channel): supremum 
of all rates achievable using the channel. 
-/
def quantum_capacity (𝒩 : quantum_channel) : ℝ := 
minimum {rates | it is bigger than any possible achievable rate}


/-
Theorem (quantum capacity equals regularized coherent information)
-/
theorem quantum_capacity_eq_reg_coh_info : 
∀ (𝒩 : quantum_channel), quantum_capacity(𝒩) = reg_coherent_information(𝒩) := 
begin
    sorry
end


/-
Theorem (quantum capacity of amp damp channel)
-/
theorem quantum_capacity_amp_damp {η : ℝ} (𝒩 := amp_damp_channel η) : 
quantum_capacity(𝒩) = min_p h₂((1-η)*p) - h₂(η*p) := 
begin
    sorry
end


---- TWO-WAY QUANTUM CAPACITY

-- can you represent the unlimited classical capacity 
-- as a list of bits of arbitrary length that Alice and Bob can 
-- send to each other?

-- can you think of the classical communication as transmission 
-- of qubits carrying only classical information through the 
-- identity channel? can you absorb the local gates in the 
-- LOCCs into the encoding channel?

/-
Defintion (two-way capacity): The quantum capacity of a channel 
if unlimited classical communication is allowed between the sender 
and the receiver.
-/
def two_way_quantum_capacity (𝒩 : quantum_channel) : ℝ := sorry



---- 

/-
Definition (σ-stretching): 
-/
def sigma_stretching (𝒩 : quantum_channel) := sorry


/-
Defintion (KL divergence): 
-/
def KL_divergence := sorry


