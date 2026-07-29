# Domain Reference Documentation

## Overview

This document provides comprehensive reference material for the Small-Scale Geothermal Heat Pump Engineering domain, including formulas, standards, best practices, and implementation guidance.

## Building Heat Load Calculation

### Fabric Heat Loss

```
Q_fabric = Σ(U × A × ΔT)

where:
- Q_fabric = fabric heat loss (W)
- U = thermal transmittance (W/m²K)
- A = surface area (m²)
- ΔT = temperature difference (indoor - outdoor) (K)
```

**Typical U-values** (W/m²K):
| Component | Poor | Average | Good | Excellent |
|-----------|------|---------|------|-----------|
| Walls | 0.6-0.8 | 0.35 | 0.25 | 0.15 |
| Roof | 0.5-0.7 | 0.25 | 0.16 | 0.10 |
| Floor | 0.6-0.8 | 0.25 | 0.20 | 0.12 |
| Windows | 2.8-3.5 | 1.8 | 1.2 | 0.8 |
| Doors | 2.5-3.0 | 1.5 | 1.0 | 0.8 |

### Ventilation Heat Loss

```
Q_vent = 0.33 × n × V × ΔT

where:
- Q_vent = ventilation heat loss (W)
- n = air changes per hour (ACH)
- V = building volume (m³)
- ΔT = temperature difference (K)
```

**Typical Air Change Rates**:
| Building Type | ACH (Modern) | ACH (Older) |
|---------------|--------------|-------------|
| Residential (tight) | 0.3-0.5 | 1.0-1.5 |
| Residential (average) | 0.5-0.7 | 1.5-2.0 |
| Commercial | 0.5-1.0 | 1.0-2.0 |

### Peak Heating Load

```
Q_peak = Q_fabric + Q_vent

where:
- Q_peak = peak heating load (W)
- ΔT = T_indoor - T_design_heating

T_indoor = 20-21°C (typical)
T_design_heating = 99% or 97.5% design temperature
```

**Design Temperatures** (selected locations):
| Location | 99% Design Temp | HDD (base 18°C) |
|----------|-----------------|------------------|
| Montreal | -23°C | 4,500 |
| Toronto | -18°C | 4,200 |
| Vancouver | -5°C | 3,000 |
| Chicago | -18°C | 4,100 |
| New York | -8°C | 3,500 |
| London | -2°C | 2,600 |
| Berlin | -8°C | 3,400 |
| Stockholm | -14°C | 4,200 |

### Annual Heating Energy

```
E_annual = Q_peak × HDD / ΔT_design

where:
- E_annual = annual heating energy (Wh)
- HDD = heating degree days (base 18°C)
- ΔT_design = T_indoor - T_design_heating
```

## Heat Pump Sizing

### Required Capacity

```
Capacity_hp = Q_peak × SF

where:
- Capacity_hp = required heat pump capacity (W)
- SF = safety factor (1.2-1.5)

SF Selection:
- 1.2: Well-insulated buildings
- 1.3-1.4: Average insulation
- 1.5: Poor insulation or extreme climate
```

### Part-Load Performance

**Variable-Speed Heat Pumps**:
- Minimum modulation: 30-50% of rated capacity
- Optimal range: 50-80% for best efficiency
- Avoid: Frequent on/off cycling below 30%

**Single-Speed Heat Pumps**:
- Acceptable cycling: 3-6 starts per hour
- Concern: >6 starts per hour (oversized)
- Consider: Two-speed or buffer tank

## Ground Loop Design

### Loop Type Selection

| Factor | Horizontal | Vertical | Pond |
|--------|-----------|----------|------|
| **Land Area Required** | 2-3× building footprint | Minimal | Suitable water body |
| **Depth** | 1.2-2m trenches | 50-150m boreholes | ≥1.8m water depth |
| **Cost per kW** | Low ($600-900) | High ($1,200-2,000) | Lowest ($400-700) |
| **Efficiency** | Good | Best | Very Good |
| **Installation Disruption** | High (trenching) | Low (minimal footprint) | Low |
| **Climate Sensitivity** | High (surface temps) | Low (stable ground) | Medium |
| **Best For** | Large lots, shallow bedrock | Small lots, deep bedrock | Water available |

