from flask import Flask, jsonify
import random
import math
from datetime import datetime, timedelta

app = Flask(__name__)

def get_time_factor():
    now = datetime.now()
    hour = now.hour + now.minute / 60
    solar_factor = max(0, math.sin(math.pi * (hour - 6) / 12)) if 6 <= hour <= 18 else 0
    usage_factor = 0.4 + 0.6 * (
        math.exp(-0.5 * ((hour - 8) ** 2) / 2) +
        math.exp(-0.5 * ((hour - 19) ** 2) / 2)
    )
    return solar_factor, min(usage_factor, 1.0)

def generate_data():
    solar_f, usage_f = get_time_factor()
    now = datetime.now()

    base_energy = 3.0 + 5.0 * usage_f + random.uniform(-0.3, 0.3)
    solar = round((4.8 * solar_f + random.uniform(-0.2, 0.2)), 2)
    battery = random.randint(60, 95)
    grid = round(max(0, base_energy - solar), 2)
    total_energy = round(base_energy, 2)

    living = round(0.8 + 1.2 * usage_f + random.uniform(-0.1, 0.2), 2)
    kitchen = round(0.4 + 2.0 * usage_f + random.uniform(-0.2, 0.3), 2)
    bedroom1 = round(0.3 + 0.9 * usage_f + random.uniform(-0.1, 0.1), 2)
    bedroom2 = round(0.2 + 0.6 * usage_f + random.uniform(-0.05, 0.1), 2)
    bathroom = round(0.1 + 0.4 * random.random(), 2)
    garage = round(0.1 + 0.8 * random.random(), 2)

    appliances = {
        "AC": round(1200 + random.randint(-100, 200), 0),
        "Refrigerator": round(150 + random.randint(-20, 20), 0),
        "Washing Machine": round(random.choice([0, 0, 0, 800, 1200]), 0),
        "TV": round(random.choice([0, 120, 120, 150]), 0),
        "Water Heater": round(random.choice([0, 0, 2000, 2000]), 0),
        "Fans": round(75 * random.randint(2, 5), 0),
        "Lights": round(40 * random.randint(3, 8), 0),
        "Router": 15,
    }

    temp_in = round(23 + 5 * usage_f + random.uniform(-0.5, 0.5), 1)
    temp_out = round(28 + random.uniform(-2, 2), 1)
    humidity = round(55 + 20 * random.random(), 1)
    aqi = round(random.choice([35, 42, 55, 68, 80]) + random.uniform(-5, 10), 0)
    co2 = round(400 + random.randint(0, 300), 0)
    noise = round(30 + random.uniform(0, 25), 1)
    uv_index = round(random.uniform(0, 11), 1)
    wind_speed = round(random.uniform(5, 30), 1)
    pressure = round(1013 + random.uniform(-5, 5), 1)

    tank_level = random.randint(55, 90)
    daily_water = round(120 + random.uniform(-30, 80), 1)
    motor_status = random.choice(["Running", "Idle", "Idle", "Idle"])
    water_quality = random.choice(["Excellent", "Good", "Good"])
    hot_water_temp = round(55 + random.uniform(-5, 10), 1)
    filter_life = random.randint(60, 95)

    cams = [
        {"id": "CAM-01", "location": "Front Door", "status": random.choice(["Active", "Active", "Motion"]), "resolution": "4K"},
        {"id": "CAM-02", "location": "Back Yard", "status": random.choice(["Active", "Active", "Idle"]), "resolution": "1080p"},
        {"id": "CAM-03", "location": "Garage", "status": random.choice(["Active", "Idle"]), "resolution": "1080p"},
        {"id": "CAM-04", "location": "Living Room", "status": "Active", "resolution": "4K"},
    ]
    doors = {
        "Front Door": random.choice(["Locked", "Locked", "Locked", "Unlocked"]),
        "Back Door": random.choice(["Locked", "Locked", "Unlocked"]),
        "Garage": random.choice(["Closed", "Closed", "Open"]),
        "Main Gate": random.choice(["Locked", "Locked", "Locked"]),
    }
    fire = random.choice(["Clear", "Clear", "Clear", "Alert"])
    gas = random.choice(["Normal", "Normal", "Normal", "Warning"])
    smoke = random.choice(["Clear", "Clear", "Clear", "Clear"])
    motion_zones = random.choices(
        ["Living Room", "Kitchen", "Front Yard", "Garage", "Bedroom"],
        k=random.randint(0, 2)
    )
    visitors_today = random.randint(2, 8)
    last_event = random.choice(["Motion at Front Door", "Door unlocked", "Package delivered", "All clear"])

    solar_panels = [
        {"id": f"Panel-{i+1}", "output": round(solar / 6 + random.uniform(-0.1, 0.1), 2), "efficiency": round(85 + random.uniform(-5, 5), 1), "temp": round(45 + random.uniform(-5, 10), 1)}
        for i in range(6)
    ]
    battery_health = round(92 + random.uniform(-3, 2), 1)
    battery_temp = round(28 + random.uniform(-2, 4), 1)
    battery_cycles = random.randint(120, 180)
    inverter = random.choice(["Online", "Online", "Online", "Standby"])
    grid_export = round(max(0, solar - base_energy * 0.5 + random.uniform(-0.5, 0.5)), 2)
    lifetime_solar = round(random.uniform(1200, 1500), 1)
    co2_saved = round(lifetime_solar * 0.82, 1)
    savings_month = round(grid_export * 8.5 * 30, 2)

    cost_today = round(base_energy * 8.5 * (now.hour + 1) / 24, 2)
    cost_month = round(cost_today * 28 + random.uniform(-50, 100), 2)
    cost_yesterday = round(cost_today * random.uniform(0.85, 1.15), 2)
    peak_demand = round(base_energy * 1.3, 2)

    insights = []
    if kitchen > 2.5:
        insights.append({"type": "warning", "msg": "Kitchen power unusually high — check appliances", "action": "View Appliances"})
    if battery < 65:
        insights.append({"type": "alert", "msg": "Battery below 65% — solar may not charge fully tonight", "action": "View Solar"})
    if aqi > 70:
        insights.append({"type": "alert", "msg": "Air quality degrading — consider closing windows", "action": "View Environment"})
    if solar_f > 0.7:
        insights.append({"type": "info", "msg": "Peak solar hours — ideal time to run heavy appliances", "action": "View Solar"})
    if not insights:
        insights.append({"type": "info", "msg": "All systems normal — home running efficiently", "action": "View Overview"})

    hourly = []
    for i in range(24):
        h = i
        sf = max(0, math.sin(math.pi * (h - 6) / 12)) if 6 <= h <= 18 else 0
        uf = 0.4 + 0.6 * (
            math.exp(-0.5 * ((h - 8) ** 2) / 2) +
            math.exp(-0.5 * ((h - 19) ** 2) / 2)
        )
        hourly.append({
            "hour": f"{h:02d}:00",
            "energy": round(3.0 + 5.0 * min(uf, 1.0) + random.uniform(-0.2, 0.2), 2),
            "solar": round(4.8 * sf + random.uniform(-0.1, 0.1), 2),
            "cost": round((3.0 + 5.0 * min(uf, 1.0)) * 8.5, 2),
        })

    weekly = []
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    for i, day in enumerate(days):
        weekly.append({
            "day": day,
            "energy": round(40 + random.uniform(-8, 12), 1),
            "solar": round(18 + random.uniform(-4, 6), 1),
            "cost": round(340 + random.uniform(-50, 80), 0),
            "water": round(130 + random.uniform(-20, 40), 1),
        })

    # Automation rules
    automations = [
        {"name": "Morning Routine", "trigger": "06:30 AM", "action": "Turn on lights + AC", "status": "Active", "last_run": "Today 06:30"},
        {"name": "Leave Home", "trigger": "Motion off 15min", "action": "Lock doors + AC off", "status": "Active", "last_run": "Today 09:15"},
        {"name": "Solar Peak", "trigger": "Solar > 3kW", "action": "Run washing machine", "status": "Active", "last_run": "Today 12:00"},
        {"name": "Night Mode", "trigger": "10:00 PM", "action": "Dim lights + Security on", "status": "Active", "last_run": "Yesterday"},
        {"name": "Rain Mode", "trigger": "Humidity > 85%", "action": "Close windows alert", "status": "Paused", "last_run": "3 days ago"},
    ]

    # Energy tariff
    current_hour = now.hour
    tariff_zone = "Peak" if (9 <= current_hour <= 12 or 18 <= current_hour <= 21) else "Off-Peak" if (0 <= current_hour <= 6) else "Standard"
    tariff_rate = 12.5 if tariff_zone == "Peak" else 5.0 if tariff_zone == "Off-Peak" else 8.5

    return {
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%d %b %Y"),
        "day": now.strftime("%A"),

        "total_energy": total_energy,
        "solar": solar,
        "battery": battery,
        "grid": grid,
        "voltage": round(220 + random.uniform(-5, 5), 1),
        "frequency": round(50 + random.uniform(-0.1, 0.1), 2),
        "power_factor": round(0.92 + random.uniform(-0.05, 0.05), 2),
        "devices_online": random.randint(14, 22),
        "cost_today": cost_today,
        "cost_month": cost_month,
        "cost_yesterday": cost_yesterday,
        "peak_demand": peak_demand,
        "tariff_zone": tariff_zone,
        "tariff_rate": tariff_rate,

        "rooms": {
            "Living Room": living,
            "Kitchen": kitchen,
            "Bedroom 1": bedroom1,
            "Bedroom 2": bedroom2,
            "Bathroom": bathroom,
            "Garage": garage,
        },

        "appliances": appliances,

        "temp_in": temp_in,
        "temp_out": temp_out,
        "humidity": humidity,
        "aqi": int(aqi),
        "co2": co2,
        "noise": noise,
        "uv_index": uv_index,
        "wind_speed": wind_speed,
        "pressure": pressure,

        "tank_level": tank_level,
        "daily_water": daily_water,
        "motor_status": motor_status,
        "water_quality": water_quality,
        "hot_water_temp": hot_water_temp,
        "filter_life": filter_life,

        "cameras": cams,
        "doors": doors,
        "fire": fire,
        "gas": gas,
        "smoke": smoke,
        "motion_zones": motion_zones,
        "visitors_today": visitors_today,
        "last_event": last_event,

        "solar_panels": solar_panels,
        "battery_health": battery_health,
        "battery_temp": battery_temp,
        "battery_cycles": battery_cycles,
        "inverter": inverter,
        "grid_export": grid_export,
        "lifetime_solar": lifetime_solar,
        "co2_saved": co2_saved,
        "savings_month": savings_month,

        "insights": insights,
        "hourly": hourly,
        "weekly": weekly,
        "automations": automations,
    }


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NexaHome — Smart Home Command Centre</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,400&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {
  --white: #ffffff;
  --bg: #f4f5f7;
  --bg2: #eceef2;
  --surface: #ffffff;
  --surface2: #f9fafb;
  --border: #e2e5ea;
  --border2: #edf0f4;

  --ink: #111827;
  --ink2: #374151;
  --ink3: #6b7280;
  --ink4: #9ca3af;

  --blue: #2563eb;
  --blue-light: #eff6ff;
  --blue-mid: #bfdbfe;
  --green: #16a34a;
  --green-light: #f0fdf4;
  --green-mid: #bbf7d0;
  --amber: #d97706;
  --amber-light: #fffbeb;
  --amber-mid: #fde68a;
  --red: #dc2626;
  --red-light: #fef2f2;
  --red-mid: #fecaca;
  --purple: #7c3aed;
  --purple-light: #f5f3ff;
  --teal: #0d9488;
  --teal-light: #f0fdfa;
  --orange: #ea580c;
  --orange-light: #fff7ed;

  --sidebar-w: 220px;
  --topbar-h: 60px;
  --radius: 12px;
  --radius-sm: 8px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.04);
  --shadow: 0 4px 12px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
  --shadow-lg: 0 10px 30px rgba(0,0,0,0.08), 0 2px 6px rgba(0,0,0,0.04);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'DM Sans', -apple-system, sans-serif;
  background: var(--bg);
  color: var(--ink);
  min-height: 100vh;
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

