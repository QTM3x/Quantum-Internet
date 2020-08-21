import data.complex.basic
import linear_algebra.matrix

variables {n m k l : ℕ}

noncomputable theory

---- EIGENVALUES

def eigenvalues (M : matrix (fin n) (fin n) ℂ) : list ℝ := sorry

def positive_semidefinite (M : matrix (fin n) (fin n) ℂ) : Prop :=
∀ (e : ℝ) (he : e ∈ eigenvalues M), e ≥ 0




---- IDENTITY MAP

/-
Definition (identity map of dimension n):
It's a map that takes a matrix M to itself.
-/
def id_map (n : ℕ) : 
matrix (fin n) (fin n) ℂ → matrix (fin n) (fin n) ℂ := 
λ M, M

/-
Definition (identity matrix of dimension n):
It's the matrix with 1's on the diagonal and 
0's everywhere else.
-/
def id_matrix (n : ℕ) : matrix (fin n) (fin n) ℂ := sorry

/-
Theorem (identity matrix is identity map):
Multiplying by the identity matrix is the 
identity map.
-/
theorem id_map_of_id_matrix : 
∀ (M : matrix (fin n) (fin n) ℂ),
    (id_matrix n) * M = id_map n M := 
begin
    sorry
end




---- TENSOR PRODUCT OF MAPS

/-
Definition (tensor product of two maps)
-/
def tensor_prod_maps 
(map1 : matrix (fin n) (fin n) ℂ → matrix (fin m) (fin m) ℂ)
(map2 : matrix (fin k) (fin k) ℂ → matrix (fin l) (fin l) ℂ)
: 
matrix (fin(n*k)) (fin(n*k)) ℂ → matrix (fin (m*l)) (fin (m*l)) ℂ
:= sorry

notation map1 `⊗_m` map2 := tensor_prod_maps map1 map2




---- PROPERTIES OF SOME MAPS

/-
Definition (linearity)
-/
def linear (map : matrix (fin n) (fin n) ℂ → matrix (fin m) (fin m) ℂ) : Prop :=
∀ (α β : ℂ) (X Y : matrix (fin n) (fin n) ℂ), 
    map(α • X + β • Y) = α • map(X) + β • map(Y)

/-
Definition (positivity)
-/
def positive (map : matrix (fin n) (fin n) ℂ → matrix (fin m) (fin m) ℂ) := 
∀ (M : matrix (fin n) (fin n) ℂ) (hM : positive_semidefinite M), 
    positive_semidefinite (map M) 

/-
Definition (complete positivity)
-/
def completely_positive (map : matrix (fin n) (fin n) ℂ → matrix (fin m) (fin m) ℂ) :=
∀ (n : ℕ), positive ((id_map n) ⊗_m map)

/-
Definition (trace preservation)
-/
def trace_preserving 
(map : matrix (fin n) (fin n) ℂ → matrix (fin m) (fin m) ℂ) := 
trace (map ρ) = trace ρ




---- ADJOINT

def conjugate (M : matrix (fin n) (fin n) ℂ) : matrix (fin n) (fin n) ℂ := 
M.map (λ (c : ℂ), c.conj)

notation M`†` := conjugate (matrix.transpose M)




---- MATRIX EXPONENTIAL

def matrix_exp (M : matrix (fin n) (fin n) ℂ) : matrix (fin n) (fin n) ℂ := 
I + pow_sum 1..∞ 1/k! * Mᵏ 

theorem exp_zero (M : matrix (fin n) (fin n) ℂ) : matrix_exp(0) = I := 
begin
    sorry
end

theorem exp_transpose (M : matrix (fin n) (fin n) ℂ) : 
matrix_exp(Mᵀ) = matrix_exp(M)ᵀ := 
begin
    sorry
end 

theorem exp_adjoint (M : matrix (fin n) (fin n) ℂ) :
matrix_exp(M†) = matrix_exp(M)† :=
begin
    sorry
end

theorem exp_add (M₁ M₂ : matrix (fin n) (fin n) ℂ) :
matrix_exp(M₁ + M₂) = matrix_exp(M₁) * matrix_exp(M₂) :=
begin
    sorry
end

theorem exp_mul_neg_self (M : matrix (fin n) (fin n) ℂ) : 
matrix_exp(M) * matrix_exp(-M) = I :=
begin
    sorry
end 




---- MATRIX LOGARITHM

def matrix_log (M : matrix (fin n) (fin n) ℂ) : 
matrix (fin n) (fin n) ℂ
:= sorry




---- KRONECKER PRODUCT

def kronecker_product (M₁ : matrix (fin n) (fin n) ℂ) (M₂ : matrix (fin m) (fin m) ℂ) :
matrix (fin(n*m)) (fin(n*m)) ℂ := sorry

notation `⊗` := kronecker_product




---- TRACE

def trace' (M : matrix (fin n) (fin n) ℂ) : ℂ :=
matrix.trace (fin n) ℂ ℂ M

notation `Tr(`M`)` := trace' M

def partial_trace (M: matrix (fin n) (fin n) ℂ) (partition_point : ℕ) := sorry

notation `pTr(`M`,`p`)` := partial_trace M p




---- UNITARITY

def is_unitary (M : matrix (fin n) (fin n) ℂ) : Prop := M†*M = I ∧ M*M† = I