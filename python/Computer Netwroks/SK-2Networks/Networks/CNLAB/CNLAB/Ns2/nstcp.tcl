# Create a simulator object
set ns [new Simulator]

# Define the trace file for NAM visualization
set nf [open out.nam w]
$ns namtrace-all $nf

# Define a 'finish' procedure
proc finish {} {
    global ns nf
    $ns flush-trace
    close $nf
    exec nam out.nam &
    exit 0
}

# Create nodes
set n0 [$ns node]  ;# Sender
set n1 [$ns node]  ;# Receiver

# Create a link between the nodes (2Mb bandwidth, 10ms delay)
$ns duplex-link $n0 $n1 2Mb 10ms DropTail

# Setup a TCP connection
set tcp [new Agent/TCP]
$ns attach-agent $n0 $tcp  ;# Attach TCP agent to sender node
set sink [new Agent/TCPSink]
$ns attach-agent $n1 $sink   ;# Attach TCP sink to receiver node
$ns connect $tcp $sink        ;# Connect TCP agent to TCP sink

# Create an FTP application and attach it to the TCP agent
set ftp [new Application/FTP]
$ftp attach-agent $tcp

# Schedule the start of the FTP traffic
$ns at 1.0 "$ftp start"

# Schedule the end of the simulation
$ns at 5.0 "finish"

# Run the simulation
$ns run