.app { display: flex; height: 100vh; overflow: hidden; }

/* ===== SIDEBAR ===== */
.sidebar {
  width: var(--sidebar-w);
  background: var(--white);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow: hidden;
  position: relative;
  z-index: 20;
}

.sidebar-header {
  padding: 20px 18px 16px;
  border-bottom: 1px solid var(--border2);
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  width: 34px; height: 34px;
  background: var(--blue);
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(37,99,235,0.3);
}

.brand-name {
  font-family: 'Fraunces', serif;
  font-size: 17px;
  font-weight: 600;
  color: var(--ink);
  letter-spacing: -0.3px;
}
.brand-sub {
  font-size: 11px;
  color: var(--ink4);
  font-weight: 400;
  letter-spacing: 0.2px;
}

.nav-section {
  padding: 12px 10px 4px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  color: var(--ink4);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 10px;
  margin: 1px 8px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13.5px;
  font-weight: 500;
  color: var(--ink3);
  transition: all 0.15s;
  position: relative;
}

.nav-item:hover { background: var(--bg); color: var(--ink); }

.nav-item.active {
  background: var(--blue-light);
  color: var(--blue);
  font-weight: 600;
}

.nav-icon {
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  background: transparent;
  transition: all 0.15s;
  flex-shrink: 0;
}

.nav-item.active .nav-icon {
  background: var(--blue);
  filter: none;
}

.nav-badge {
  margin-left: auto;
  background: var(--red);
  color: white;
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 10px;
  line-height: 1.6;
}

.sidebar-footer {
  margin-top: auto;
  padding: 14px;
  border-top: 1px solid var(--border2);
}

.home-status {
  background: var(--green-light);
  border: 1px solid var(--green-mid);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--green);
  flex-shrink: 0;
  box-shadow: 0 0 0 3px rgba(22,163,74,0.2);
  animation: statusPulse 2.5s infinite;
}

@keyframes statusPulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(22,163,74,0.2); }
  50% { box-shadow: 0 0 0 5px rgba(22,163,74,0.1); }
}

.status-dot.amber { background: var(--amber); box-shadow: 0 0 0 3px rgba(217,119,6,0.2); }
.status-dot.red { background: var(--red); box-shadow: 0 0 0 3px rgba(220,38,38,0.2); }

.home-status-text { font-size: 12px; font-weight: 600; color: var(--green); }
.home-status-sub { font-size: 11px; color: var(--ink3); }

/* ===== MAIN ===== */
.main { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }

/* ===== TOPBAR ===== */
.topbar {
  height: var(--topbar-h);
  background: var(--white);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 16px;
  flex-shrink: 0;
  z-index: 10;
}

.topbar-title {
  font-family: 'Fraunces', serif;
  font-size: 19px;
  font-weight: 600;
  color: var(--ink);
  letter-spacing: -0.3px;
  flex: 1;
}

.topbar-pills { display: flex; align-items: center; gap: 8px; }

.pill {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12.5px;
  font-weight: 500;
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--ink2);
  white-space: nowrap;
}

.pill.green { background: var(--green-light); border-color: var(--green-mid); color: var(--green); }
.pill.amber { background: var(--amber-light); border-color: var(--amber-mid); color: var(--amber); }
.pill.red { background: var(--red-light); border-color: var(--red-mid); color: var(--red); }
.pill.blue { background: var(--blue-light); border-color: var(--blue-mid); color: var(--blue); }

.pill-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.8;
}

.clock-wrap {
  font-family: 'DM Mono', monospace;
  font-size: 14px;
  font-weight: 500;
  color: var(--ink2);
  background: var(--bg);
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
}

/* ===== ALERT BANNER ===== */
.alert-banner {
  background: var(--red-light);
  border-bottom: 1px solid var(--red-mid);
  padding: 10px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  font-weight: 500;
  color: var(--red);
}
.alert-banner.hidden { display: none; }

/* ===== CONTENT ===== */
.content {
  flex: 1;
  overflow-y: auto;
  padding: 22px 24px;
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
}

.tab-pane { display: none; }
.tab-pane.active { display: block; }

/* ===== GRID LAYOUTS ===== */
.g1 { display: grid; grid-template-columns: 1fr; gap: 16px; }
.g2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.g3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.g4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.g6 { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; }
.gauto { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; }
.span2 { grid-column: span 2; }
.span3 { grid-column: span 3; }
.span4 { grid-column: span 4; }

/* ===== CARDS ===== */
.card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px;
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s, transform 0.2s;
}
.card:hover { box-shadow: var(--shadow); }

.card-sm { padding: 14px 16px; }
.card-lg { padding: 22px; }

/* KPI Cards */
.kpi-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}
.kpi-card:hover { box-shadow: var(--shadow); transform: translateY(-1px); }

.kpi-accent {
  position: absolute;
  top: 0; left: 0;
  width: 3px; height: 100%;
  border-radius: 4px 0 0 4px;
}

.kpi-label {
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: 0.3px;
  color: var(--ink3);
  text-transform: uppercase;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.kpi-value {
  font-family: 'Fraunces', serif;
  font-size: 30px;
  font-weight: 600;
  color: var(--ink);
  line-height: 1;
  letter-spacing: -0.5px;
}

.kpi-unit {
  font-size: 14px;
  font-weight: 500;
  color: var(--ink3);
  margin-left: 2px;
  font-family: 'DM Sans', sans-serif;
}

.kpi-sub {
  font-size: 12px;
  color: var(--ink4);
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.kpi-trend {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11.5px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 10px;
}
.kpi-trend.up { background: var(--green-light); color: var(--green); }
.kpi-trend.down { background: var(--red-light); color: var(--red); }
.kpi-trend.neutral { background: var(--bg2); color: var(--ink3); }

.kpi-icon {
  width: 36px; height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

/* Section headers */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 24px 0 14px;
}

.section-title {
  font-family: 'Fraunces', serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  letter-spacing: -0.2px;
}

.section-sub {
  font-size: 12.5px;
  color: var(--ink3);
  font-weight: 400;
}

.section-action {
  font-size: 12.5px;
  color: var(--blue);
  font-weight: 500;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: var(--radius-sm);
  transition: background 0.15s;
}
.section-action:hover { background: var(--blue-light); }

/* Chart cards */
.chart-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  box-shadow: var(--shadow-sm);
}

.chart-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}

.chart-title {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--ink);
}

.chart-sub {
  font-size: 12px;
  color: var(--ink4);
  margin-top: 2px;
}

