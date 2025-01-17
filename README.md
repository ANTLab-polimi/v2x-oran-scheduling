# V2X & O-RAN Resource Allocation/Management 

This project includes an e2e setup and integration of [V2X ns3 module](https://5g-lena.cttc.es/blog/23/) of [5G-LENA](https://5g-lena.cttc.es/) with [OpenRAN](https://openrangym.com/) architecture with the purpose of implementing the resource allocation functionality of V2X networks in O-RAN architecture.

It contains the [OpenRAN RIC](https://github.com/fgjeci/colosseum-near-rt-ric) of [O-RAN architecture](https://openrangym.com/), the xApp implementing the logic of [resource scheduling in V2X networks](https://github.com/fgjeci/v2x-xapp), the modified [V2X ns3 module](https://github.com/fgjeci/ns3-v2x-scheduling) of [5G-LENA](https://5g-lena.cttc.es/blog/23/) and the [E2 inteface](https://github.com/fgjeci/oran-e2sim) connecting the ns3 module with [O-RAN](https://www.o-ran.org/).

If you use this module in your research, please cite:

F. Gjeci, E. Moro, F. Linsalata, I. Filippini and A. Capone, "Towards Smarter Vehicular Communications: Leveraging Open RAN for Enhanced Vehicle-to-Vehicle Resources Management," 2024 IEEE 100th Vehicular Technology Conference (VTC2024-Fall), Washington, DC, USA, 2024, pp. 1-7, doi: 10.1109/VTC2024-Fall63153.2024.10758024. [bibtex available here](https://ieeexplore.ieee.org/abstract/document/10758024?casa_token=05MkNMAbLDEAAAAA:GBR57H3P3-NCW_lgLZgCX3dyOmvrT-1QwTjJTRcWAAWBoo-rmPzUTiPU3oYHB4oOHb5O2YoNhA)

To run the project:
- Install the [ns3 packages](https://www.nsnam.org/wiki/Installation) needed to run ns3. 
- Configure & build [ns3-v2x-scheduling](https://github.com/fgjeci/ns3-v2x-scheduling)
```
cd ../ns3-v2x-scheduling
./ns3 configure --build-profile=debug --disable-werror --enable-examples
./ns3 build
```
- Import docker images and setup docker containers of [OpenRAN RIC](https://github.com/fgjeci/colosseum-near-rt-ric) based on [OpenRAN GYM](https://openrangym.com/tutorials/ns-o-ran)
```
cd ../colosseum-near-rt-ric/setup-scripts
./setup-ric-bronze.sh
```

At the end of the build, the added containers in docker should be the following: e2term, db, e2mgr, e2rtmansim.

- Create & install the shared library [e2sim](https://github.com/fgjeci/oran-e2sim) (E2-interface connecting ns3-module with OpenRAN-RIC via SCTP/IP)
```
cd ../oran-e2sim/e2sim
./build_e2sim.sh
```
- Setup the [xApp container](https://github.com/fgjeci/v2x-xapp)
```
cd ../v2x-xapp/setup-scripts
./setup-xapp-base.sh # Downloads & install the base image with the updated libraries. The base image shall have the e2 interface pre-installed, thus by default having enabled the connection with e2term and the exchange of E2 messages
./start-xapp-ns-o-ran.sh # Creates a secondary image with the python scripts of the xapp logic
# if outside the xapp container, access bash mode of the container -> docker exec -it xapp-v2x-24 bash
# Once inside the xapp container, go to /home/xapp-sm-connector directory
```
Following the aforementioned steps, the xApp is configured to receive E2 messages, decode the xml format of the these messages and send back E2-Ric encoded messages.

## Simulation steps
The simulation involves these steps:
1. Starting the xApp Agent in the xApp container: It starts the SCTP/IP server and binds to local address and accepts connection from the RIC
2. Starting the ns3 simulation instances: Inside the ns3 it is started the ns3-E2-Termination endpoint, which connects ns3 to RIC via SCTP/IP. This simulation instance waits for Subscription Requests coming from RIC to start sending reports to the xApp.
3. Starting RIC-E2-endpoint: The end point responsible to decode the incoming E2 messages, route them to the appropriate xApp and maintain the Service Model paradigm.

It is crucial to execute the steps as shown above: ns3 simulation instances (2) before the RIC-E2-endpoint(3), so that the ns3-E2-Termination endpoint can received and decode the Subscribe Requests generated by the RIC-E2-endpoint; start xApp-Agent (1) before the RIC-E2-endpoint, as the last opens a TCP/IP socket connection to the xApp and if xApp has not started and bind to the receiving address, the RIC won't be able to forward the incoming control messages

### Commands
1. Start xApp-Aggent
```
# Enter inside xApp container
docker exec -it xapp-v2x-24 bash
cd /home/xapp-v2x
python3 run_xapp_parallel.py
```
2. Starting ns3 simulation instances
```
cd ../v2x-oran-scheduling
python3 v2x_sched.py # Launches multiple processes in parallel, one per each simulation scenario
```
3. Starting RIC-E2-endpoint
```
docker exec -it xapp-v2x-24 bash
cd /home/xapp-sm-connector
./run_xapp.sh
```
