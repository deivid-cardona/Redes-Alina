# Teoría: seguridad en el servicio DHCP

## 1. Proceso DORA

DHCPv4 utiliza el intercambio DORA para asignar configuración de red a los clientes:

| Paso | Mensaje | Emisor | Función |
|---|---|---|---|
| 1 | `DHCPDISCOVER` | Cliente | Busca servidores DHCP mediante broadcast |
| 2 | `DHCPOFFER` | Servidor | Propone una dirección IP y parámetros de red |
| 3 | `DHCPREQUEST` | Cliente | Solicita formalmente una oferta recibida |
| 4 | `DHCPACK` | Servidor | Confirma la asignación y establece el lease |

El cliente comienza normalmente sin dirección IP válida y envía `DHCPDISCOVER` a la dirección de broadcast `255.255.255.255`. Por este motivo, todos los equipos del mismo segmento pueden observar el tráfico DHCP.

### Implicaciones de seguridad

Un atacante situado en el mismo segmento puede:

- Capturar mensajes DHCP.
- Identificar clientes, servidores y direcciones MAC.
- Observar las IP ofrecidas y las opciones de red.
- Suplantar un servidor DHCP legítimo mediante un Rogue DHCP.
- Generar múltiples solicitudes para agotar el pool de direcciones.

## 2. Campo `chaddr` y MAC Ethernet

El campo `chaddr` (*Client Hardware Address*) es la dirección hardware declarada por el cliente dentro del mensaje DHCP, que se encuentra en la capa de aplicación.

La MAC de origen Ethernet es la dirección física incluida en la cabecera de la trama de capa 2.

En un cliente legítimo, ambos valores coinciden. Sin embargo, un atacante puede modificar el campo `chaddr` del paquete DHCP y utilizar una MAC Ethernet distinta.

El servidor DHCP utiliza `chaddr` para identificar al cliente, asignarle una IP y mantener el lease. Esta confianza en un campo controlado por el cliente permite realizar suplantación o *spoofing*.

## 3. Falta de autenticación

El RFC 2131 define el funcionamiento básico de DHCP, pero no establece un mecanismo obligatorio de autenticación o cifrado para los mensajes DHCP estándar.

Por ello:

- Cualquier host puede enviar un `DHCPDISCOVER`.
- Cualquier host puede intentar responder como servidor DHCP.
- No existe una limitación inherente que impida solicitar muchas direcciones IP.

### RFC 3118

El RFC 3118 define una opción de autenticación para mensajes DHCP. Permite que cliente y servidor validen la procedencia e integridad de los mensajes.

Su adopción es prácticamente nula porque requiere configuración adicional en clientes y servidores, muchos dispositivos no lo implementan y las organizaciones suelen utilizar controles de capa 2 como DHCP Snooping, Port Security y 802.1X.

## 4. DHCP Starvation

El ataque de DHCP Starvation consiste en agotar el pool de direcciones IP de un servidor DHCP legítimo.

### Ataque simple

El atacante modifica únicamente el campo `chaddr` en cada petición DHCP. El servidor considera que cada valor corresponde a un cliente distinto y asigna una IP diferente.

### Ataque complejo

El atacante modifica tanto la MAC de origen Ethernet como el campo `chaddr`. De esta forma, cada petición parece proceder de un equipo físico diferente.

Este segundo escenario es más difícil de mitigar porque el switch no puede identificar al atacante únicamente mediante una MAC fija.

## 5. Ciclo de vida del lease

Si un atacante obtiene muchas direcciones IP y se desconecta, estas no quedan disponibles inmediatamente: permanecen reservadas hasta que expire el lease.

- Con un lease de 7 días, el efecto puede durar hasta 7 días.
- Con un lease de 5 minutos, las direcciones vuelven a estar disponibles rápidamente.

Un lease corto reduce el impacto del ataque, pero aumenta el tráfico de renovación.

## 6. APIPA

APIPA (*Automatic Private IP Addressing*) es un mecanismo de autoconfiguración utilizado cuando un cliente no recibe respuesta de un servidor DHCP.

Las direcciones APIPA pertenecen al rango:

```text
169.254.0.0/16
```

Limitaciones:

- Máscara `255.255.0.0`.
- No hay puerta de enlace predeterminada.
- No hay acceso a Internet ni a redes remotas.
- Solo permite comunicación local dentro del mismo segmento.

## 7. DHCP Snooping

DHCP Snooping es una función de seguridad de capa 2 presente en switches de acceso. Filtra mensajes DHCP según el tipo de puerto.

| Tipo de puerto | Uso | Comportamiento |
|---|---|---|
| Trusted | Conecta al servidor DHCP legítimo | Permite mensajes de servidor DHCP |
| Untrusted | Conecta a clientes | Bloquea respuestas de servidores no autorizados |

La base de vinculación registra:

- MAC del cliente.
- IP asignada.
- VLAN.
- Puerto de acceso.
- Tipo y tiempo de lease.

## 8. Port Security

Port Security limita el número de direcciones MAC que pueden aprenderse por un puerto físico.

Si un atacante intenta enviar tramas con muchas MAC origen distintas desde un mismo puerto, el switch puede descartar el tráfico, generar alertas o desactivar el puerto.

## 9. hashlimit y ebtables

El módulo `hashlimit` de iptables permite limitar la tasa de paquetes por grupos, por ejemplo por IP de origen. Es útil para limitar ráfagas de `DHCPDISCOVER`.

`ebtables` filtra tramas Ethernet en un bridge Linux. Actúa en capa 2, mientras que `iptables` actúa principalmente en capa 3 y superior.

## 10. Modo promiscuo

El modo promiscuo permite que una interfaz acepte y observe tramas que no están dirigidas específicamente a su MAC.

En VirtualBox está restringido por defecto porque puede exponer tráfico de otras máquinas virtuales o del host. En una Red Interna, habilitar `Allow All` facilita que Scapy envíe y reciba paquetes DHCP durante la práctica.

Un script puede enviar tramas con MAC origen inventada aunque la interfaz no esté en modo promiscuo, pero la recepción y observación completa del tráfico puede verse afectada.