/* Progress bars */
.progress-row { margin: 10px 0; }
.progress-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 13px;
}
.progress-name { font-weight: 500; color: var(--ink2); }
.progress-val { font-family: 'DM Mono', monospace; font-size: 12px; color: var(--ink3); font-weight: 500; }
.progress-track {
  height: 6px;
  background: var(--bg2);
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
.pf-blue { background: linear-gradient(90deg, #60a5fa, #2563eb); }
.pf-green { background: linear-gradient(90deg, #4ade80, #16a34a); }
.pf-amber { background: linear-gradient(90deg, #fbbf24, #d97706); }
.pf-red { background: linear-gradient(90deg, #f87171, #dc2626); }
.pf-purple { background: linear-gradient(90deg, #a78bfa, #7c3aed); }
.pf-teal { background: linear-gradient(90deg, #2dd4bf, #0d9488); }

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 9px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
}
.badge-green { background: var(--green-light); color: var(--green); border: 1px solid var(--green-mid); }
.badge-red { background: var(--red-light); color: var(--red); border: 1px solid var(--red-mid); }
.badge-amber { background: var(--amber-light); color: var(--amber); border: 1px solid var(--amber-mid); }
.badge-blue { background: var(--blue-light); color: var(--blue); border: 1px solid var(--blue-mid); }
.badge-purple { background: var(--purple-light); color: var(--purple); border: 1px solid rgba(124,58,237,0.2); }
.badge-gray { background: var(--bg2); color: var(--ink3); border: 1px solid var(--border); }

/* Toggle */
.toggle {
  width: 40px; height: 22px;
  border-radius: 11px;
  background: var(--border);
  position: relative;
  cursor: pointer;
  transition: background 0.25s;
  flex-shrink: 0;
  border: none;
  outline: none;
}
.toggle::after {
  content: '';
  position: absolute;
  top: 3px; left: 3px;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: white;
  box-shadow: var(--shadow-sm);
  transition: left 0.25s;
}
.toggle.on { background: var(--blue); }
.toggle.on::after { left: 21px; }

/* ===== OVERVIEW-SPECIFIC ===== */
.energy-flow {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  flex-wrap: wrap;
}

.flow-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 16px 20px;
  border-radius: var(--radius);
  min-width: 110px;
}

.flow-icon-wrap {
  width: 52px; height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.flow-label { font-size: 11px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; color: var(--ink3); }
.flow-val { font-family: 'Fraunces', serif; font-size: 20px; font-weight: 600; color: var(--ink); }
.flow-unit { font-size: 11px; color: var(--ink4); font-family: 'DM Sans', sans-serif; }

.flow-arrow {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 8px;
  margin-top: -16px;
}

.arrow-line {
  width: 50px; height: 2px;
  background: linear-gradient(90deg, #e2e5ea, #2563eb);
  position: relative;
}

.arrow-line::after {
  content: '';
  position: absolute;
  right: -5px; top: -4px;
  border: 5px solid transparent;
  border-left: 7px solid var(--blue);
}

.arrow-label { font-size: 10px; font-weight: 600; color: var(--blue); margin-top: 4px; }

/* Room cards */
.room-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s;
  cursor: default;
}
.room-card:hover { box-shadow: var(--shadow); transform: translateY(-1px); }

.room-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.room-name { font-size: 12px; font-weight: 600; color: var(--ink3); letter-spacing: 0.3px; }
.room-icon-wrap {
  width: 30px; height: 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
}

.room-val { font-family: 'Fraunces', serif; font-size: 22px; font-weight: 600; color: var(--ink); }
.room-unit { font-size: 12px; color: var(--ink4); font-family: 'DM Sans', sans-serif; }
.room-bar { margin-top: 10px; }

/* Security */
.cam-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.cam-card { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow-sm); }
.cam-screen {
  height: 110px;
  background: #1a2332;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.cam-screen::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(0deg, rgba(255,255,255,0.015) 0, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 3px);
}
.cam-icon { font-size: 32px; opacity: 0.3; }
.cam-rec-badge { position: absolute; top: 8px; right: 8px; display: flex; align-items: center; gap: 4px; background: rgba(220,38,38,0.85); color: white; font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 4px; letter-spacing: 0.5px; }
.cam-motion-badge { position: absolute; bottom: 8px; left: 8px; background: rgba(220,38,38,0.9); color: white; font-size: 10px; font-weight: 600; padding: 3px 8px; border-radius: 4px; }
.cam-res { position: absolute; top: 8px; left: 8px; background: rgba(0,0,0,0.5); color: rgba(255,255,255,0.7); font-size: 9px; font-weight: 600; padding: 2px 6px; border-radius: 3px; }
.cam-info { padding: 10px 14px; }
.cam-id { font-family: 'DM Mono', monospace; font-size: 11px; font-weight: 500; color: var(--ink3); }
.cam-loc { font-size: 13px; font-weight: 600; color: var(--ink); margin: 2px 0; }

.door-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.door-item {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-sm);
}
.door-name { font-size: 13px; font-weight: 600; color: var(--ink2); }
.door-icon { font-size: 18px; margin-right: 8px; }

/* Solar panels */
.panel-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.panel-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px;
  text-align: center;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s;
}
.panel-card:hover { box-shadow: var(--shadow); }
.panel-id { font-family: 'DM Mono', monospace; font-size: 10.5px; color: var(--ink3); font-weight: 500; letter-spacing: 0.5px; }
.panel-output { font-family: 'Fraunces', serif; font-size: 20px; color: var(--amber); margin: 6px 0 3px; font-weight: 600; }
.panel-eff { font-size: 11.5px; color: var(--ink3); }
.panel-temp { font-size: 11px; color: var(--ink4); margin-top: 3px; }

/* Appliance list */
.appliance-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 0;
  border-bottom: 1px solid var(--border2);
  transition: all 0.15s;
}
.appliance-row:last-child { border-bottom: none; }
.app-icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.app-name { flex: 1; font-size: 13.5px; font-weight: 500; color: var(--ink2); }
.app-watts { font-family: 'DM Mono', monospace; font-size: 13px; font-weight: 500; color: var(--amber); }
.app-status { font-size: 11.5px; color: var(--ink4); }

/* AI Insights */
.insight-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  border-radius: var(--radius-sm);
  margin-bottom: 10px;
  border: 1px solid;
  transition: all 0.15s;
}
.insight-item:hover { transform: translateX(3px); }
.insight-item.info { background: var(--blue-light); border-color: var(--blue-mid); }
.insight-item.warning { background: var(--amber-light); border-color: var(--amber-mid); }
.insight-item.alert { background: var(--red-light); border-color: var(--red-mid); }

.insight-icon-wrap {
  width: 34px; height: 34px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  flex-shrink: 0;
}
.insight-item.info .insight-icon-wrap { background: var(--blue-mid); }
.insight-item.warning .insight-icon-wrap { background: var(--amber-mid); }
.insight-item.alert .insight-icon-wrap { background: var(--red-mid); }

.insight-body { flex: 1; }
.insight-msg { font-size: 13.5px; font-weight: 500; color: var(--ink); line-height: 1.4; }
.insight-action { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; font-weight: 600; margin-top: 5px; cursor: pointer; }
.insight-item.info .insight-action { color: var(--blue); }
.insight-item.warning .insight-action { color: var(--amber); }
.insight-item.alert .insight-action { color: var(--red); }

/* Automation */
.auto-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid var(--border2);
}
.auto-row:last-child { border-bottom: none; }
.auto-icon { width: 38px; height: 38px; border-radius: 10px; background: var(--bg2); display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
.auto-name { font-size: 13.5px; font-weight: 600; color: var(--ink); }
.auto-trigger { font-size: 12px; color: var(--ink3); }
.auto-action { font-size: 12px; color: var(--ink4); font-style: italic; }
.auto-last { font-size: 11px; color: var(--ink4); }
.auto-info { flex: 1; }

/* Tariff badge */
.tariff-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12.5px;
  font-weight: 600;
}
.tariff-peak { background: var(--red-light); color: var(--red); border: 1px solid var(--red-mid); }
.tariff-standard { background: var(--amber-light); color: var(--amber); border: 1px solid var(--amber-mid); }
.tariff-offpeak { background: var(--green-light); color: var(--green); border: 1px solid var(--green-mid); }

/* Tank visual */
.tank-visual {
  width: 72px; height: 130px;
  border: 2px solid var(--border);
  border-radius: 4px 4px 8px 8px;
  overflow: hidden;
  background: var(--bg2);
  position: relative;
  flex-shrink: 0;
}
.tank-water {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(180deg, #60a5fa 0%, #2563eb 100%);
  transition: height 1s ease;
  opacity: 0.7;
}
.tank-label {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
}

/* Stat row */
.stat-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 0;
  border-bottom: 1px solid var(--border2);
  font-size: 13px;
}
.stat-row:last-child { border-bottom: none; }
.stat-label { color: var(--ink3); font-weight: 500; }
.stat-value { font-family: 'DM Mono', monospace; font-weight: 500; color: var(--ink); }

/* Divider */
.divider { height: 1px; background: var(--border2); margin: 16px 0; }

/* Spacing */
.mt8 { margin-top: 8px; }
.mt12 { margin-top: 12px; }
.mt16 { margin-top: 16px; }
.mt20 { margin-top: 20px; }
.mb4 { margin-bottom: 4px; }
.flex { display: flex; align-items: center; }
.flex-between { display: flex; align-items: center; justify-content: space-between; }
.gap4 { gap: 4px; }
.gap8 { gap: 8px; }
.gap12 { gap: 12px; }
.gap16 { gap: 16px; }
.gap20 { gap: 20px; }
.text-sm { font-size: 12px; }
.text-xs { font-size: 11px; }
.mono { font-family: 'DM Mono', monospace; }
.fw6 { font-weight: 600; }
.color-ink3 { color: var(--ink3); }
.color-ink4 { color: var(--ink4); }
.color-green { color: var(--green); }
.color-amber { color: var(--amber); }
.color-red { color: var(--red); }
.color-blue { color: var(--blue); }
.color-purple { color: var(--purple); }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* Chart legend pill */
.legend-pills { display: flex; gap: 12px; flex-wrap: wrap; }
.legend-pill { display: flex; align-items: center; gap: 5px; font-size: 12px; color: var(--ink3); }
.legend-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

/* Summary row for environmental */
.env-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}
.env-cell {
  background: var(--white);
  padding: 14px 16px;
  text-align: center;
}
.env-cell-label { font-size: 11px; font-weight: 600; color: var(--ink4); letter-spacing: 0.4px; text-transform: uppercase; margin-bottom: 4px; }
.env-cell-val { font-family: 'Fraunces', serif; font-size: 22px; font-weight: 600; color: var(--ink); }
.env-cell-unit { font-size: 12px; color: var(--ink4); font-family: 'DM Sans', sans-serif; }

/* Weekly table */
.week-table { width: 100%; border-collapse: collapse; }
.week-table th { font-size: 11px; font-weight: 600; color: var(--ink3); letter-spacing: 0.4px; text-transform: uppercase; padding: 0 12px 10px; text-align: right; }
.week-table th:first-child { text-align: left; }
.week-table td { font-size: 13px; padding: 10px 12px; border-top: 1px solid var(--border2); color: var(--ink2); text-align: right; }
.week-table td:first-child { font-weight: 600; color: var(--ink); text-align: left; }
.week-table tbody tr:hover td { background: var(--bg2); }
.week-table .mono { font-family: 'DM Mono', monospace; font-size: 12.5px; }
</style>
</head>
<body>
<div class="app">

<!-- ===== SIDEBAR ===== -->
<div class="sidebar">
  <div class="sidebar-header">
    <div class="brand-icon">🏡</div>
    <div>
      <div class="brand-name">NexaHome</div>
      <div class="brand-sub">Command Centre</div>
    </div>
  </div>

  <div class="nav-section">Monitoring</div>
  <div class="nav-item active" onclick="switchTab('overview')" id="nav-overview">
    <div class="nav-icon">📊</div> Overview
  </div>
  <div class="nav-item" onclick="switchTab('energy')" id="nav-energy">
    <div class="nav-icon">⚡</div> Energy
  </div>
  <div class="nav-item" onclick="switchTab('solar')" id="nav-solar">
    <div class="nav-icon">☀️</div> Solar & Battery
  </div>
  <div class="nav-item" onclick="switchTab('environment')" id="nav-environment">
    <div class="nav-icon">🌿</div> Environment
  </div>
  <div class="nav-item" onclick="switchTab('water')" id="nav-water">
    <div class="nav-icon">💧</div> Water
  </div>

  <div class="nav-section" style="margin-top:8px">Control</div>
  <div class="nav-item" onclick="switchTab('security')" id="nav-security">
    <div class="nav-icon">🔒</div> Security
    <span class="nav-badge" id="sec-nav-badge" style="display:none">!</span>
  </div>
  <div class="nav-item" onclick="switchTab('appliances')" id="nav-appliances">
    <div class="nav-icon">🔌</div> Appliances
  </div>
  <div class="nav-item" onclick="switchTab('automations')" id="nav-automations">
    <div class="nav-icon">⚙️</div> Automations
  </div>
  <div class="nav-item" onclick="switchTab('ai')" id="nav-ai">
    <div class="nav-icon">🤖</div> AI Insights
  </div>

  <div class="sidebar-footer">
    <div class="home-status" id="sidebar-status">
      <div class="status-dot" id="sidebar-dot"></div>
      <div>
        <div class="home-status-text" id="sidebar-status-text">All Systems Normal</div>
        <div class="home-status-sub" id="sidebar-status-sub">22 devices active</div>
      </div>
    </div>
  </div>
</div>

<!-- ===== MAIN ===== -->
<div class="main">

  <!-- TOPBAR -->
  <div class="topbar">
    <div class="topbar-title" id="page-title">Home Overview</div>
    <div class="topbar-pills">
      <div class="pill green"><div class="pill-dot"></div>Grid Online</div>
      <div class="pill blue" id="solar-pill"><div class="pill-dot"></div>Solar Active</div>
      <div class="pill green" id="security-pill"><div class="pill-dot"></div>Secure</div>
      <div class="pill" id="tariff-pill"><div class="pill-dot"></div><span id="tariff-text">Standard Rate</span></div>
    </div>
    <div class="clock-wrap mono" id="clock">--:--:--</div>
  </div>

  <!-- ALERT BANNER -->
  <div class="alert-banner hidden" id="alert-banner">
    <span style="font-size:16px">⚠️</span>
    <span id="alert-text">Security alert detected</span>
    <span style="margin-left:auto;font-size:12px;cursor:pointer;opacity:0.7" onclick="this.parentElement.classList.add('hidden')">Dismiss ✕</span>
  </div>

  <!-- CONTENT -->
  <div class="content">

    <!-- ============================== -->
    <!-- OVERVIEW TAB -->
    <!-- ============================== -->
    <div class="tab-pane active" id="tab-overview">

      <!-- KPI Row 1 -->
      <div class="g4">
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--blue)"></div>
          <div class="kpi-label">
            <span>Total Power</span>
            <div class="kpi-icon" style="background:var(--blue-light)">⚡</div>
          </div>
          <div class="kpi-value" id="ov-energy">—<span class="kpi-unit">kWh</span></div>
          <div class="kpi-sub"><span class="kpi-trend neutral" id="ov-energy-trend">—</span> vs yesterday</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--green)"></div>
          <div class="kpi-label">
            <span>Solar Output</span>
            <div class="kpi-icon" style="background:var(--green-light)">☀️</div>
          </div>
          <div class="kpi-value" style="color:var(--green)" id="ov-solar">—<span class="kpi-unit">kW</span></div>
          <div class="kpi-sub" id="ov-solar-sub">—</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--amber)"></div>
          <div class="kpi-label">
            <span>Battery Level</span>
            <div class="kpi-icon" style="background:var(--amber-light)">🔋</div>
          </div>
          <div class="kpi-value" style="color:var(--amber)" id="ov-battery">—<span class="kpi-unit">%</span></div>
          <div class="kpi-sub" id="ov-battery-sub">Health: —</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--purple)"></div>
          <div class="kpi-label">
            <span>Cost Today</span>
            <div class="kpi-icon" style="background:var(--purple-light)">₹</div>
          </div>
          <div class="kpi-value" style="color:var(--purple)" id="ov-cost">—</div>
          <div class="kpi-sub" id="ov-cost-sub">Monthly: —</div>
        </div>
      </div>

      <!-- KPI Row 2 -->
      <div class="g4 mt12">
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--teal)"></div>
          <div class="kpi-label">
            <span>Indoor Temp</span>
            <div class="kpi-icon" style="background:var(--teal-light)">🌡️</div>
          </div>
          <div class="kpi-value" id="ov-temp">—<span class="kpi-unit">°C</span></div>
          <div class="kpi-sub" id="ov-temp-out">Outdoor: —</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--blue)"></div>
          <div class="kpi-label">
            <span>Humidity</span>
            <div class="kpi-icon" style="background:var(--blue-light)">💧</div>
          </div>
          <div class="kpi-value" id="ov-humidity">—<span class="kpi-unit">%</span></div>
          <div class="kpi-sub">Relative humidity</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--orange)"></div>
          <div class="kpi-label">
            <span>Grid Draw</span>
            <div class="kpi-icon" style="background:var(--orange-light)">🔌</div>
          </div>
          <div class="kpi-value" id="ov-grid">—<span class="kpi-unit">kW</span></div>
          <div class="kpi-sub">From utility grid</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--green)"></div>
          <div class="kpi-label">
            <span>Devices Online</span>
            <div class="kpi-icon" style="background:var(--green-light)">📡</div>
          </div>
          <div class="kpi-value" id="ov-devices">—</div>
          <div class="kpi-sub">Smart home devices</div>
        </div>
      </div>

      <!-- Energy Flow -->
      <div class="section-header mt20">
        <div><div class="section-title">Live Energy Flow</div><div class="section-sub">Real-time power routing</div></div>
      </div>
      <div class="energy-flow">
        <div class="flow-node">
          <div class="flow-icon-wrap" style="background:var(--amber-light)">☀️</div>
          <div class="flow-label">Solar</div>
          <div class="flow-val" id="flow-solar">— <span class="flow-unit">kW</span></div>
        </div>
        <div class="flow-arrow"><div class="arrow-line"></div><div class="arrow-label" id="flow-arrow1">→</div></div>
        <div class="flow-node" style="background:var(--bg2); border:1px solid var(--border); border-radius:var(--radius);">
          <div class="flow-icon-wrap" style="background:var(--blue-light)">🏠</div>
          <div class="flow-label">Home</div>
          <div class="flow-val" id="flow-home">— <span class="flow-unit">kWh</span></div>
        </div>
        <div class="flow-arrow"><div class="arrow-line" style="background:linear-gradient(90deg,#e2e5ea,var(--amber))"></div><div class="arrow-label" id="flow-arrow2">→</div></div>
        <div class="flow-node">
          <div class="flow-icon-wrap" style="background:var(--amber-light)">🔋</div>
          <div class="flow-label">Battery</div>
          <div class="flow-val" id="flow-battery">—<span class="flow-unit">%</span></div>
        </div>
        <div class="flow-arrow"><div class="arrow-line" style="background:linear-gradient(90deg,#e2e5ea,var(--purple))"></div><div class="arrow-label">→</div></div>
        <div class="flow-node">
          <div class="flow-icon-wrap" style="background:var(--purple-light)">🔌</div>
          <div class="flow-label">Grid</div>
          <div class="flow-val" id="flow-grid">— <span class="flow-unit">kW</span></div>
        </div>
      </div>

      <!-- Charts row -->
      <div class="section-header mt20">
        <div><div class="section-title">Live Monitoring</div><div class="section-sub">Auto-refreshing every 3 seconds</div></div>
        <div class="legend-pills">
          <div class="legend-pill"><div class="legend-dot" style="background:#2563eb"></div>Energy</div>
          <div class="legend-pill"><div class="legend-dot" style="background:#16a34a"></div>Solar</div>
        </div>
      </div>
      <div class="chart-card">
        <canvas id="liveChart" height="90"></canvas>
      </div>

      <div class="g2 mt16">
        <div class="chart-card">
          <div class="chart-header">
            <div><div class="chart-title">12-Hour History</div><div class="chart-sub">Energy consumption & generation</div></div>
          </div>
          <canvas id="historyChart" height="140"></canvas>
        </div>
        <div class="chart-card">
          <div class="chart-header">
            <div><div class="chart-title">Room Breakdown</div><div class="chart-sub">Power distribution by room</div></div>
          </div>
          <canvas id="roomPieChart" height="140"></canvas>
        </div>
      </div>

      <!-- Rooms -->
      <div class="section-header mt20">
        <div><div class="section-title">Room Status</div><div class="section-sub">Live consumption by room</div></div>
      </div>
      <div class="g3" id="room-grid"></div>

      <!-- Weekly summary -->
      <div class="section-header mt20">
        <div><div class="section-title">Weekly Summary</div><div class="section-sub">Last 7 days</div></div>
      </div>
      <div class="card">
        <table class="week-table" id="week-table">
          <thead>
            <tr>
              <th>Day</th>
              <th>Energy (kWh)</th>
              <th>Solar (kWh)</th>
              <th>Water (L)</th>
              <th>Cost (₹)</th>
            </tr>
          </thead>
          <tbody id="week-tbody"></tbody>
        </table>
      </div>

    </div><!-- /overview -->

    <!-- ============================== -->
    <!-- ENERGY TAB -->
    <!-- ============================== -->
    <div class="tab-pane" id="tab-energy">

      <div class="g4">
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--blue)"></div>
          <div class="kpi-label">Voltage<div class="kpi-icon" style="background:var(--blue-light)">⚡</div></div>
          <div class="kpi-value" id="en-voltage">—<span class="kpi-unit">V</span></div>
          <div class="kpi-sub">Nominal: 220V</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--teal)"></div>
          <div class="kpi-label">Frequency<div class="kpi-icon" style="background:var(--teal-light)">📶</div></div>
          <div class="kpi-value" id="en-freq">—<span class="kpi-unit">Hz</span></div>
          <div class="kpi-sub">Nominal: 50Hz</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--green)"></div>
          <div class="kpi-label">Power Factor<div class="kpi-icon" style="background:var(--green-light)">📊</div></div>
          <div class="kpi-value" style="color:var(--green)" id="en-pf">—</div>
          <div class="kpi-sub">Target: ≥ 0.90</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--red)"></div>
          <div class="kpi-label">Peak Demand<div class="kpi-icon" style="background:var(--red-light)">📈</div></div>
          <div class="kpi-value" style="color:var(--red)" id="en-peak">—<span class="kpi-unit">kW</span></div>
          <div class="kpi-sub" id="en-tariff-label">—</div>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Consumption Analysis</div><div class="section-sub">24-hour breakdown</div></div>
      </div>
      <div class="g2">
        <div class="chart-card">
          <div class="chart-header"><div><div class="chart-title">Hourly Usage (kWh)</div><div class="chart-sub">Full day view</div></div></div>
          <canvas id="hourlyBar" height="160"></canvas>
        </div>
        <div class="chart-card">
          <div class="chart-header"><div><div class="chart-title">Cost per Hour (₹)</div><div class="chart-sub">Electricity spend</div></div></div>
          <canvas id="costChart" height="160"></canvas>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Room Breakdown</div><div class="section-sub">Power distribution</div></div>
      </div>
      <div class="card">
        <div id="room-bars"></div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Energy vs Solar Flow</div><div class="section-sub">Last 20 readings</div></div>
      </div>
      <div class="chart-card">
        <canvas id="energyAreaChart" height="100"></canvas>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Cost Summary</div></div>
      </div>
      <div class="g3">
        <div class="card">
          <div class="kpi-label">Today</div>
          <div class="kpi-value" id="en-cost-today" style="color:var(--purple)">—</div>
          <div class="kpi-sub">Electricity cost</div>
        </div>
        <div class="card">
          <div class="kpi-label">Yesterday</div>
          <div class="kpi-value" id="en-cost-yest">—</div>
          <div class="kpi-sub">Reference day</div>
        </div>
        <div class="card">
          <div class="kpi-label">Estimated Month</div>
          <div class="kpi-value" id="en-cost-month" style="color:var(--amber)">—</div>
          <div class="kpi-sub">Projected spend</div>
        </div>
      </div>

    </div><!-- /energy -->

    <!-- ============================== -->
    <!-- SOLAR TAB -->
    <!-- ============================== -->
    <div class="tab-pane" id="tab-solar">

      <div class="g4">
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--amber)"></div>
          <div class="kpi-label">Solar Output<div class="kpi-icon" style="background:var(--amber-light)">☀️</div></div>
          <div class="kpi-value" style="color:var(--amber)" id="sol-output">—<span class="kpi-unit">kW</span></div>
          <div class="kpi-sub" id="sol-output-sub">—</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--green)"></div>
          <div class="kpi-label">Battery Level<div class="kpi-icon" style="background:var(--green-light)">🔋</div></div>
          <div class="kpi-value" style="color:var(--green)" id="sol-battery">—<span class="kpi-unit">%</span></div>
          <div class="kpi-sub" id="sol-bhealth">Health: —%</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--teal)"></div>
          <div class="kpi-label">Grid Export<div class="kpi-icon" style="background:var(--teal-light)">⬆️</div></div>
          <div class="kpi-value" style="color:var(--teal)" id="sol-export">—<span class="kpi-unit">kW</span></div>
          <div class="kpi-sub" id="sol-savings">Savings: —</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--purple)"></div>
          <div class="kpi-label">CO₂ Saved<div class="kpi-icon" style="background:var(--purple-light)">🌱</div></div>
          <div class="kpi-value" style="color:var(--purple)" id="sol-co2">—<span class="kpi-unit">kg</span></div>
          <div class="kpi-sub">Lifetime generation</div>
        </div>
      </div>

      <div class="g2 mt12">
        <div class="card" style="display:flex;align-items:center;gap:16px">
          <div style="flex:1">
            <div class="stat-row"><span class="stat-label">Inverter Status</span><span class="stat-value" id="sol-inverter">—</span></div>
            <div class="stat-row"><span class="stat-label">Battery Temp</span><span class="stat-value" id="sol-btemp">—</span></div>
            <div class="stat-row"><span class="stat-label">Charge Cycles</span><span class="stat-value" id="sol-cycles">—</span></div>
            <div class="stat-row"><span class="stat-label">Lifetime Generated</span><span class="stat-value" id="sol-lifetime">—</span></div>
          </div>
        </div>
        <div class="card">
          <div class="kpi-label mb4">Battery Charge</div>
          <div class="progress-row">
            <div class="progress-label"><span class="progress-name">Level</span><span class="progress-val" id="sol-bat-pct">—%</span></div>
            <div class="progress-track"><div class="progress-fill pf-amber" id="sol-bat-bar" style="width:0%"></div></div>
          </div>
          <div class="progress-row mt12">
            <div class="progress-label"><span class="progress-name">Health</span><span class="progress-val" id="sol-health-pct">—%</span></div>
            <div class="progress-track"><div class="progress-fill pf-green" id="sol-health-bar" style="width:0%"></div></div>
          </div>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Solar Analytics</div><div class="section-sub">Generation trends</div></div>
      </div>
      <div class="g2">
        <div class="chart-card">
          <div class="chart-header"><div class="chart-title">Solar Output — Live</div></div>
          <canvas id="solarLiveChart" height="160"></canvas>
        </div>
        <div class="chart-card">
          <div class="chart-header"><div class="chart-title">Battery Level Trend</div></div>
          <canvas id="batteryChart" height="160"></canvas>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Panel Status</div><div class="section-sub">Individual panel monitoring</div></div>
      </div>
      <div class="panel-grid" id="panel-grid"></div>

    </div><!-- /solar -->

    <!-- ============================== -->
    <!-- ENVIRONMENT TAB -->
    <!-- ============================== -->
    <div class="tab-pane" id="tab-environment">

      <div class="g4">
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--teal)"></div>
          <div class="kpi-label">Indoor Temp<div class="kpi-icon" style="background:var(--teal-light)">🌡️</div></div>
          <div class="kpi-value" id="env-tempin">—<span class="kpi-unit">°C</span></div>
          <div class="kpi-sub">Living room sensor</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--orange)"></div>
          <div class="kpi-label">Outdoor Temp<div class="kpi-icon" style="background:var(--orange-light)">🌤️</div></div>
          <div class="kpi-value" id="env-tempout">—<span class="kpi-unit">°C</span></div>
          <div class="kpi-sub">Ambient temperature</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--blue)"></div>
          <div class="kpi-label">Humidity<div class="kpi-icon" style="background:var(--blue-light)">💧</div></div>
          <div class="kpi-value" id="env-humidity">—<span class="kpi-unit">%</span></div>
          <div class="kpi-sub">Relative humidity</div>
        </div>
        <div class="kpi-card" id="env-aqi-card">
          <div class="kpi-accent" style="background:var(--green)"></div>
          <div class="kpi-label">Air Quality Index<div class="kpi-icon" style="background:var(--green-light)">🌬️</div></div>
          <div class="kpi-value" id="env-aqi">—</div>
          <div class="kpi-sub" id="env-aqi-label">—</div>
        </div>
      </div>

      <div class="g3 mt12">
        <div class="kpi-card">
          <div class="kpi-label">CO₂ Level</div>
          <div class="kpi-value" id="env-co2">—<span class="kpi-unit">ppm</span></div>
          <div class="kpi-sub" id="env-co2-label">—</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Noise Level</div>
          <div class="kpi-value" id="env-noise">—<span class="kpi-unit">dB</span></div>
          <div class="kpi-sub">Ambient sound</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">UV Index</div>
          <div class="kpi-value" id="env-uv">—</div>
          <div class="kpi-sub" id="env-uv-label">—</div>
        </div>
      </div>

      <!-- Additional weather metrics -->
      <div class="g3 mt12">
        <div class="kpi-card">
          <div class="kpi-label">Wind Speed</div>
          <div class="kpi-value" id="env-wind">—<span class="kpi-unit">km/h</span></div>
          <div class="kpi-sub">Outside sensor</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Atmospheric Pressure</div>
          <div class="kpi-value" id="env-pressure">—<span class="kpi-unit">hPa</span></div>
          <div class="kpi-sub">Barometric</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Comfort Rating</div>
          <div class="kpi-value" style="color:var(--green)" id="env-comfort">—</div>
          <div class="kpi-sub">Overall indoor comfort</div>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Comfort Metrics</div></div>
      </div>
      <div class="card">
        <div class="progress-row">
          <div class="progress-label"><span class="progress-name">Temperature Comfort</span><span class="progress-val" id="env-temp-pct">—%</span></div>
          <div class="progress-track"><div class="progress-fill pf-teal" id="env-temp-bar" style="width:0%"></div></div>
        </div>
        <div class="progress-row mt12">
          <div class="progress-label"><span class="progress-name">Humidity Comfort</span><span class="progress-val" id="env-hum-pct">—%</span></div>
          <div class="progress-track"><div class="progress-fill pf-blue" id="env-hum-bar" style="width:0%"></div></div>
        </div>
        <div class="progress-row mt12">
          <div class="progress-label"><span class="progress-name">Air Quality</span><span class="progress-val" id="env-air-pct">—%</span></div>
          <div class="progress-track"><div class="progress-fill pf-green" id="env-air-bar" style="width:0%"></div></div>
        </div>
        <div class="progress-row mt12">
          <div class="progress-label"><span class="progress-name">Noise Level</span><span class="progress-val" id="env-noise-pct">—%</span></div>
          <div class="progress-track"><div class="progress-fill pf-purple" id="env-noise-bar" style="width:0%"></div></div>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Trend Charts</div></div>
      </div>
      <div class="g2">
        <div class="chart-card">
          <div class="chart-header"><div class="chart-title">Temperature Trend (°C)</div></div>
          <canvas id="tempChart" height="160"></canvas>
        </div>
        <div class="chart-card">
          <div class="chart-header"><div class="chart-title">Humidity & AQI</div></div>
          <canvas id="humidityChart" height="160"></canvas>
        </div>
      </div>

    </div><!-- /environment -->

    <!-- ============================== -->
    <!-- WATER TAB -->
    <!-- ============================== -->
    <div class="tab-pane" id="tab-water">

      <div class="g4">
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--blue)"></div>
          <div class="kpi-label">Tank Level<div class="kpi-icon" style="background:var(--blue-light)">🫙</div></div>
          <div class="kpi-value" id="wat-tank">—<span class="kpi-unit">%</span></div>
          <div class="kpi-sub" id="wat-days-sub">— days remaining</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--teal)"></div>
          <div class="kpi-label">Daily Usage<div class="kpi-icon" style="background:var(--teal-light)">💧</div></div>
          <div class="kpi-value" id="wat-daily">—<span class="kpi-unit">L</span></div>
          <div class="kpi-sub">Today's consumption</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--green)"></div>
          <div class="kpi-label">Motor Status<div class="kpi-icon" style="background:var(--green-light)">⚙️</div></div>
          <div class="kpi-value" id="wat-motor" style="font-size:20px">—</div>
          <div class="kpi-sub">Pump system</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--amber)"></div>
          <div class="kpi-label">Water Quality<div class="kpi-icon" style="background:var(--amber-light)">✅</div></div>
          <div class="kpi-value" style="color:var(--green); font-size:20px" id="wat-quality">—</div>
          <div class="kpi-sub" id="wat-filter">Filter: —%</div>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Tank Visualization</div></div>
      </div>
      <div class="card" style="display:flex;align-items:flex-start;gap:28px">
        <div class="tank-visual">
          <div class="tank-water" id="tank-fill" style="height:0%"></div>
          <div class="tank-label" id="tank-pct-text">—</div>
        </div>
        <div style="flex:1">
          <div class="progress-row">
            <div class="progress-label"><span class="progress-name">Tank Level</span><span class="progress-val" id="wat-tank-pct">—%</span></div>
            <div class="progress-track" style="height:8px"><div class="progress-fill pf-blue" id="wat-tank-bar" style="width:0%"></div></div>
          </div>
          <div class="divider"></div>
          <div class="stat-row"><span class="stat-label">Estimated days remaining</span><span class="stat-value color-blue" id="wat-days">—</span></div>
          <div class="stat-row"><span class="stat-label">Hot water temperature</span><span class="stat-value" id="wat-hot">—</span></div>
          <div class="stat-row"><span class="stat-label">Filter life remaining</span><span class="stat-value color-green" id="wat-filter2">—</span></div>
          <div class="stat-row"><span class="stat-label">Tank capacity</span><span class="stat-value">1,000 L</span></div>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Consumption Trend</div></div>
      </div>
      <div class="chart-card">
        <canvas id="waterChart" height="120"></canvas>
      </div>

    </div><!-- /water -->

    <!-- ============================== -->
    <!-- SECURITY TAB -->
    <!-- ============================== -->
    <div class="tab-pane" id="tab-security">

      <div class="g4">
        <div class="kpi-card">
          <div class="kpi-label">Overall Status<div class="kpi-icon" style="background:var(--green-light)">🛡️</div></div>
          <div class="kpi-value" id="sec-overall" style="font-size:20px;color:var(--green)">SECURE</div>
        </div>
        <div class="kpi-card" id="sec-fire-card">
          <div class="kpi-label">Fire Detection</div>
          <div class="kpi-value" id="sec-fire" style="color:var(--green);font-size:20px">—</div>
          <div class="kpi-sub">Smoke sensors: Active</div>
        </div>
        <div class="kpi-card" id="sec-gas-card">
          <div class="kpi-label">Gas Detection</div>
          <div class="kpi-value" id="sec-gas" style="color:var(--green);font-size:20px">—</div>
          <div class="kpi-sub">LPG/CNG sensors</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Motion Zones</div>
          <div class="kpi-value" id="sec-motion-count">0</div>
          <div class="kpi-sub" id="sec-motion-zones">All clear</div>
        </div>
      </div>

      <div class="g2 mt12">
        <div class="card" style="display:flex;align-items:center;gap:14px">
          <div style="font-size:28px">👥</div>
          <div>
            <div class="kpi-label">Visitors Today</div>
            <div style="font-family:'Fraunces',serif;font-size:28px;font-weight:600" id="sec-visitors">—</div>
          </div>
        </div>
        <div class="card" style="display:flex;align-items:center;gap:14px">
          <div style="font-size:28px">📋</div>
          <div>
            <div class="kpi-label">Last Event</div>
            <div style="font-size:14px;font-weight:600;color:var(--ink)" id="sec-last-event">—</div>
          </div>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">CCTV Cameras</div><div class="section-sub">Live monitoring</div></div>
      </div>
      <div class="cam-grid" id="cam-grid"></div>

      <div class="section-header mt20">
        <div><div class="section-title">Doors & Locks</div></div>
      </div>
      <div class="door-grid" id="door-grid"></div>

      <div class="section-header mt20">
        <div><div class="section-title">Security Event Timeline</div></div>
      </div>
      <div class="chart-card">
        <canvas id="securityChart" height="100"></canvas>
      </div>

    </div><!-- /security -->

    <!-- ============================== -->
    <!-- APPLIANCES TAB -->
    <!-- ============================== -->
    <div class="tab-pane" id="tab-appliances">

      <div class="g2">
        <div class="card">
          <div class="chart-header"><div><div class="chart-title">Power Draw</div><div class="chart-sub">Live wattage per appliance</div></div></div>
          <div id="appliance-list"></div>
        </div>
        <div class="chart-card">
          <div class="chart-header"><div class="chart-title">Appliance Share</div></div>
          <canvas id="appliancePie" height="200"></canvas>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Smart Controls</div><div class="section-sub">Toggle devices on/off</div></div>
      </div>
      <div class="g3" id="smart-controls"></div>

      <div class="section-header mt20">
        <div><div class="section-title">Consumption Comparison</div></div>
      </div>
      <div class="chart-card">
        <canvas id="applianceBar" height="120"></canvas>
      </div>

    </div><!-- /appliances -->

    <!-- ============================== -->
    <!-- AUTOMATIONS TAB -->
    <!-- ============================== -->
    <div class="tab-pane" id="tab-automations">

      <div class="section-header">
        <div><div class="section-title">Automation Rules</div><div class="section-sub">Smart triggers and actions</div></div>
        <div class="section-action">+ Add Rule</div>
      </div>

      <div class="g3">
        <div class="kpi-card">
          <div class="kpi-label">Active Rules</div>
          <div class="kpi-value" style="color:var(--green)">4</div>
          <div class="kpi-sub">Running automations</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Paused Rules</div>
          <div class="kpi-value" style="color:var(--amber)">1</div>
          <div class="kpi-sub">Temporarily off</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Runs Today</div>
          <div class="kpi-value" id="auto-runs">12</div>
          <div class="kpi-sub">Triggered automations</div>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">All Rules</div></div>
      </div>
      <div class="card">
        <div id="automation-list"></div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Scenes</div><div class="section-sub">One-tap home modes</div></div>
      </div>
      <div class="g4">
        <div class="card" style="text-align:center;cursor:pointer;transition:all .2s" onclick="this.style.background='var(--amber-light)'">
          <div style="font-size:28px;margin-bottom:8px">🌅</div>
          <div style="font-weight:600;color:var(--ink);font-size:13px">Morning</div>
          <div style="font-size:11px;color:var(--ink4);margin-top:3px">Lights + AC + Coffee</div>
        </div>
        <div class="card" style="text-align:center;cursor:pointer;transition:all .2s" onclick="this.style.background='var(--blue-light)'">
          <div style="font-size:28px;margin-bottom:8px">🌙</div>
          <div style="font-weight:600;color:var(--ink);font-size:13px">Night</div>
          <div style="font-size:11px;color:var(--ink4);margin-top:3px">Dim + Lock + Fan low</div>
        </div>
        <div class="card" style="text-align:center;cursor:pointer;transition:all .2s" onclick="this.style.background='var(--green-light)'">
          <div style="font-size:28px;margin-bottom:8px">🏡</div>
          <div style="font-weight:600;color:var(--ink);font-size:13px">Away</div>
          <div style="font-size:11px;color:var(--ink4);margin-top:3px">Off + Security on</div>
        </div>
        <div class="card" style="text-align:center;cursor:pointer;transition:all .2s" onclick="this.style.background='var(--purple-light)'">
          <div style="font-size:28px;margin-bottom:8px">🎬</div>
          <div style="font-weight:600;color:var(--ink);font-size:13px">Movie</div>
          <div style="font-size:11px;color:var(--ink4);margin-top:3px">Dim + TV + AC 24°</div>
        </div>
      </div>

    </div><!-- /automations -->

    <!-- ============================== -->
    <!-- AI TAB -->
    <!-- ============================== -->
    <div class="tab-pane" id="tab-ai">

      <div class="g3">
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--green)"></div>
          <div class="kpi-label">Energy Score<div class="kpi-icon" style="background:var(--green-light)">⚡</div></div>
          <div class="kpi-value" style="color:var(--green)" id="ai-energy-score">—<span class="kpi-unit">/100</span></div>
          <div class="kpi-sub">Based on solar utilisation</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--blue)"></div>
          <div class="kpi-label">Water Score<div class="kpi-icon" style="background:var(--blue-light)">💧</div></div>
          <div class="kpi-value" id="ai-water-score">—<span class="kpi-unit">/100</span></div>
          <div class="kpi-sub">Based on usage efficiency</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-accent" style="background:var(--purple)"></div>
          <div class="kpi-label">Security Score<div class="kpi-icon" style="background:var(--purple-light)">🛡️</div></div>
          <div class="kpi-value" style="color:var(--purple)" id="ai-sec-score">—<span class="kpi-unit">/100</span></div>
          <div class="kpi-sub">Based on active alerts</div>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">AI Insights</div><div class="section-sub">Smart home analysis</div></div>
      </div>
      <div id="insights-container"></div>

      <div class="section-header mt20">
        <div><div class="section-title">Predictive Analytics</div></div>
      </div>
      <div class="g2">
        <div class="chart-card">
          <div class="chart-header"><div class="chart-title">Predicted vs Actual Energy (kWh)</div></div>
          <canvas id="aiPredChart" height="160"></canvas>
        </div>
        <div class="chart-card">
          <div class="chart-header"><div class="chart-title">Anomaly Detection</div></div>
          <canvas id="anomalyChart" height="160"></canvas>
        </div>
      </div>

      <div class="section-header mt20">
        <div><div class="section-title">Recommendations</div></div>
      </div>
      <div class="card">
        <div id="ai-recommendations"></div>
      </div>

    </div><!-- /ai -->

  </div><!-- /content -->
