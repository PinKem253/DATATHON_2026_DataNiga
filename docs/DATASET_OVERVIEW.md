# Dataset Overview & Domain Explanation

## 📋 Project Context

**Challenge**: Datathon 2026 - E-commerce Sales Forecasting & Analysis  
**Goal**: Predict daily revenue (sales forecasting) using operational, transaction, and analytical data  
**Time Period**: 2012-2022 (11 years)  
**Business Type**: E-commerce Platform (Fashion/Streetwear focus)

---

## 🏗️ Data Architecture

```
DATATHON_2026_DataNiga/
├── Master Data (Reference/Dimension Tables)
│   ├── products.csv (2,412 products)
│   ├── customers.csv (121,930 customers)
│   └── geography.csv (1,000 locations)
│
├── Transaction Data (Fact Tables)
│   ├── orders.csv (646,945 orders)
│   ├── order_items.csv (714,669 line items)
│   ├── payments.csv (646,945 payments)
│   ├── shipments.csv (646,945 shipments)
│   └── returns.csv (36,142 returns)
│
└── Analytics Data (KPIs & External)
    ├── sales.csv (3,833 daily aggregates - TARGET)
    ├── web_traffic.csv (10,000 daily web metrics)
    └── inventory.csv (product stock levels)
```

---

## 📊 Detailed Table Structure

### **1. MASTER DATA - Reference Tables**

#### **products.csv** (2,412 unique SKUs)
- **Purpose**: Product master data  
- **Key Columns**:
  - `product_id`: Unique product identifier
  - `product_name`: Product name/SKU
  - `category`: Streetwear, Outdoor, Casual, GenZ (4 categories)
  - `segment`: Activewear, Everyday, Performance, Balanced... (8 segments)
  - `size`: S, M, L, XL (uniform distribution)
  - `color`: 10 colors (balanced)
  - `price`: Selling price (mean: $7,800)
  - `cogs`: Cost of goods sold (mean: $6,200)
  - **Margin**: price - cogs (avg ~27%)

**Key Insight**: 
- Balanced product portfolio across categories/sizes
- No products with negative margin ✅
- Price range: high-end fashion/streetwear

---

#### **customers.csv** (121,930 unique buyers)
- **Purpose**: Customer master data  
- **Key Columns**:
  - `customer_id`: Unique customer identifier
  - `city`: 42 Vietnamese cities (fairly balanced)
  - `zip`: Geography code → geography.csv
  - `gender`: Female (48.9%), Male (47.1%), Non-binary (4%)
  - `age_group`: 18-24, 25-34, 35-44, 45-54, 55+ (peak: 25-34 at 29.8%)
  - `signup_date`: Customer registration date (3,941 unique dates)
  - `acquisition_channel`: organic_search (29.9%), social_media (20%), paid_search (19.9%)...

**Key Insight**:
- Diverse customer base across geographies
- Most customers acquired through organic/paid search
- Relatively balanced demographics

---

#### **geography.csv** (1,000 locations)
- **Purpose**: Master geography/postal code data  
- **Key Columns**:
  - `zip`: Postal code
  - Likely: region, province, logistics info

**Link**: customers.zip → geography.zip (referential integrity ✅)

---

### **2. TRANSACTION DATA - Fact Tables**

#### **orders.csv** (646,945 orders from 121,930 customers)
- **Purpose**: Order header/master record  
- **Key Columns**:
  - `order_id`: Unique order identifier
  - `customer_id` → customers.customer_id ✅
  - `order_date`: When order was placed (2012-2022)
  - `zip`: Delivery location
  - `order_status`: delivered (79.9%), cancelled (9.2%), returned (5.6%), shipped (2.1%), paid (2.1%)
  - `payment_method`: credit_card (55.1%), paypal (15%), COD (14.9%), apple_pay (10%), bank_transfer (5%)
  - `device_type`: mobile (45.1%), desktop (40%), tablet (14.9%)
  - `order_source`: organic_search (28%), paid_search (21.9%), social_media (20%)

**Key Insight**:
- **Imbalanced order status**: 80% delivered (learning challenge)
- **Delivery method preference**: credit_card dominant
- **Channel mix**: Multi-channel (search, social, email...)
- **Mobile-first**: 45% orders from mobile devices

---

