o_nic_name=$1


# rate = guaranteed bandwidth
# ceil = peak bandwidth
# 1:10 for small bandwidth traffic
# 1:20 for low delay traffic
# 1:30 is default


# Before starting to configure qdiscs, first we need to remove any existing qdisc from the root.
tc qdisc del root dev $o_nic_name 2>/dev/null

# This line sets a HTB qdisc on the root of $o_nic_name, and it specifies that the class 1:30 is used by default. It sets the name of the root as 1:, for future references.
tc qdisc add dev $o_nic_name root handle 1: htb default 30

# This creates a class called 1:1, which is direct descendant of root (the parent is 1:), this class gets assigned also an HTB qdisc, and then it sets a max rate of 6000mbits, with a burst of 500mbit
tc class add dev $o_nic_name parent 1: classid 1:1 htb rate 6000mbit burst 1000mbit

# The previous class has this branches:

# Class 1:10, which has a rate of 100mbit
tc class add dev $o_nic_name parent 1:1 classid 1:10 htb rate 100mbit ceil 500mbit burst 10mbit prio 1

# Class 1:20, which has a rate of 100mbit
tc class add dev $o_nic_name parent 1:1 classid 1:20 htb rate 100mbit ceil 200mbit burst 10mbit prio 0

# Class 1:30, which has a rate of 2000mbit. This one is the default class.
tc class add dev $o_nic_name parent 1:1 classid 1:30 htb rate 2000mbit ceil 6000mbit burst 500mbit prio 1

# Martin Devera, author of HTB, then recommends SFQ for beneath these classes:
tc qdisc add dev $o_nic_name parent 1:10 handle 10: sfq perturb 10
tc qdisc add dev $o_nic_name parent 1:20 handle 20: sfq perturb 10
tc qdisc add dev $o_nic_name parent 1:30 handle 30: sfq perturb 10

# filter
tc filter add dev $o_nic_name parent 1: protocol ip prio 1 u32 match ip src 123.125.46.113/32 flowid 1:10


# show result
ip link show $o_nic_name
tc filter show dev $o_nic_name
tc qdisc show dev $o_nic_name
tc class show dev $o_nic_name