</div><!-- /main -->
</div><!-- /app -->

<script>
// ============================================================
// CHART DEFAULTS
// ============================================================
const FONT = "'DM Sans', sans-serif";
const MONO = "'DM Mono', monospace";

Chart.defaults.font.family = FONT;
Chart.defaults.color = '#6b7280';
Chart.defaults.plugins.legend.labels.boxWidth = 10;
Chart.defaults.plugins.legend.labels.usePointStyle = true;

const gridColor = 'rgba(0,0,0,0.05)';
const tickColor = '#9ca3af';

function baseOpts(yLabel) {
  return {
    responsive: true,
    animation: { duration: 350 },
    plugins: {
      legend: { labels: { color: tickColor, font: { family: FONT, size: 12 } } },
      tooltip: {
        backgroundColor: '#ffffff',
        borderColor: '#e2e5ea',
        borderWidth: 1,
        titleColor: '#111827',
        bodyColor: '#374151',
        padding: 10,
        cornerRadius: 8,
        titleFont: { family: FONT, weight: '600', size: 13 },
        bodyFont: { family: MONO, size: 12 }
      }
    },
    scales: {
      x: {
        ticks: { color: tickColor, font: { size: 11, family: FONT } },
        grid: { color: gridColor },
        border: { color: '#e2e5ea' }
      },
      y: {
        ticks: { color: tickColor, font: { size: 11, family: MONO } },
        grid: { color: gridColor },
        border: { color: '#e2e5ea' },
        title: yLabel ? { display: true, text: yLabel, color: tickColor, font: { size: 11 } } : { display: false }
      }
    }
  };
}

