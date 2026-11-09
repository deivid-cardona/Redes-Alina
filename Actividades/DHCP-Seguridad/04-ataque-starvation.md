# Ataque DHCP Starvation

## Aviso ético

Este procedimiento debe ejecutarse únicamente en una **Red Interna de VirtualBox** creada para la práctica. No debe utilizarse contra redes domésticas, educativas, corporativas ni redes de terceros.

## Objetivo

Comprobar cómo un atacante puede agotar el pool de direcciones IP de un servidor DHCP generando múltiples identidades de cliente.

## 1. Comprobar el pool inicial

En el servidor:

```bash
sudo cat /var/lib/dhcp/dhcpd.leases
```

Comprobar cuántas direcciones están disponibles en el rango configurado.

## 2. Instalar Scapy en Kali

```bash
sudo apt update
sudo apt install python3-scapy -y
```

## 3. Ejecutar el script controlado

El script incluido en `scripts/dhcp_starvation_laboratorio.py` genera un número limitado de peticiones DHCP para laboratorio.

```bash
python3 scripts/dhcp_starvation_laboratorio.py --interface eth0 --cantidad 10
```

El parámetro `--cantidad` limita el número de peticiones generadas. No debe utilizarse un valor alto en un entorno real.

## 4. Comprobar el agotamiento

En el servidor:

```bash
sudo cat /var/lib/dhcp/dhcpd.leases
```

En Kali, intentar obtener una nueva IP:

```bash
sudo dhclient -r enp0s3
sudo dhclient -v enp0s3
```

Si el pool está agotado, el cliente no recibirá una dirección DHCP válida.

## 5. Comprobar APIPA

En Kali:

```bash
ip a
```

Si el sistema está configurado para APIPA, puede aparecer una dirección del rango:

```text
169.254.0.0/16
```

## 6. Efecto del lease

Si el atacante se desconecta después de agotar el pool, las direcciones permanecen reservadas hasta que expire el lease.

- Lease de 7 días: el efecto puede durar hasta 7 días.
- Lease de 5 minutos: el efecto desaparece rápidamente.

## 7. Evidencias

- [ ] Captura del pool antes del ataque.
- [ ] Captura del script generando peticiones.
- [ ] Captura del pool después del ataque.
- [ ] Captura de un cliente sin IP o con APIPA.
- [ ] Captura de Wireshark mostrando múltiples `DHCPDISCOVER`.