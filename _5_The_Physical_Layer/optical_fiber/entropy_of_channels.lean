import data.real.basic
import analysis.special_functions.exp_log
import _5_The_Physical_Layer.optical_fiber.quantum_channel
import _5_The_Physical_Layer.qubit_carriers.quantum_state
import common.matrix_ops

notation `|` x `|` := abs x

---- HOLEVO INFORMATION

/-
Definition (Holevo information of a quantum channel)
"The Holevo information χ(𝒩) of a channel 𝒩 is a measure 
of the classical correlations that Alice can establish
with Bob where the maximization is with respect to all 
input classical–quantum states."
https://arxiv.org/pdf/1106.1445.pdf
-/
def Holevo_info (𝒩 : quantum_channel) : ℝ := 
begin
    -- the set of all classical-quantum states
    let CQ_states := {ρ : density_operator | is_classical_quantum(ρ)},
    -- the states after the channel acts on Bob's system
    let output_states := {I⊗𝒩 ρ | ρ ∈ CQ_states}
    -- the set of all values of mutual information for the output states
    let I_out := {I(X;B)_ρ | ρ ∈ CQ_states},
    -- let maximum be a real number
    let maximum : ℝ := _,
    -- the maximum is in I_CQ
    let h := maximum ∈ I_out,
    -- the maximum is at least as big as any element in I_CQ
    let h' := ∀ x ∈ I_out, maximum ≥ x,
    -- Holevo info is the maximum
    exact maximum,
end

notation `χ(` 𝒩 `)` := Holevo_info 𝒩

/-
Definition (regularized Holevo information of a quantum channel)
-/
def reg_Holevo_info (𝒩 : quantum_channel) : ℝ := 
begin
    -- let lim be a real number
    let lim : ℝ := _,
    -- let the Holevo information of many uses of the channel 
    -- tend to this limit lim.
    let h := ∀ ε > 0, ∃ N, ∀ n > N, |lim - χ(𝒩⊗..n..⊗𝒩)| ≤ ε,
    -- the regularized Holevo information is this limit
    exact lim,
end

notation `χ_reg(` ρ `)` := reg_Holevo_info 𝒩

/-
Theorem (Holevo information of entanglement-breaking channels)
-/
theorem Holevo_info_eq_reg_Holevo_info_of_entanglement_breaking {𝒩 : quantum_channel} :
is_entanglement_breaking(𝒩) → χ(𝒩) = χ_reg(𝒩) := 
begin
    sorry
end




---- SQUASHED ENTANGLEMENT

/-
Definition (squashed entanglement of a quantum channel)
-/
def squashed_entanglement (𝒩 : quantum_channel) : ℝ := 
maximum_ρ squashed_entanglement(ρ)

/-
Theorem (upper bound on squashed entanglement of 
phase-insensisitve Gaussian quantum channels)
https://arxiv.org/pdf/1511.08710.pdf
-/
notation `ζ(` a `,` b `)` := a * b * real.log(a/b)

theorem squashed_entanglement_phase_insensitive_channels_up_bound
{𝒩 : phase_insensitive_channel} : 
squashed_entanglement(𝒩) ≤ 
    (ζ(1 + 𝒩.noise + 3*𝒩.gain, 1 + 𝒩.noise - 𝒩.gain) - 𝒩.gain * ζ(𝒩.gain + 𝒩.noise + 3, 𝒩.gain + 𝒩.noise - 1)) / (2 * (1 + 𝒩.noise + 𝒩.gain) * (1 - 𝒩.gain^2)) :=
begin
    sorry
end




---- MUTUAL INFORMATION

/-
Definition (mutual information of a quantum channel)
"The mutual information of a quantum channel corresponds 
to an important operational task that is not particularly 
obvious from the above discussion. Suppose that Alice and 
Bob share unlimited bipartite entanglement in whatever 
form they wish, and suppose they have access to a large 
number of independent uses of the channel NA0→B. Then the 
mutual information of the channel corresponds to the maximal 
amount of classical information that they can transmit in 
such a setting."
https://arxiv.org/pdf/1106.1445.pdf
-/
def mut_info (𝒩 : quantum_channel) : ℝ :=  
begin
    -- the set of all pure states
    let pure_states := {ρ : density_operator | is_pure(ρ)},
    -- the states after the channel acts on Bob's system
    let output_states := {I⊗𝒩 ρ | ρ ∈ pure_states}
    -- the set of all values of mutual information
    let I_out := {I(A;B)_ρ | ρ ∈ pure_states},
    -- let maximum be a real number
    let maximum : ℝ := _,
    -- the maximum is in I_CQ
    let h := maximum ∈ I_pure,
    -- the maximum is at least as big as any element in I_CQ
    let h' := ∀ x ∈ I_out, maximum ≥ x,
    -- Holevo info is the maximum
    exact maximum,
