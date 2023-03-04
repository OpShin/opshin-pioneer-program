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

for script in "${scripts[@]}"; do
  eopsin build "$week_dir/lecture/$script" -o "$week_dir/assets/${script%.*}"
done
