#!/bin/bash

# Define TikTok domains
TIKTOK_DOMAINS=(
    "api.tiktokv.com"
    "api-h2.tiktokv.com"
    "api21-h2.tiktokv.com"
    "tiktokcdn.com"
    "tiktokv.com"
    "ib.tiktokv.com"
    "m.tiktok.com"
    "p16-tiktokcdn-com.akamaized.net"
    "v16.tiktokcdn.com"
    "v19.tiktokcdn.com"
    "mon.tiktokv.com"
    "log.tiktokv.com"
    "t.tiktok.com"
    "tiktok.com"
    "tiktok.org"
    "vt.tiktok.com"
    "v16a.tiktokcdn.com"
    "v16m.tiktokcdn.com"
    "muscdn.com"
    "musical.ly"
    "ibyteimg.com"
    "ibytedtos.com"
    "byteoversea.com"
    "isnssdk.com"
    "myqcloud.com"
    "ns-440.awsdns-55.com"
    "ns-722.awsdns-26.net"
    "ns-1475.awsdns-56.org"
    "ns-1574.awsdns-04.co.uk"
    "tiktokcdn-com.akamaized.net"
    "v16-tiktokcdn-com.akamaized.net"
    "47.252.102.50"
    "161.117.71.74"
    "47.252.102.182"
    "161.117.71.35"
    "161.117.70.89"
    "161.117.70.145"
    "161.117.70.136"
    "47.252.50.101"
    "47.252.102.193"
    "161.117.71.34"
    "161.117.71.73"
    "47.252.102.48"
    "47.252.50.157"
    "34.196.79.125"
    "47.252.102.198"
    "161.117.70.68"
    "akamai.net"
    "www.tiktok.com"
)

# Define Instagram domains
INSTAGRAM_DOMAINS=(
    "instagram.com"
    "www.instagram.com"
    "api.instagram.com"
    "i.instagram.com"
    "cdninstagram.com"
    "instagramstatic-a.akamaihd.net"
    "instagramstatic-a.akamaihd.net.edgesuite.net"
    "platform.instagram.com"
    "scontent.cdninstagram.com"
    "scontent-fallback.cdninstagram.com"
    "star.fallback.c10r.instagram.com"
    "black.ish.instagram.com"
    "instagram-shv-01-ams2.fbcdn.net"
    "instagram-shv-01-ams3.fbcdn.net"
    "instagram-shv-01-ash5.fbcdn.net"
    "instagram-shv-01-atl1.fbcdn.net"
    "instagram-shv-01-bru2.fbcdn.net"
    "instagram-shv-01-cai1.fbcdn.net"
    "instagram-shv-01-cdg2.fbcdn.net"
    "instagram-shv-01-dfw1.fbcdn.net"
    "instagram-shv-01-fra3.fbcdn.net"
    "instagram-shv-01-gru1.fbcdn.net"
    "instagram-shv-01-hkg2.fbcdn.net"
    "instagram-shv-01-iad3.fbcdn.net"
    "instagram-shv-01-kul1.fbcdn.net"
    "instagram-shv-01-lax1.fbcdn.net"
    "instagram-shv-01-lga1.fbcdn.net"
    "instagram-shv-01-lhr3.fbcdn.net"
    "instagram-shv-01-mad1.fbcdn.net"
    "instagram-shv-01-mia1.fbcdn.net"
    "instagram-shv-01-mxp1.fbcdn.net"
    "instagram-shv-01-nrt1.fbcdn.net"
    "instagram-shv-01-ord1.fbcdn.net"
    "instagram-shv-01-sea1.fbcdn.net"
    "instagram-shv-01-sin1.fbcdn.net"
    "instagram-shv-01-sjc2.fbcdn.net"
    "instagram-shv-01-syd1.fbcdn.net"
    "instagram-shv-01-tpe1.fbcdn.net"
    "instagram-shv-01-vie1.fbcdn.net"
    "instagram-shv-02-cai1.fbcdn.net"
    "instagram-shv-02-hkg2.fbcdn.net"
    "instagram-shv-03-ash5.fbcdn.net"
    "instagram-shv-03-atn1.fbcdn.net"
    "instagram-shv-03-hkg1.fbcdn.net"
    "instagram-shv-03-lla1.fbcdn.net"
    "instagram-shv-03-prn2.fbcdn.net"
    "instagram-shv-03-xdc1.fbcdn.net"
    "instagram-shv-04-hkg1.fbcdn.net"
    "instagram-shv-06-atn1.fbcdn.net"
    "instagram-shv-06-lla1.fbcdn.net"
    "instagram-shv-07-ash4.fbcdn.net"
    "instagram-shv-07-frc3.fbcdn.net"
    "instagram-shv-09-frc1.fbcdn.net"
    "instagram-shv-09-lla1.fbcdn.net"
    "instagram-shv-12-frc1.fbcdn.net"
    "instagram-shv-12-frc3.fbcdn.net"
    "instagram-shv-12-lla1.fbcdn.net"
    "instagram-shv-12-prn1.fbcdn.net"
    "instagram-shv-13-frc1.fbcdn.net"
    "instagram-shv-17-prn1.fbcdn.net"
    "instagram-shv-18-prn1.fbcdn.net"
    "logger.instagram.com"
    "scontent-iad3-1.cdninstagram.com"
    "telegraph-ash.instagram.com"
    "white.ish.instagram.com"
    "cdn.instagram.com"
)

