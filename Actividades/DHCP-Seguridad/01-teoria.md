# Análisis teórico: seguridad en el servicio DHCP

## Introducción

En esta primera parte de la práctica voy a analizar el funcionamiento del protocolo DHCPv4 y los principales riesgos de seguridad asociados a su uso. DHCP (*Dynamic Host Configuration Protocol*) es el servicio que permite a un dispositivo obtener de forma automática una dirección IP, la máscara de red, la puerta de enlace y otros parámetros necesarios para comunicarse en una red.

Aunque DHCP facilita mucho la administración de una red, también presenta debilidades importantes. Al tratarse de un protocolo diseñado para funcionar de forma automática y sin autenticación obligatoria, un atacante situado en el mismo segmento de red puede suplantar un servidor DHCP, capturar tráfico o agotar el pool de direcciones IP mediante un ataque de *DHCP Starvation*.

En esta práctica analizaré estos conceptos desde el punto de vista teórico y, posteriormente, los comprobaré en un entorno aislado de VirtualBox.

## Contexto: ¿por qué DHCP es importante?

En una red pequeña, podríamos configurar manualmente la dirección IP de cada equipo. Sin embargo, en una red con muchos dispositivos —ordenadores, móviles, impresoras, cámaras, servidores o máquinas virtuales— esta tarea sería lenta y propensa a errores.

DHCP resuelve este problema asignando direcciones IP de forma dinámica. Cuando un equipo se conecta a la red, solicita una configuración al servidor DHCP y recibe una dirección disponible durante un tiempo determinado, llamado *lease* o concesión.

El problema de seguridad aparece porque DHCP fue diseñado priorizando la facilidad de uso y la compatibilidad, no la autenticación. Por este motivo, un dispositivo malicioso puede participar en el proceso como si fuera un cliente legítimo o incluso hacerse pasar por un servidor DHCP.

## El proceso DORA

El funcionamiento básico de DHCPv4 se basa en cuatro mensajes conocidos como **DORA**:

| Paso | Mensaje | Emisor | Función |
|---|---|---|---|
| 1 | `DHCPDISCOVER` | Cliente | Busca servidores DHCP disponibles |
| 2 | `DHCPOFFER` | Servidor | Propone una dirección IP y parámetros de red |
| 3 | `DHCPREQUEST` | Cliente | Solicita formalmente una oferta recibida |
| 4 | `DHCPACK` | Servidor | Confirma la asignación y establece el lease |

### DHCPDISCOVER

Cuando un equipo se conecta a la red y está configurado para obtener IP automáticamente, no conoce ningún servidor DHCP. Por ello, envía un mensaje `DHCPDISCOVER` en broadcast hacia la dirección `255.255.255.255`.

En este momento, el cliente todavía no tiene una dirección IP válida, por lo que normalmente utiliza la dirección `0.0.0.0` como origen.

### DHCPOFFER

Los servidores DHCP que reciben la solicitud pueden responder con un mensaje `DHCPOFFER`. En este mensaje, el servidor propone una dirección IP, una máscara, una puerta de enlace, servidores DNS y otros parámetros.

Si hay varios servidores DHCP en la red, el cliente puede recibir varias ofertas y deberá elegir una.

### DHCPREQUEST

Una vez que el cliente ha recibido una oferta, envía un `DHCPREQUEST` para indicar qué servidor y qué dirección IP desea aceptar. Este mensaje también se envía en broadcast para informar a los demás servidores de que no se ha aceptado su oferta.

### DHCPACK

Finalmente, el servidor seleccionado responde con un `DHCPACK`. Este mensaje confirma la asignación de la IP y establece el tiempo de concesión.

A partir de este momento, el cliente puede utilizar la dirección IP recibida para comunicarse en la red.

### Esquema del proceso

```text
Cliente                         Servidor DHCP
  │                                 │
  │──── DHCPDISCOVER ──────────────▶│
  │                                 │
  │◀──────────── DHCPOFFER ─────────│
  │                                 │
  │──── DHCPREQUEST ───────────────▶│
  │                                 │
  │◀────────────── DHCPACK ─────────│
```

### Evidencia práctica

En la parte práctica capturaré este intercambio utilizando Wireshark. La captura deberá mostrar los cuatro mensajes DORA.

> **Captura pendiente:** intercambio DORA capturado en Wireshark.

## El broadcast y su riesgo

El uso de broadcast es necesario porque el cliente no conoce inicialmente la dirección del servidor DHCP. Sin embargo, esto tiene consecuencias de seguridad.

Al ser un mensaje broadcast, cualquier equipo del mismo segmento puede observar el tráfico DHCP. Un atacante puede utilizar herramientas de captura de paquetes para obtener información sobre los clientes, los servidores y las configuraciones que se están asignando.