// Live chart
const liveCtx = document.getElementById('liveChart').getContext('2d');
const liveChart = new Chart(liveCtx, {
  type: 'line',
  data: { labels: [], datasets: [
    { label: 'Energy (kWh)', data: [], borderColor: '#2563eb', backgroundColor: 'rgba(37,99,235,0.06)', tension: 0.4, fill: true, pointRadius: 3, pointBackgroundColor: '#2563eb', borderWidth: 2 },
    { label: 'Solar (kW)', data: [], borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,0.06)', tension: 0.4, fill: true, pointRadius: 3, pointBackgroundColor: '#16a34a', borderWidth: 2 }
  ]},
  options: baseOpts('kWh / kW')
});

// History bar
const histCtx = document.getElementById('historyChart').getContext('2d');
const histChart = new Chart(histCtx, {
  type: 'bar',
  data: { labels: [], datasets: [
    { label: 'Energy', data: [], backgroundColor: 'rgba(37,99,235,0.7)', borderRadius: 3, borderSkipped: false },
    { label: 'Solar', data: [], backgroundColor: 'rgba(22,163,74,0.7)', borderRadius: 3, borderSkipped: false }
  ]},
  options: baseOpts()
});

// Room Doughnut
const roomPieCtx = document.getElementById('roomPieChart').getContext('2d');
const roomPieChart = new Chart(roomPieCtx, {
  type: 'doughnut',
  data: { labels: [], datasets: [{ data: [], backgroundColor: ['#2563eb','#16a34a','#d97706','#ea580c','#7c3aed','#0d9488'], borderWidth: 2, borderColor: '#fff', hoverOffset: 6 }]},
  options: {
    responsive: true,
    cutout: '68%',
    plugins: {
      legend: { position: 'bottom', labels: { color: tickColor, font: { family: FONT, size: 12 }, padding: 12 } },
      tooltip: { backgroundColor: '#fff', borderColor: '#e2e5ea', borderWidth: 1, titleColor: '#111', bodyColor: '#374151', bodyFont: { family: MONO } }
    }
  }
});