# Define Facebook domains
FACEBOOK_DOMAINS=(
    "facebook.com"
    "www.facebook.com"
    "api.facebook.com"
    "m.facebook.com"
    "staticxx.facebook.com"
    "connect.facebook.net"
    "graph.facebook.com"
    "star.c10r.facebook.com"
    "star.fallback.c10r.facebook.com"
)

# Combine all domains into one array
BLOCKED_DOMAINS=( "${TIKTOK_DOMAINS[@]}" "${INSTAGRAM_DOMAINS[@]}" "${FACEBOOK_DOMAINS[@]}" )

# Get the current hour (24-hour format)
CURRENT_HOUR=$(date +%H)

# Create a temporary file to hold the blocklist
TEMP_FILE=$(mktemp)
for domain in "${BLOCKED_DOMAINS[@]}"; do
    echo "$domain" >> "$TEMP_FILE"
done
# Remove duplicates
sort -u "$TEMP_FILE" -o "$TEMP_FILE"

# Set a batch size to avoid overloading the command line
BATCH_SIZE=100

# Helper function to process domains in batches.
# The first argument is the subcommand (deny or allow).
process_in_batches() {
  local action="$1"
  local file="$2"
  local batch=()
  while IFS= read -r domain; do
      batch+=("$domain")
      if (( ${#batch[@]} >= BATCH_SIZE )); then
          sudo pihole "$action" "${batch[@]}"
          batch=()
      fi
  done < "$file"
  # Process any remaining domains
  if (( ${#batch[@]} > 0 )); then
      sudo pihole "$action" "${batch[@]}"
  fi
}

if [[ "$CURRENT_HOUR" == "00" || "$CURRENT_HOUR" == "01" ]]; then
    echo "Blocking domains..."
    # Use the new syntax: 'deny' to block domains
    process_in_batches "deny" "$TEMP_FILE"
    sudo pihole -g
elif [[ "$CURRENT_HOUR" == "06" || "$CURRENT_HOUR" == "07" ]]; then
    echo "Unblocking domains..."
    # Use 'allow' to remove from the blocklist
    process_in_batches "allow" "$TEMP_FILE"
    sudo pihole -g
else
    echo "No state change needed at hour $CURRENT_HOUR."
fi

# Clean up
rm -f "$TEMP_FILE"
