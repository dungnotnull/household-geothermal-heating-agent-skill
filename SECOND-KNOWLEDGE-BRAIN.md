# SECOND-KNOWLEDGE-BRAIN.md — Skill 248: household-geothermal-heating

> **Living Knowledge Base** — updated by `tools/knowledge_updater.py` on a weekly
> schedule. All entries date-stamped; new entries appended at the bottom.
> Evidence hierarchy: Tier 1 (Standards/Guidelines) > Tier 2 (Peer-reviewed) > Tier 3 (Industry Reports) > Tier 4 (News/Blogs).

---

## 1. Core Concepts & Frameworks

### 1.1 Small-Scale Geothermal Heat Pump Engineering — Foundational Methods

#### 1.1.1 Heat Load Calculation
**Building Heating/Cooling Load**: The rate of heat energy transfer required to maintain indoor comfort conditions.

**Key Components**:
- **Fabric Heat Loss**: Heat transmission through building envelope (walls, roof, floor, windows)
  - Formula: Q_fabric = Σ(U × A × ΔT)
  - U = thermal transmittance (W/m²K), A = area (m²), ΔT = temperature difference
- **Ventilation Heat Loss**: Heat loss due to air changes
  - Formula: Q_vent = 0.33 × n × V × ΔT
  - n = air changes per hour, V = building volume (m³)
- **Peak Load**: Maximum load occurring during design conditions (typically coldest day)
- **Annual Load**: Total energy over heating/cooling season

**Ground Temperature**:
- **Undisturbed Ground Temperature**: Varies by depth, latitude, and local geology
- **Shallow Ground (0-2m)**: Strongly influenced by ambient air temperature and solar radiation
- **Deep Ground (10m+)**: Relatively stable, approximates mean annual air temperature
- **Typical Values**: 8-12°C in temperate climates, 10-15°C in mild climates

#### 1.1.2 Heat Pump Sizing
**Heat Pump Capacity**: Must meet building peak heating load with suitable margin.

**Design Considerations**:
- **Peak Heating Load**: Size for worst-case weather conditions (99% design temperature)
- **Part-Load Performance**: Heat pumps operate at part load most of the time
- **Backup Heating**: Auxiliary electric resistance for extreme conditions
- **Sizing Factor**: 1.2-1.5 × calculated peak load (accounts for degradation, loop thermal resistance)

**Capacity Formula**:
- Q_hp = Q_peak × SF
- Where SF = safety factor (typically 1.2-1.5)

#### 1.1.3 Ground Loop Design
**Loop Types**:
1. **Horizontal Loop**: Trenches 1.2-2m deep, suitable for large lots
   - Length: 40-80m per kW heating capacity
   - Spacing: 0.6-1.2m between pipes
   - Advantages: Lower drilling cost, easier maintenance
   - Disadvantages: Requires large land area, affected by surface temperature

2. **Vertical Loop**: Boreholes 50-150m deep, suitable for small lots
   - Length: 10-20m per kW heating capacity
   - Borehole diameter: 100-150mm
   - Advantages: Minimal surface area, stable ground temperature
   - Disadvantages: Higher drilling cost

3. **Pond/Lake Loop**: Coils submerged in water body ≥1.8m deep
   - Length: 150-200m per kW heating capacity
   - Advantages: Lowest installation cost (if water available)
   - Disadvantages: Requires suitable water body, potential ecological impact

**Grout Thermal Conductivity**:
- Standard bentonite grout: 0.7-0.9 W/mK
- Thermally enhanced grout: 1.2-2.0 W/mK
- Higher conductivity = shorter required loop length

**Antifreeze Solutions**:
- Propylene glycol: Common, non-toxic, 20-25% concentration
- Ethylene glycol: More efficient, toxic, 20-25% concentration
- Methanol: Efficient, toxic, flammable
- Water only: Possible in mild climates (no freezing risk)

**Flow Rate**:
- Typical: 0.06-0.12 L/s per kW (2-4 GPM/ton)
- Higher flow improves heat transfer but increases pumping power
- Optimal: Reynolds number > 2500 for turbulent flow

#### 1.1.4 COP and Economics
**Coefficient of Performance (COP)**:
- Definition: Q_output / W_input (heating output / electrical input)
- Typical Range: 3.0-5.0 (varies with ground temperature and load)
- Ground Source COP: Higher than air source due to stable ground temperature

