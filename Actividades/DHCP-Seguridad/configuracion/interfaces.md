# Configuración de red del servidor

## Debian/Ubuntu

Editar:

```bash
sudo nano /etc/network/interfaces
```

Ejemplo:

```text
auto enp0s3
iface enp0s3 inet static
    address 192.168.10.1
    netmask 255.255.255.0
```

Aplicar cambios:

```bash
sudo systemctl restart networking
```

Comprobar:

```bash
ip a
ip route
```

## Configurar la interfaz DHCP

Editar:

```bash
sudo nano /etc/default/isc-dhcp-server
```

```text
INTERFACESv4="enp0s3"
```

Reiniciar el servicio:

```bash
sudo systemctl restart isc-dhcp-server
sudo systemctl status isc-dhcp-server
```