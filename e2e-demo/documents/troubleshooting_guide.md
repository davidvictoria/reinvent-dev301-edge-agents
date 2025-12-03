# Industrial Equipment Troubleshooting Guide

## General Troubleshooting Methodology

### Step 1: Identify the Problem
- Note exact symptoms and when they occur
- Check alarm codes on HMI/control panel
- Review recent changes to equipment or process

### Step 2: Gather Information
- Check sensor readings and status indicators
- Review production logs for patterns
- Consult equipment manuals for specifications

### Step 3: Isolate the Cause
- Use process of elimination
- Test individual components
- Verify inputs and outputs

### Step 4: Implement Solution
- Follow proper lockout/tagout procedures
- Make one change at a time
- Document all changes made

### Step 5: Verify Resolution
- Test equipment under normal conditions
- Monitor for recurrence
- Update maintenance logs

---

## Common Equipment Issues

### Motor Problems

#### Motor Won't Start
**Possible Causes:**
1. Power supply issue
   - Check main disconnect is ON
   - Verify fuses/breakers are intact
   - Test voltage at motor terminals

2. Overload tripped
   - Check thermal overload relay
   - Investigate cause of overload
   - Reset after cooling period

3. Control circuit fault
   - Verify start signal from PLC
   - Check contactor coil voltage
   - Inspect control wiring

**Resolution Steps:**
1. Verify power at main disconnect
2. Check and reset overload if tripped
3. Test control circuit continuity
4. If motor hums but doesn't start, check for mechanical binding

#### Motor Overheating
**Possible Causes:**
- Overloaded beyond rated capacity
- Poor ventilation/blocked cooling
- Bearing failure
- Voltage imbalance

**Resolution Steps:**
1. Reduce load to rated capacity
2. Clean cooling fan and vents
3. Check bearing condition (listen for noise)
4. Measure voltage on all phases

### Sensor Issues

#### Proximity Sensor Not Detecting
**Possible Causes:**
- Incorrect sensing distance
- Target material incompatible
- Sensor damaged or dirty
- Wiring fault

**Resolution Steps:**
1. Verify target is within sensing range
2. Clean sensor face
3. Check LED indicator status
4. Test wiring continuity
5. Replace sensor if faulty

#### Temperature Sensor Reading Incorrect
**Possible Causes:**
- Sensor drift or calibration error
- Poor thermal contact
- Wiring resistance
- Damaged sensor element

**Resolution Steps:**
1. Compare with reference thermometer
2. Check sensor mounting and contact
3. Inspect wiring for damage
4. Recalibrate or replace sensor

### Pneumatic System Issues

#### Low Air Pressure
**Possible Causes:**
- Compressor fault
- Air leak in system
- Clogged filter
- Regulator malfunction

**Resolution Steps:**
1. Check compressor operation
2. Listen for air leaks
3. Inspect and replace filters
4. Verify regulator setting

#### Cylinder Not Operating
**Possible Causes:**
- No air supply
- Solenoid valve fault
- Cylinder seal failure
- Mechanical obstruction

**Resolution Steps:**
1. Verify air pressure at cylinder
2. Check solenoid valve operation (listen for click)
3. Inspect cylinder for leaks
4. Check for mechanical binding

### Communication Errors

#### PLC Communication Fault
**Possible Causes:**
- Network cable disconnected
- IP address conflict
- Switch/router failure
- PLC module fault

**Resolution Steps:**
1. Check physical connections
2. Verify network settings
3. Test with ping command
4. Check PLC diagnostic LEDs

#### HMI Not Responding
**Possible Causes:**
- Communication timeout
- HMI software crash
- Network issue
- PLC program fault

**Resolution Steps:**
1. Restart HMI application
2. Check communication cables
3. Verify PLC is running
4. Power cycle HMI if necessary

---

## Equipment-Specific Troubleshooting

### Conveyor Belt System (CB-2000)

#### Belt Tracking Off-Center
**Symptoms:** Belt drifting to one side
**Causes:**
- Uneven load distribution
- Misaligned rollers
- Belt splice issue
- Worn belt edge

**Solution:**
1. Redistribute load evenly
2. Adjust tracking rollers (turn toward direction belt is moving)
3. Inspect belt splice
4. Replace belt if edge is damaged

#### Belt Slipping
**Symptoms:** Motor running but belt not moving at correct speed
**Causes:**
- Insufficient tension
- Wet or oily belt surface
- Worn drive pulley
- Overloaded

**Solution:**
1. Increase belt tension
2. Clean belt and pulleys
3. Inspect drive pulley lagging
4. Reduce load

### Packaging Unit (PU-500)

#### Inconsistent Glue Application
**Symptoms:** Some cartons have weak seals
**Causes:**
- Glue temperature variation
- Clogged nozzles
- Air in glue lines
- Incorrect glue viscosity

**Solution:**
1. Verify glue temperature is stable at 165°C
2. Clean or replace nozzles
3. Purge air from system
4. Check glue specification

#### Carton Forming Failures
**Symptoms:** Cartons not opening correctly
**Causes:**
- Vacuum pressure low
- Worn gripper cups
- Carton blank quality
- Timing issue

**Solution:**
1. Check vacuum pump and lines
2. Replace gripper cups
3. Verify carton blanks meet spec
4. Adjust forming station timing

---

## Emergency Procedures

### Equipment Emergency Stop
1. Press nearest E-STOP button
2. Notify supervisor immediately
3. Do not reset until cause is identified
4. Document incident in safety log

### Power Failure Recovery
1. Wait for power restoration
2. Check all E-STOPs are reset
3. Verify equipment is in safe state
4. Follow normal startup sequence
5. Monitor closely for first hour of operation

### Fire or Smoke
1. Activate fire alarm
2. Press all E-STOPs in area
3. Evacuate immediately
4. Do not attempt to fight fire unless trained
5. Call emergency services

---

## Maintenance Contact Information

| Issue Type | Contact | Response Time |
|------------|---------|---------------|
| Electrical | Maintenance Ext. 2100 | 30 min |
| Mechanical | Maintenance Ext. 2101 | 30 min |
| Controls/PLC | Automation Ext. 2102 | 1 hour |
| Emergency | Security Ext. 9999 | Immediate |

## Documentation Requirements

After any troubleshooting activity:
1. Complete work order in CMMS
2. Update equipment maintenance log
3. Report recurring issues to engineering
4. Document any temporary fixes