### Horizontal Loop Length

```
L_horizontal = (Q_peak × 1000) / (q × ΔT_loop)

where:
- L_horizontal = required pipe length (m)
- q = heat extraction rate (W/m)
  - Typical: 35-50 W/m
  - High conductivity: 50-65 W/m
  - Low conductivity: 25-35 W/m
- ΔT_loop = temperature drop across loop (°C)
  - Typical: 3-5°C

Simplified: L_horizontal ≈ 40-80 m per kW heating capacity
```

### Vertical Borehole Length

```
L_vertical = (Q_peak × 1000) / (q_b × ΔT_loop)

where:
- L_vertical = required borehole depth (m)
- q_b = heat extraction rate per meter (W/m)
  - Standard: 50-70 W/m
  - Adjusted: q_b = 50 × (k_ground / 1.5)
  - High conductivity: 70-90 W/m
  - Low conductivity: 35-50 W/m

Simplified: L_vertical ≈ 10-20 m per kW heating capacity
```

**Soil/Rock Thermal Conductivity** (k):
| Material | k (W/mK) | Loop Length Adjustment |
|----------|----------|----------------------|
| Wet clay | 1.0-1.5 | +30-50% |
| Dry clay | 0.8-1.2 | +40-70% |
| Wet sand | 1.5-2.5 | -10-30% |
| Dry sand | 0.5-1.0 | +50-100% |
| Rock (granite) | 2.5-3.5 | -30-50% |
| Rock (limestone) | 1.5-2.5 | -10-30% |
| Gravel | 0.7-1.2 | +40-60% |

### Pond Loop Length

```
L_pond = (Q_peak × 1000) / (q_p × ΔT_loop)

where:
- L_pond = required coil length (m)
- q_p = heat extraction rate (W/m)
  - Typical: 25-35 W/m

Simplified: L_pond ≈ 150-200 m per kW heating capacity

Minimum Requirements:
- Water depth: ≥1.8m (6 ft)
- Surface area: ≥150 m² per 5 kW
- Minimum volume: ≥300 m³ per 5 kW
```

### Pipe Specifications

**HDPE Pipe** (High-Density Polyethylene):
| Size | Nominal | OD | ID | Flow Capacity (L/min) | Application |
|------|---------|----|----|----------------------|-------------|
| 1.25" | 32mm | 40mm | 33mm | 15-25 | Small systems (<5 kW) |
| 1.5" | 38mm | 48mm | 40mm | 20-35 | Typical residential (5-10 kW) |
| 2" | 50mm | 60mm | 50mm | 30-50 | Large systems (10-20 kW) |

**Pressure Rating**:
- SDR-11: 160 psi at 23°C (standard for ground loops)
- SDR-9: 200 psi at 23°C (higher pressure applications)

**Flow Rate**:
```
Flow_total = Flow_rate_per_kW × Capacity_hp

where:
- Flow_total = total flow rate (L/min)
- Flow_rate_per_kW = 0.06-0.12 L/s per kW (2-4 GPM/ton)
  - Lower end: High ΔT (5°C) designs
  - Higher end: Low ΔT (3°C) designs

Reynolds Number (for turbulent flow):
Re = (ρ × v × D) / μ

Target: Re > 2500 for turbulent flow
where:
- ρ = fluid density (~1000 kg/m³ for water)
- v = fluid velocity (m/s)
- D = pipe diameter (m)
- μ = dynamic viscosity (~0.001 Pa·s for water at 20°C)
```

### Grout Selection

**Thermal Conductivity** (k):
| Grout Type | k (W/mK) | Cost | Application |
|------------|----------|------|-------------|
| Standard Bentonite | 0.7-0.9 | Low | Most applications |
| Thermally Enhanced #1 | 1.2-1.5 | Medium | Low k ground |
| Thermally Enhanced #2 | 1.5-2.0 | High | Very low k ground |
| Concrete | 1.4-1.8 | Medium | Structural fills |
| Sand-Bentonite | 0.9-1.2 | Low-Medium | Moderate enhancement |

