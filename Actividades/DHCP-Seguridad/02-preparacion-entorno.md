# Preparación del entorno

## 1. Topología propuesta

```text
┌────────────────────┐        ┌────────────────────┐
│   Debian/Ubuntu    │        │      Kali Linux     │
│  Servidor DHCP     │────────│  Cliente / atacante │
│  192.168.10.1      │        │  DHCP / Scapy       │
└────────────────────┘        └────────────────────┘
              Red interna VirtualBox
```

## 2. Crear la red interna

En VirtualBox:

1. Abrir **Configuración** de cada máquina virtual.
2. Ir a **Red**.
3. Seleccionar **Adaptador 1**.
4. Elegir **Red interna**.
5. Asignar el mismo nombre, por ejemplo `DHCP-LAB`.
6. En Kali, configurar **Modo promiscuo: Permitir todo**.

## 3. Configuración del servidor

En Debian/Ubuntu, editar la interfaz de red:

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

Aplicar la configuración:

```bash
sudo systemctl restart networking
```

Comprobar:

```bash
ip a
ip route
```

## 4. Instalar el servidor DHCP

```bash
sudo apt update
sudo apt install isc-dhcp-server -y
```

Comprobar el nombre de la interfaz:

```bash
ip a
```

Editar el archivo:

```bash
sudo nano /etc/default/isc-dhcp-server
```

Configurar:

```text
INTERFACESv4="enp0s3"
```

## 5. Configurar el pool DHCP

Editar:

```bash
sudo nano /etc/dhcp/dhcpd.conf
```

Ejemplo base:

```conf
authoritative;

subnet 192.168.10.0 netmask 255.255.255.0 {
    range 192.168.10.100 192.168.10.110;
    option routers 192.168.10.1;
    option subnet-mask 255.255.255.0;
    option domain-name-servers 8.8.8.8;
    default-lease-time 600;
    max-lease-time 7200;
}
```

Para la práctica se recomienda utilizar un pool pequeño, por ejemplo de 10 direcciones, para poder comprobar fácilmente el agotamiento.

## 6. Reiniciar y comprobar

```bash
sudo systemctl restart isc-dhcp-server
sudo systemctl status isc-dhcp-server
sudo ss -ulpn | grep 67
```

## 7. Comprobación desde Kali

```bash
sudo dhclient -v enp0s3
ip a
```

El cliente debe recibir una IP dentro del rango configurado.

## 8. Captura de tráfico

En Kali:

```bash
sudo tcpdump -i eth0 -n port 67 or port 68
```

O utilizando Wireshark con el filtro:

```text
bootp || dhcp
```

## Evidencias pendientes

- [ ] Captura de la configuración de red interna en VirtualBox.
- [ ] Captura de `ip a` en el servidor.
- [ ] Captura del estado de `isc-dhcp-server`.
- [ ] Captura del cliente obteniendo IP.
- [ ] Captura de Wireshark mostrando DORA.