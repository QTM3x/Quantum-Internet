import data.complex.basic
import linear_algebra.matrix

variables {n m : ℕ}

def eigenvalues (M : matrix (fin n) (fin n) ℂ) : list ℝ := sorry

def positive_semidefinite (M : matrix (fin n) (fin n) ℂ) :=
∀ e ∈ eigenvalues M, e ≥ 0

def kronecker_product (M₁ : matrix (fin n) (fin n) ℂ) (M₂ : matrix (fin m) (fin m) ℂ) :
matrix (fin(n*m)) (fin(n*m)) ℂ := sorry

notation `⊗` := kronecker_product