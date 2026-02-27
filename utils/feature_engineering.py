import pandas as pd


def find_column(df, possible_names):
    """
    Find column from possible names safely
    """
    for name in possible_names:
        for col in df.columns:
            if col.lower() == name.lower():
                return col
    return None


def create_features(df):

    df = df.copy()

    # ---------- FIND REQUIRED COLUMNS SAFELY ----------

    instore_rev = find_column(df, ["InStoreRevenue"])
    ue_rev = find_column(df, ["UberEatsRevenue"])
    dd_rev = find_column(df, ["DoorDashRevenue"])
    sd_rev = find_column(df, ["SelfDeliveryRevenue"])

    instore_profit = find_column(df, ["InStoreNetProfit"])
    ue_profit = find_column(df, ["UberEatsNetProfit"])
    dd_profit = find_column(df, ["DoorDashNetProfit"])
    sd_profit = find_column(df, ["SelfDeliveryNetProfit"])

    monthly_orders = find_column(df, ["MonthlyOrders"])

    commission = find_column(df, ["CommissionRate"])

    delivery_cost = find_column(df, [
        "DeliveryCostOrder",
        "DeliveryCostPerOrder",
        "SelfDeliveryCost",
        "SD_DeliveryCost"
    ])

    growth = find_column(df, ["GrowthFactor"])

    # ---------- CREATE FEATURES ----------

    # Total Revenue
    if instore_rev and ue_rev and dd_rev and sd_rev:
        df["TotalRevenue"] = (
            df[instore_rev]
            + df[ue_rev]
            + df[dd_rev]
            + df[sd_rev]
        )
    else:
        df["TotalRevenue"] = 0

    # Total Profit
    if instore_profit and ue_profit and dd_profit and sd_profit:
        df["TotalNetProfit"] = (
            df[instore_profit]
            + df[ue_profit]
            + df[dd_profit]
            + df[sd_profit]
        )
    else:
        df["TotalNetProfit"] = 0

    # Profit per order
    if monthly_orders:
        df["ProfitPerOrder"] = (
            df["TotalNetProfit"]
            / df[monthly_orders].replace(0, 1)
        )
    else:
        df["ProfitPerOrder"] = 0

    # Commission impact
    if commission and "UE_share" in df.columns and "DD_share" in df.columns:
        df["CommissionImpact"] = (
            df[commission]
            * (df["UE_share"] + df["DD_share"])
        )
    else:
        df["CommissionImpact"] = 0

    # Delivery cost impact
    if delivery_cost and "SD_share" in df.columns:
        df["DeliveryCostImpact"] = (
            df[delivery_cost]
            * df["SD_share"]
        )
    else:
        df["DeliveryCostImpact"] = 0

    # Growth adjusted orders
    if monthly_orders and growth:
        df["AdjustedOrders"] = (
            df[monthly_orders]
            * df[growth]
        )
    else:
        df["AdjustedOrders"] = 0

    return df


def encode_categorical(df):

    categorical_cols = []

    for col in ["CuisineType", "Segment", "Subregion"]:
        if col in df.columns:
            categorical_cols.append(col)

    if categorical_cols:
        df = pd.get_dummies(
            df,
            columns=categorical_cols,
            drop_first=True
        )

    return df