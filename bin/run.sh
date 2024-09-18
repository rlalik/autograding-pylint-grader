#! /bin/sh

root=${root:-"/opt/test-runner"}
export PYTHONPATH="$root:$PYTHONPATH"

mkdir autograding_output

for arg in "$@"; do
  case "$arg" in
    --timeout=*)
      TIMEOUT="${1#*=}"
      shift
      ;;
    --max-score=*)
      MAX_SCORE="${1#*=}"
      MAX_SCORE="${MAX_SCORE:-0}"
      shift
      ;;
    --setup-command=*)
      SETUP_COMMAND="${1#*=}"
      shift
      ;;
    --pylint-args=*)
      PYLINT_ARGS="${1#*=}"
      shift
      ;;
    --*)
      printf "******************************\n"
      printf "* Warning: Unknown argument. *\n"
      printf "******************************\n"
  esac
done

TIMEOUT=$((TIMEOUT * 60))
echo "TIMEOUT is $TIMEOUT seconds"
echo "MAX_SCORE is $MAX_SCORE"
echo "PYLINT_ARGS is $PYLINT_ARGS"
echo "FILES are ${@}"

if [ -n "$SETUP_COMMAND" ]; then
  echo "Running setup command: $SETUP_COMMAND"
  eval "$SETUP_COMMAND"
fi

timeout "$TIMEOUT" python3 $root/bin/run.py ./ ./autograding_output/ "$MAX_SCORE" -- "$PYLINT_ARGS" ${@}
exit_status=$?
if [ $exit_status -eq 124 ]; then
  echo "The command took longer than $TIMEOUT seconds to execute. Please increase the timeout to avoid this error."
  echo '{"status": "error", "message": "The command timed out"}' > autograding_output/results.json
fi

echo "result=$(jq -c . autograding_output/results.json | jq -sRr @base64)" >> "$GITHUB_OUTPUT"
