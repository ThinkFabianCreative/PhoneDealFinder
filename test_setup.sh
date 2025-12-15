#!/bin/bash
# Quick test setup script

echo "🧪 iPhone Price Monitor - Test Setup"
echo "===================================="
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Check Node
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js found: $NODE_VERSION"
else
    echo "✗ Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✓ npm found: v$NPM_VERSION"
else
    echo "✗ npm not found"
    exit 1
fi

echo ""
echo "📦 Installing Python dependencies..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
echo "✓ Python dependencies installed"

echo ""
echo "📦 Installing Node dependencies..."
cd web_ui
npm install --silent
echo "✓ Node dependencies installed"
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Test backend: cd backend && python price_monitor.py"
echo "3. Test API: cd backend && python app.py (in one terminal)"
echo "4. Test frontend: cd web_ui && npm run dev (in another terminal)"
