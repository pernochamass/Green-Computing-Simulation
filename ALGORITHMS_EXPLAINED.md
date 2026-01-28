# ALGORITHM EXPLANATIONS - Step by Step
## For Team Understanding and Presentation

---

## 🎯 ALGORITHM 1: CPU P-STATE MANAGEMENT

### What is it?
P-States (Performance States) control the CPU's voltage and frequency to balance power and performance.

### Simple Analogy
Think of your car:
- **P0** = Full throttle on highway (fast but uses lots of fuel)
- **P1** = Normal city driving (balanced)
- **P2** = Eco mode (slower but fuel efficient)
- **P3** = Idle at traffic light (minimal fuel)

### The Algorithm (Decision Tree)

```
START
  ↓
Read CPU Utilization (%)
  ↓
┌─────────────────────────────────┐
│ Is utilization < 10%?           │
│ YES → Go to ALGORITHM 2 (Sleep) │
│ NO → Continue                   │
└─────────────────────────────────┘
  ↓
┌─────────────────────────┐
│ Is utilization < 20%?   │
│ YES → Select P3 (10W)   │
│ NO → Continue           │
└─────────────────────────┘
  ↓
┌─────────────────────────┐
│ Is utilization < 50%?   │
│ YES → Select P2 (25W)   │
│ NO → Continue           │
└─────────────────────────┘
  ↓
┌─────────────────────────┐
│ Is utilization < 75%?   │
│ YES → Select P1 (45W)   │
│ NO → Select P0 (65W)    │
└─────────────────────────┘
  ↓
Apply selected P-State
  ↓
Log decision
  ↓
END
```

### Code Walkthrough

```python
# Step 1: Get current CPU workload (0-100%)
cpu_util = psutil.cpu_percent(interval=0.5)

# Step 2: Decision tree
if cpu_util < 10:
    # Very low activity - enter sleep mode instead
    new_cpu_state = 'C1'
    cpu_power = 5  # watts
    
elif cpu_util < 20:
    # Light tasks (web browsing, text editing)
    new_cpu_state = 'P3'
    cpu_power = 10  # watts
    
elif cpu_util < 50:
    # Moderate work (multiple apps open)
    new_cpu_state = 'P2'
    cpu_power = 25  # watts
    
elif cpu_util < 75:
    # Heavy work (video editing, gaming)
    new_cpu_state = 'P1'
    cpu_power = 45  # watts
    
else:
    # Maximum load (rendering, compiling)
    new_cpu_state = 'P0'
    cpu_power = 65  # watts

# Step 3: Apply the state
components['cpu']['state'] = new_cpu_state
components['cpu']['power'] = cpu_power
```

### Why These Thresholds?

| Threshold | Rationale |
|-----------|-----------|
| 10% | Below this = CPU mostly idle, sleep is better |
| 20% | Single light application active |
| 50% | Multiple applications, moderate multitasking |
| 75% | Heavy workload, need high performance |
| >75% | Maximum performance required |

### Power Savings Example

```
Scenario: Student typing a document
- CPU utilization: 15%
- Traditional system: P0 (65W)
- Our system: P3 (10W)
- Savings: 55W

If typing for 2 hours:
- Energy saved = 55W × 2h = 110 Wh
- Cost saved = 110 Wh × $0.15/kWh = $0.0165
- Monthly (40 hrs) = $0.33
- Semester (4 months) = $1.32
```

---

## 😴 ALGORITHM 2: CPU C-STATE MANAGEMENT (Sleep States)

### What is it?
C-States put the CPU to sleep when it's not actively processing tasks.

### Simple Analogy
Like closing your laptop:
- **C0** = Laptop open and active
- **C1** = Screen off but laptop on (instant wake)
- **C3** = Laptop sleeping (takes a moment to wake)

### The Algorithm

```
START
  ↓
Check CPU Utilization
  ↓
┌──────────────────────────┐
│ Is utilization < 10%?    │
│ YES → CPU is mostly idle │
│ NO → Stay in C0 (Active) │
└──────────────────────────┘
  ↓
┌──────────────────────────┐
│ Enter C1 (Light Sleep)   │
│ - Stop CPU clock         │
│ - Maintain full state    │
│ - Power: 5W              │
│ - Wake time: <1ms        │
└──────────────────────────┘
  ↓
Log: "CPU entering light sleep"
  ↓
Wait for activity increase
  ↓
┌──────────────────────────┐
│ Utilization > 10%?       │
│ YES → Wake up to P-state │
└──────────────────────────┘
  ↓
END
```