**Selection Guidelines**:
- k_ground < 1.5 W/mK → Use enhanced grout (1.2+ W/mK)
- k_ground ≥ 1.5 W/mK → Standard grout acceptable
- Deep boreholes (>150m) → Consider enhanced grout for cost savings

### Antifreeze Solutions

**Properties**:
| Solution | Freeze Point (25%) | Toxicity | COP Impact | Cost |
|----------|-------------------|----------|------------|------|
| Propylene Glycol | -10°C | Non-toxic | ~5% reduction | Medium |
| Ethylene Glycol | -12°C | Toxic | ~3% reduction | Low |
| Methanol | -15°C | Toxic, Flammable | ~2% reduction | Low |
| Water Only | 0°C | None | None | Low |

**Selection Guidelines**:
- Ground temp > 5°C → Water only possible
- Ground temp 0-5°C → 20% propylene glycol
- Ground temp < 0°C → 25% propylene glycol
- Ecological concerns → Propylene glycol only
- Secondary containment available → Ethylene glycol acceptable

## Heat Pump Performance

### COP Calculation

```
COP = COP_rated × f_T × f_load

where:
- COP_rated = manufacturer rating at ARI/ISO conditions
  - ARI 320/330: 21°C entering water, -8.3°C source
  - ISO 13256: 20°C entering water, 0°C source
  - Typical ratings: 3.5-4.5

- f_T = temperature correction factor
  - f_T = 1 - 0.02 × (EWT_entering - 10)
  - EWT = entering water temperature
  - Higher EWT → Better COP

- f_load = part-load correction
  - Variable-speed: 0.95-1.05 (depends on modulation)
  - Single-speed: 0.85-0.95 (cycling losses)
```

**Entering Water Temperature (EWT) Impact**:
| EWT | f_T Factor | COP (rated 4.0) |
|-----|-----------|-----------------|
| -5°C | 0.70 | 2.8 |
| 0°C | 0.80 | 3.2 |
| 5°C | 0.90 | 3.6 |
| 10°C | 1.00 | 4.0 |
| 15°C | 1.10 | 4.4 |

### Seasonal Performance Factor (SPF)

```
SPF = COP × f_seasonal

where:
- f_seasonal = 0.85-0.95 (accounts for defrost, pump power, degradation)

Typical SPF ranges:
- Cold climate: 2.8-3.4
- Temperate climate: 3.2-3.8
- Mild climate: 3.5-4.2

Components affecting SPF:
- Heat pump COP: 70-80% of total
- Circulating pump power: 5-10% of total
- Defrost cycles: 5-10% reduction
- Control losses: 3-5% reduction
- Degradation over time: 5-10% reduction
```

## Economic Analysis

### CAPEX Estimation

**Component Breakdown** (typical residential 10 kW system):
| Component | Cost Range | % of Total |
|-----------|------------|------------|
| Ground Loop | $6,000-12,000 | 40-60% |
| Heat Pump Unit | $4,000-6,000 | 25-35% |
| Distribution System | $2,000-4,000 | 10-20% |
| Installation Labor | $2,000-4,000 | 15-20% |
| **Total** | **$14,000-26,000** | **100%** |

**Loop Installation Costs**:
| Type | Cost per meter | Notes |
|------|--------------|-------|
| Horizontal trenching | $15-25/m | Includes excavation, backfill |
| Vertical drilling | $40-70/m | Includes rig, grout, casing |
| Pond coil | $10-20/m | Includes coil, anchors |

### OPEX Estimation

**Annual Electricity Consumption**:
```
E_annual_kWh = E_annual_kWh_heat / SPF

where:
- E_annual_kWh = calculated from heating load
- SPF = seasonal performance factor

Typical values (200 m² house, temperate climate):
- Heating demand: 15,000 kWh/year
- SPF 3.2: 4,700 kWh/year
- SPF 3.8: 3,900 kWh/year
```

**Annual Costs**:
```
OPEX_annual = E_annual_kWh × electricity_cost + maintenance_cost

where:
- maintenance_cost = 0.05-0.10 × CAPEX_total annually
  - Professional service: $200-400/year
  - Filter changes: $50-100/year
  - Antifreeze check: $50-100/year
```

### Payback Analysis

