# B+Rope

I don't know if this is a well know data structure or not, but I made a variant of the B+Tree as a rope instead. It's similar to a B+Tree, only the keys represent how many elements are stored on the left of them. 

## TODO
1. Bulk update nodes rather than going down then up over again 
2. Memory efficiency

## Some notes about the difference between a B+Tree

1. Within a single node, keys describe how many elements are in their left sub node AND their left neighbor sub tree:
```
                [5,                 10,                     15]
[1, 2, 3, 4, 5] -> [6, 7, 8, 9, 10] -> [11, 12, 13, 14, 15] -> [16, 17, 18, 19, 20]
```


See how 5 tells you that there are 5 elements to the left, 10 tells you there are 10 elements to the left child tree AND all of 5's sub tree, 15 tells you that there are 15 elements to the left (including 5 and 10 and it's own left sub tree).

2. The algorithms for splitting are pretty similar, you just need to make sure you update the keys on the right.

3. Each leaf node has a limited capacity, and splits when it overflows

4. This library isn't meant to be optimized (feel free to if you want), it was scratch work for another optimized library in C I'm writing

## Algorithms:

1. Insert 
    - Inserts data starting at index \[start\]
    - If start is -1, goes to the end. Otherwise, throws index out of bounds errors

2. Read 
    - Reads the data from start to end with step size 
    - log(n) to find start, then a sequential process   
        - so it's technically slower than your run of the mill array to 
          find items, but has more powerful inner insertions
