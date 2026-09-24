library(dplyr)

# Importing CSV Data
df <- read.csv("liquid ozone.csv")

# Strip commas and force numeric evals
df$total_trade_volume <- as.numeric(gsub(",", "", df$total_trade_volume))
df$bid_ask_spread <- as.numeric(gsub(",", "", df$bid_ask_spread))

# Formatting date column for time-series
df$full_date <- as.Date(df$full_date, format="%Y-%m-%d %H:%M:%S")

# Start date of data pull
shock_date <- as.Date("2026-07-15")

# Construct DiD variables
df <- df %>%
  mutate(
    # Treatment Group: 1 if Jita, 0 if Peripheral System
    treatment = ifelse(is_central_hub == "true", 1, 0),
    
    # Time Period: 1 if the date falls after the economic shock, 0 if before
    post_shock = ifelse(full_date >= shock_date, 1, 0),
    
    # Interaction Term: Estimator for measuring isolated effects on Jita
    did_interaction = treatment * post_shock
  )

# DiD linear regression:
# Model 1: Testing the impact of the shock on market liquidity
model_volume <- lm(total_trade_volume ~ treatment + post_shock + did_interaction, data = df)

# Model 2: Testing the impact of the shock on pricing inefficiencies
model_spread <- lm(bid_ask_spread ~ treatment + post_shock + did_interaction, data = df)

summary(model_volume)
summary(model_spread)