Además, un atacante puede responder a las peticiones DHCP como si fuera un servidor legítimo. Esto se conoce como **Rogue DHCP** o servidor DHCP no autorizado.

Si el atacante consigue que un cliente acepte su oferta, puede asignarle una puerta de enlace o un servidor DNS falsos. De esta forma podría redirigir el tráfico, interceptar comunicaciones o realizar ataques de *Man-in-the-Middle*.

## Campo `chaddr` y MAC Ethernet

Dentro de un mensaje DHCP existe un campo llamado `chaddr`, que significa *Client Hardware Address*. Este campo contiene la dirección hardware que el cliente declara tener.

Por otro lado, la cabecera Ethernet incluye la **MAC de origen**, que es la dirección de capa 2 utilizada para enviar la trama.

En un equipo legítimo, ambos valores deberían coincidir:

```text
MAC Ethernet de origen = chaddr del mensaje DHCP
```

Sin embargo, no existe una comprobación obligatoria que garantice esta coincidencia. Un atacante puede modificar el campo `chaddr` dentro del paquete DHCP y utilizar una MAC Ethernet diferente.

El servidor DHCP utiliza principalmente `chaddr` para identificar al cliente, asignarle una dirección IP y mantener el lease. Esto significa que, si el atacante cambia este campo, el servidor puede interpretar que se trata de un cliente nuevo.

### Riesgo de suplantación

Esta diferencia entre la capa 2 y la capa 7 permite realizar suplantación o *spoofing*. Un atacante puede generar muchas identidades falsas simplemente modificando el campo `chaddr` en cada petición.

> **Captura pendiente:** análisis de un paquete DHCP en Wireshark mostrando el campo `chaddr`.

## Falta de autenticación en DHCP

El RFC 2131 define el funcionamiento básico de DHCP. Sin embargo, no establece un mecanismo obligatorio de autenticación o cifrado para los mensajes DHCP estándar.

Esto tiene dos consecuencias importantes:

- Cualquier host puede enviar un `DHCPDISCOVER` y solicitar una dirección IP.
- Cualquier host puede intentar responder como servidor DHCP.

No existe una comprobación inherente que permita al servidor saber si el cliente es legítimo, ni al cliente saber si el servidor es de confianza.

### RFC 3118

El RFC 3118 propone un mecanismo de autenticación para mensajes DHCP. Su objetivo es permitir que cliente y servidor validen la procedencia e integridad de los mensajes.

A pesar de ser una solución teóricamente útil, su adopción real ha sido muy limitada. Esto se debe a que requiere configuración adicional en clientes y servidores, muchos dispositivos antiguos no lo implementan y las organizaciones suelen preferir soluciones de capa 2 como DHCP Snooping, Port Security y 802.1X.

## DHCP Starvation

El ataque de **DHCP Starvation** consiste en agotar el pool de direcciones IP de un servidor DHCP legítimo.

El atacante envía múltiples peticiones DHCP utilizando diferentes valores en el campo `chaddr`. El servidor interpreta que cada petición proviene de un cliente distinto y asigna una dirección IP diferente.

Cuando el rango de direcciones disponible se agota, los nuevos clientes no pueden obtener una IP.

### Ataque simple

En el ataque simple, el atacante modifica únicamente el campo `chaddr` del mensaje DHCP. La MAC Ethernet puede permanecer igual.

Este tipo de ataque es más fácil de detectar porque la MAC real de la trama se repite.

### Ataque complejo

En el ataque complejo, el atacante modifica tanto la MAC de origen Ethernet como el campo `chaddr`.

De esta forma, cada petición parece proceder de un equipo físico diferente. Esto dificulta la detección, porque el switch observa muchas MACs distintas aunque el origen real sea el mismo.

### Comparación

| Tipo de ataque | Campo modificado | Dificultad de detección |
|---|---|---|
| Simple | `chaddr` | Más fácil de detectar |
| Complejo | MAC Ethernet y `chaddr` | Más difícil de detectar |

> **Captura pendiente:** múltiples peticiones `DHCPDISCOVER` generadas desde Kali Linux.

## Ciclo de vida del lease

Cuando el servidor asigna una dirección IP, no la entrega de forma permanente. La asigna durante un tiempo determinado llamado *lease*.

Si un atacante obtiene muchas direcciones y se desconecta, estas no quedan libres inmediatamente. Permanecen reservadas hasta que expire el lease.

Por ejemplo:

- Con un lease de 7 días, el efecto del ataque puede durar hasta 7 días.
- Con un lease de 5 minutos, las direcciones vuelven a estar disponibles rápidamente.

