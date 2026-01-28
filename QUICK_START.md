# QUICK START GUIDE - Green Computing Power Manager
## Group 40

---

## 🚀 5-MINUTE SETUP

### Method 1: Using the Start Script (Easiest)
```
1. Double-click: start.bat
2. Wait for "Server starting on http://localhost:5000"
3. Open: index_integrated.html in your browser
4. Click "Start Monitoring"
```

### Method 2: Manual Steps
```
1. Open Command Prompt in this folder
2. Type: pip install -r requirements.txt
3. Type: python power_backend.py
4. Open index_integrated.html in browser
5. Click "Start Monitoring"
```

---

## ❓ TROUBLESHOOTING

### Problem: "Backend Disconnected" message
**Solution:** 
- Make sure power_backend.py is running
- Check terminal shows "Running on http://localhost:5000"
- Refresh browser page

### Problem: "pip is not recognized"
**Solution:**
- Install Python from https://www.python.org/
- During installation, check "Add Python to PATH"
- Restart Command Prompt

### Problem: Port 5000 already in use
**Solution:**
- Close other programs using port 5000
- Or edit power_backend.py line 381: change `port=5000` to `port=5001`
- And edit index_integrated.html line 138: change `localhost:5000` to `localhost:5001`

---

## 📊 WHAT TO EXPECT

### When Running Correctly:
✅ Terminal shows: "Server starting on http://localhost:5000"  
✅ Browser shows: "● Backend Connected" (green)  
✅ CPU utilization updates every second  
✅ Power consumption graph fills up  
✅ Activity log shows power state changes  

### Example Session:
```
0s:  Start monitoring
5s:  CPU at 45% → P1 state (45W)
10s: CPU drops to 8% → C1 sleep (5W)
15s: Disk enters standby (7W → 2W)
20s: Display dims to 50% (25W → 12W)
Total saved: 0.15 Wh
```

---

## 🎯 DEMO SCENARIOS

### Scenario 1: Show Energy Savings
```
1. Start with empty system (close programs)
2. Show power at ~20-30W (sleep states active)
3. Open several programs
4. Show power spike to ~80-100W
5. Close programs
6. Watch adaptive algorithm reduce power
7. Generate report to show savings
```

### Scenario 2: Component Control
```
1. Watch CPU state in Component Status
2. Create load (open tabs, run programs)
3. Observe state changes: P3 → P2 → P1 → P0
4. Stop load
5. Watch reverse: P0 → P1 → P2 → C1
6. Point out power reduction in each step
```

### Scenario 3: Long-term Savings
```
1. Run for 10 minutes
2. Generate Report
3. Show efficiency percentage
4. Calculate: "If this ran 8 hours/day..."
   - Daily savings × electricity rate = cost savings
   - Monthly savings = Daily × 30
   - Semester savings = Monthly × 4
```

---

## 📈 KEY METRICS TO HIGHLIGHT

| Metric | Meaning | Good Value |
|--------|---------|------------|
| Current Power | Real-time consumption | <50W when idle |
| Total Energy | Cumulative usage | Depends on runtime |
| Energy Saved | Savings vs max power | Should increase |
| Efficiency | Percentage saved | >30% |

---

## 🎓 PRESENTATION TALKING POINTS

### Introduction (2 min)
- Problem: Computers waste energy when power is not managed
- Impact: High electricity costs, environmental waste
- Solution: OS-level adaptive power management

### Algorithms (5 min)
- **P-States:** Explain voltage/frequency scaling (show diagram)
- **C-States:** Explain sleep modes (show power drop)
- **Adaptive:** Explain threshold-based decisions (show code logic)
- **Device Management:** Disk, display, network optimization

### Demo (5 min)
- Show real-time monitoring
- Create workload and show adaptation
- Generate report and explain savings

### Results (3 min)
- Energy saved: XX Wh in YY minutes
- Efficiency: ZZ%
- Cost savings: Calculate based on local rates
- Environmental impact: kWh saved = CO₂ reduced

### Conclusion (1 min)
- All objectives achieved
- Practical solution for students
- Scalable to larger systems

---

## 💻 SYSTEM REQUIREMENTS

**Minimum:**
- Windows 10 or later (macOS/Linux compatible)
- Python 3.8 or later
- 2GB RAM
- Modern web browser (Chrome, Firefox, Edge)
- Internet connection (for CDN libraries)

**Recommended:**
- Python 3.10+
- 4GB RAM
- Dual-core processor
- Multiple programs to create realistic workload

---

## 📝 TESTING CHECKLIST

Before presentation, verify:
- [ ] Backend starts without errors
- [ ] HTML shows "Backend Connected"
- [ ] CPU utilization updates in real-time
- [ ] Power graph displays data
- [ ] Activity log shows messages
- [ ] All buttons work (Start, Reset, Report)
- [ ] Component cards update correctly
- [ ] Energy metrics calculate properly

---

## 🏆 GRADING CRITERIA ALIGNMENT

| Criterion | Implementation |
|-----------|----------------|
| CPU Power Management | ✅ P-States + C-States |
| Device Optimization | ✅ Disk, Display, Network |
| Adaptive Algorithms | ✅ Threshold-based decision tree |
| Energy Tracking | ✅ Real-time monitoring + reporting |
| Workload Balancing | ✅ Performance vs efficiency trade-off |
| User Interface | ✅ Web-based real-time dashboard |
| Documentation | ✅ README + code comments |

---

## 📞 SUPPORT

**If something isn't working:**
1. Check README.md for detailed instructions
2. Read troubleshooting section above
3. Check power_backend.py comments
4. Review Python error messages in terminal

**Common Issues:**
- Port conflicts → Change port number
- Import errors → Run `pip install -r requirements.txt`
- Browser errors → Enable JavaScript, use modern browser
- No data → Make sure backend is running

---

## ✨ FINAL CHECKLIST FOR SUBMISSION

- [ ] All code files present
- [ ] README.md completed
- [ ] Requirements.txt included
- [ ] Code properly commented
- [ ] Project runs successfully
- [ ] Demo prepared
- [ ] Report generated
- [ ] Group members listed
- [ ] Documentation complete

---

**Good luck with your presentation! 🎉**

*Remember: This project solves a REAL problem. Energy efficiency matters for students, the environment, and the future of computing!*