### Code Example

```python
if cpu_util < 10:
    # CPU is idle - enter sleep mode
    new_cpu_state = 'C1'
    cpu_power = CPU_C_STATES['C1']['power']  # 5W
    
    # Log for user transparency
    add_log('CPU entering light sleep (C1) - Low utilization', 'success')
```

### Advanced: C3 Deep Sleep
For even longer idle periods (not implemented in basic version):

```python
if idle_time > 60 seconds:
    state = 'C3'  # Deep sleep
    power = 1W    # Maximum savings
    wakeup_time = 10ms  # Slightly slower wake
```

---

## 💾 ALGORITHM 3: DISK SPIN-DOWN MANAGEMENT

### What is it?
Hard drives have spinning platters. We stop them spinning when not in use.

### Simple Analogy
Like a ceiling fan:
- **Active** = Fan spinning (uses electricity, creates noise)
- **Standby** = Fan off (silent, no power)
- But turning it on/off too frequently wears it out!

### The Algorithm

```
START
  ↓
Track last disk access time
  ↓
Calculate: time_idle = current_time - last_access
  ↓
┌─────────────────────────────────────────┐
│ Is time_idle > 20 seconds?              │
│ AND disk is currently spinning?         │
│ YES → Spin down disk                    │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ Spin-down sequence:                     │
│ 1. Finish pending operations           │
│ 2. Write buffers to disk               │
│ 3. Stop motor                           │
│ 4. Power: 7W → 2W (saves 5W)           │
└─────────────────────────────────────────┘
  ↓
WAIT and monitor CPU activity
  ↓
┌─────────────────────────────────────────┐
│ Is CPU utilization > 40%?               │
│ AND disk is in standby?                 │
│ YES → Preemptive spin-up                │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ Spin-up sequence:                       │
│ 1. Start motor (takes ~3 seconds)      │
│ 2. Wait for platters to reach speed    │
│ 3. Power: 2W → 7W                       │
│ 4. Update last_access time              │
└─────────────────────────────────────────┘
  ↓
END
```

### Code Implementation

```python
# Calculate time since last disk activity
current_time = time.time() - start_time
time_since_access = current_time - disk['lastAccess']

# Check if we should spin down
if time_since_access > 20 and disk['state'] == 'Active':
    # Disk has been idle for >20 seconds
    disk['state'] = 'Standby'
    disk['power'] = 2  # watts
    add_log('Disk entering standby - No activity detected', 'success')

# Check if we should spin up preemptively
elif cpu_util > 40 and disk['state'] == 'Standby':
    # CPU active = user working = likely to need disk soon
    disk['state'] = 'Active'
    disk['power'] = 7  # watts
    disk['lastAccess'] = current_time
    add_log('Disk spinning up - Activity detected', 'warning')
```

### Why 20 Seconds?

```
Too short (5s):
- Disk spins down while user is thinking
- Spins up immediately when they continue
- Wastes energy on spin-up/down cycles
- Wears out disk motor

Too long (60s):
- Miss energy saving opportunities
- User already moved to next task

20 seconds:
- Good balance
- If user idle >20s, likely doing something else
- Enough time to justify spin-down energy cost
```

### Energy Analysis

```
Scenario: Student reading a PDF for 5 minutes
- No disk access during reading
- Disk spins down after 20s
- Standby for 4 min 40s = 280 seconds

Energy saved:
- Active power: 7W
- Standby power: 2W
- Savings per second: 5W
- Total saved: 5W × 280s = 1400 Ws = 0.39 Wh
```

---

## 🖥️ ALGORITHM 4: DISPLAY ADAPTIVE BRIGHTNESS

### What is it?
Reduces screen brightness when user appears idle or inactive.

### Simple Analogy
Like auto-dimming in a car:
- Bright lights when actively driving
- Dimmer lights when stopped at light
- But not so dim you can't see!

### The Algorithm

