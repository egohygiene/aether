#!/usr/bin/env sh

set -eu

script_directory=$(CDPATH= cd "$(dirname "$0")" && pwd)
repository_root=$(CDPATH= cd "$script_directory/../.." && pwd)
skills_root="$repository_root/.agents/skills"
agents_root="$repository_root/.github/agents"
temporary_file="${TMPDIR:-/tmp}/agent-system-validation-$$.txt"
error_count=0

trap 'rm -f "$temporary_file"' EXIT HUP INT TERM

## print_error
## Print one validation error to standard error.
##
## @param $1 Error message.
print_error() {
    printf 'error: %s\n' "$1" >&2
}

## frontmatter_value
## Read one scalar value from the first YAML frontmatter block.
##
## @param $1 File to inspect.
## @param $2 Frontmatter key.
frontmatter_value() {
    awk -v requested_key="$2" '
        NR == 1 && $0 == "---" {
            in_frontmatter = 1
            next
        }
        in_frontmatter && $0 == "---" {
            exit
        }
        in_frontmatter {
            separator = index($0, ":")
            if (separator == 0) {
                next
            }
            key = substr($0, 1, separator - 1)
            value = substr($0, separator + 1)
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", key)
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
            if (key == requested_key) {
                if ((substr(value, 1, 1) == "\"" && substr(value, length(value), 1) == "\"") ||
                    (substr(value, 1, 1) == "\047" && substr(value, length(value), 1) == "\047")) {
                    value = substr(value, 2, length(value) - 2)
                }
                print value
                exit
            }
        }
    ' "$1"
}

## validate_skill
## Validate one portable project skill directory.
##
## @param $1 Skill directory.
validate_skill() (
    skill_directory=$1
    skill_file="$skill_directory/SKILL.md"
    directory_name=$(basename "$skill_directory")
    skill_failed=0

    if [ ! -f "$skill_file" ]; then
        print_error "$skill_directory does not contain SKILL.md"
        return 1
    fi

    if [ "$(sed -n '1p' "$skill_file")" != "---" ]; then
        print_error "$skill_file does not start with YAML frontmatter"
        skill_failed=1
    fi

    skill_name=$(frontmatter_value "$skill_file" "name")
    skill_description=$(frontmatter_value "$skill_file" "description")

    if [ -z "$skill_name" ]; then
        print_error "$skill_file is missing a frontmatter name"
        skill_failed=1
    fi

    if [ "$skill_name" != "$directory_name" ]; then
        print_error "$skill_file name '$skill_name' does not match directory '$directory_name'"
        skill_failed=1
    fi

    case "$skill_name" in
        ""|*[!a-z0-9-]*|-*|*-|*--*)
            print_error "$skill_file uses an invalid portable skill name: '$skill_name'"
            skill_failed=1
            ;;
    esac

    if [ "${#skill_name}" -gt 64 ]; then
        print_error "$skill_file skill name exceeds 64 characters"
        skill_failed=1
    fi

    if [ -z "$skill_description" ]; then
        print_error "$skill_file is missing a frontmatter description"
        skill_failed=1
    elif [ "${#skill_description}" -gt 1024 ]; then
        print_error "$skill_file description exceeds 1024 characters"
        skill_failed=1
    fi

    awk '
        NR == 1 && $0 == "---" {
            in_frontmatter = 1
            next
        }
        in_frontmatter && $0 == "---" {
            exit
        }
        in_frontmatter && /^[A-Za-z0-9_-]+[[:space:]]*:/ {
            key = $0
            sub(/[[:space:]]*:.*/, "", key)
            if (key != "name" && key != "description") {
                print key
            }
        }
    ' "$skill_file" > "$temporary_file"

    if [ -s "$temporary_file" ]; then
        print_error "$skill_file contains non-portable frontmatter keys: $(tr '\n' ' ' < "$temporary_file")"
        skill_failed=1
    fi

    skill_lines=$(wc -l < "$skill_file" | tr -d ' ')
    if [ "$skill_lines" -gt 500 ]; then
        print_error "$skill_file exceeds 500 lines; move details into references"
        skill_failed=1
    fi

    return "$skill_failed"
)

## validate_agent
## Validate one GitHub Copilot custom agent profile.
##
## @param $1 Agent profile.
validate_agent() (
    agent_file=$1
    agent_failed=0

    if [ "$(sed -n '1p' "$agent_file")" != "---" ]; then
        print_error "$agent_file does not start with YAML frontmatter"
        agent_failed=1
    fi

    if [ -z "$(frontmatter_value "$agent_file" "description")" ]; then
        print_error "$agent_file is missing a frontmatter description"
        agent_failed=1
    fi

    if [ -n "$(frontmatter_value "$agent_file" "infer")" ]; then
        print_error "$agent_file uses deprecated frontmatter key 'infer'"
        agent_failed=1
    fi

    agent_size=$(wc -c < "$agent_file" | tr -d ' ')
    if [ "$agent_size" -gt 30000 ]; then
        print_error "$agent_file exceeds the 30,000-character profile limit"
        agent_failed=1
    fi

    return "$agent_failed"
)

if [ ! -d "$skills_root" ]; then
    print_error "missing skills directory: $skills_root"
    error_count=$((error_count + 1))
else
    for skill_directory in "$skills_root"/*; do
        [ -d "$skill_directory" ] || continue
        if ! validate_skill "$skill_directory"; then
            error_count=$((error_count + 1))
        fi
    done
fi

if [ ! -d "$agents_root" ]; then
    print_error "missing agents directory: $agents_root"
    error_count=$((error_count + 1))
else
    for agent_file in "$agents_root"/*.agent.md; do
        [ -f "$agent_file" ] || continue
        if ! validate_agent "$agent_file"; then
            error_count=$((error_count + 1))
        fi
    done
fi

find "$repository_root" -type f -name '.DS_Store' -print > "$temporary_file"
if [ -s "$temporary_file" ]; then
    print_error "operating-system metadata files are present: $(tr '\n' ' ' < "$temporary_file")"
    error_count=$((error_count + 1))
fi

find "$repository_root/.github/specs" -type f -name '*.agent.md' -print > "$temporary_file"
if [ -s "$temporary_file" ]; then
    print_error "agent profiles are misplaced under .github/specs: $(tr '\n' ' ' < "$temporary_file")"
    error_count=$((error_count + 1))
fi

if [ "$error_count" -ne 0 ]; then
    printf 'Agent system validation failed with %s error group(s).\n' "$error_count" >&2
    exit 1
fi

printf 'Agent system validation passed.\n'
