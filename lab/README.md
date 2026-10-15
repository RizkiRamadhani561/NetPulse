# Isolated network lab — Phase 0

The lab is deliberately opt-in. It defines a dummy HTTP endpoint and an SNMP simulator on the internal-only Docker network `lab_internal`. These services are not published to the Windows host or the LAN.

## Start the lab overlay

```powershell
docker compose -f docker-compose.yml -f docker-compose.lab.yml --profile lab up --build
```

Stop it with:

```powershell
docker compose -f docker-compose.yml -f docker-compose.lab.yml --profile lab down
```

The API is attached to the internal lab network only when this overlay is selected. No ping, subnet scan, or discovery runs automatically. Real monitoring workers and scenario controls are not implemented until later phases.

## Fixtures

- `fixtures/snmp/system.snmprec`: synthetic SNMP values only, no real device data.
- `fixtures/oui-mini.csv`: synthetic fixture rows for parser tests; it is not a vendor database.
- `scenarios/*.yml`: early scenario descriptions; execution/control is not implemented yet.

**Authorization rule:** use NetPulse to monitor only networks you own or are authorized to monitor. Do not change the lab network to bridge into a real office/school network without first reviewing the security boundary.
