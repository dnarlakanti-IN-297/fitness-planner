#!/bin/bash
# ArgoCD Installation Script for Fitness Planner

set -e

echo "🚀 Installing ArgoCD..."

# Create argocd namespace
echo "Creating argocd namespace..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

# Install ArgoCD
echo "Installing ArgoCD components..."
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
echo "Waiting for ArgoCD pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

# Get initial admin password
echo ""
echo "✅ ArgoCD installed successfully!"
echo ""
echo "📋 Getting initial admin password..."
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ArgoCD Login Credentials"
echo "════════════════════════════════════════════════════════════"
echo "  Username: admin"
echo "  Password: $ARGOCD_PASSWORD"
echo "════════════════════════════════════════════════════════════"
echo ""

# Optionally install ArgoCD CLI
if ! command -v argocd &> /dev/null; then
    echo "ArgoCD CLI not found. Install it with:"
    echo "  macOS: brew install argocd"
    echo "  Linux: curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64"
    echo ""
fi

echo "🌐 To access ArgoCD UI, run in another terminal:"
echo "  kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo ""
echo "Then open: https://localhost:8080"
echo "(Accept the self-signed certificate warning)"
echo ""
echo "🔧 To deploy fitness-planner application, run:"
echo "  kubectl apply -f argocd/application.yaml"
echo ""