```
Savings_annual = OPEX_alternative - OPEX_annual

where:
- OPEX_alternative = annual fuel cost for alternative system

Alternative Systems (typical efficiency):
- Electric resistance: 98% efficient
- Natural gas furnace: 85-95% efficient
- Oil boiler: 80-90% efficient
- Propane furnace: 85-92% efficient
- Air-source heat pump: COP 1.5-2.5 (varies with climate)

Payback_years = (CAPEX_total - CAPEX_alternative - incentives) / Savings_annual

Typical Payback Periods:
- vs. Electric resistance: 5-8 years
- vs. Natural gas: 8-15 years
- vs. Oil: 6-12 years
- vs. Air-source HP: 8-12 years
```

### Net Present Value (NPV)

```
NPV = -CAPEX + Σ(Net_cash_flow_t / (1 + r)^t)

where:
- Net_cash_flow_t = Savings_annual - OPEX_annual (year t)
- r = discount rate (typically 3-5%)
- t = year (1-20 for residential systems)

Example calculation:
- CAPEX: $20,000
- Annual savings: $1,500
- Discount rate: 4%
- System life: 20 years
- NPV ≈ $5,600 (positive = economically viable)
```

### Incentives

**United States** (2024):
| Program | Incentive | Notes |
|---------|-----------|-------|
| Federal Tax Credit | 26% of qualified cost | Expires 2032 |
| State Credits | 0-30% additional | Varies by state |
| Utility Rebates | $500-2,000/ton | Varies by utility |
| Property Tax Exemption | Varies | Some states |

**Example Incentive Impact**:
- System cost: $20,000
- Federal credit (26%): -$5,200
- State credit (20%): -$4,000
- Utility rebate: -$1,000
- **Net cost**: $9,800
- **Effective payback**: 4-7 years

## Operation & Maintenance

### Maintenance Schedule

**Monthly**:
- Check system pressures (should be stable ±5 psi)
- Monitor entering/leaving water temperatures
- Verify normal operation (no unusual sounds/leaks)

**Quarterly**:
- Inspect air filters (if forced-air distribution)
- Check thermostat operation
- Review energy consumption (compare to baseline)

**Annually**:
- Professional inspection and servicing
- Check antifreeze concentration and pH
- Verify loop pressure and integrity
- Clean heat pump coils (if accessible)
- Test safety controls
- Document performance metrics

**Every 3-5 Years**:
- Complete system performance evaluation
- Pump wear assessment
- Refrigerant check (if accessible)

### Common Issues & Troubleshooting

| Symptom | Possible Cause | Diagnostic | Action |
|---------|----------------|------------|--------|
| Reduced heating output | Loop scaling/fouling | Check ΔT across loop, flow rate | Flush loop, chemical cleaning |
| High electricity use | Low refrigerant | Check superheat/subcooling | Find leak, recharge |
| Short cycling | Oversized unit | Measure run time vs. load | Verify load calculation |
| Low delta-T | Flow too low | Check pump performance | Verify pump, check loop integrity |
| Freezing protection trips | Low antifreeze concentration | Test antifreeze | Adjust concentration |
| High loop pressure | Blocked flow | Check isolation valves | Clear obstruction, flush loop |

### System Longevity

**Expected Life** (with proper maintenance):
| Component | Expected Life | Maintenance Impact |
|-----------|--------------|-------------------|
| Heat Pump | 20-25 years | +5 years with regular service |
| Ground Loop | 50+ years | Minimal impact |
| Distribution System | 15-20 years | +3-5 years with maintenance |
| Circulating Pumps | 10-15 years | +3-5 years with maintenance |
| Controls/Thermostat | 10-15 years | Minimal impact |

## Standards & References

**Key Standards**:
1. **ASHRAE Handbook—HVAC Systems and Equipment** (2020)
   - Chapter 34: Ground-Source Heat Pumps
   - Design guidance, sizing procedures

2. **IGSHPA Installation Guide** (2019)
   - Residential and light commercial systems
   - Installation best practices

3. **ISO 13256** (2021)
   - Water-source heat pump testing and rating
   - Performance certification

4. **EN 14511** (2018)
   - European heat pump testing standard
   - Efficiency requirements

---

**Document Version**: 1.0.0
**Last Updated**: 2026-07-27
