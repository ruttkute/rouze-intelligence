# ROUZE EXECUTION GUIDE: Vilnius Caravan Investment Research

## QUICK START COMMANDS

### 1. WHERE TO PLACE FILES

**Download the research brief and place it here:**
```bash
# On your laptop, place in Rouze project folder:
~/Desktop/rouze/rouze_agent/pitches/ROUZE_Caravan_Rental_Research_Brief.md
```

**Alternative path if different structure:**
```bash
/path/to/your/rouze/folder/ROUZE_Caravan_Rental_Research_Brief.md
```

---

## 2. HOW TO EXECUTE WITH ROUZE

### Option A: Direct Command (If Rouze has CLI)
```bash
cd ~/Desktop/rouze/rouze_agent
python scripts/rouze_research.py --input pitches/ROUZE_Caravan_Rental_Research_Brief.md --output deliveries/
```

### Option B: Manual Research Execution
If Rouze doesn't have automated execution, break down into phases:

**Phase 1: Market Demand (Days 1-2)**
```bash
python scripts/rouze_scrape.py --query "caravan rental Vilnius Airbnb"
python scripts/rouze_scrape.py --query "mobile home Vilnius booking.com"
python scripts/rouze_scrape.py --query "Lithuania tourism statistics caravans"
```

**Phase 2: Positioning Analysis (Days 2-3)**
```bash
python scripts/rouze_analyze.py --input data/market_demand --method positioning_strategy
```

**Phase 3: Bank Research (Days 3-5)**
```bash
python scripts/rouze_scrape.py --query "Swedbank Lithuania business loan 50000"
python scripts/rouze_scrape.py --query "DNB Norway business loan 550000 NOK"
# Repeat for all banks listed in brief
```

**Phase 4: Financial Analysis (Days 5-7)**
```bash
python scripts/rouze_analyze.py --input data/bank_loans --method financial_modeling
```

---

## 3. ROUZE CONFIGURATION

### Create/Update Rouze Config File
**File:** `rouze_agent/config/caravan_research_config.yaml`

```yaml
project:
  name: "Vilnius Caravan Investment Analysis"
  code: "VCR-2025-001"
  priority: "HIGH"
  
research_phases:
  - phase: "market_demand"
    duration_days: 2
    output: "market_demand_report.md"
    
  - phase: "positioning_strategy"
    duration_days: 1
    output: "positioning_analysis.md"
    
  - phase: "bank_comparison"
    duration_days: 2
    output: "loan_comparison_report.md"
    
  - phase: "financial_viability"
    duration_days: 2
    output: "financial_projections.xlsx"

data_sources:
  real_estate:
    - "airbnb.com"
    - "booking.com"
    - "aruodas.lt"
    
  banks_lithuania:
    - "swedbank.lt"
    - "seb.lt"
    - "luminor.lt"
    - "sb.lt"
    
  banks_norway:
    - "dnb.no"
    - "nordea.no"
    - "sparebank1.no"
    
  tourism_data:
    - "lithuania.travel"
    - "tourism.lt"
    - "stat.gov.lt"

output:
  format: "html"
  location: "deliveries/"
  filename: "Vilnius_Caravan_Investment_Analysis_{date}.html"
```

---

## 4. EXPECTED ROUZE OUTPUTS

After completion, you should have these files in `rouze_agent/deliveries/`:

```
deliveries/
├── Vilnius_Caravan_Investment_Analysis_2025-11-01.html (MAIN REPORT)
├── market_demand_data.json
├── positioning_strategy_analysis.md
├── bank_comparison_lithuania.csv
├── bank_comparison_norway.csv
├── loan_calculator.xlsx
├── payback_scenarios.xlsx
└── raw_data/
    ├── airbnb_listings.json
    ├── booking_data.json
    ├── bank_terms_lithuania.json
    └── bank_terms_norway.json
```

---

## 5. MANUAL RESEARCH WORKFLOW (If Rouze Not Automated)

### Step 1: Market Demand Research
**What to search:**
1. Go to Airbnb.com → Search "Vilnius" → Filter: "Campers/RVs"
2. Note: Number of listings, prices, review frequency
3. Go to Booking.com → Search "Vilnius caravan" or "mobile home"
4. Visit lithuania.travel → Tourism statistics
5. Google: "caravan rental demand Lithuania statistics"

**Record in:** `data/market_demand_raw.txt`

---

### Step 2: Bank Research - Lithuania
**Banks to visit:**
1. **Swedbank:** www.swedbank.lt → Business → Loans → Investment loans
2. **SEB:** www.seb.lt → Business loans
3. **Luminor:** www.luminor.lt → Business → Financing
4. **Šiaulių Bankas:** www.sb.lt → Business loans

**For each bank, record:**
- Interest rate for €50,000
- Loan term options (5/7/10 years)
- Requirements (income, collateral, credit score)
- Processing fees
- Monthly payment calculation

**Record in:** `data/banks_lithuania.csv`

---

### Step 3: Bank Research - Norway
**Banks to visit:**
1. **DNB:** www.dnb.no → Bedrift (Business) → Lån (Loans)
2. **Nordea:** www.nordea.no → Business loans
3. **SpareBank 1:** www.sparebank1.no → Bedriftslån

