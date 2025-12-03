# Edge Operator Agent - Demo Script

This document provides example interactions demonstrating each capability of the Edge Operator Agent. Use these examples to explore the agent's features.

---

## Prerequisites

Before running the demo:

1. Start Ollama: `ollama serve`
2. Launch the app: `streamlit run streamlit_app.py`
3. Index the sample documents (upload from `documents/` folder via sidebar)

---

## 1. IoT Device Control

### List Available Devices

**User Input:**
```
What IoT devices are available in the system?
```

**Expected Response:**
```
Here are the available IoT devices:

Sensors:
- temp-sensor-001 (Temperature Sensor) - Location: Production Line A
  Range: -40°C to 85°C
- humidity-sensor-001 (Humidity Sensor) - Location: Warehouse B
  Range: 0% to 100% RH

Actuators:
- valve-actuator-001 (Valve Actuator) - Location: Cooling System
  States: OPEN, CLOSED, PARTIAL
  Current State: CLOSED
```

### Read Sensor Values

**User Input:**
```
What is the current temperature reading from the production line?
```

**Expected Response:**
```
Reading from temp-sensor-001 at Production Line A:
Temperature: 23.5°C
Timestamp: 2024-12-03T10:30:45Z

The reading is within normal operating range (-40°C to 85°C).
```

**User Input:**
```
Check the humidity level in the warehouse
```

**Expected Response:**
```
Reading from humidity-sensor-001 at Warehouse B:
Humidity: 45.2% RH
Timestamp: 2024-12-03T10:31:12Z

This is within the acceptable range for storage (30-70% RH).
```

### Control Actuators

**User Input:**
```
Open the cooling system valve
```

**Expected Response:**
```
Sending command to valve-actuator-001...

✓ Valve actuator successfully set to OPEN state.
Previous state: CLOSED
Location: Cooling System

The operation has been logged to the telemetry database.
```

**User Input:**
```
Set the valve to partial open position
```

**Expected Response:**
```
Sending command to valve-actuator-001...

✓ Valve actuator successfully set to PARTIAL state.
Previous state: OPEN
Location: Cooling System
```

### Error Handling Examples

**User Input:**
```
Read the pressure sensor
```

**Expected Response:**
```
Error: Device 'pressure-sensor' not found.

Available devices:
- temp-sensor-001 (sensor)
- humidity-sensor-001 (sensor)
- valve-actuator-001 (actuator)

Please specify one of the available devices.
```

**User Input:**
```
Set the temperature sensor to 25 degrees
```

**Expected Response:**
```
Error: Cannot control temp-sensor-001 - it is a sensor device, not an actuator.

Sensors can only be read, not controlled. Available actuators:
- valve-actuator-001 (states: OPEN, CLOSED, PARTIAL)
```

---

## 2. Structured Data Extraction (SCADA/MES)

### Extract Production Metrics

**User Input:**
```
Extract the production metrics from this SCADA report:

Production Line A - Shift Report
Date: December 3, 2024
Shift: Morning (06:00-14:00)

Production Summary:
- Units Produced: 1,247
- Target: 1,500 units
- Efficiency: 83.1%

Equipment Status:
1. Conveyor CB-2000
   - Status: Running
   - Speed: 1.8 m/s
   - Motor Temp: 72°C
   - Active Alarms: None

2. Packaging Unit PU-500
   - Status: Running
   - Speed: 45 cartons/min
   - Glue Temp: 165°C
   - Active Alarms: 
     * A002 - Glue tank low (Medium severity)
```

**Expected Response:**
```
Extracted Production Metrics:

{
  "line_id": "Production Line A",
  "shift": "Morning (06:00-14:00)",
  "units_produced": 1247,
  "units_target": 1500,
  "efficiency_percent": 83.1,
  "equipment": [
    {
      "equipment_id": "CB-2000",
      "name": "Conveyor",
      "status": "running",
      "readings": [
        {"sensor_id": "speed", "value": 1.8, "unit": "m/s"},
        {"sensor_id": "motor_temp", "value": 72.0, "unit": "°C"}
      ],
      "active_alarms": []
    },
    {
      "equipment_id": "PU-500",
      "name": "Packaging Unit",
      "status": "running",
      "readings": [
        {"sensor_id": "speed", "value": 45.0, "unit": "cartons/min"},
        {"sensor_id": "glue_temp", "value": 165.0, "unit": "°C"}
      ],
      "active_alarms": [
        {
          "alarm_id": "A002",
          "severity": "medium",
          "message": "Glue tank low",
          "acknowledged": false
        }
      ]
    }
  ]
}

Note: Production efficiency is at 83.1%, below the 100% target. 
The packaging unit has an active alarm for low glue tank level.
```

