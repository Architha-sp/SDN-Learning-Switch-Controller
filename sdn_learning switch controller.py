from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

mac_to_port = {}

def _handle_PacketIn(event):
    packet = event.parsed
    dpid = event.connection.dpid
    in_port = event.port

    if not packet.parsed:
        log.warning("Ignoring incomplete packet")
        return

    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    # Learn source MAC
    mac_to_port[dpid][packet.src] = in_port

    # If destination known, forward
    if packet.dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][packet.dst]

        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, in_port)
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.data = event.ofp
        event.connection.send(msg)

        log.info("Forwarding %s -> %s via port %s", packet.src, packet.dst, out_port)
    else:
        # Flood
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        action = of.ofp_action_output(port=of.OFPP_FLOOD)
        msg.actions.append(action)
        event.connection.send(msg)

core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
