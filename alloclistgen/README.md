Generate allocation file for 3456-node Dragonfly topology.

To generate allocation without background:
$./my_test.py [RANK1 RANK2 ...] 0

To generate allocation with background:
$./my_test.py [RANK1 RANK2 ...] 1

For example, allocation for 1000-rank MG with 2456-node running synthetic background:
$./my_test.py 1000 2456 1