end

notation `I(` 𝒩 `)` := mut_info 𝒩

/-
Definition (regularized mutual information)
-/
def reg_mut_info (𝒩 : quantum_channel) : ℝ := 
begin
    -- let lim be a real number
    let lim : ℝ := _,
    -- let the mutual information of many uses of the channel 
    -- tend to this limit lim.
    let h := ∀ ε > 0, ∃ N, ∀ n > N, |lim - I(𝒩⊗..n..⊗𝒩)| ≤ ε,
    -- the regularized private information is this limit
    exact lim,
end

notation `I_reg(` 𝒩 `)` := reg_mut_info 𝒩

/-
Theorem (additivity)
-/
@[simp]
theorem mut_info_additive {𝒩 : quantum_channel} {ℳ : quantum_channel}: 
I(𝒩⊗ℳ) = I(𝒩) + I(ℳ) :=
begin
    sorry
end

/-
Theorem (regularized mutual information = mutual information)
-/
theorem reg_mut_info_eq_mut_info {𝒩 : quantum_channel} :
I_reg(𝒩) = I(𝒩) :=
begin
    sorry
end




---- COHERENT INFORMATION

/-
Definition (coherent information of a quantum channel)
"The coherent information of a quantum channel corresponds 
to an important operational task (perhaps the most important 
for quantum information). It is a good lower bound on the 
capacity for Alice to transmit quantum information to Bob, 
but it is actually equal to such a quantum communication 
capacity of a quantum channel in some special cases."
https://arxiv.org/pdf/1106.1445.pdf
-/
def coherent_info (𝒩 : quantum_channel) : ℝ := 
begin
    -- the set of all pure states
    let pure_states := {ρ : density_operator | is_pure(ρ)},
    -- the states after the channel acts on Bob's system
    let output_states := {I⊗𝒩 ρ | ρ ∈ pure_states}
    -- the set of all values of coherent information
    let I_out := {I(A⟩B)_ρ | ρ ∈ pure_states},
    -- let maximum be a real number
    let maximum : ℝ := _,
    -- the maximum is in I_CQ
    let h := maximum ∈ I_pure,
    -- the maximum is at least as big as any element in I_CQ
    let h' := ∀ x ∈ I_out, maximum ≥ x,
    -- Holevo info is the maximum
    exact maximum,
end

notation `Q(` 𝒩 `)` := coherent_info 𝒩

/-
Definition (regularized coherent information)
-/
def reg_coherent_info (𝒩 : quantum_channel) : ℝ := 
begin
    -- let lim be a real number
    let lim : ℝ := _,
    -- let the coherent information of many uses of the channel 
    -- tend to this limit lim.
    let h := ∀ ε > 0, ∃ N, ∀ n > N, |lim - Q(𝒩⊗..n..⊗𝒩)| ≤ ε,
    -- the regularized coherent information is this limit
    exact lim,
end

notation `Q_reg(` 𝒩 `)` := reg_coherent_info 𝒩

/-
Theorem (non-negativity)
-/
theorem coherent_info_nonneg {𝒩 : quantum_channel} : 
Q(𝒩) ≥ 0 := 
begin
    sorry
end




---- REVERSE COHERENT INFORMATION

/-
Definition (reverse coherent information)
-/
def reverse_coherent_info (𝒩 : quantum_channel) : ℝ := 
begin
    -- the set of all pure states
    let pure_states := {ρ : density_operator | is_pure(ρ)},
    -- the states after the channel acts on Bob's system
    let output_states := {I⊗𝒩 ρ | ρ ∈ pure_states}
    -- the set of all values of coherent information
    let I_out := {I(B⟩A)_ρ | ρ ∈ pure_states},
    -- let maximum be a real number
    let maximum : ℝ := _,
    -- the maximum is in I_CQ
    let h := maximum ∈ I_pure,
    -- the maximum is at least as big as any element in I_CQ
    let h' := ∀ x ∈ I_out, maximum ≥ x,
    -- Holevo info is the maximum
    exact maximum,
