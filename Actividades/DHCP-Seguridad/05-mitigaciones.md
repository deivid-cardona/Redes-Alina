# Mitigaciones

## 1. Límite de peticiones con hashlimit

El módulo `hashlimit` de iptables permite limitar la tasa de paquetes por grupos, por ejemplo por IP de origen.

Ejemplo:

```bash
sudo iptables -A INPUT -p udp --dport 67 \
  -m hashlimit \
  --hashlimit-name dhcp_limit \
  --hashlimit-above 10/minute \
  --hashlimit-mode srcip \
  --hashlimit-burst 15 \
  -j DROP
```

Este comando limita las peticiones DHCP desde una misma IP de origen.

Para comprobar las reglas:

```bash
sudo iptables -L INPUT -v -n
```

## 2. Políticas de lease

Un lease corto reduce el tiempo durante el cual las IP permanecen reservadas tras un ataque.

Ejemplo:

```conf
default-lease-time 300;
max-lease-time 600;
```

Sin embargo, un lease demasiado corto aumenta el tráfico de renovación.

## 3. Detección de conflictos

El servidor DHCP puede comprobar si una IP ya está en uso antes de asignarla.

En `dhcpd.conf` se puede habilitar:

```conf
ping-check true;
```

Esto ayuda a evitar asignar direcciones que ya están siendo utilizadas por otro equipo.

## 4. DHCP Snooping

En un switch físico gestionable, DHCP Snooping permite diferenciar entre:

- **Puertos trusted:** conectados al servidor DHCP legítimo.
- **Puertos untrusted:** conectados a clientes.

Los mensajes de servidor DHCP recibidos por puertos untrusted son descartados, lo que impide la actuación de un Rogue DHCP.

## 5. Port Security

Port Security limita el número de MACs que pueden aprenderse por un puerto físico.

Esto dificulta que un único equipo genere múltiples identidades de capa 2 para realizar un ataque de Starvation complejo.

## 6. ebtables

`ebtables` permite filtrar tramas Ethernet en un bridge Linux. Actúa en capa 2, mientras que `iptables` actúa principalmente en capa 3.

Puede utilizarse para limitar el número de MACs origen que atraviesan un puerto del bridge.

## 7. Evidencias

- [ ] Captura de las reglas iptables aplicadas.
- [ ] Captura del pool antes y después de aplicar límites.
- [ ] Captura del comportamiento del lease.
- [ ] Captura de la configuración de `ping-check`.