---

## 3. Document Search (RAG)

### Search Technical Documentation

**User Input:**
```
How do I troubleshoot belt tracking issues on the conveyor?
```

**Expected Response:**
```
Based on the Conveyor Belt System manual (CB-2000):

**Belt Tracking Off-Center**

Symptoms: Belt drifting to one side

Causes:
- Uneven load distribution
- Misaligned rollers
- Belt splice issue
- Worn belt edge

Solution:
1. Redistribute load evenly across belt width
2. Adjust tracking rollers (turn toward direction belt is moving)
3. Inspect belt splice for damage
4. Replace belt if edge is damaged

Source: conveyor_belt_manual.md
```

**User Input:**
```
What are the lockout tagout procedures?
```

**Expected Response:**
```
Based on the Safety Procedures Manual:

**Lockout/Tagout (LOTO) Procedure Steps**

Step 1: Preparation
- Identify all energy sources for the equipment
- Notify affected employees of the shutdown
- Gather required locks, tags, and blocking devices

Step 2: Shutdown
- Follow normal equipment shutdown procedure
- Operate stop controls to shut down equipment

Step 3: Isolation
- Locate all energy isolating devices
- Isolate from ALL energy sources (electrical, pneumatic, hydraulic, mechanical)

Step 4: Lockout/Tagout Application
- Apply personal lock to each energy isolating device
- Attach completed lockout tag with your name, date, and reason

Step 5: Stored Energy Release
- Release or restrain all stored energy
- Discharge capacitors, bleed lines, block elevated components

Step 6: Verification
- Verify all personnel are clear
- Attempt to start equipment (should not start)
- Return controls to OFF position

Source: safety_procedures.md
```

**User Input:**
```
What's the glue temperature for the packaging unit?
```

**Expected Response:**
```
Based on the Packaging Unit Manual (PU-500):

The glue system operates at **165°C** (±5°C tolerance).

Important notes:
- Wait for glue heater to reach temperature before starting production
- CAUTION: Hot surfaces present - wear heat-resistant gloves when servicing
- If glue temperature is incorrect, check:
  - Heater operation
  - Thermocouple connection
  - Temperature controller calibration

Related alarm: A003 - Glue temperature fault

Source: packaging_unit_manual.md
```

### Search with No Results

**User Input:**
```
How do I configure the robotic arm?
```

**Expected Response:**
```
I couldn't find specific documentation about robotic arm configuration in the indexed documents.

The available documentation covers:
- Conveyor Belt System (CB-2000)
- Packaging Unit (PU-500)
- Safety Procedures
- General Troubleshooting

Suggestions:
- Try searching for related terms like "actuator" or "automation"
- Upload the robotic arm manual to index it for search
- Check if the equipment has a different name in the system
```

---

## 4. Database Operations

### Log Telemetry Data

**User Input:**
```
Log a temperature reading of 24.5 degrees from the production line sensor
```

**Expected Response:**
```
Telemetry record logged successfully:

Device ID: temp-sensor-001
Metric Type: temperature
Value: 24.5
Unit: °C
Timestamp: 2024-12-03T10:45:23Z

Record ID: 127
```

### Query Telemetry Data

**User Input:**
```
Show me the last 5 temperature readings
```

**Expected Response:**
```
Recent temperature readings from temp-sensor-001:

| Timestamp           | Value  | Unit |
|---------------------|--------|------|
| 2024-12-03 10:45:23 | 24.5   | °C   |
| 2024-12-03 10:30:45 | 23.5   | °C   |
| 2024-12-03 10:15:12 | 23.8   | °C   |
| 2024-12-03 10:00:33 | 24.1   | °C   |
| 2024-12-03 09:45:18 | 23.2   | °C   |

Total records: 5
```

### Aggregation Queries

**User Input:**
```
What's the average temperature today?
```

