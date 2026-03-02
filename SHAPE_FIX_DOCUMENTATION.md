# Fix for Visdom Line Plot Shape Incompatibility Issue

## Problem Description

When plotting a line using `visdom.line()` with:
- Y of size `Nx1` (e.g., `[[1], [2], [3]]`)
- X of size `N` (e.g., `[0, 1, 2]`)

The code would crash with a shape incompatibility error.

## Root Cause

The issue was in the `line()` function around line 1688-1694 of `__init__.py`:

### Original Code (Buggy):
```python
if Y.ndim == 2 and X.ndim == 1:
    X = np.tile(X, (Y.shape[1], 1)).transpose()

assert X.shape == Y.shape, "X and Y should be the same shape"
```

### What Happened:
1. When Y has shape `(N, 1)`, it's a 2D array with 1 column
2. When X has shape `(N,)`, it's a 1D array
3. The condition `Y.ndim == 2 and X.ndim == 1` is True
4. X gets tiled to shape `(N, 1)` using `np.tile(X, (Y.shape[1], 1)).transpose()`
5. However, Y with shape `(N, 1)` should be treated as a single line, not multiple lines
6. The assertion `X.shape == Y.shape` would fail because shapes don't match properly

## Solution

### Fixed Code:
```python
if Y.ndim == 2 and Y.shape[1] == 1:
    Y = Y.reshape(Y.shape[0])

if Y.ndim == 2 and X.ndim == 1:
    X = np.tile(X, (Y.shape[1], 1)).transpose()

assert X.shape == Y.shape, "X and Y should be the same shape"
```

### How It Works:
1. **First check**: If Y is 2D with only 1 column `(N, 1)`, reshape it to 1D `(N,)`
2. **Second check**: If Y is still 2D (meaning it has multiple columns) and X is 1D, tile X to match
3. **Assertion**: Now X and Y will have matching shapes

## Benefits

This fix:
- ✓ Handles `Nx1` Y arrays correctly by treating them as single lines
- ✓ Maintains backward compatibility with existing code
- ✓ Works with the edge case of `1x1` arrays
- ✓ Preserves the original behavior for multi-line plots `(N, M)` where M > 1

## Test Cases

### Case 1: Single line with Nx1 Y
```python
Y = np.array([[1], [2], [3], [4], [5]])  # Shape: (5, 1)
X = np.array([0, 1, 2, 3, 4])            # Shape: (5,)
vis.line(Y=Y, X=X)  # ✓ Works now!
```

### Case 2: Multiple lines
```python
Y = np.array([[1, 2], [3, 4], [5, 6]])   # Shape: (3, 2)
X = np.array([0, 1, 2])                   # Shape: (3,)
vis.line(Y=Y, X=X)  # ✓ Still works!
```

### Case 3: Edge case 1x1
```python
Y = np.array([[1]])  # Shape: (1, 1)
X = np.array([0])    # Shape: (1,)
vis.line(Y=Y, X=X)   # ✓ Works!
```

## Files Modified

- `py/visdom/__init__.py` - Line ~1688: Added reshape logic for `Nx1` Y arrays

## Related Issues

This fix resolves the issue where users reported:
- "incompatible shapes for X and Y when using inputs Y of size Nx1 and X of size N"
- "The first time I use the plot function where Y has size 1x1 it does work correctly"