```
START
  ↓
Monitor CPU utilization (user activity indicator)
  ↓
┌────────────────────────────────────────┐
│ Is CPU util < 15%?                     │
│ (Suggests user idle/away)              │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ Is current brightness > 50%?           │
│ YES → Reduce to 50%                    │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ Brightness reduction:                  │
│ - Old: 100% brightness = 25W           │
│ - New: 50% brightness = 12W            │
│ - Savings: 13W                         │
└────────────────────────────────────────┘
  ↓
Log: "Display brightness reduced to 50%"
  ↓
MONITOR for activity increase
  ↓
┌────────────────────────────────────────┐
│ Is CPU util > 50%?                     │
│ (User actively working)                │
│ YES → Restore brightness               │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ Brightness restoration:                │
│ - Restore: 50% → 100%                  │
│ - Power: 12W → 25W                     │
└────────────────────────────────────────┘
  ↓
Log: "Display brightness restored to 100%"
  ↓
END
```

### Code Implementation

```python
# Check if user appears idle (low CPU = not working)
if cpu_util < 15 and display['brightness'] > 50:
    # User likely idle or away from desk
    display['brightness'] = 50    # Reduce to 50%
    display['power'] = 12          # Watts
    add_log('Display brightness reduced to 50% - Low activity', 'success')

# Check if user has returned (high CPU = working)
elif cpu_util > 50 and display['brightness'] < 100:
    # User actively working - restore full brightness
    display['brightness'] = 100
    display['power'] = 25          # Watts
    add_log('Display brightness restored to 100%', 'info')
```

### Why These Thresholds?

| Threshold | Reasoning |
|-----------|-----------|
| <15% CPU | User likely reading or idle, not actively typing/clicking |
| 50% brightness | Dim enough to save power, bright enough to see if they glance back |
| >50% CPU | Clear indication user has returned to work |

### Power Savings

```
Display Power Consumption:
- 100% brightness: ~25W
- 75% brightness: ~18W
- 50% brightness: ~12W
- 25% brightness: ~7W

Our choice (50%):
- Saves 13W vs full brightness
- Still readable for quick glances
- Quick return to 100% when needed

Example:
Student steps away for 10 minutes
- Savings: 13W × 10min = 130 W-minutes = 2.17 Wh
- Daily (1 hour away): 13 Wh
- Monthly: ~390 Wh
```

---

## 🌐 ALGORITHM 5: NETWORK POWER MANAGEMENT

### What is it?
Modern network cards can operate in reduced power mode while maintaining connectivity.

### Simple Analogy
Like your phone's WiFi:
- **Active Mode** = Constantly scanning and maintaining full speed
- **Low Power Mode** = Periodic checks, slower but connected

### The Algorithm

```
START
  ↓
Monitor CPU utilization (network activity proxy)
  ↓
┌────────────────────────────────────────┐
│ Is CPU util < 20%?                     │
│ (Low activity = probably low network)  │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ Is network in Active mode?             │
│ YES → Switch to Low Power              │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ Low Power Mode:                        │
│ - Reduce polling frequency             │
│ - Lower power state                    │
│ - Still maintains connection           │
│ - Power: 3W → 1W (saves 2W)            │
└────────────────────────────────────────┘
  ↓
WAIT and monitor
  ↓
┌────────────────────────────────────────┐
│ Is CPU util > 40%?                     │
│ (Activity increase)                    │
│ YES → Restore to Active                │
└────────────────────────────────────────┘
  ↓
END
```

### Code Implementation

```python
# Check if we can reduce network power
if cpu_util < 20 and network['state'] == 'Active':
    # Low system activity = likely low network use
    network['state'] = 'Low Power'
    network['power'] = 1  # watts
    add_log('Network adapter entering low power mode', 'success')

# Check if we need full network power
elif cpu_util > 40 and network['state'] == 'Low Power':
    # System active = restore full network capability
    network['state'] = 'Active'
    network['power'] = 3  # watts
    add_log('Network adapter restored to active', 'info')
```

---

## 📊 ALGORITHM 6: ENERGY TRACKING & EFFICIENCY CALCULATION

### What is it?
Calculates how much energy we're using vs. how much we're saving.

### Formulas

```
Power (Watts) = Energy per second
Energy (Watt-hours) = Power (W) × Time (hours)

Example:
- Power: 50W
- Time: 2 hours
- Energy: 50W × 2h = 100 Wh
```

### The Algorithm

