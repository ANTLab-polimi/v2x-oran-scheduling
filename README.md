# V2X & O-RAN Resource Allocation/Management 
This project includes an e2e setup and integration of [V2X ns3 module](https://5g-lena.cttc.es/blog/23/) of [5G-LENA](https://5g-lena.cttc.es/) with [OpenRAN](https://openrangym.com/) architecture with the purpose of implementing the resource allocation functionality of V2X networks in O-RAN architecture.

It contains the [local deployment](https://github.com/fgjeci/colosseum-near-rt-ric) of [O-RAN architecture](https://openrangym.com/), the xApp which implements the logic of [resource scheduling in V2X networks](https://github.com/fgjeci/v2x-xapp.git), the modified [V2X ns3 module](https://github.com/fgjeci/ns3-v2x-scheduling.git) of [5G-LENA](https://5g-lena.cttc.es/blog/23/) and the [E2 inteface](https://github.com/fgjeci/oran-e2sim) connecting the ns3 module with O-RAN.

To run the project:
- Install the [ns3 packages](https://www.nsnam.org/wiki/Installation) needed to run ns3. 
- Configure & build [ns3-mmwave-millicar](https://github.com/fgjeci/ns3-mmwave-millicar)
