# Mitigación con iptables y hashlimit

## Objetivo

Limitar las ráfagas de peticiones DHCP desde una misma IP de origen.

## Regla propuesta

```bash
sudo iptables -A INPUT -p udp --dport 67 \
  -m hashlimit \
  --hashlimit-name dhcp_limit \
  --hashlimit-above 10/minute \
  --hashlimit-mode srcip \
  --hashlimit-burst 15 \
  -j DROP
```

## Comprobar reglas

```bash
sudo iptables -L INPUT -v -n
```

## Eliminar la regla

```bash
sudo iptables -D INPUT -p udp --dport 67 \
  -m hashlimit \
  --hashlimit-name dhcp_limit \
  --hashlimit-above 10/minute \
  --hashlimit-mode srcip \
  --hashlimit-burst 15 \
  -j DROP
```

## Nota

El límite debe ajustarse según el número real de clientes. Un valor demasiado bajo puede afectar a clientes legítimos que renuevan su lease.