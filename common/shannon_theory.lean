import algebra.big_operators
import data.real.basic
import tactic
import analysis.special_functions.exp_log
import measure_theory.probability_mass_function

-- open_locale big_operators -- this enables the notation

noncomputable theory -- without this there is an error

---- HELPER LEMMAS

lemma multiset.map_repeat {α β : Sort*} (f : α → β) (x : α) (n : ℕ) :
  (multiset.repeat x n).map f = multiset.repeat (f x) n :=
nat.rec_on n rfl $ λ n ih, by simp_rw [multiset.repeat_succ, multiset.map_cons, ih]

theorem prod_ne_zero' {R : Type*} [integral_domain R] {m : multiset R} :
  (∀ x ∈ m, (x : _) ≠ 0) → m.prod ≠ 0 :=
begin
    intros,
    sorry
    -- multiset.induction_on m (λ _, one_ne_zero) $ λ hd tl ih H,
    --   by { rw multiset.forall_mem_cons at H, rw multiset.prod_cons, exact mul_ne_zero H.1 (ih H.2) }
end

lemma multiset.sum_geq_zero {m : multiset ℝ} : 
(∀ x ∈ m, (x : _) ≥ 0) → m.sum ≥ 0 :=
begin
    sorry
end 




---- SHANNON ENTROPY

/-
Definition (Shannon entropy): The entropy of a discrete random 
variable X with probability distribution p_X(x)  
-/
def shannon_entropy (X : multiset ℝ) : ℝ
:= (multiset.map (λ (x : ℝ), x * real.log(1/x)) X).sum

/-
Theorem (non-negativity): Shannon entropy is non-negative for 
any discrete random variable X.
"It is perhaps intuitive that the entropy should be non-negative 
because non-negativity implies that we always learn some number of
bits upon learning random variable X (if we already know beforehand 
what the outcome of a random experiment will be, then we learn zero 
bits of information once we perform it). In a classical sense, we 
can never learn a negative amount of information!"
https://arxiv.org/pdf/1106.1445.pdf
-/
theorem shannon_entropy_nonneg : 
∀ (X : multiset ℝ) {hX : ∀ (x : ℝ), x ∈ X → x ≤ 1 ∧ x > 0}, 
    shannon_entropy(X) ≥ 0 := 
begin
    intros,
    unfold shannon_entropy,
    -- Each x * log(1/x) term in the sum 
    -- is non-negative because for x < 1 
    -- log(1/x) is positive and log(1/0) is 
    -- defined to be 0.
    let X_image := multiset.map (λ (x : ℝ), x * real.log(1/x)) X,
    have h : ∀ x ∈ X_image, (x : _) ≥ 0, {
        intros x hx,
        sorry,
    },
    -- And the sum of a set of nonnegative numbers is nonnegative.
    exact multiset.sum_geq_zero h,
end

/-
Theorem (concavity): Shannon entropy is concave in the probability 
density.
-/
theorem concavity := sorry

/-
Definition (deterministic random variable): 
-/
def is_deterministic := sorry

/-
Theorem (minimum value): Shannon entropy vanishes if and only if 
X is a deterministic variable.
-/
theorem shannon_entropy_minimum_value : 
∀ (X : multiset ℝ), shannon_entropy(X) = 0 ↔ is_deterministic X :=
begin
    sorry
end

/-
Definition (uniform random variable): a random variable
whose  probabilities are equal to 1/n, where n 
is the number of symbols that the random variable 
can assume.
-/
def is_uniform_rnd_var (X : multiset ℝ) : Prop :=
X = multiset.repeat (1/X.card) X.card

/-
Theorem: The Shannon entropy of a uniform 
random variable is log(n).
-/
theorem shannon_entropy_uniform_rdm_var (X : multiset ℝ) (hX : X.card ≠ 0) : 
is_uniform_rnd_var(X) → shannon_entropy X = real.log(X.card)
:=
begin
    intro,
    unfold is_uniform_rnd_var at a,
    rw a,
    simp,
    unfold shannon_entropy,
    rw multiset.map_repeat,
    simp,
    rw ← mul_assoc,
    rw mul_inv_cancel,
    simp,
    norm_cast,
    exact hX,
end