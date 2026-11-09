# Práctica: Análisis e implementación de la seguridad en el servicio DHCP

**Módulo:** Alina  
**Ciclo formativo:** ASIX  
**Alumno:** Deivid Cardona  

## Objetivo

Analizar el funcionamiento del protocolo DHCPv4, identificar sus debilidades de seguridad y comprobar en un entorno virtual aislado el impacto de un ataque de DHCP Starvation. Posteriormente, se aplicarán medidas de mitigación a nivel de servidor Linux y se documentarán las soluciones utilizadas en infraestructuras reales.

## Entorno de práctica

- VirtualBox.
- Red interna aislada.
- Debian/Ubuntu Server como servidor DHCP.
- Kali Linux como cliente y equipo de pruebas.
- Wireshark o tcpdump para captura de tráfico.
- Scapy para generar peticiones DHCP controladas.

## Índice

1. [Teoría](01-teoria.md)
2. [Preparación del entorno](02-preparacion-entorno.md)
3. [Práctica DHCP](03-practica-dhcp.md)
4. [Ataque DHCP Starvation](04-ataque-starvation.md)
5. [Mitigaciones](05-mitigaciones.md)
6. [Conclusiones](06-conclusiones.md)

## Estructura

```text
DHCP-Seguridad/
├── README.md
├── 01-teoria.md
├── 02-preparacion-entorno.md
├── 03-practica-dhcp.md
├── 04-ataque-starvation.md
├── 05-mitigaciones.md
├── 06-conclusiones.md
├── scripts/
│   └── dhcp_starvation_laboratorio.py
├── configuracion/
│   ├── dhcpd.conf
│   ├── interfaces.md
│   └── iptables-hashlimit.md
└── capturas/
    └── README.md
```

## Checklist de entrega

- [ ] Explicar el proceso DORA.
- [ ] Explicar el campo `chaddr` y su relación con la MAC Ethernet.
- [ ] Documentar la falta de autenticación nativa de DHCP.
- [ ] Configurar el servidor DHCP en Debian/Ubuntu.
- [ ] Capturar el intercambio DORA.
- [ ] Comprobar la asignación de una IP al cliente.
- [ ] Ejecutar el ataque de Starvation solo en la red interna de laboratorio.
- [ ] Comprobar el agotamiento del pool.
- [ ] Comprobar el comportamiento APIPA.
- [ ] Aplicar límite de peticiones con `hashlimit`.
- [ ] Documentar DHCP Snooping y Port Security.
- [ ] Añadir capturas de evidencia.
- [ ] Redactar conclusiones.

## Aviso ético

Las pruebas de ataque deben realizarse exclusivamente en una red interna propia de VirtualBox. No se deben realizar pruebas contra redes domésticas, educativas, corporativas ni redes de terceros.