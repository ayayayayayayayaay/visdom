import numpy as np
import sys
sys.path.insert(0, 'c:\\Users\\LENOVO\\OneDrive\\Documents\\Web Developing course\\project_github\\visdom\\py')

from visdom import Visdom

# Test cases for the shape fix
print("Testing Visdom line plot with various input shapes")
print("="*60)

# Initialize Visdom in offline mode to avoid server connection
vis = Visdom(offline=True, log_to_filename='test_log.json')

# Test Case 1: Y with shape (N, 1) and X with shape (N,)
print("\nTest 1: Y shape (N, 1), X shape (N,)")
Y1 = np.array([[1], [2], [3], [4], [5]])  # Shape: (5, 1)
X1 = np.array([0, 1, 2, 3, 4])  # Shape: (5,)
print(f"Y shape: {Y1.shape}, X shape: {X1.shape}")
try:
    vis.line(Y=Y1, X=X1, win='test1', opts=dict(title='Test 1'))
    print("✓ SUCCESS: No shape error!")
except Exception as e:
    print(f"✗ FAILED: {e}")

# Test Case 2: Y with shape (N,) and X with shape (N,)
print("\nTest 2: Y shape (N,), X shape (N,)")
Y2 = np.array([1, 2, 3, 4, 5])  # Shape: (5,)
X2 = np.array([0, 1, 2, 3, 4])  # Shape: (5,)
print(f"Y shape: {Y2.shape}, X shape: {X2.shape}")
try:
    vis.line(Y=Y2, X=X2, win='test2', opts=dict(title='Test 2'))
    print("✓ SUCCESS: No shape error!")
except Exception as e:
    print(f"✗ FAILED: {e}")

# Test Case 3: Y with shape (N, M) and X with shape (N,)
print("\nTest 3: Y shape (N, M), X shape (N,)")
Y3 = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])  # Shape: (5, 2)
X3 = np.array([0, 1, 2, 3, 4])  # Shape: (5,)
print(f"Y shape: {Y3.shape}, X shape: {X3.shape}")
try:
    vis.line(Y=Y3, X=X3, win='test3', opts=dict(title='Test 3', legend=['a', 'b']))
    print("✓ SUCCESS: No shape error!")
except Exception as e:
    print(f"✗ FAILED: {e}")

# Test Case 4: Y with shape (N, M) and X with shape (N, M)
print("\nTest 4: Y shape (N, M), X shape (N, M)")
Y4 = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])  # Shape: (5, 2)
X4 = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])  # Shape: (5, 2)
print(f"Y shape: {Y4.shape}, X shape: {X4.shape}")
try:
    vis.line(Y=Y4, X=X4, win='test4', opts=dict(title='Test 4', legend=['a', 'b']))
    print("✓ SUCCESS: No shape error!")
except Exception as e:
    print(f"✗ FAILED: {e}")

# Test Case 5: Y with shape (1, 1) - edge case mentioned in the issue
print("\nTest 5: Y shape (1, 1), X shape (1,)")
Y5 = np.array([[1]])  # Shape: (1, 1)
X5 = np.array([0])  # Shape: (1,)
print(f"Y shape: {Y5.shape}, X shape: {X5.shape}")
try:
    vis.line(Y=Y5, X=X5, win='test5', opts=dict(title='Test 5'))
    print("✓ SUCCESS: No shape error!")
except Exception as e:
    print(f"✗ FAILED: {e}")

print("\n" + "="*60)
print("All tests completed!")
