#!/usr/bin/env bash
set -euo pipefail

# Config
HOST="${HOST:-http://localhost:8888}"
FUNC_PATH="${FUNC_PATH:-/.netlify/functions/philosopher_rag}"
PHIL="${PHIL:-spinoza}"

echo "Testing philosopher_rag on ${HOST}${FUNC_PATH} (philosopher=${PHIL})"

if ! command -v jq >/dev/null 2>&1; then
  echo "jq non trouvé. Installez-le pour un affichage lisible (brew install jq)."
fi

INIT_PAYLOAD=$(cat <<EOF
{"action":"init","philosopher":"${PHIL}"}
EOF
)

RESPOND_PAYLOAD=$(cat <<'EOF'
{
  "action":"respond",
  "philosopher":"spinoza",
  "message":"Je pense que la liberté c est choisir sans contrainte."
}
EOF
)

echo "→ INIT"
RESP_INIT=$(curl -s "${HOST}${FUNC_PATH}" -H 'Content-Type: application/json' -d "${INIT_PAYLOAD}")
echo "${RESP_INIT}" | { jq . 2>/dev/null || cat; }

echo
echo "→ RESPOND"
RESP_RESP=$(curl -s "${HOST}${FUNC_PATH}" -H 'Content-Type: application/json' -d "${RESPOND_PAYLOAD}")
echo "${RESP_RESP}" | { jq . 2>/dev/null || cat; }

echo
echo "Done."