#### **order_items.csv** (714,669 line items)
- **Purpose**: Order detail/line items  
- **Relationship**: orders.order_id → order_items.order_id (1:N) ✅
- **Key Columns**:
  - `order_id`: Link to orders
  - `product_id` → products.product_id ✅
  - `quantity`: Items per order line
  - `unit_price`: Price at time of purchase
  - `discount_amount`: Promotional discount (0-2,419)
  - `promo_id`: Promotion identifier (38.7% missing ⚠️)
  - `promo_id_2`: Secondary promo? (99.97% missing ⚠️⚠️ - DATA QUALITY ISSUE)

**Key Insight**:
- **High discount volatility**: 105K outliers detected (>$2,400)
- **Sparse promotion data**: Can't use promo_id reliably
- **Avg items per order**: ~1.1 (mostly single-item orders)

---

#### **payments.csv** (646,945 payments)
- **Purpose**: Payment records  
- **Relationship**: orders.order_id → payments.order_id (1:1) ✅
- **Key Columns**:
  - `order_id`: Link to orders
  - `payment_method`: Type of payment
  - `payment_value`: Amount paid (mean: $1,280)
  - `installments`: Payment plan (1, 2, 3... months)

**Key Insight**:
- **30K payment outliers** detected (>$72K transactions)
- **Installments available**: Multi-payment options

---

#### **shipments.csv** (646,945 shipments)
- **Purpose**: Logistics/shipping records  
- **Relationship**: orders.order_id → shipments.order_id (1:1) ✅
- **Key Columns**:
  - `order_id`: Link to orders
  - `ship_date`: When shipped (✅ always > order_date)
  - `delivery_date`: Estimated/actual delivery (✅ always > ship_date)
  - `shipping_fee`: Cost (mean: ~$0.80, range -1.72 to 5.20)
  - **76K shipping fee outliers** (mostly ~$5 flat rate)

**Key Insight**:
- **Tight shipping timeline**: Most orders shipped same-day/next-day
- **Negative shipping fees exist**: Likely discounts/promotions

---

#### **returns.csv** (36,142 returns)
- **Purpose**: Return/refund records  
- **Relationship**: orders.order_id → returns.order_id (1:N - multiple returns per order possible)
- **Key Columns**:
  - `order_id`: Link to orders
  - `return_date`: When returned (✅ always > order_date)
  - `return_quantity`: Items returned
  - `return_reason`: Likely quality/fit/other

**Key Insight**:
- **5.6% return rate**: In line with industry
- **Return lag**: Some items returned weeks/months later

---

### **3. ANALYTICS DATA - Aggregated/External**

#### **sales.csv** (3,833 daily records - 2012-2022)
- **Purpose**: 🎯 **TARGET VARIABLE** for forecasting  
- **Key Columns**:
  - `Date`: Daily date (no missing dates ✅)
  - `Revenue`: Daily total sales (mean: $4.3M)
  - `COGS`: Daily total cost (mean: $3.7M)

**Critical Findings from EDA**:
- ⚠️ **Revenue-COGS Correlation: 0.976** 
  - Indicates strong linear relationship
  - **Leakage risk**: If COGS is computed from same-day orders, can't use for forecasting
  - **Solution**: Use historical/lagged COGS only
  
- ⚠️ **High Skewness: 1.67**
  - Revenue distribution is right-skewed
  - **Solution**: Log transformation needed for modeling
  
- ⚠️ **Autocorrelation Lag-1: 0.8655**
  - Tomorrow's revenue strongly depends on today's
  - **Implication**: ARIMA/Prophet models suitable
  - **Challenge**: Hard to beat "yesterday's value" as baseline
  
- ✅ **Autocorrelation Lag-7: 0.4920**
  - Weekly seasonality detected
  - Likely: Weekday vs weekend patterns

---

#### **web_traffic.csv** (10,000 daily web metrics)
- **Purpose**: Website analytics proxy for demand signal  
- **Key Columns**:
  - `Date`: Daily date
  - `page_views`: Unique page views (mean: 48K, range: 235 - 235K)
  - `unique_visitors`: Unique visitors
  - `bounce_rate`: % bounces (0-100%)
  - `session_duration`: Avg session time
  - `traffic_source`: organic, paid, social, direct...

**Key Insight**:
- **18 outlier days** in page_views (potential data issues)
- **Leading indicator**: Web traffic likely precedes orders by 1-7 days
- **Temporal relationship**: Can use for lag features

