# Práctica DHCP: proceso DORA

## Objetivo

Comprobar el funcionamiento del protocolo DHCP y capturar el intercambio DORA entre cliente y servidor.

## 1. Comprobar el servidor

En el servidor Debian/Ubuntu:

```bash
sudo systemctl status isc-dhcp-server
sudo journalctl -u isc-dhcp-server -f
```

## 2. Solicitar una IP desde Kali

En Kali:

```bash
sudo dhclient -r enp0s3
sudo dhclient -v enp0s3
ip a
```

## 3. Capturar el intercambio

Abrir Wireshark en Kali y aplicar el filtro:

```text
bootp || dhcp
```

También se puede utilizar tcpdump:

```bash
sudo tcpdump -i eth0 -n port 67 or port 68
```

## 4. Mensajes esperados

| Mensaje | Origen | Destino | Función |
|---|---|---|---|
| `DHCPDISCOVER` | Cliente | Broadcast | Busca servidores DHCP |
| `DHCPOFFER` | Servidor | Cliente/broadcast | Ofrece una IP |
| `DHCPREQUEST` | Cliente | Broadcast | Solicita la oferta |
| `DHCPACK` | Servidor | Cliente/broadcast | Confirma la asignación |

## 5. Comprobar el lease

En el servidor:

```bash
sudo cat /var/lib/dhcp/dhcpd.leases
```

En el cliente:

```bash
ip a
ip route
```

## 6. Evidencias

- [ ] Captura de `DHCPDISCOVER`.
- [ ] Captura de `DHCPOFFER`.
- [ ] Captura de `DHCPREQUEST`.
- [ ] Captura de `DHCPACK`.
- [ ] Captura de la IP asignada en Kali.
- [ ] Captura del archivo `dhcpd.leases`.