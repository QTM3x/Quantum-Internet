import data.complex.basic
import linear_algebra.matrix

variables {n m : ℕ}

noncomputable theory

-- ADJOINT

def conjugate (M : matrix (fin n) (fin n) ℂ) : matrix (fin n) (fin n) ℂ := 
M.map (λ (c : ℂ), c.conj)

notation M`†` := conjugate (matrix.transpose M)




-- EIGENVALUES

def eigenvalues (M : matrix (fin n) (fin n) ℂ) : list ℝ := sorry

def positive_semidefinite (M : matrix (fin n) (fin n) ℂ) :=
∀ e ∈ eigenvalues M, e ≥ 0




-- MATRIX EXPONENTIAL

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




-- MATRIX LOGARITHM

def matrix_log (M : matrix (fin n) (fin n) ℂ) : 
matrix (fin n) (fin n) ℂ
:= sorry




-- KRONECKER PRODUCT

def kronecker_product (M₁ : matrix (fin n) (fin n) ℂ) (M₂ : matrix (fin m) (fin m) ℂ) :
matrix (fin(n*m)) (fin(n*m)) ℂ := sorry

notation `⊗` := kronecker_product




-- TRACE

def trace' (M : matrix (fin n) (fin n) ℂ) : ℂ :=
matrix.trace (fin n) ℂ ℂ M

notation `Tr(`M`)` := trace' M

def partial_trace (M: matrix (fin n) (fin n) ℂ) := sorry




-- UNITARITY

def is_unitary (M : matrix (fin n) (fin n) ℂ) : Prop := M†*M = I ∧ M*M† = I