```
EVERY SECOND:
  ↓
Step 1: Get current total power
  ↓
current_power = sum of all component powers
  ↓
Step 2: Calculate energy used this second
  ↓
energy_increment = current_power / 3600
(Divide by 3600 to convert seconds to hours)
  ↓
Step 3: Add to cumulative total
  ↓
total_energy += energy_increment
  ↓
Step 4: Calculate what maximum system would use
  ↓
max_power = 108W  (all components at maximum)
  ↓
Step 5: Calculate savings
  ↓
energy_saved_increment = (max_power - current_power) / 3600
  ↓
energy_saved += energy_saved_increment
  ↓
Step 6: Calculate efficiency percentage
  ↓
efficiency = (energy_saved / (total_energy + energy_saved)) × 100%
  ↓
END (repeat next second)
```

### Code Implementation

```python
def update_energy_tracking():
    # Step 1: Current power consumption
    current_power = sum(comp['power'] for comp in components.values())
    
    # Step 2: Energy used in this 1-second interval
    energy_increment = current_power / 3600  # Convert to Wh
    total_energy += energy_increment
    
    # Step 3: Savings vs maximum power
    max_power = 108  # watts (all components at max)
    energy_saved_increment = (max_power - current_power) / 3600
    energy_saved += max(0, energy_saved_increment)
    
    # Step 4: Calculate efficiency
    if total_energy + energy_saved > 0:
        efficiency = (energy_saved / (total_energy + energy_saved)) * 100
```

### Example Calculation

```
Scenario: System runs for 10 minutes (600 seconds)
Average power: 45W

Total Energy Used:
= 45W × 600s / 3600
= 7.5 Wh

Maximum Possible Energy:
= 108W × 600s / 3600
= 18 Wh

Energy Saved:
= 18 Wh - 7.5 Wh
= 10.5 Wh

Efficiency:
= (10.5 / 18) × 100%
= 58.3%

This means we saved 58.3% compared to running at maximum power!
```

---

## 🔄 PUTTING IT ALL TOGETHER: THE MAIN LOOP

### How All Algorithms Work Together

```
BACKGROUND THREAD (Runs every 1 second):
  ↓
┌────────────────────────────────────────┐
│ 1. Read Real System Data               │
│    - CPU utilization (psutil)          │
│    - Current time                      │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ 2. Run Adaptive Power Management       │
│    ├→ CPU P-State Selection            │
│    ├→ CPU C-State Check                │
│    ├→ Disk Spin-down Logic             │
│    ├→ Display Brightness Adjustment    │
│    └→ Network Power Mode               │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ 3. Update Component States             │
│    - Apply new power values            │
│    - Update temperatures               │
│    - Track access times                │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ 4. Calculate Energy Metrics            │
│    - Total power consumption           │
│    - Energy used                       │
│    - Energy saved                      │
│    - Efficiency percentage             │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ 5. Log Important Events                │
│    - State changes                     │
│    - Power savings                     │
│    - User-facing messages              │
└────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────┐
│ 6. Send Data to Web Interface          │
│    - Update component cards            │
│    - Update power graph                │
│    - Update activity log               │
└────────────────────────────────────────┘
  ↓
Wait 1 second
  ↓
REPEAT
```

---

## 🎯 KEY LEARNING POINTS

### For Understanding:
1. **Threshold-based decisions** are simple but effective
2. **Monitoring loops** enable real-time adaptation
3. **Trade-offs** exist between power and performance
4. **Preemptive wake-up** prevents user-noticeable delays
5. **Logging** provides transparency and debugging

### For Presentation:
1. Start with the problem (wasted energy)
2. Explain one algorithm at a time with analogies
3. Show real results (power graphs, savings)
4. Demonstrate live with the interface
5. Calculate real cost savings (makes it tangible)

---

## 📈 EXPECTED RESULTS

### Typical Performance:

| Scenario | Without Management | With Management | Savings |
|----------|-------------------|-----------------|---------|
| Idle (0-10% CPU) | 108W | 25-30W | ~75W (69%) |
| Light (10-30% CPU) | 108W | 35-45W | ~65W (60%) |
| Medium (30-60% CPU) | 108W | 50-70W | ~45W (42%) |
| Heavy (60-100% CPU) | 108W | 85-108W | ~10W (9%) |

### Real-World Impact:

```
Student laptop usage (8 hours/day):
- Without management: 108W × 8h = 864 Wh/day
- With management: 55W × 8h = 440 Wh/day
- Daily savings: 424 Wh
- Monthly savings: ~12.7 kWh
- Semester savings: ~51 kWh
- Cost savings (at $0.15/kWh): $7.65/semester
```

---

**This completes the algorithm explanations! You now understand every decision the system makes and can explain it clearly to others.**
