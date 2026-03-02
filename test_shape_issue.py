import numpy as np
import sys
sys.path.insert(0, 'c:\\Users\\LENOVO\\OneDrive\\Documents\\Web Developing course\\project_github\\visdom\\py')

# Test the issue described
# Y of size Nx1 and X of size N causes shape mismatch

# Simulate the problematic code section
Y = np.array([[1], [2], [3], [4], [5]])  # Shape: (5, 1)
X = np.array([0, 1, 2, 3, 4])  # Shape: (5,)

print("Original shapes:")
print(f"Y shape: {Y.shape}")
print(f"X shape: {X.shape}")

# This is what happens in line 1688 (approximately)
if Y.ndim == 2 and Y.shape[1] == 1:
    print("\nY is reshaped from (N, 1) to (1, N)")
    Y_reshaped = Y.reshape(1, Y.shape[0])  # Current problematic code
    print(f"Y reshaped: {Y_reshaped.shape}")
    
    # Line 1691 condition
    if Y_reshaped.ndim != X.ndim:
        print(f"\nY.ndim ({Y_reshaped.ndim}) != X.ndim ({X.ndim})")
        print("X will be tiled to match Y dimensions")
        X_tiled = np.tile(X, (Y_reshaped.shape[0], 1))
        print(f"X tiled shape: {X_tiled.shape}")
        
        # Line 1694 - This is where the error occurs
        print(f"\nChecking if X.shape == Y.shape:")
        print(f"X shape: {X_tiled.shape}, Y shape: {Y_reshaped.shape}")
        print(f"Match: {X_tiled.shape == Y_reshaped.shape}")

print("\n" + "="*50)
print("PROPOSED FIX:")
print("="*50)

# Reset
Y = np.array([[1], [2], [3], [4], [5]])
X = np.array([0, 1, 2, 3, 4])

print(f"\nOriginal Y shape: {Y.shape}")
print(f"Original X shape: {X.shape}")

# Proposed fix: reshape to (N,) instead of (1, N)
if Y.ndim == 2 and Y.shape[1] == 1:
    Y_fixed = Y.reshape(Y.shape[0])  # Fixed version
    print(f"Y reshaped (fixed): {Y_fixed.shape}")
    
    print(f"\nY.ndim ({Y_fixed.ndim}) == X.ndim ({X.ndim})")
    print("No tiling needed!")
    print(f"X shape: {X.shape}, Y shape: {Y_fixed.shape}")
    print(f"Match: {X.shape == Y_fixed.shape}")
