# Packaging Unit - Equipment Manual

## Model: PU-500 Automated Packaging System

### Overview

The PU-500 Automated Packaging System provides high-speed carton forming, filling, and sealing capabilities for manufacturing lines. This manual covers operation, maintenance, and troubleshooting.

### Specifications

| Parameter | Value |
|-----------|-------|
| Packaging Speed | Up to 60 cartons/minute |
| Carton Size Range | 100x100x50mm to 400x300x250mm |
| Power Requirements | 380V 3-phase, 15 kW |
| Air Supply | 6 bar, 200 L/min |
| Operating Temperature | 15°C to 35°C |
| Humidity Range | 30% - 70% RH |

### System Components

1. **Carton Magazine**: Holds flat carton blanks (capacity: 500 cartons)
2. **Forming Station**: Pneumatic carton erector with vacuum grippers
3. **Filling Station**: Gravity or conveyor-fed product insertion
4. **Sealing Station**: Hot melt glue applicator with compression rollers
5. **Outfeed Conveyor**: Transfers sealed cartons to downstream equipment
6. **Control Panel**: HMI touchscreen with PLC integration

### Operating Procedures

#### Pre-Operation Checklist

1. Verify air supply pressure (6 bar minimum)
2. Check glue tank level (minimum 50%)
3. Load carton blanks into magazine
4. Confirm all guards are closed and interlocked
5. Verify product supply is ready

#### Startup Sequence

1. Power on main disconnect
2. Wait for HMI initialization (approximately 30 seconds)
3. Select product recipe from HMI menu
4. Enable glue heater and wait for temperature (165°C)
5. Press AUTO START to begin production

#### Recipe Configuration

Access recipe editor via HMI: Menu > Recipes > Edit

Parameters to configure:
- Carton dimensions (L x W x H)
- Glue pattern selection
- Sealing pressure
- Line speed synchronization

#### Shutdown Procedure

1. Press STOP to halt production
2. Allow machine to complete current cycle
3. Run glue purge cycle (prevents nozzle clogging)
4. Power off glue heater
5. Disable main power after 10-minute cooldown

### Maintenance Schedule

#### Every Shift
- Clean glue nozzles with approved solvent
- Check vacuum gripper suction cups for wear
- Verify carton magazine alignment
- Empty scrap bin

#### Daily Maintenance
- Lubricate forming station guides (use food-grade grease)
- Check pneumatic cylinder operation
- Inspect sealing rollers for glue buildup
- Verify sensor alignment

#### Weekly Maintenance
- Full glue system inspection and cleaning
- Check all pneumatic fittings for leaks
- Inspect drive belts for wear
- Clean all photoelectric sensors
- Verify safety interlock operation

#### Monthly Maintenance
- Replace vacuum gripper cups
- Calibrate glue temperature controller
- Check PLC battery status
- Inspect electrical connections
- Update production logs backup

### Troubleshooting Guide

#### Carton Forming Issues

**Problem**: Cartons not opening properly
- Check vacuum pressure (should be -0.6 bar)
- Inspect gripper cups for damage
- Verify carton blank quality
- Adjust forming station timing

**Problem**: Cartons jamming in magazine
- Check carton blank alignment
- Reduce magazine stack height
- Verify separator fingers operation

#### Sealing Issues

**Problem**: Weak seal or carton opening
- Verify glue temperature (165°C ± 5°C)
- Check glue nozzle for blockage
- Increase sealing pressure
- Verify compression roller alignment

**Problem**: Glue stringing or dripping
- Reduce glue temperature
- Check nozzle air assist pressure
- Clean nozzle tips
- Verify glue viscosity

### Alarm Codes

| Code | Description | Action |
|------|-------------|--------|
| A001 | Low air pressure | Check supply, inspect for leaks |
| A002 | Glue tank low | Refill glue tank |
| A003 | Glue temperature fault | Check heater, verify thermocouple |
| A004 | Carton jam detected | Clear jam, check alignment |
| A005 | Vacuum fault | Check pump, inspect lines |
| A006 | Safety guard open | Close guard, reset interlock |
| A007 | Motor overload | Check for mechanical binding |
| A008 | Communication error | Check network connections |

### Safety Information

**CAUTION**: Hot surfaces present. Glue system operates at 165°C.

- Wear heat-resistant gloves when servicing glue system
- Lock out/tag out before any maintenance
- Never bypass safety interlocks
- Keep hands clear of forming and sealing stations
- Wear safety glasses when operating or servicing

### Contact Information

Technical Support: support@packaging-systems.example.com
Spare Parts: parts@packaging-systems.example.com
Service Hotline: +1-555-PACKAGE (24/7)
