#!/usr/bin/env bash

set -u

status=0

check_command() {
  local command_name="$1"
  if command -v "$command_name" >/dev/null 2>&1; then
    printf 'ok      %-12s %s\n' "$command_name" "$(command -v "$command_name")"
  else
    printf 'missing %-12s\n' "$command_name"
    status=1
  fi
}

printf 'Ego Hygiene local-agent doctor\n\n'

for command_name in git task ollama opencode uv; do
  check_command "$command_name"
done

printf '\nOllama service\n'
if command -v ollama >/dev/null 2>&1 && ollama list >/dev/null 2>&1; then
  printf 'ok      Ollama is responding\n'
else
  printf 'missing Ollama is not responding; start the Ollama application or service\n'
  status=1
fi

expected_models=(
  'llama3.2:latest'
  'qwen3:8b'
  'qwen2.5-coder:7b'
  'qwen2.5:14b'
  'qwen3-vl:latest'
)

if command -v ollama >/dev/null 2>&1; then
  printf '\nConfigured models\n'
  installed_models="$(ollama list 2>/dev/null | awk 'NR > 1 {print $1}')"
  for model in "${expected_models[@]}"; do
    if printf '%s\n' "$installed_models" | grep -Fxq "$model"; then
      printf 'ok      %s\n' "$model"
    else
      printf 'missing %s\n' "$model"
      status=1
    fi
  done
fi

printf '\nRepository layout\n'
for path in '.github/specs' 'mindgarden' 'tools/mindcap' '.agents/skills'; do
  if [[ -e "$path" ]]; then
    printf 'ok      %s\n' "$path"
  else
    printf 'missing %s\n' "$path"
    status=1
  fi
done

printf '\nDisk availability\n'
if [[ -d '/System/Volumes/Data' ]]; then
  df -h '/System/Volumes/Data'
else
  df -h '.'
fi

exit "$status"