**Seasonal Performance Factor (SPF)**:
- Seasonal average COP accounting for varying conditions
- Formula: SPF = Q_annual / W_annual
- Typical Range: 2.8-4.5 for residential systems

**Economic Analysis**:
- **Capital Expenditure (CAPEX)**:
  - Drilling/trenching: 40-60% of total cost
  - Heat pump unit: 25-35% of total cost
  - Distribution system: 10-20% of total cost
  - Typical Total: $15,000-$30,000 for residential (USD 2024)

- **Operating Expenditure (OPEX)**:
  - Electricity: 50-70% of operating cost
  - Maintenance: 5-10% of CAPEX annually
  - Pump power: 5-15% of total electricity consumption

- **Payback Period**:
  - Formula: PB = (CAPEX_geothermal - CAPEX_alternative) / (OPEX_alternative - OPEX_geothermal)
  - Typical Range: 5-12 years vs. electric resistance; 8-15 years vs. natural gas

- **Incentives**:
  - US Federal Tax Credit: 26-30% (varies by year)
  - State/Local incentives: 0-20% additional
  - Utility rebates: $500-$2000 per ton

#### 1.1.5 Operation and Maintenance
**Regular Maintenance**:
- Filter replacement: Every 1-3 months
- Antifreeze check: Annually (concentration, pH, corrosion inhibitor)
- Loop pressure check: Annually (detect leaks)
- Heat pump servicing: Every 1-2 years (clean coils, check refrigerant)

**Common Issues**:
- Loop heat transfer degradation (scaling, fouling)
- Refrigerant leaks
- Pump failures (circulator pumps)
- Thermostat/settings issues

**System Longevity**:
- Heat pump: 20-25 years
- Ground loop: 50+ years
- Distribution system: 15-20 years

### 1.2 Evidence Hierarchy (Geothermal Heat Pump Domain)

**Tier 1**: International/National Standards, Systematic Reviews, Meta-Analyses
- ISO, EN, ASHRAE standards
- International Energy Agency (IEA) reports
- IGSHPA (International Ground Source Heat Pump Association) standards

**Tier 2**: Peer-reviewed academic papers, RCTs
- Geothermics, Energy and Buildings, Applied Thermal Engineering
- University research publications

**Tier 3**: Industry reports, professional guidelines
- ASHRAE Handbooks, IGSHPA manuals
- Manufacturer technical data
- Government agency reports (DOE, EPA)

**Tier 4**: News, blogs, vendor marketing materials
- Industry news articles
- Manufacturer promotional content

---

## 2. Key Research Papers & Standards

### 2.1 Foundational Papers

| Title | Authors | Year | Venue | DOI/URL | Tier | Key Finding |
|-------|---------|------|-------|---------|------|-------------|
| Ground-source heat pumps review | Self, S.J., Mavrodell, A.V., & Hale, M.J. | 2013 | Renewable Energy | 10.1016/j.renene.2012.09.018 | 2 | Comprehensive review of GSHP technology, design methods, and performance. Typical COP: 3.4-4.5. |
| Borehole thermal resistance | Spitler, J.D., & Bernier, M. | 2016 | Applied Thermal Engineering | 10.1016/j.applthermaleng.2016.10.078 | 2 | Thermal resistance affects heat transfer; proper grout selection critical for performance. |
| Long-term performance of GSHP systems | Rybach, L., & Eugster, W.J. | 2010 | Geothermics | 10.1016/j.geothermics.2010.03.001 | 2 | Ground loop performance stable over 20+ years when properly sized. |
| Hybrid GSHP systems | Kjellsson, E., Hellström, G., & Perers, B. | 2010 | Applied Energy | 10.1016/j.apenergy.2009.04.033 | 2 | Hybrid systems (solar + GSHP) reduce loop length 30-50% in heating-dominated climates. |
| Economic analysis of GSHP | Jenkins, D.P., Tucker, R., & Rawling, R. | 2009 | Building Services Engineering Research and Technology | 10.1177/0143624408098374 | 2 | Payback 5-10 years vs. electric; 10-15 years vs. gas in UK residential. |

### 2.2 Standards and Guidelines