// Hourly bar
const hourlyCtx = document.getElementById('hourlyBar').getContext('2d');
const hourlyBar = new Chart(hourlyCtx, {
  type: 'bar',
  data: { labels: [], datasets: [{ label: 'kWh', data: [], backgroundColor: 'rgba(37,99,235,0.65)', borderRadius: 3, borderSkipped: false }]},
  options: baseOpts('kWh')
});

// Cost line
const costCtx = document.getElementById('costChart').getContext('2d');
const costChart = new Chart(costCtx, {
  type: 'line',
  data: { labels: [], datasets: [{ label: '₹ Cost', data: [], borderColor: '#7c3aed', backgroundColor: 'rgba(124,58,237,0.06)', tension: 0.4, fill: true, borderWidth: 2, pointRadius: 2 }]},
  options: baseOpts('₹')
});

// Energy area
const eaCtx = document.getElementById('energyAreaChart').getContext('2d');
const energyArea = new Chart(eaCtx, {
  type: 'line',
  data: { labels: [], datasets: [
    { label: 'Grid Draw', data: [], borderColor: '#ea580c', backgroundColor: 'rgba(234,88,12,0.07)', tension: 0.4, fill: true, borderWidth: 2, pointRadius: 2 },
    { label: 'Solar', data: [], borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,0.07)', tension: 0.4, fill: true, borderWidth: 2, pointRadius: 2 }
  ]},
  options: baseOpts('kW')
});

// Security
const secCtx = document.getElementById('securityChart').getContext('2d');
const secChart = new Chart(secCtx, {
  type: 'bar',
  data: { labels: [], datasets: [{ label: 'Events', data: [], backgroundColor: 'rgba(220,38,38,0.6)', borderRadius: 3 }]},
  options: baseOpts('Events')
});

// Solar live
const solLiveCtx = document.getElementById('solarLiveChart').getContext('2d');
const solLiveChart = new Chart(solLiveCtx, {
  type: 'line',
  data: { labels: [], datasets: [{ label: 'Solar Output (kW)', data: [], borderColor: '#d97706', backgroundColor: 'rgba(217,119,6,0.06)', tension: 0.4, fill: true, borderWidth: 2 }]},
  options: baseOpts('kW')
});

