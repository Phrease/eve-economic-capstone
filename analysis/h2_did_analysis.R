library(dplyr)
library(lubridate)

df <- read.csv("did_analysis_data_1.csv")

# Convert string dates to date objects and map them to the start of the week
df <- df %>%
  mutate(
    full_date = as.Date(full_date),
    week_start = floor_date(full_date, "week") # Groups days into 7-day buckets
  )

# Aggregate to the weekly grain
weekly_df <- df %>%
  group_by(system_name, is_central_hub, week_start) %>%
  summarize(
    # Average the spread over a week. ignore daily NAs
    weekly_spread = mean(bid_ask_spread, na.rm=TRUE),
    
    # Sum the macroeconomic volume and destruction metrics
    weekly_volume = sum(total_trade_volume, na.rm=TRUE),
    weekly_destroyed = sum(calculated_destroyed_isk, na.rm=TRUE),
    .groups = "drop"
  ) %>%
  # Drop weeks where the spread is still mathematically incalculable
  filter(!is.na(weekly_spread) & weekly_spread != "NaN")

# Execute the Multiple Linear Regression for H2
# Evaluating if pricing inefficiencies (spread) impact macroeconomic velocity (volume)
# Controlling for whether the system is a central hub to isolate the spread's effect
h2_model <- lm(weekly_volume ~ weekly_spread + is_central_hub, data = weekly_df)

summary(h2_model)