**Important:** Check if they offer loans for foreign property (Lithuania)

**Record in:** `data/banks_norway.csv`

---

### Step 4: Financial Calculations
**Use this spreadsheet structure:**

| Strategy | Caravans | Occupancy | Annual Revenue | Loan Payment | Payback Months |
|----------|----------|-----------|----------------|--------------|----------------|
| Budget   | 6        | 70%       | €XXX          | €XXX         | XX             |
| Premium  | 4        | 50%       | €XXX          | €XXX         | XX             |
| Hybrid   | 5        | 60%       | €XXX          | €XXX         | XX             |

**Calculate:**
- Monthly revenue = (Caravans × €30/night × 30 days × Occupancy%)
- Annual revenue = Monthly × 12
- Operating costs = Annual revenue × 0.30
- Net profit = Revenue - Operating costs
- Available for loan = Net profit - living expenses
- Payback months = €50,000 ÷ (Available per month)

**Record in:** `data/financial_projections.xlsx`

---

## 6. VERIFICATION CHECKLIST

Before considering research complete:

**Market Demand:**
- [ ] Found at least 10 active caravan rental listings in Vilnius
- [ ] Verified occupancy rates from review frequency
- [ ] Confirmed €30/night is competitive pricing
- [ ] Identified peak vs low season patterns

**Bank Loans:**
- [ ] Researched minimum 5 Lithuanian banks
- [ ] Researched minimum 3 Norwegian banks
- [ ] Confirmed exact interest rates (not estimates)
- [ ] Verified eligibility requirements
- [ ] Calculated total loan cost (principal + interest)

**Financial Viability:**
- [ ] Calculated payback for at least 3 strategies
- [ ] Included realistic operating costs (30%)
- [ ] Accounted for seasonal occupancy variance
- [ ] Stress-tested with worst-case scenario (-20% revenue)

**Recommendations:**
- [ ] Clear recommendation: Which strategy?
- [ ] Clear recommendation: Which bank?
- [ ] Clear recommendation: Which land plot?
- [ ] Risk mitigation strategies documented

---

## 7. ROUZE PROMPT (If Using AI Agent)

**Paste this into Rouze:**

```
Execute comprehensive market research for Vilnius caravan rental investment:

RESEARCH SCOPE:
1. Market demand analysis for caravan rentals in Vilnius (short-term & long-term)
2. Positioning strategy comparison (5 strategies)
3. Bank loan comparison: Lithuania vs Norway for €50,000
4. Financial viability and payback period calculations

CONTEXT:
- Investment: €50,000 loan
- Caravan cost: €8,000 per unit
- Land: Already identified (13 plots in Vilnius)
- Target: Short-term rental €30/night OR long-term €500/month

DELIVERABLES:
- HTML comprehensive report
- Bank comparison table (exact interest rates)
- Payback calculation for each strategy
- Clear GO/NO-GO recommendation

DATA SOURCES:
- Airbnb, Booking.com (demand data)
- Lithuanian banks: Swedbank, SEB, Luminor, Šiaulių Bankas
- Norwegian banks: DNB, Nordea, SpareBank 1
- Tourism statistics: lithuania.travel
- Competitor analysis

OUTPUT FORMAT: Professional HTML report with:
- Executive summary
- Comparison tables
- Financial projections
- Implementation roadmap

PRIORITY: Loan comparison (biggest financial impact) and realistic occupancy rates (determines viability).

Start with Phase 1: Market demand research.
```

---

## 8. TIMELINE

**Total research time:** 5-7 days

**Daily breakdown:**
- **Day 1:** Market demand - Airbnb/Booking.com analysis
- **Day 2:** Market demand - Tourism stats, competitor analysis
- **Day 3:** Bank research - Lithuanian banks (5 banks)
- **Day 4:** Bank research - Norwegian banks (3 banks)
- **Day 5:** Financial modeling - Calculate all scenarios
- **Day 6:** Report writing - Compile findings
- **Day 7:** Review and recommendations - Finalize

---

## 9. TROUBLE SHOOTING

**Problem:** Rouze can't access certain websites
**Solution:** Use web_search tool for publicly available data, manually input bank data from official websites

**Problem:** No clear data on occupancy rates
**Solution:** Use review frequency as proxy (reviews per month × 2 = approximate monthly bookings)

**Problem:** Banks don't publish rates online
**Solution:** Call bank business loan department, request loan simulation

**Problem:** Conflicting data from different sources
**Solution:** Use most conservative estimate, note variance in report

---

## 10. FINAL OUTPUT LOCATION

**Main report will be saved to:**
```
~/Desktop/rouze/rouze_agent/deliveries/Vilnius_Caravan_Investment_Analysis_2025-11-01.html
```

**Open with any web browser or share with stakeholders**

---

## CONTACT FOR CLARIFICATION

If research reveals need for client input:
- Citizenship status (affects loan eligibility)
- Current income level (affects loan approval)
- Risk tolerance (affects strategy recommendation)

Document these as "DECISION POINTS REQUIRING CLIENT INPUT" in final report.

---

**RESEARCH STATUS:** Ready to execute
**PRIORITY:** HIGH - €50,000+ investment decision
**DEADLINE:** 7 days from start

Execute systematically. Document thoroughly. Deliver actionable intelligence.