---

#### **inventory.csv**
- **Purpose**: Product stock levels  
- **Potential Columns**: product_id, warehouse_qty, date...
- **Usage**: Stock-out risk, replenishment timing

*(Not deeply analyzed yet, but important for supply constraint)*

---

## 🎯 Business Problem Definition

### **Primary Objective**:
**Sales Forecasting** - Predict daily revenue for next period

### **Target Variable**:
- `sales.Revenue` (daily aggregation)
- Time range: 2012-2022 (training window)
- Frequency: Daily

### **Typical Use Cases**:
1. **Revenue forecasting** → Budget planning, resource allocation
2. **Demand forecasting** → Inventory management, supply chain
3. **Customer segmentation** → Targeted marketing
4. **RFM analysis** → Customer lifetime value

---

## 🧩 Data Relationships

```
geography.csv (1K zips)
        ↑
        | (zip)
customers.csv (121K) ←─────────┐
        ↑                       │
        | (customer_id)        │
        |                      │
orders.csv (646K) ──────────────┘ (zip)
    ↓          ↓          ↓
    |          |          └─→ shipments.csv (646K)
    |          |              order_date ✓ ship_date ✓ delivery_date
    |          |
    |          └─→ payments.csv (646K)
    |
    └─→ order_items.csv (714K)
            ↓
            | (product_id)
            v
        products.csv (2.4K)


ANALYTICS LAYER:
    sales.csv ← aggregated from orders + order_items (3.8K daily)
    web_traffic.csv ← independent (10K daily)
    inventory.csv ← product-level (external?)
```

---

## 📈 Key Insights from EDA

| Aspect | Finding | Status |
|--------|---------|--------|
| **Data Integrity** | 0 duplicates, all FKs valid, all constraints satisfied | ✅ Clean |
| **Missing Values** | promo_id (38.7% missing), promo_id_2 (99.97% missing) | ⚠️ Sparse features |
| **Target (Revenue)** | Skewed (1.67), high autocorrelation (0.86 lag-1), seasonal (0.49 lag-7) | ⚠️ Needs transformation |
| **Leakage Risk** | Revenue-COGS correlation 0.976 | ⚠️ Use lagged COGS |
| **Categorical Imbalance** | order_status: 80% delivered; payment: 55% credit_card | ⚠️ Imbalanced |
| **Outliers** | 76K in shipping_fee, 105K in discount_amount, 30K in payment_value | ⚠️ Business-driven |
| **Time Coverage** | 2012-2022, no gaps, 0 zero/negative revenue | ✅ Complete |
| **Customer Diversity** | 121K unique customers, 42 cities, 6 channels | ✅ Rich segmentation |

---

## 🚀 Recommended Feature Engineering Pipeline

### **Layer 1: Raw Features** (from tables)
```
From orders: order_status, payment_method, device_type, order_source
From order_items: discount_rate, items_per_order, avg_item_price
From products: category, segment, price_band
From customers: age_group, gender, city, days_since_signup
From web_traffic: page_views, unique_visitors, bounce_rate
From temporal: day_of_week, month, quarter, is_holiday
```

### **Layer 2: Aggregations** (daily level)
```
Daily orders count
Daily avg order value (AOV)
Daily items sold
Daily discount amount (total & avg)
Daily customer acquisition (new vs repeat)
Daily return rate
Daily payment method distribution
Daily device type distribution
Web traffic metrics (page views, visitors)
```

### **Layer 3: Lags & Rolling** (time series)
```
Lag-1 to Lag-7: Revenue, orders count, AOV
Rolling-7: avg revenue, volatility
Rolling-30: trend
Seasonal dummies: day of week, month
```

### **Layer 4: Interactions** (domain logic)
```
(orders_count * avg_order_value) → revenue proxy
(discount_pct * orders_count) → promo impact
(page_views → orders_count lag) → conversion proxy
(new_customers × AOV) → new customer value
```

### **🚨 AVOID**:
- ❌ COGS on same day (use lag-1 or rolling avg)
- ❌ promo_id (too sparse)
- ❌ Future data leakage (ship_date, delivery_date, return_date)

---

## 📊 Exploratory Data Analysis Status

### **Completed Checks** ✅:
1. Data types & structure
2. Duplicate detection (0 found)
3. Foreign key validation (all valid)
4. Constraint checks (all passed)
5. Outlier detection (IQR method)
6. Numeric distributions & skewness
7. Categorical value counts & imbalance
8. Target (Revenue) autocorrelation & seasonality
9. Time series continuity

