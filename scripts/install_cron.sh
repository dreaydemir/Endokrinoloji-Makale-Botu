#!/usr/bin/env bash
set -euo pipefail

# Kullanıcı crontab'ına her Pazartesi 08:00'de çalışacak şekilde ekler.
# Zamanı kendine göre düzenleyebilirsin.
CRON_ENTRY="0 8 * * 1 cd $(pwd) && $(pwd)/scripts/run_once.sh >> $(pwd)/cron.log 2>&1"

# Var olan crontab'ı al, yeni satırı ekle (aynı satır varsa tekrarlama)
( crontab -l 2>/dev/null | grep -v -F "$CRON_ENTRY" ; echo "$CRON_ENTRY" ) | crontab -

echo "Cron kuruldu. Haftalık çalışma: Pazartesi 08:00"
