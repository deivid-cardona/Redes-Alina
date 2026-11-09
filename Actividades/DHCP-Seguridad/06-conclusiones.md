# Conclusiones

## Resultado obtenido

Durante la práctica se ha comprobado el funcionamiento del protocolo DHCPv4 y su intercambio DORA. Se ha configurado un servidor DHCP en Debian/Ubuntu y se ha capturado el tráfico generado por un cliente Kali Linux.

## Vulnerabilidad identificada

DHCP no incluye un mecanismo obligatorio de autenticación en su funcionamiento estándar. Esto permite que un atacante situado en el mismo segmento pueda generar múltiples solicitudes y agotar el pool de direcciones IP.

## Impacto del ataque

Cuando el pool se agota, los nuevos clientes no pueden obtener una dirección IP válida. Según la configuración del sistema, pueden quedarse sin red o autoconfigurarse mediante APIPA en el rango `169.254.0.0/16`.

## Mitigaciones aplicadas

- Limitación de peticiones DHCP mediante `hashlimit`.
- Reducción del tiempo de lease.
- Detección de conflictos de IP.
- Documentación de DHCP Snooping y Port Security como soluciones de infraestructura.

## Conclusión final

La seguridad del servicio DHCP no depende únicamente del servidor. Debe combinarse con controles de acceso de capa 2, límites de tasa, políticas de lease adecuadas y monitorización del tráfico de red.