**Expected Response:**
```
Temperature statistics for today (2024-12-03):

- Average: 23.8°C
- Minimum: 22.1°C
- Maximum: 25.3°C
- Reading Count: 48

Data source: temp-sensor-001 at Production Line A
```

**User Input:**
```
How many valve operations were performed this week?
```

**Expected Response:**
```
Valve operation statistics (last 7 days):

Total operations: 23
- OPEN commands: 12
- CLOSED commands: 8
- PARTIAL commands: 3

Device: valve-actuator-001 at Cooling System
```

---

## 5. Model Mode Switching

### Switch to Cloud Mode

1. In the sidebar, select "Cloud (Bedrock)" from the Model Mode radio buttons
2. If AWS credentials are configured and Bedrock is accessible:

**Expected Response:**
```
✅ Switched to Cloud mode (Claude on Amazon Bedrock)
```

3. If cloud is unavailable:

**Expected Response:**
```
❌ Cloud connectivity unavailable. Remaining in Local mode.
Please check your AWS credentials and Bedrock access.
```

### Verify Mode Change

**User Input:**
```
What model are you using?
```

**In Local Mode:**
```
I'm currently running on the local Ollama model (llama3.1) for offline operation.
All capabilities (IoT control, database, document search) are available locally.
```

**In Cloud Mode:**
```
I'm currently using Claude on Amazon Bedrock for inference.
Local capabilities (session persistence, database, document search) remain available.
```

---

## 6. Session Persistence

### Test Session Continuity

1. Have a conversation with the agent
2. Note the session ID in the sidebar (e.g., `edge-operator-001`)
3. Close and reopen the browser/app
4. The conversation history should be restored

**User Input:**
```
What did we discuss earlier about the conveyor belt?
```

**Expected Response:**
```
Earlier in our conversation, we discussed:
- Belt tracking troubleshooting procedures
- The CB-2000 conveyor specifications
- [Any other relevant context from the session]
```

---

## 7. Combined Workflows

### Equipment Diagnosis Workflow

**User Input:**
```
The packaging unit is having sealing problems. Can you help me diagnose it?
```

**Expected Response:**
```
I'll help you diagnose the packaging unit sealing issues. Let me check a few things:

1. **Current Equipment Status:**
   [Checks sensors if available]

2. **From the PU-500 Manual - Sealing Issues:**

   **Problem: Weak seal or carton opening**
   Possible causes:
   - Glue temperature incorrect (should be 165°C ± 5°C)
   - Glue nozzle blockage
   - Insufficient sealing pressure
   - Compression roller misalignment

   **Problem: Glue stringing or dripping**
   Possible causes:
   - Glue temperature too high
   - Nozzle air assist pressure incorrect
   - Dirty nozzle tips
   - Wrong glue viscosity

3. **Recommended Actions:**
   - Check glue temperature on HMI (target: 165°C)
   - Inspect and clean glue nozzles
   - Verify sealing pressure settings
   - Check compression roller alignment

Would you like me to log this diagnostic session or search for more specific information?
```

### Shift Handover Report

**User Input:**
```
Generate a shift handover summary including current sensor readings and any recent alarms
```

**Expected Response:**
```
**Shift Handover Report**
Generated: 2024-12-03 14:00:00

**Current Sensor Readings:**
- Temperature (Production Line A): 24.2°C ✓ Normal
- Humidity (Warehouse B): 48.5% RH ✓ Normal

**Actuator Status:**
- Cooling Valve: OPEN

**Recent Telemetry Summary (Last 8 hours):**
- Temperature: Avg 23.8°C, Min 22.1°C, Max 25.3°C
- Humidity: Avg 46.2%, Min 42.0%, Max 51.0%

**Active Alarms:** None

**Operations Performed:**
- 12 sensor readings logged
- 3 valve state changes

**Notes:**
- All equipment operating within normal parameters
- No maintenance issues reported

Session ID: edge-operator-001
```

---

## Tips for Demo

1. **Index Documents First**: Upload the sample documents from `documents/` folder before testing document search features

2. **Generate Telemetry Data**: Perform several sensor reads and actuator controls to populate the database before testing queries

3. **Test Offline**: Disconnect from the internet to verify full offline operation in Local mode

4. **Session Persistence**: Close and reopen the app to demonstrate conversation continuity

5. **Error Handling**: Try invalid device names or actions to show graceful error handling
