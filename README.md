
# SDN-Based Learning Switch with Mininet and POX

This project implements a **Software-Defined Networking (SDN)** environment using the **POX Controller** and **Mininet**. It demonstrates the separation of the control plane and data plane by programming an Open vSwitch (OVS) to function as a Layer 2 learning switch.

##  Features
* **Centralized Control:** Uses the POX controller to manage flow rules.
* **Dynamic Learning:** Switch automatically learns MAC addresses and populates flow tables.
* **Custom Topology:** Supports various Mininet topologies (default: Single Switch, 3 Hosts).
* **Traffic Monitoring:** Compatible with Wireshark for OpenFlow packet analysis.

##  Prerequisites
Ensure you have the following installed on your Linux environment (Ubuntu recommended):
* **Mininet:** `sudo apt-get install mininet`
* **Open vSwitch:** `sudo apt-get install openvswitch-switch`
* **Python 3**
* **POX Controller:**
    ```bash
    git clone https://github.com/noxrepo/pox
    ```

## Usage Instructions

### 1. Start the SDN Controller
Open a terminal, navigate to your POX directory, and run the Layer 2 learning module:
```bash
python3 pox.py forwarding.l2_learning
```

### 2. Launch the Network Topology
In a **second terminal**, start Mininet. This command creates a topology with 3 hosts connected to 1 switch, pointing to the remote POX controller:
```bash
sudo mn --topo single,3 --mac --controller remote --switch ovsk,protocols=OpenFlow13
```

### 3. Verify Connectivity
Inside the Mininet CLI (`mininet>`), run a ping test to trigger the learning process:
```bash
mininet> pingall
```

### 4. Inspect Flow Tables
To see how the controller has programmed the switch, run this in a **third terminal**:
```bash
dpctl dump-flows
```

##  Architecture Overview

The architecture consists of:
* **Control Plane:** The POX Controller, which receives "Packet-In" messages and sends "Flow-Mod" messages.
* **Data Plane:** The Mininet-emulated Open vSwitch that forwards packets based on the flow table.
* **Southbound Interface:** OpenFlow protocol used for communication between the controller and the switch.

##  Troubleshooting
* **Clean up Mininet:** If you get an error saying the controller is already running, run `sudo mn -c`.
* **No Connectivity:** Ensure the POX controller terminal is active and showing logs of packet-in events.

---


