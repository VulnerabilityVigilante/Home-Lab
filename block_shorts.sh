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
    "tiktokcdn.com"
    "tiktokv.com"
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
)

# Combine both lists
BLOCKED_DOMAINS=("${TIKTOK_DOMAINS[@]}" "${INSTAGRAM_DOMAINS[@]}")

# Get the current hour
CURRENT_HOUR=$(date +%H)

# Define blocking hours (e.g., 0 to 6 AM)
START_BLOCK=0
END_BLOCK=6

if [ "$CURRENT_HOUR" -ge "$START_BLOCK" ] && [ "$CURRENT_HOUR" -lt "$END_BLOCK" ]; then
    # Block domains
    for domain in "${BLOCKED_DOMAINS[@]}"; do
        pihole -b -q "$domain"
    done
else
    # Unblock domains
    for domain in "${BLOCKED_DOMAINS[@]}"; do
        pihole -b -d "$domain"
    done
fi
