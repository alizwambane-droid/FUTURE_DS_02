# ============================================================
# FUTURE INTERNS – Task 2: Customer Retention & Churn Analysis
# Tool: Python (Google Colab ready)
# Repository: FUTURE_DS_02
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 5)

# ============================================================
# STEP 1: Load Data
# ============================================================
df = pd.read_csv("churn_data.csv", parse_dates=["Signup_Date"])
print("Dataset Shape:", df.shape)
print(df.head())

# ============================================================
# STEP 2: Overview & Cleaning
# ============================================================
print("\nMissing values:\n", df.isnull().sum())
print("\nChurn Distribution:\n", df["Churned"].value_counts())

# ============================================================
# STEP 3: KPI Summary
# ============================================================
total_customers = len(df)
churned = df["Churned"].sum()
churn_rate = churned / total_customers * 100
retention_rate = 100 - churn_rate
avg_tenure = df["Tenure_Months"].mean()

print("\n========== KEY PERFORMANCE INDICATORS ==========")
print(f"  Total Customers  : {total_customers:,}")
print(f"  Churned          : {churned:,}")
print(f"  Churn Rate       : {churn_rate:.1f}%")
print(f"  Retention Rate   : {retention_rate:.1f}%")
print(f"  Avg Tenure       : {avg_tenure:.1f} months")
print("=================================================")

# ============================================================
# STEP 4: Churn Rate by Plan (Bar Chart)
# ============================================================
churn_by_plan = df.groupby("Plan")["Churned"].mean() * 100

fig, ax = plt.subplots()
bars = ax.bar(churn_by_plan.index, churn_by_plan.values,
              color=["#e74c3c", "#e67e22", "#2ecc71"])
ax.set_title("Churn Rate by Subscription Plan", fontsize=16, fontweight="bold")
ax.set_xlabel("Plan")
ax.set_ylabel("Churn Rate (%)")
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{bar.get_height():.1f}%", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("churn_by_plan.png", dpi=150)
plt.show()

# ============================================================
# STEP 5: Churn Reasons (Horizontal Bar)
# ============================================================
reasons = df[df["Churned"] == 1]["Churn_Reason"].value_counts()

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(reasons.index[::-1], reasons.values[::-1], color="#e74c3c")
ax.set_title("Top Churn Reasons", fontsize=16, fontweight="bold")
ax.set_xlabel("Number of Customers")
plt.tight_layout()
plt.savefig("churn_reasons.png", dpi=150)
plt.show()

# ============================================================
# STEP 6: Churn by Tenure Group (Bar Chart)
# ============================================================
df["Tenure_Group"] = pd.cut(df["Tenure_Months"],
                             bins=[0, 6, 12, 24, 36],
                             labels=["0-6 months", "7-12 months", "13-24 months", "25-36 months"])

churn_by_tenure = df.groupby("Tenure_Group")["Churned"].mean() * 100

fig, ax = plt.subplots()
bars = ax.bar(churn_by_tenure.index.astype(str), churn_by_tenure.values,
              color=sns.color_palette("Reds_d", len(churn_by_tenure)))
ax.set_title("Churn Rate by Customer Tenure", fontsize=16, fontweight="bold")
ax.set_xlabel("Tenure Group")
ax.set_ylabel("Churn Rate (%)")
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"{bar.get_height():.1f}%", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("churn_by_tenure.png", dpi=150)
plt.show()

# ============================================================
# STEP 7: Support Calls vs Churn (Box Plot)
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))
df["Churn_Label"] = df["Churned"].map({0: "Retained", 1: "Churned"})
sns.boxplot(data=df, x="Churn_Label", y="Support_Calls",
            palette={"Retained": "#2ecc71", "Churned": "#e74c3c"}, ax=ax)
ax.set_title("Support Calls: Churned vs Retained Customers", fontsize=16, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("Number of Support Calls")
plt.tight_layout()
plt.savefig("support_calls_churn.png", dpi=150)
plt.show()

# ============================================================
# STEP 8: Monthly Cohort Retention (Line Chart)
# ============================================================
df["Signup_Month"] = df["Signup_Date"].dt.to_period("M")
cohort = df.groupby("Signup_Month").agg(
    Total=("Customer_ID", "count"),
    Churned=("Churned", "sum")
).reset_index()
cohort["Retention_Rate"] = (1 - cohort["Churned"] / cohort["Total"]) * 100
cohort["Signup_Month"] = cohort["Signup_Month"].astype(str)

fig, ax = plt.subplots()
ax.plot(cohort["Signup_Month"], cohort["Retention_Rate"],
        marker="o", color="#3498db", linewidth=2.5)
ax.fill_between(cohort["Signup_Month"], cohort["Retention_Rate"], alpha=0.15, color="#3498db")
ax.set_title("Monthly Cohort Retention Rate", fontsize=16, fontweight="bold")
ax.set_xlabel("Signup Month")
ax.set_ylabel("Retention Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("cohort_retention.png", dpi=150)
plt.show()

# ============================================================
# STEP 9: Insights & Recommendations
# ============================================================
highest_churn_plan = churn_by_plan.idxmax()
top_reason = reasons.index[0]
highest_churn_tenure = churn_by_tenure.idxmax()

print("""
╔══════════════════════════════════════════════════════════╗
║       CUSTOMER RETENTION & CHURN ANALYSIS – REPORT      ║
╚══════════════════════════════════════════════════════════╝
""")
print(f"1. CHURN RATE     : {churn_rate:.1f}% of customers have churned.")
print(f"2. WORST PLAN     : '{highest_churn_plan}' plan has the highest churn rate.")
print(f"3. TOP REASON     : '{top_reason}' is the #1 reason customers leave.")
print(f"4. RISKY TENURE   : Customers in '{highest_churn_tenure}' group churn the most.")
print("""
RECOMMENDATIONS:
  → Offer loyalty discounts to Basic plan users to encourage upgrades.
  → Improve customer support quality — high support calls correlate with churn.
  → Send re-engagement emails to customers with low login frequency.
  → Introduce onboarding programs for new customers (first 6 months are critical).
  → Address pricing concerns with flexible or discounted annual plans.
""")
print("All charts saved as PNG. Upload to your FUTURE_DS_02 GitHub repo.")