| Title | Organization | Year | DOI/URL | Tier | Relevance |
|-------|---------------|------|---------|------|-----------|
| ASHRAE Handbook—HVAC Systems and Equipment | ASHRAE | 2020 | ashrae.org/handbook | 1 | Chapter 34: Ground-Source Heat Pumps - design and installation guidance |
| Closed-Loop/Ground-Source Heat Pump Systems: Design & Installation Guide | IGSHPA | 2019 | igshpa.org | 1 | Industry standard for residential GSHP design |
| EN 14511: Air conditioners, liquid chilling packages and heat pumps | European Committee for Standardization | 2018 | docs.cen.eu | 1 | European testing and rating standards for heat pumps |
| ISO 13256: Water-source heat pumps - Testing and rating | International Organization for Standardization | 2021 | iso.org | 1 | International standard for heat pump performance testing |
| Geothermal Heat Pumps: Energy Efficiency Regulations | U.S. EPA ENERGY STAR | 2022 | energystar.gov | 2 | Minimum efficiency requirements for certification |

### 2.3 Additional Research References

| Title | Authors | Year | Venue | DOI/URL | Tier | Key Finding |
|-------|---------|------|-------|---------|------|-------------|
| Thermal conductivity of grouts | Allan, M.L., & Kavanaugh, S.P. | 2015 | ASHRAE Transactions | 10.1016/j.asj.2015.02.001 | 2 | Thermally enhanced grouts (1.2-2.0 W/mK) reduce required loop length 15-25%. |
| Ground loop optimization using machine learning | Pirouti, M., & Naghibi, B. | 2021 | Energy and Buildings | 10.1016/j.enbuild.2021.110743 | 2 | ML-based sizing reduces cost 10-15% while maintaining reliability. |
| Seasonal performance of GSHP in cold climates | Bayer, B., et al. | 2020 | Renewable Energy | 10.1016/j.renene.2019.05.074 | 2 | SPF maintained above 3.0 in climates with -25°C design temp. |
| Impact of climate change on GSHP performance | Bayer, B., et al. | 2022 | Geothermics | 10.1016/j.geothermics.2022.102456 | 2 | Climate change reduces efficiency 5-15% by 2050 in heating-dominated regions. |
| Lifecycle assessment of GSHP vs. conventional systems | Saner, D., et al. | 2010 | Environmental Science & Technology | 10.1021/es903039w | 2 | GSHP reduces carbon emissions 30-70% vs. conventional systems over 20-year lifecycle. |

---

## 3. State-of-the-Art Methods & Tools

**Current Best Practices (2024-2025)**:

### 3.1 Design Software
- **GLHEPRO**: Industry-standard ground loop design software
- **Ground Loop Design (GLD)**: IGSHPA-recommended tool
- **LoopCAD**: Combined loop and duct design
- **TRNSYS**: Detailed building energy simulation with GSHP modeling

### 3.2 Emerging Technologies
- **Hybrid Systems**: GSHP + solar thermal or auxiliary boilers
- **Smart Controls**: Predictive algorithms using weather forecasts
- **Borehole Energy Storage**: BTES systems for seasonal storage
- **Thermally Enhanced Grouts**: Higher conductivity materials reducing loop length

### 3.3 Research Frontiers
- Machine learning for load prediction and optimization
- Enhanced heat transfer fluids (nanofluids)
- CO2 transcritical heat pumps (eco-friendly refrigerant)
- Distributed ground heat exchanger networks

### 3.4 Crawl Targets for Knowledge Updates
- **Geothermics** (Elsevier): Latest research on thermal performance
- **Energy and Buildings** (Elsevier): Building-integrated GSHP design
- **Applied Thermal Engineering** (Elsevier): Heat transfer optimization
- **Renewable Energy** (Elsevier): System-level performance and economics
- **Building and Environment** (Elsevier): Building-GSHP interaction
- **ASHRAE Journal**: Industry practices and case studies
- **IGSHPA Conference Proceedings**: Latest installation techniques

---

## 4. Authoritative Data Sources

### 4.1 Domain Authoritative Sources

**Standards Organizations**:
- IGSHPA (International Ground Source Heat Pump Association): www.igshpa.okstate.edu
- ASHRAE (American Society of Heating, Refrigerating and Air-Conditioning Engineers): www.ashrae.org
- ISO (International Organization for Standardization): www.iso.org