Un lease corto reduce el impacto de un ataque, pero aumenta el tráfico de renovación. Por ello, el administrador debe encontrar un equilibrio entre seguridad y rendimiento.

## APIPA

Cuando un cliente configurado por DHCP no recibe respuesta de ningún servidor, puede autoconfigurarse mediante APIPA (*Automatic Private IP Addressing*).

Las direcciones APIPA pertenecen al rango:

```text
169.254.0.0/16
```

Estas direcciones permiten comunicación local dentro del mismo segmento, pero tienen limitaciones importantes:

- No proporcionan puerta de enlace predeterminada.
- No permiten acceder a Internet.
- No permiten comunicarse con otras redes.
- Solo sirven para comunicación local entre equipos que utilicen el mismo rango.

En un ataque de DHCP Starvation, es posible que un cliente obtenga una dirección APIPA porque el servidor DHCP legítimo ya no tiene direcciones disponibles.

> **Captura pendiente:** cliente con dirección APIPA tras agotar el pool.

## DHCP Snooping

DHCP Snooping es una función de seguridad de capa 2 presente en switches de acceso. Su objetivo es proteger la red frente a servidores DHCP no autorizados.

El switch diferencia entre dos tipos de puertos:

| Tipo de puerto | Uso | Comportamiento |
|---|---|---|
| Trusted | Conecta al servidor DHCP legítimo | Permite mensajes de servidor DHCP |
| Untrusted | Conecta a clientes | Bloquea respuestas de servidores no autorizados |

Por defecto, los puertos de acceso son untrusted. Solo el puerto que conecta con el servidor DHCP legítimo debe configurarse como trusted.

De esta forma, si un atacante conecta un Rogue DHCP a un puerto de acceso, sus respuestas serán descartadas por el switch.

### Base de vinculación

La base de vinculación o *DHCP Snooping Binding Database* registra información sobre las asignaciones legítimas:

- Dirección MAC del cliente.
- Dirección IP asignada.
- VLAN.
- Puerto de acceso.
- Tipo y tiempo de lease.

Esta información puede utilizarse posteriormente por otras funciones de seguridad, como Dynamic ARP Inspection o IP Source Guard.

## Port Security

Port Security limita el número de direcciones MAC que pueden aprenderse por un puerto físico de un switch.

Si un atacante intenta enviar tramas con muchas MAC origen distintas desde un mismo puerto, el switch puede:

- Descartar las tramas adicionales.
- Generar una alerta.
- Desactivar el puerto.

Esta medida dificulta el ataque de Starvation complejo, ya que impide que un único equipo simule masivamente muchos dispositivos diferentes.

## hashlimit y ebtables

En un entorno virtual como VirtualBox no disponemos de un switch físico gestionable. Por este motivo, el servidor Linux debe protegerse mediante medidas propias.

### hashlimit

El módulo `hashlimit` de iptables permite limitar la tasa de paquetes por grupos, por ejemplo por IP de origen. Es útil para limitar ráfagas de mensajes `DHCPDISCOVER`.

A diferencia del módulo `limit`, que aplica una tasa global, `hashlimit` crea límites independientes para cada grupo.

### ebtables

`ebtables` es una herramienta de filtrado para bridges Linux. Actúa en capa 2, mientras que `iptables` actúa principalmente en capa 3 y superior.

Con `ebtables` se pueden aplicar reglas basadas en direcciones MAC, tipo de trama, VLAN o protocolo Ethernet.

En esta práctica, `ebtables` podría utilizarse para limitar el número de MACs origen que atraviesan un bridge. La comprobación estricta de que la MAC Ethernet coincide con el campo `chaddr` requeriría un análisis más profundo del contenido del paquete DHCP.

## Modo promiscuo en VirtualBox

El modo promiscuo permite que una interfaz de red acepte y observe tramas que no están dirigidas específicamente a su dirección MAC.

En VirtualBox, esta opción está restringida por defecto porque puede exponer tráfico de otras máquinas virtuales o del host.

Para esta práctica, configuraré la interfaz de Kali Linux en **Modo promiscuo: Permitir todo** dentro de una Red Interna. Esto facilitará el envío y la recepción de paquetes DHCP durante las pruebas.

Un script puede enviar tramas con MAC origen inventada aunque la interfaz no esté en modo promiscuo. Sin embargo, la recepción y observación completa del tráfico puede verse afectada si esta opción no está habilitada.

> **Captura pendiente:** configuración del adaptador de Kali en modo promiscuo.

## Consideración ética

Las pruebas de este ataque deben realizarse únicamente en una red interna propia de VirtualBox. No deben realizarse contra redes domésticas, educativas, corporativas ni redes de terceros.

El objetivo de esta práctica es comprender la vulnerabilidad, reproducirla en un entorno controlado y aplicar medidas de mitigación.