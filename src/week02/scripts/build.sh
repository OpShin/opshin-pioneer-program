#!/bin/bash

path=$(readlink -f "$0")
week_dir=$(dirname "$(dirname "$path")")
scripts=(
  "burn.py"
  "custom_types.py"
  "fourty_two.py"
  "fourty_two_typed.py"
  "gift.py"
)
assets_dir="$week_dir/assets"
mkdir -p "$assets_dir"

for script in "${scripts[@]}"; do
  opshin build "$week_dir/lecture/$script" -o "$assets_dir/${script%.*}"
done