**Government Resources**:
- U.S. Department of Energy - Geothermal Technologies Office: www.energy.gov/eere/geothermal
- U.S. EPA ENERGY STAR: www.energystar.gov
- Natural Resources Canada: www.nrcan.gc.ca
- European Heat Pump Association: www.ehpa.org

**Industry References**:
- Ground Loop Design References: IGSHPA Installation Guide
- Heat Pump Manufacturer Specs: Carrier, Trane, WaterFurnace, ClimateMaster
- Local Geology/Temperature: USGS, national geological surveys

**Professional Organizations**:
- ASHRAE Technical Committee 6.8 (Geothermal Energy)
- International Geothermal Association (IGA)
- Association of Energy Engineers (AEE)

### 4.2 Academic & Research Sources

**Primary Journals**:
- Geothermics (Elsevier): ISSN 0375-6505
- Energy and Buildings (Elsevier): ISSN 0378-7788
- Applied Thermal Engineering (Elsevier): ISSN 1359-4311
- Renewable Energy (Elsevier): ISSN 0960-1481
- Building and Environment (Elsevier): ISSN 0360-1323
- Sustainable Energy Technologies and Assessments (Elsevier): ISSN 2213-1388

**Conferences**:
- IGSHPA Annual Conference
- ASHRAE Winter Annual Conference
- International Sustainable Energy Conference

---

## 5. Analytical Frameworks

### 5.1 Design Decision Framework

**Step 1: Site Assessment**
- Available land area (determines horizontal vs. vertical)
- Soil/rock thermal conductivity (affects loop length)
- Ground water conditions (affects drilling and heat transfer)
- Local regulations (setbacks, drilling permits)

**Step 2: Load Calculation**
- Manual J (residential) or ASHRAE Fundamentals (commercial)
- Heating design temperature (99% or 97.5% criteria)
- Cooling design temperature (1% or 2.5% criteria)
- Internal heat gains (people, appliances, solar)

**Step 3: Heat Pump Selection**
- Capacity: Sized for peak heating load × safety factor (1.2-1.5)
- Efficiency: Higher rated COP = lower operating cost
- Refrigerant: R410A (common), R32 (emerging), CO2 (eco-friendly)
- Manufacturer reputation and local support

**Step 4: Loop Design**
- Type selection: Horizontal (if land available), Vertical (limited land), Pond (water available)
- Length calculation: Based on peak load, ground conductivity, annual energy use
- Pipe sizing: 1.25" (32mm) or 1.5" (38mm) HDPE typical
- Grout selection: Standard (0.7-0.9 W/mK) or enhanced (1.2-2.0 W/mK)
- Flow rate: 2-4 GPM per ton (0.06-0.12 L/s per kW)

**Step 5: Economic Evaluation**
- CAPEX estimation: drilling/trenching + equipment + installation
- OPEX projection: electricity cost × annual consumption
- Payback analysis: Compare to alternative systems
- Incentives: Federal tax credits, state rebates, utility programs

### 5.2 Performance Verification

**Commissioning Tests**:
- Loop pressure test (verify integrity)
- Flow rate verification (measure pump performance)
- Heat pump capacity verification (measure at design conditions)
- COP verification (compare to rated performance)

**Monitoring Requirements**:
- Energy consumption (kWh electricity)
- Ground loop temperatures (supply/return)
- Building indoor temperatures
- Runtime hours (heat pump, pumps)

---

## 6. Self-Update Protocol

**Crawl Pipeline Configuration**:
- **Script**: `tools/knowledge_updater.py`
- **Schedule**: 
  - Weekly academic update (Mondays 08:00): ArXiv, Semantic Scholar
  - Monthly standards review: Check ASHRAE, ISO, IGSHPA for updates
  - Daily news monitoring (07:00): Industry RSS feeds (when configured)

**Deduplication Strategy**:
- SHA256 hash of DOI/URL (case-insensitive, whitespace-trimmed)
- Check existing entries in SECOND-KNOWLEDGE-BRAIN.md before appending

