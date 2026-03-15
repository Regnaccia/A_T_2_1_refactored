# ActiveThermo Configuration Assembler v2.1

Questa revisione introduce un layer `entities` più strutturato rispetto alla versione iniziale:

1. separazione esplicita tra `provider` e `role`
2. supporto a entità primitive e derived
3. derived consentite in v1 solo per `sensor` e `binary_sensor`
4. supporto iniziale a `mqtt` tramite `source.topic`
5. split del vecchio `models.py` in più file, uno per tipo di entità

## Pipeline

1. load raw YAML
2. validate con Pydantic
3. assemble delle istanze inizializzate
4. apply naming policy sugli entity id esportati
5. build di un unico `AssembledConfiguration`
6. dump opzionale in JSON o YAML

## Regole chiave

- `domain` è implicito dalla sezione YAML
- `provider` è sempre esplicito: `config`, `mqtt`, `runtime`, `derived`
- `role` è sempre esplicito: `input`, `internal`, `output`
- entità primitive: nessuna `dependencies`, nessuna `evaluation`
- entità derived: `provider: derived`, `dependencies` + `evaluation`
- solo `sensor` e `binary_sensor` possono essere derived in v1
- `mqtt` richiede `source.topic`

## Esempio rapido

```yaml
sensor:
  - id: temp_raw
    name: Raw temperature
    provider: mqtt
    role: input
    source:
      topic: thermo/zone/01/temp_raw/state

  - id: temp_corrected
    name: Corrected temperature
    provider: derived
    role: internal
    dependencies:
      - temp_raw
      - temp_offset
    evaluation:
      kind: math
      operator: add
```

## File principali

```text
app_v2_1/
  assembler/
  entities/
    base.py
    sensor.py
    binary_sensor.py
    ...
  loaders/
  normalizers/
  tests/
  utils/
  models.py        # compatibility re-export
main_v2_1.py
```

## Nota

Questa proposta non introduce ancora il registry builder con cycle detection. Prepara però il contratto dati corretto per quel passo.