end

notation `Q_rev(` 𝒩 `)` := reverse_coherent_info 𝒩




---- PRIVATE INFORMATION

/-
Definition (private information)
"Alice would like to establish classical correlations with Bob, 
but does not want the environment of the channel to have access 
to these classical correlations."
https://arxiv.org/pdf/1106.1445.pdf
-/
def private_info (𝒩 : quantum_channel) : ℝ := 
begin
    -- the set of all classical-quantum states
    let CQ_states := {ρ : density_operator | is_classical_quantum(ρ)},
    -- the states after the channel acts on Bob's system
    let output_states := {(isometric_extension 𝒩) ρ | ρ ∈ CQ_states}
    -- the set of all values of mutual information for the output states
    let I_out := {I(X;B)_ρ - I(X;E)_ρ | ρ ∈ CQ_states},
    -- let maximum be a real number
    let maximum : ℝ := _,
    -- the maximum is in I_CQ
    let h := maximum ∈ I_out,
    -- the maximum is at least as big as any element in I_CQ
    let h' := ∀ x ∈ I_out, maximum ≥ x,
    -- Holevo info is the maximum
    exact maximum,
end

notation `P(` 𝒩 `)` := private_info 𝒩

/-
Definition (regularized private information)
-/
def reg_private_info {ε : ℝ} (𝒩 : quantum_channel) : ℝ := 
begin
    -- let lim be a real number
    let lim : ℝ := _,
    -- let the private information of many uses of the channel 
    -- tend to this limit lim.
    let h := ∀ ε > 0, ∃ N, ∀ n > N, |lim - P(𝒩⊗..n..⊗𝒩)| ≤ ε,
    -- the regularized private information is this limit
    exact lim,
end

notation `P_reg(` 𝒩 `)` := reg_private_info 𝒩

/-
Theorem (private info ≥ coherent info for any channel)
-/
theorem private_info_geq_coherent_info :
∀ (𝒩 : quantum_channel), P(𝒩) ≥ Q(𝒩) :=
begin
    sorry
end

/-
Theorem (private info is = coherent info for degradable channels)
-/
theorem private_info_eq_coherent_info_of_degradable : 
∀ (𝒩 : quantum_channel), is_degradable(𝒩) → P(𝒩) = Q(𝒩) :=
begin
    sorry
end




-- QUANTUM CAPACITY

/-
Definition (quantum communication code)
-/
structure code : Type :=
(𝒩 : quantum_channel) -- the channel the code is designed for
(n : ℕ) -- uses of the channel
(ε : ℝ) -- allowed error
(ℰ : quantum_channel) -- encoding channel
(𝒟 : quantum_channel) -- decoding channel
-- output state is within allowed error for all input states
(hε : ∀ (ρ :  density_operator), 
    1/2 * ∥ρ - 𝒟(tensor_pow_channel 𝒩 n (ℰ(ρ)))∥₁ ≤ ε)
(rate_achieved : ℝ := 1/n * log ℰ.in_dim) -- the rate of the code

/-
Definition (achievable rate using a channel)
-/
def is_achievable_rate (𝒩 : quantum_channel) (rate : ℝ) : Prop :=
∀ (ε δ : ℝ) (hε : ε > 0 ∧ ε < 1) (hδ : δ > 0), 
∃ (c : code), c.rate_achieved ≥ rate - δ ∧ c.ε ≤ ε

/-
Definition (quantum capacity of a quantum channel): supremum 
of all rates achievable using the channel. 
-/
def quantum_capacity (𝒩 : quantum_channel) : ℝ :=
begin
    let achievable_rates := {rate : ℝ | is_achievable_rate 𝒩 rate},
    let bigger_rates := {rate : ℝ | ∀ ar ∈ achievable_rates, rate > ar},
    let supremum_rate : ℝ := _,
    let h_supremum_rate  : Prop := ∀ rate ∈ bigger_rates, supremum_rate ≤ rate,
    let h_supremum_rate' : Prop := ∀ rate ∈ achievable_rates, supremum_rate > rate, 
    exact supremum_rate,
end

/-
Theorem (quantum capacity equals regularized coherent information)
https://arxiv.org/pdf/1106.1445.pdf
-/
theorem quantum_capacity_eq_reg_coh_info {𝒩 : quantum_channel} : 
quantum_capacity(𝒩) = reg_coherent_info(𝒩) := 
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

-- can you represent the unlimited classical communication 
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