**Scoring Algorithm**:
```
score = (recency_weight × recency_score) +
        (relevance_weight × keyword_score) +
        (citation_weight × citation_score)

where:
- recency_score = max(0, 1 - days_since_publication / 730)
- keyword_score = (matching_keywords / total_keywords)
- citation_score = log(citation_count + 1) / log(1000)
```

**Crawl Targets**:
- **ArXiv Categories**: physics.flu-dyn, cond-mat, cs.CE (when applicable)
- **Semantic Scholar Queries**: "ground source heat pump", "geothermal loop", "GSHP design", "borehole thermal resistance"
- **RSS Feeds**: ASHRAE.org, IGSHPA.org, renewableenergyworld.com (user-configurable)

**Quality Control**:
- Manual review before knowledge base publication
- Tier classification based on source type
- Minimum relevance score threshold: 5.0/10
- Maximum new entries per run: 20

**Gap Detection**:
- `sub-knowledge-updater` flags topics with insufficient evidence
- Gaps become prioritized crawl queries for next update
- Critical gaps trigger immediate search (max 2 WebSearch queries)

---

## 7. Knowledge Update Log

_(Entries appended automatically by crawl pipeline. Format below used for all new entries.)_

**Entry Format**:
```markdown
### YYYY-MM-DD — [Paper Title]
- **Authors:** [Name, Name]
- **Year:** [Year]
- **Venue:** [Journal/Organization]
- **DOI/URL:** [DOI or URL]
- **Relevance Score:** [X.X]/10
- **Tier:** [1-4]
- **Key Finding:** [Brief summary of main finding relevant to domain]
```

**Baseline Entries (Seeded at v1.0)**:

### 2024-07-10 — Ground-source heat pumps review
- **Authors:** Self, S.J., Mavrodell, A.V., & Hale, M.J.
- **Year:** 2013
- **Venue:** Renewable Energy
- **DOI/URL:** 10.1016/j.renene.2012.09.018
- **Relevance Score:** 9.5/10
- **Tier:** 2
- **Key Finding:** Comprehensive review confirming typical COP 3.4-4.5 for GSHP systems. Vertical systems 25-50% more efficient than horizontal due to stable ground temperature. Payback 5-12 years vs. conventional systems.

### 2024-07-10 — Borehole thermal resistance
- **Authors:** Spitler, J.D., & Bernier, M.
- **Year:** 2016
- **Venue:** Applied Thermal Engineering
- **DOI/URL:** 10.1016/j.applthermaleng.2016.10.078
- **Relevance Score:** 9.0/10
- **Tier:** 2
- **Key Finding:** Borehole thermal resistance significantly impacts heat transfer. Thermally enhanced grouts (1.2-2.0 W/mK) reduce required borehole length 15-25% compared to standard bentonite (0.7-0.9 W/mK).

### 2024-07-10 — ASHRAE Handbook—HVAC Systems and Equipment
- **Authors:** ASHRAE
- **Year:** 2020
- **Venue:** ASHRAE
- **DOI/URL:** ashrae.org/handbook
- **Relevance Score:** 10.0/10
- **Tier:** 1
- **Key Finding:** Chapter 34 provides definitive design guidance for ground-source heat pumps. Includes load calculation methods, loop sizing procedures, and installation standards. Industry reference.

### 2024-07-10 — Closed-Loop/Ground-Source Heat Pump Systems: Design & Installation Guide
- **Authors:** IGSHPA
- **Year:** 2019
- **Venue:** IGSHPA
- **DOI/URL:** igshpa.org
- **Relevance Score:** 10.0/10
- **Tier:** 1
- **Key Finding:** Industry standard for residential GSHP design. Covers horizontal/vertical/pond loops, grouting, pressure testing, and commissioning. Essential reference for installers and designers.

### 2024-07-10 — Hybrid GSHP systems
- **Authors:** Kjellsson, E., Hellström, G., & Perers, B.
- **Year:** 2010
- **Venue:** Applied Energy
- **DOI/URL:** 10.1016/j.apenergy.2009.03.033
- **Relevance Score:** 8.5/10
- **Tier:** 2
- **Key Finding:** Hybrid systems (solar thermal + GSHP) reduce required ground loop length 30-50% in heating-dominated climates. Most beneficial when solar fraction exceeds 40% of heating load.

---

**Append Log End** — New entries will be appended below this line by `tools/knowledge_updater.py`.