### **Remaining EDA Tasks** 📋:
1. **Missing values heatmap** - Pattern analysis
2. **Correlation matrix** - Feature relationships
3. **Customer RFM analysis** - Repeat rate, lifetime value
4. **Product performance** - Top sellers, slow movers
5. **Date alignment check** - order→ship→delivery timeline
6. **Revenue decomposition** - By customer, product, channel
7. **Temporal trends** - Growth, seasonality, anomalies
8. **Geographic insights** - Regional performance
9. **Payment method analysis** - By order status, device
10. **Promotion impact** - Discount effectiveness

---

## 🔮 Forecasting Considerations

### **Time Series Characteristics**:
- **Trend**: Growing (2012-2022, need to analyze)
- **Seasonality**: Weekly (lag-7: 0.49), likely daily (weekday/weekend)
- **Autocorrelation**: Strong (lag-1: 0.87) → AR models suitable
- **Volatility**: Skewed distribution → Log transform

### **Candidate Models**:
1. **ARIMA/SARIMA** - Classical time series (handle autocorrelation)
2. **Exponential Smoothing** - Seasonal decomposition
3. **Prophet** (Facebook) - Handles trends + seasonality
4. **LSTM/RNN** - Deep learning for nonlinear patterns
5. **XGBoost/LightGBM** - Regression with lag features + external variables

### **External Features** (Predictors):
- Web traffic (leading indicator)
- Day of week, month, holidays
- Promotions (if data improves)
- Inventory levels
- Customer acquisition (new customers)

### **Validation Strategy**:
- **Train**: 2012-2021
- **Test**: 2022 (holdout evaluation)
- **Cross-validation**: Time series split (no data leakage)
- **Metrics**: MAE, RMSE, MAPE

---

## 💡 Domain Knowledge Summary

**E-commerce Sales Forecasting** is about predicting demand given:
- **Customer behavior** (repeat purchases, channel preference)
- **Product performance** (category seasonality)
- **External signals** (web traffic, marketing spend)
- **Temporal patterns** (days of week, holidays, trends)

**Key challenges**:
1. **Imbalanced outcomes** (80% orders delivered)
2. **Sparse promotion data** (can't measure promo ROI)
3. **Data leakage** (Revenue-COGS correlation)
4. **Strong autocorrelation** (hard to beat baseline)
5. **Seasonal patterns** (must handle properly)

**Success metrics**:
- MAPE < 10% is considered good
- Beat simple baselines (historical mean, naive forecast)
- Capture seasonality accurately

---

## 📁 Files Reference

| File | Rows | Purpose | Status |
|------|------|---------|--------|
| products.csv | 2,412 | Master product catalog | ✅ Clean |
| customers.csv | 121,930 | Customer directory | ✅ Clean |
| geography.csv | 1,000 | Location master | ✅ Clean |
| orders.csv | 646,945 | Order header | ✅ Clean |
| order_items.csv | 714,669 | Order line items | ⚠️ Sparse promo |
| payments.csv | 646,945 | Payment details | ✅ Clean |
| shipments.csv | 646,945 | Shipping info | ✅ Clean |
| returns.csv | 36,142 | Return/refund | ✅ Clean |
| sales.csv | 3,833 | Daily KPI (TARGET) | ⚠️ Check COGS source |
| web_traffic.csv | 10,000 | Web analytics | ⚠️ 18 outliers |
| inventory.csv | ? | Stock levels | ❓ Not analyzed |

---

## 🎓 Learning Outcomes

After completing this EDA + forecasting project, you'll understand:

✅ **Data Architecture**: Star schema (dimension + fact tables)  
✅ **Business Domain**: E-commerce metrics (AOV, return rate, CAC)  
✅ **Time Series Analysis**: Autocorrelation, seasonality, decomposition  
✅ **Feature Engineering**: Lags, rolling stats, aggregations, interactions  
✅ **Data Quality**: Validation, leakage detection, outlier handling  
✅ **Forecasting Methods**: ARIMA, Prophet, ML ensembles  
✅ **Model Evaluation**: Time series cross-validation, production metrics  

---

**Next Step**: Continue with missing values analysis + correlation matrix for deeper relationship understanding.
