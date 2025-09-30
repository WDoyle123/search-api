#!/usr/bin/env bash

MINIKUBE_PROFILE="search-api"
NAMESPACE="search-api"
API_PORT=8000
DB_PORT=5432

MOUNT_PID=""
API_PF_LOOP_PID=""
DB_PF_LOOP_PID=""
API_LOG_PID=""

function check_minikube() {
  echo "Checking Minikube status for profile '${MINIKUBE_PROFILE}'..."
  if ! minikube -p "${MINIKUBE_PROFILE}" status &>/dev/null; then
    echo "Minikube (profile: ${MINIKUBE_PROFILE}) is not running. Starting Minikube..."
    minikube -p "${MINIKUBE_PROFILE}" start || { echo "Minikube failed to start."; exit 1; }
  else
    echo "Minikube (profile: ${MINIKUBE_PROFILE}) is already running."
  fi
}

function create_namespace() {
  if ! kubectl get namespace "${NAMESPACE}" &>/dev/null; then
    echo "Namespace '${NAMESPACE}' not found. Creating..."
    kubectl create namespace "${NAMESPACE}" || { echo "Failed to create namespace '${NAMESPACE}'."; exit 1; }
  else
    echo "Namespace '${NAMESPACE}' already exists."
  fi
}

function kill_existing_port_forward() {
  local port=$1
  local pids
  pids=$(lsof -ti tcp:"$port")
  if [ -n "$pids" ]; then
    echo "Killing existing processes on port $port: $pids"
    kill -9 $pids
  else
    echo "No processes found on port $port."
  fi
}

function check_port_open() {
  local port=$1
  if (echo > /dev/tcp/127.0.0.1/"$port") &>/dev/null; then
    return 0
  else
    return 1
  fi
}

# Main Execution 
check_minikube
create_namespace

kill_existing_port_forward "${API_PORT}"
kill_existing_port_forward "${DB_PORT}"

echo ""
echo "Minikube development environment is set up (profile: ${MINIKUBE_PROFILE})."
echo "  • Port forwarding is active:"
echo "       - API: http://localhost:${API_PORT}"
echo "       - DB:  localhost:${DB_PORT}"
echo ""

cd ..

tilt up &
TILT_PID=$!

cd scripts

 wait $TILT_PID
