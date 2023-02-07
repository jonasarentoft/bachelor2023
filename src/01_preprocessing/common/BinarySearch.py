from bisect import bisect_left

def BinarySearchTF(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return True
    else:
        return False
    
def BinarySearchIndex(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    