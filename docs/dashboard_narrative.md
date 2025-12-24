# 📊 Dashboard Narrative & Storytelling Guide

This document provides guidance for enhancing the Power BI dashboard with decision-ready storytelling elements.

---

## Executive Summary Page

Every effective dashboard should open with an executive summary that answers: **"What happened, why should I care, and what should I do?"**

### Recommended Elements

1. **Key Performance Indicators (KPIs)** - Top of page
   - Total Revenue: `$XX.X M`
   - Total Gross Profit: `$XX.X M`
   - Average Profit Margin: `XX.X%`
   - Vendor Count: `XXX`
   - Inventory Turnover Rate: `X.XX`

2. **Trend Sparklines** - Next to each KPI
   - Show month-over-month direction
   - Color code: green for positive, red for negative

3. **Top 3 Insights** - Prominent callout boxes
   ```
   ⚠️ INSIGHT 1: Top 10 vendors account for 65% of purchases
   → Risk: Vendor concentration creates supply chain vulnerability
   
   💰 INSIGHT 2: Bulk purchases yield 72% lower unit costs
   → Opportunity: Expand bulk purchasing agreements
   
   📦 INSIGHT 3: $2.7M tied up in slow-moving inventory
   → Action: Review markdown/liquidation strategy
   ```

---

## Vendor Performance Page

### Recommended Visuals

1. **Vendor Pareto Chart**
   - X-axis: Vendors (sorted by revenue contribution)
   - Y-axis (bar): Revenue
   - Y-axis (line): Cumulative % of total revenue
   - Highlight the 80/20 breakpoint

2. **Vendor Quadrant Matrix**
   - X-axis: Profit Margin
   - Y-axis: Sales Volume
   - Quadrants:
     - High Margin + High Volume = ⭐ Stars
     - High Margin + Low Volume = 💎 Gems (grow these)
     - Low Margin + High Volume = 🐄 Cash Cows (optimize)
     - Low Margin + Low Volume = ❓ Question Marks (review)

3. **Vendor Risk Scorecard**
   - Dependency score (% of purchases)
   - Lead time performance
   - Freight cost efficiency

---

## Inventory Analysis Page

### Recommended Visuals

1. **Inventory Turnover Heatmap**
   - Rows: Product categories
   - Columns: Months
   - Color: Turnover rate (red = slow, green = fast)

2. **Dead Stock Identifier**
   - Products with turnover < 0.5
   - Estimated capital locked
   - Days since last sale

3. **Stock-to-Sales Ratio Trend**
   - Monthly trend line
   - Target range overlay
   - Anomaly callouts

---

## Financial Impact Page

### Recommended Visuals

1. **Margin Waterfall Chart**
   - Starting: Gross Revenue
   - Subtract: Cost of Goods
   - Subtract: Freight
   - Subtract: Excise Tax
   - Ending: Net Profit

2. **Cost Breakdown Pie/Donut**
   - Purchase cost %
   - Freight %
   - Tax %
   - Other %

3. **Profitability by Category**
   - Stacked bar showing margin by product category
   - Sort by worst to best margin

---

## Storytelling Best Practices

### Do's ✅

1. **Lead with the "So What?"**
   - Don't just show data, tell what it means
   - Every visual should answer a business question

2. **Use Natural Language Insights**
   - "Revenue increased 15% MoM" → "Strong growth driven by seasonal demand"
   - "10 vendors = 65% purchases" → "High vendor concentration creates risk"

3. **Provide Context**
   - Show targets/benchmarks
   - Show prior period comparisons
   - Show industry averages if available

4. **Call to Action**
   - Each insight should suggest an action
   - "Consider..." or "Recommend..." language

5. **Use Consistent Color Coding**
   - Green = Good/Growth
   - Red = Bad/Decline
   - Yellow = Warning/Attention
   - Blue = Neutral/Information

### Don'ts ❌

1. **Don't overwhelm with visuals**
   - Max 4-6 visuals per page
   - White space is valuable

2. **Don't use 3D charts**
   - They distort perception
   - Stick to 2D

3. **Don't hide methodology**
   - Include calculation tooltips
   - Document assumptions

4. **Don't forget mobile view**
   - Design for different screen sizes
   - Priority ranking for elements

---

## Methodology Page

Every analytical dashboard should include a methodology section:

### Data Sources
- Source system names
- Data refresh frequency
- Date range covered

### Calculations
| Metric | Formula | Notes |
|--------|---------|-------|
| Gross Profit | Sales Revenue - Purchase Cost | |
| Profit Margin | Gross Profit / Sales Revenue × 100 | Zero sales = 0% |
| Stock Turnover | Sales Quantity / Purchase Quantity | < 1 = excess inventory |
| Sales:Purchase Ratio | Sales $ / Purchase $ | > 1 = profitable |

### Data Quality Notes
- Missing values handling
- Known data issues
- Exclusions/filters applied

### Assumptions
- Document any business assumptions
- Document any technical assumptions

---

## Implementation Checklist

- [ ] Add executive summary page
- [ ] Add key insights callout boxes
- [ ] Create vendor quadrant matrix
- [ ] Add methodology/about page
- [ ] Implement consistent color scheme
- [ ] Add natural language insights
- [ ] Include action recommendations
- [ ] Add comparison benchmarks
- [ ] Mobile-optimize layout

---

## Resources

- [Power BI Storytelling Best Practices](https://docs.microsoft.com/en-us/power-bi/create-reports/power-bi-report-add-visualizations-i)
- [The Big Book of Dashboards](https://www.bigbookofdashboards.com/)
- [Storytelling with Data](https://www.storytellingwithdata.com/)
