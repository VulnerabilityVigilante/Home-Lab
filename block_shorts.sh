#!/bin/bash
# This script uses regex filters to block or unblock traffic from Instagram,
# Facebook, and TikTok/ByteDance domains. The regex patterns are designed to match
# any domain that includes the relevant keywords (and additional variants).

# Define regex patterns for the social platforms
REGEX_PATTERNS=(
    ".*instagram.*"
    ".*facebook.*"
    ".*(tiktok|musical\\.ly|muscdn|ibyteimg|ibytedtos|byteoversea|bytedance).*"
)

# Get the current hour (24-hour format)
CURRENT_HOUR=$(date +%H)

if [[ "$CURRENT_HOUR" == "00" || "$CURRENT_HOUR" == "01" ]]; then
    echo "Blocking social media domains via regex..."
    for regex in "${REGEX_PATTERNS[@]}"; do
        sudo pihole --regex "$regex"
    done
    sudo pihole -g
elif [[ "$CURRENT_HOUR" == "06" || "$CURRENT_HOUR" == "07" ]]; then
    echo "Unblocking social media domains via regex..."
    for regex in "${REGEX_PATTERNS[@]}"; do
        # Use the short deletion flag for regex filters
        sudo pihole --regex -d "$regex"
    done
    sudo pihole -g
else
    echo "No state change needed at hour $CURRENT_HOUR."
fi
