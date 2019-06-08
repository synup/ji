if [[ ! -o interactive ]]; then
    return
fi

compctl -K _ji ji

_ji() {
  local word words completions
  read -cA words
  word="${words[2]}"

  if [ "${#words}" -eq 2 ]; then
    completions="$(ji commands)"
  else
    completions="$(ji completions "${word}")"
  fi

  reply=("${(ps:\n:)completions}")
}