// Battery
const batCtx = document.getElementById('batteryChart').getContext('2d');
const batChart = new Chart(batCtx, {
  type: 'line',
  data: { labels: [], datasets: [{ label: 'Battery %', data: [], borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,0.06)', tension: 0.4, fill: true, borderWidth: 2 }]},
  options: baseOpts('%')
});

// Temperature
const tempCtx = document.getElementById('tempChart').getContext('2d');
const tempChart = new Chart(tempCtx, {
  type: 'line',
  data: { labels: [], datasets: [
    { label: 'Indoor (°C)', data: [], borderColor: '#0d9488', tension: 0.4, pointRadius: 2, borderWidth: 2 },
    { label: 'Outdoor (°C)', data: [], borderColor: '#ea580c', tension: 0.4, pointRadius: 2, borderWidth: 2 }
  ]},
  options: baseOpts('°C')
});

// Humidity
const humCtx = document.getElementById('humidityChart').getContext('2d');
const humChart = new Chart(humCtx, {
  type: 'line',
  data: { labels: [], datasets: [
    { label: 'Humidity (%)', data: [], borderColor: '#2563eb', tension: 0.4, pointRadius: 2, borderWidth: 2 },
    { label: 'AQI', data: [], borderColor: '#7c3aed', tension: 0.4, pointRadius: 2, borderWidth: 2, borderDash: [4,3] }
  ]},
  options: baseOpts()
});

// Water
const watCtx = document.getElementById('waterChart').getContext('2d');
const watChart = new Chart(watCtx, {
  type: 'bar',
  data: { labels: [], datasets: [{ label: 'Litres', data: [], backgroundColor: 'rgba(37,99,235,0.6)', borderRadius: 3 }]},
  options: baseOpts('L')
});

// Appliance pie
const appPieCtx = document.getElementById('appliancePie').getContext('2d');
const appPieChart = new Chart(appPieCtx, {
  type: 'doughnut',
  data: { labels: [], datasets: [{ data: [], backgroundColor: ['#2563eb','#16a34a','#d97706','#ea580c','#7c3aed','#0d9488','#dc2626','#0d9488'], borderWidth: 2, borderColor: '#fff' }]},
  options: { responsive: true, cutout: '55%', plugins: { legend: { position: 'bottom', labels: { color: tickColor, font: { family: FONT, size: 11 }, padding: 10 } }, tooltip: { backgroundColor: '#fff', borderColor: '#e2e5ea', borderWidth: 1, titleColor: '#111', bodyFont: { family: MONO } } } }
});

// Appliance bar
const appBarCtx = document.getElementById('applianceBar').getContext('2d');
const appBarChart = new Chart(appBarCtx, {
  type: 'bar',
  data: { labels: [], datasets: [{ label: 'Watts', data: [], backgroundColor: 'rgba(217,119,6,0.65)', borderRadius: 3 }]},
  options: { ...baseOpts('W'), indexAxis: 'y' }
});

// AI pred
const aiPredCtx = document.getElementById('aiPredChart').getContext('2d');
const aiPredChart = new Chart(aiPredCtx, {
  type: 'line',
  data: { labels: [], datasets: [
    { label: 'Actual', data: [], borderColor: '#2563eb', tension: 0.4, pointRadius: 2, borderWidth: 2 },
    { label: 'Predicted', data: [], borderColor: '#7c3aed', borderDash: [5,4], tension: 0.4, pointRadius: 0, borderWidth: 2 }
  ]},
  options: baseOpts('kWh')
});

// Anomaly
const anomCtx = document.getElementById('anomalyChart').getContext('2d');
const anomChart = new Chart(anomCtx, {
  type: 'scatter',
  data: { datasets: [
    { label: 'Normal', data: [], backgroundColor: 'rgba(37,99,235,0.5)', pointRadius: 5 },
    { label: 'Anomaly', data: [], backgroundColor: 'rgba(220,38,38,0.8)', pointRadius: 8, pointStyle: 'triangle' }
  ]},
  options: { ...baseOpts(), plugins: { ...baseOpts().plugins } }
});

// ============================================================
// HELPERS
// ============================================================
function push(chart, dsIdx, label, value, limit = 20) {
  if (label !== undefined) {
    chart.data.labels.push(label);
    if (chart.data.labels.length > limit) chart.data.labels.shift();
  }
  chart.data.datasets[dsIdx].data.push(value);
  if (chart.data.datasets[dsIdx].data.length > limit) chart.data.datasets[dsIdx].data.shift();
}

function badge(status) {
  const s = status.toLowerCase();
  if (['locked','closed','active','clear','normal','online','excellent','good'].some(k => s.includes(k)))
    return `<span class="badge badge-green">✓ ${status}</span>`;
  if (['motion','warning','open','unlocked','standby','running'].some(k => s.includes(k)))
    return `<span class="badge badge-amber">! ${status}</span>`;
  if (['alert','danger','fire','gas','intrusion'].some(k => s.includes(k)))
    return `<span class="badge badge-red">⚠ ${status}</span>`;
  return `<span class="badge badge-blue">${status}</span>`;
}

function appIcon(name) {
  const icons = { 'AC':'❄️','Refrigerator':'🧊','Washing Machine':'🫧','TV':'📺','Water Heater':'🔥','Fans':'💨','Lights':'💡','Router':'📡' };
  return icons[name] || '🔌';
}
function appColor(name) {
  const colors = { 'AC':'var(--blue-light)','Refrigerator':'var(--teal-light)','Washing Machine':'var(--purple-light)','TV':'var(--amber-light)','Water Heater':'var(--red-light)','Fans':'var(--green-light)','Lights':'var(--amber-light)','Router':'var(--bg2)' };
  return colors[name] || 'var(--bg2)';
}

// ============================================================
// TABS
// ============================================================
const TAB_TITLES = {
  overview: 'Home Overview', energy: 'Energy Management', security: 'Security Centre',
  solar: 'Solar & Battery', environment: 'Environment', water: 'Water System',
  appliances: 'Smart Appliances', automations: 'Automations', ai: 'AI Analytics'
};

function switchTab(name) {
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  document.getElementById('nav-' + name).classList.add('active');
  document.getElementById('page-title').textContent = TAB_TITLES[name];
}

// ============================================================
// MAIN UPDATE
// ============================================================
async function update() {
  try {
    const res = await fetch('/data');
    const d = await res.json();

    // Clock
    document.getElementById('clock').textContent = d.time;

    const hasAlert = d.fire !== 'Clear' || d.gas !== 'Normal' || d.motion_zones.length > 0;

    // Sidebar status
    const sdot = document.getElementById('sidebar-dot');
    const stxt = document.getElementById('sidebar-status-text');
    const ssub = document.getElementById('sidebar-status-sub');
    sdot.className = 'status-dot ' + (hasAlert ? 'red' : '');
    stxt.textContent = hasAlert ? 'Alert Detected' : 'All Systems Normal';
    stxt.style.color = hasAlert ? 'var(--red)' : 'var(--green)';
    ssub.textContent = d.devices_online + ' devices active';

    // Nav badge
    const badge_el = document.getElementById('sec-nav-badge');
    badge_el.style.display = hasAlert ? 'inline' : 'none';

    // Security pill
    const spill = document.getElementById('security-pill');
    spill.className = 'pill ' + (hasAlert ? 'red' : 'green');
    spill.innerHTML = `<div class="pill-dot"></div>${hasAlert ? 'Alert' : 'Secure'}`;

    // Tariff pill
    const tariffPill = document.getElementById('tariff-pill');
    const tariffClass = d.tariff_zone === 'Peak' ? 'amber' : d.tariff_zone === 'Off-Peak' ? 'green' : '';
    tariffPill.className = 'pill ' + tariffClass;
    document.getElementById('tariff-text').textContent = `${d.tariff_zone} ₹${d.tariff_rate}/kWh`;

    // Alert banner
    const ab = document.getElementById('alert-banner');
    if (hasAlert) {
      ab.classList.remove('hidden');
      let msgs = [];
      if (d.fire !== 'Clear') msgs.push('🔥 Fire Alert detected!');
      if (d.gas !== 'Normal') msgs.push('💨 Gas Warning!');
      if (d.motion_zones.length > 0) msgs.push('🚨 Motion detected in ' + d.motion_zones.join(', '));
      document.getElementById('alert-text').textContent = msgs.join('  ·  ');
    } else { ab.classList.add('hidden'); }

    // ---- OVERVIEW ----
    const energyTrend = d.total_energy > 5 ? '↑ High' : '↓ Low';
    const trendClass = d.total_energy > 5 ? 'up' : 'down';
    document.getElementById('ov-energy').innerHTML = d.total_energy + '<span class="kpi-unit">kWh</span>';
    document.getElementById('ov-energy-trend').className = 'kpi-trend ' + trendClass;
    document.getElementById('ov-energy-trend').textContent = energyTrend;
    document.getElementById('ov-solar').innerHTML = d.solar + '<span class="kpi-unit">kW</span>';
    document.getElementById('ov-solar-sub').textContent = d.solar > 2 ? '☀️ Peak generation active' : '🌤 Low irradiance';
    document.getElementById('ov-battery').innerHTML = d.battery + '<span class="kpi-unit">%</span>';
    document.getElementById('ov-battery-sub').textContent = 'Health: ' + d.battery_health + '%';
    document.getElementById('ov-cost').textContent = '₹' + d.cost_today;
    document.getElementById('ov-cost-sub').textContent = 'Monthly est: ₹' + d.cost_month;
    document.getElementById('ov-temp').innerHTML = d.temp_in + '<span class="kpi-unit">°C</span>';
    document.getElementById('ov-temp-out').textContent = 'Outdoor: ' + d.temp_out + '°C';
    document.getElementById('ov-humidity').innerHTML = d.humidity + '<span class="kpi-unit">%</span>';
    document.getElementById('ov-grid').innerHTML = d.grid + '<span class="kpi-unit">kW</span>';
    document.getElementById('ov-devices').textContent = d.devices_online;

    // Energy flow nodes
    document.getElementById('flow-solar').innerHTML = d.solar + ' <span class="flow-unit">kW</span>';
    document.getElementById('flow-home').innerHTML = d.total_energy + ' <span class="flow-unit">kWh</span>';
    document.getElementById('flow-battery').innerHTML = d.battery + '<span class="flow-unit">%</span>';
    document.getElementById('flow-grid').innerHTML = d.grid + ' <span class="flow-unit">kW</span>';

    // Live chart
    push(liveChart, 0, d.time, d.total_energy);
    push(liveChart, 1, undefined, d.solar);
    liveChart.update();

    // History
    histChart.data.labels = d.hourly.slice(0,12).map(h => h.hour);
    histChart.data.datasets[0].data = d.hourly.slice(0,12).map(h => h.energy);
    histChart.data.datasets[1].data = d.hourly.slice(0,12).map(h => h.solar);
    histChart.update();

    // Room pie & grid
    const rooms = d.rooms;
    const roomIcons = { 'Living Room':'🛋️','Kitchen':'🍳','Bedroom 1':'🛏️','Bedroom 2':'🛏️','Bathroom':'🚿','Garage':'🚗' };
    const roomColors = { 'Living Room':'var(--blue-light)','Kitchen':'var(--amber-light)','Bedroom 1':'var(--purple-light)','Bedroom 2':'var(--purple-light)','Bathroom':'var(--teal-light)','Garage':'var(--green-light)' };
    roomPieChart.data.labels = Object.keys(rooms);
    roomPieChart.data.datasets[0].data = Object.values(rooms);
    roomPieChart.update();

    document.getElementById('room-grid').innerHTML = Object.entries(rooms).map(([name, val]) => {
      const pct = Math.min(100, (val / 3.5 * 100)).toFixed(0);
      const color = val > 2.5 ? 'var(--red)' : val > 1.5 ? 'var(--amber)' : 'var(--green)';
      return `<div class="room-card">
        <div class="room-header">
          <div class="room-name">${name.toUpperCase()}</div>
          <div class="room-icon-wrap" style="background:${roomColors[name]||'var(--bg2)'}">${roomIcons[name]||'🏠'}</div>
        </div>
        <div class="room-val" style="color:${color}">${val}<span class="room-unit"> kWh</span></div>
        <div class="room-bar">
          <div class="progress-track">
            <div class="progress-fill" style="width:${pct}%;background:${color};"></div>
          </div>
        </div>
      </div>`;
    }).join('');

    // Weekly table
    if (d.weekly) {
      const tbody = document.getElementById('week-tbody');
      tbody.innerHTML = d.weekly.map(w => `
        <tr>
          <td>${w.day}</td>
          <td class="mono">${w.energy}</td>
          <td class="mono" style="color:var(--amber)">${w.solar}</td>
          <td class="mono" style="color:var(--blue)">${w.water}</td>
          <td class="mono" style="color:var(--purple)">₹${w.cost}</td>
        </tr>`).join('');
    }

    // ---- ENERGY ----
    document.getElementById('en-voltage').innerHTML = d.voltage + '<span class="kpi-unit">V</span>';
    document.getElementById('en-freq').innerHTML = d.frequency + '<span class="kpi-unit">Hz</span>';
    document.getElementById('en-pf').textContent = d.power_factor;
    document.getElementById('en-peak').innerHTML = d.peak_demand + '<span class="kpi-unit">kW</span>';
    document.getElementById('en-tariff-label').innerHTML = `<span class="tariff-chip tariff-${d.tariff_zone.toLowerCase().replace('-','')}">${d.tariff_zone}: ₹${d.tariff_rate}/unit</span>`;
    document.getElementById('en-cost-today').textContent = '₹' + d.cost_today;
    document.getElementById('en-cost-yest').textContent = '₹' + d.cost_yesterday;
    document.getElementById('en-cost-month').textContent = '₹' + d.cost_month;

    hourlyBar.data.labels = d.hourly.map(h => h.hour);
    hourlyBar.data.datasets[0].data = d.hourly.map(h => h.energy);
    hourlyBar.update();
    costChart.data.labels = d.hourly.map(h => h.hour);
    costChart.data.datasets[0].data = d.hourly.map(h => h.cost);
    costChart.update();

    document.getElementById('room-bars').innerHTML = Object.entries(rooms).map(([name, val]) => {
      const pct = Math.min(100, (val / 3.5 * 100)).toFixed(0);
      const cls = val > 2.5 ? 'pf-red' : val > 1.5 ? 'pf-amber' : 'pf-blue';
      return `<div class="progress-row"><div class="progress-label"><span class="progress-name">${name}</span><span class="progress-val">${val} kWh</span></div><div class="progress-track"><div class="progress-fill ${cls}" style="width:${pct}%"></div></div></div>`;
    }).join('');

    push(energyArea, 0, d.time, d.grid);
    push(energyArea, 1, undefined, d.solar);
    energyArea.update();

    // ---- SECURITY ----
    document.getElementById('sec-fire').textContent = d.fire;
    document.getElementById('sec-fire').style.color = d.fire === 'Clear' ? 'var(--green)' : 'var(--red)';
    document.getElementById('sec-gas').textContent = d.gas;
    document.getElementById('sec-gas').style.color = d.gas === 'Normal' ? 'var(--green)' : 'var(--amber)';
    document.getElementById('sec-motion-count').textContent = d.motion_zones.length;
    document.getElementById('sec-motion-zones').textContent = d.motion_zones.length ? d.motion_zones.join(', ') : 'All clear';
    document.getElementById('sec-overall').textContent = hasAlert ? 'ALERT' : 'SECURE';
    document.getElementById('sec-overall').style.color = hasAlert ? 'var(--red)' : 'var(--green)';
    document.getElementById('sec-visitors').textContent = d.visitors_today;
    document.getElementById('sec-last-event').textContent = d.last_event;

    document.getElementById('cam-grid').innerHTML = d.cameras.map(c => `
      <div class="cam-card">
        <div class="cam-screen">
          <div class="cam-icon">📷</div>
          <div class="cam-rec-badge">● REC</div>
          <div class="cam-res">${c.resolution}</div>
          ${c.status === 'Motion' ? '<div class="cam-motion-badge">⚠ MOTION</div>' : ''}
        </div>
        <div class="cam-info">
          <div class="cam-id">${c.id}</div>
          <div class="cam-loc">${c.location}</div>
          <div style="margin-top:5px">${badge(c.status)}</div>
        </div>
      </div>`).join('');

    document.getElementById('door-grid').innerHTML = Object.entries(d.doors).map(([name, status]) => {
      const icons = {'Front Door':'🚪','Back Door':'🚪','Garage':'🏠','Main Gate':'⛩️'};
      return `<div class="door-item"><div class="flex gap8"><span class="door-icon">${icons[name]||'🚪'}</span><span class="door-name">${name}</span></div>${badge(status)}</div>`;
    }).join('');

    push(secChart, 0, d.time, d.motion_zones.length + (d.fire !== 'Clear' ? 2 : 0) + (d.gas !== 'Normal' ? 1 : 0));
    secChart.update();

    // ---- SOLAR ----
    document.getElementById('sol-output').innerHTML = d.solar + '<span class="kpi-unit">kW</span>';
    document.getElementById('sol-output-sub').textContent = d.solar > 3 ? '🌞 Excellent generation' : d.solar > 1 ? '🌤 Moderate generation' : '☁ Low generation';
    document.getElementById('sol-battery').innerHTML = d.battery + '<span class="kpi-unit">%</span>';
    document.getElementById('sol-bhealth').textContent = 'Health: ' + d.battery_health + '%';
    document.getElementById('sol-export').innerHTML = d.grid_export + '<span class="kpi-unit">kW</span>';
    document.getElementById('sol-savings').textContent = 'Monthly savings: ₹' + d.savings_month;
    document.getElementById('sol-co2').innerHTML = d.co2_saved + '<span class="kpi-unit">kg</span>';
    document.getElementById('sol-inverter').textContent = d.inverter;
    document.getElementById('sol-btemp').textContent = d.battery_temp + '°C';
    document.getElementById('sol-cycles').textContent = d.battery_cycles + ' cycles';
    document.getElementById('sol-lifetime').textContent = d.lifetime_solar + ' kWh';
    document.getElementById('sol-bat-pct').textContent = d.battery + '%';
    document.getElementById('sol-bat-bar').style.width = d.battery + '%';
    document.getElementById('sol-health-pct').textContent = d.battery_health + '%';
    document.getElementById('sol-health-bar').style.width = d.battery_health + '%';

    push(solLiveChart, 0, d.time, d.solar);
    solLiveChart.update();
    push(batChart, 0, d.time, d.battery);
    batChart.update();

    document.getElementById('panel-grid').innerHTML = d.solar_panels.map(p => `
      <div class="panel-card">
        <div class="panel-id">${p.id}</div>
        <div class="panel-output">${p.output} kW</div>
        <div class="panel-eff">Efficiency: ${p.efficiency}%</div>
        <div class="panel-temp">🌡 ${p.temp}°C</div>
      </div>`).join('');

    // ---- ENVIRONMENT ----
    document.getElementById('env-tempin').innerHTML = d.temp_in + '<span class="kpi-unit">°C</span>';
    document.getElementById('env-tempout').innerHTML = d.temp_out + '<span class="kpi-unit">°C</span>';
    document.getElementById('env-humidity').innerHTML = d.humidity + '<span class="kpi-unit">%</span>';
    document.getElementById('env-aqi').innerHTML = d.aqi + '';
    const aqiLabel = d.aqi < 50 ? 'Good' : d.aqi < 100 ? 'Moderate' : d.aqi < 150 ? 'Unhealthy' : 'Hazardous';
    document.getElementById('env-aqi').style.color = d.aqi < 50 ? 'var(--green)' : d.aqi < 100 ? 'var(--amber)' : 'var(--red)';
    document.getElementById('env-aqi-label').textContent = aqiLabel;
    document.getElementById('env-co2').innerHTML = d.co2 + '<span class="kpi-unit">ppm</span>';
    document.getElementById('env-co2-label').textContent = d.co2 < 600 ? 'Normal — Fresh air' : d.co2 < 1000 ? 'Elevated — Ventilate' : 'High — Open windows';
    document.getElementById('env-noise').innerHTML = d.noise + '<span class="kpi-unit">dB</span>';
    document.getElementById('env-uv').textContent = d.uv_index;
    const uvLabel = d.uv_index < 3 ? 'Low' : d.uv_index < 6 ? 'Moderate' : d.uv_index < 8 ? 'High' : 'Very High';
    document.getElementById('env-uv-label').textContent = uvLabel;
    document.getElementById('env-wind').innerHTML = d.wind_speed + '<span class="kpi-unit">km/h</span>';
    document.getElementById('env-pressure').innerHTML = d.pressure + '<span class="kpi-unit">hPa</span>';

    const comfort = (d.temp_in >= 22 && d.temp_in <= 26 && d.humidity >= 40 && d.humidity <= 60 && d.aqi < 80) ? 'Excellent' : 'Good';
    document.getElementById('env-comfort').textContent = comfort;

    const tempC = Math.max(0, 100 - Math.abs(d.temp_in - 24) * 10);
    const humC = Math.max(0, 100 - Math.abs(d.humidity - 50) * 2);
    const airC = Math.max(0, 100 - d.aqi);
    const noiseC = Math.max(0, 100 - (d.noise - 30) * 2);

    document.getElementById('env-temp-pct').textContent = tempC.toFixed(0) + '%';
    document.getElementById('env-temp-bar').style.width = tempC + '%';
    document.getElementById('env-hum-pct').textContent = humC.toFixed(0) + '%';
    document.getElementById('env-hum-bar').style.width = humC + '%';
    document.getElementById('env-air-pct').textContent = airC.toFixed(0) + '%';
    document.getElementById('env-air-bar').style.width = airC + '%';
    document.getElementById('env-air-bar').className = 'progress-fill ' + (airC > 60 ? 'pf-green' : airC > 30 ? 'pf-amber' : 'pf-red');
    document.getElementById('env-noise-pct').textContent = noiseC.toFixed(0) + '%';
    document.getElementById('env-noise-bar').style.width = Math.max(0, noiseC) + '%';

    push(tempChart, 0, d.time, d.temp_in);
    push(tempChart, 1, undefined, d.temp_out);
    tempChart.update();
    push(humChart, 0, d.time, d.humidity);
    push(humChart, 1, undefined, d.aqi);
    humChart.update();

    // ---- WATER ----
    document.getElementById('wat-tank').innerHTML = d.tank_level + '<span class="kpi-unit">%</span>';
    document.getElementById('wat-daily').innerHTML = d.daily_water + '<span class="kpi-unit">L</span>';
    document.getElementById('wat-motor').textContent = d.motor_status;
    document.getElementById('wat-quality').textContent = d.water_quality;
    document.getElementById('wat-filter').textContent = 'Filter life: ' + d.filter_life + '%';
    document.getElementById('tank-fill').style.height = d.tank_level + '%';
    document.getElementById('tank-pct-text').textContent = d.tank_level + '%';
    document.getElementById('wat-tank-pct').textContent = d.tank_level + '%';
    document.getElementById('wat-tank-bar').style.width = d.tank_level + '%';
    const daysLeft = ((d.tank_level / 100) * 1000 / d.daily_water).toFixed(1);
    document.getElementById('wat-days').textContent = daysLeft + ' days';
    document.getElementById('wat-days-sub').textContent = daysLeft + ' days remaining at current rate';
    document.getElementById('wat-hot').textContent = d.hot_water_temp + '°C';
    document.getElementById('wat-filter2').textContent = d.filter_life + '% remaining';

    push(watChart, 0, d.time, d.daily_water);
    watChart.update();

    // ---- APPLIANCES ----
    const apps = d.appliances;
    document.getElementById('appliance-list').innerHTML = Object.entries(apps).map(([name, watts]) => `
      <div class="appliance-row">
        <div class="app-icon" style="background:${appColor(name)}">${appIcon(name)}</div>
        <div>
          <div class="app-name">${name}</div>
          <div class="app-status">${watts > 0 ? 'Active' : 'Standby'}</div>
        </div>
        <div class="app-watts">${watts}W</div>
      </div>`).join('');

    appPieChart.data.labels = Object.keys(apps);
    appPieChart.data.datasets[0].data = Object.values(apps);
    appPieChart.update();
    appBarChart.data.labels = Object.keys(apps);
    appBarChart.data.datasets[0].data = Object.values(apps);
    appBarChart.update();

    const controlItems = ['AC','Lights','Fans','TV','Water Heater','Washing Machine'];
    document.getElementById('smart-controls').innerHTML = controlItems.map(name => {
      const on = (apps[name] || 0) > 0;
      return `<div class="card" style="display:flex;align-items:center;gap:14px">
        <div style="font-size:22px;width:36px;text-align:center">${appIcon(name)}</div>
        <div style="flex:1">
          <div style="font-size:13.5px;font-weight:600;color:var(--ink)">${name}</div>
          <div style="font-size:12px;color:${on ? 'var(--green)' : 'var(--ink4)'};margin-top:2px">${on ? 'On · ' + apps[name] + 'W' : 'Off'}</div>
        </div>
        <div class="toggle ${on ? 'on' : ''}"></div>
      </div>`;
    }).join('');

    // ---- AUTOMATIONS ----
    if (d.automations) {
      const autoIcons = ['🌅','🏃','☀️','🌙','🌧️'];
      document.getElementById('automation-list').innerHTML = d.automations.map((a, i) => `
        <div class="auto-row">
          <div class="auto-icon">${autoIcons[i] || '⚙️'}</div>
          <div class="auto-info">
            <div class="auto-name">${a.name}</div>
            <div class="auto-trigger" style="margin-top:2px">Trigger: ${a.trigger}</div>
            <div class="auto-action">Action: ${a.action}</div>
          </div>
          <div style="text-align:right">
            <span class="badge ${a.status === 'Active' ? 'badge-green' : 'badge-amber'}">${a.status}</span>
            <div class="auto-last" style="margin-top:5px">Last: ${a.last_run}</div>
          </div>
        </div>`).join('');
    }

    // ---- AI ----
    document.getElementById('insights-container').innerHTML = d.insights.map(i => `
      <div class="insight-item ${i.type}">
        <div class="insight-icon-wrap">${i.type === 'info' ? 'ℹ️' : i.type === 'warning' ? '⚠️' : '🔴'}</div>
        <div class="insight-body">
          <div class="insight-msg">${i.msg}</div>
          <div class="insight-action">${i.action} →</div>
        </div>
      </div>`).join('');

    push(aiPredChart, 0, d.time, d.total_energy);
    push(aiPredChart, 1, undefined, +(d.total_energy + (Math.random() - 0.5) * 0.8).toFixed(2));
    aiPredChart.update();

    const normalPts = Array.from({length: 15}, () => ({ x: +(Math.random() * 8 + 1).toFixed(2), y: +(Math.random() * 3 + 1).toFixed(2) }));
    anomChart.data.datasets[0].data = normalPts;
    anomChart.data.datasets[1].data = d.total_energy > 7 ? [{ x: d.total_energy, y: d.solar }] : [];
    anomChart.update();

    document.getElementById('ai-energy-score').innerHTML = Math.round(70 + d.solar / d.total_energy * 20) + '<span class="kpi-unit">/100</span>';
    document.getElementById('ai-water-score').innerHTML = Math.round(60 + d.tank_level / 5) + '<span class="kpi-unit">/100</span>';
    document.getElementById('ai-sec-score').innerHTML = (hasAlert ? 65 : 92) + '<span class="kpi-unit">/100</span>';

    const daysLeftAI = ((d.tank_level / 100) * 1000 / d.daily_water).toFixed(1);
    const tips = [
      { icon: '💡', tip: 'Shift Bedroom 2 loads to off-peak hours (23:00–06:00) to save approx ₹' + (Math.random() * 20 + 10).toFixed(0) + '/day.', color: 'var(--amber)' },
      { icon: '☀️', tip: `Peak solar window is 12:00–14:00 today. Schedule washing machine and dishwasher during this time.`, color: 'var(--green)' },
      { icon: '🌡️', tip: 'Setting AC to 26°C instead of 24°C reduces energy use by approximately 18–22%.', color: 'var(--blue)' },
      { icon: '💧', tip: `Water tank at ${d.tank_level}% — approximately ${daysLeftAI} days at current usage. Consider running motor during off-peak hours.`, color: 'var(--teal)' },
    ];
    document.getElementById('ai-recommendations').innerHTML = tips.map(t =>
      `<div style="display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-bottom:1px solid var(--border2)">
        <div style="width:36px;height:36px;border-radius:10px;background:var(--bg2);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">${t.icon}</div>
        <div style="font-size:13.5px;color:var(--ink2);line-height:1.5;padding-top:6px">${t.tip}</div>
      </div>`
    ).join('');

  } catch(e) { console.error('Fetch error:', e); }
}

// Local clock tick
setInterval(() => {
  document.getElementById('clock').textContent = new Date().toLocaleTimeString('en-IN', { hour12: false });
}, 1000);

// Data refresh every 3s
setInterval(update, 3000);
update();
</script>
</body>
</html>"""

@app.route('/')
def home():
    return HTML

@app.route('/data')
def data():
    return jsonify(generate_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
