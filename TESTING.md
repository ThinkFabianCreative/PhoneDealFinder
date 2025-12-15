# Testing Guide

This guide explains how to test the iPhone Price Monitor application locally.

## Quick Test Steps

### 1. Test Backend Price Monitor

First, set up the Python environment and test the price scraping:

```bash
# Navigate to project root
cd "/Users/andresfabian/Library/Mobile Documents/com~apple~CloudDocs/#_vibecoding/PhoneDealFinder"

# Create virtual environment (if not already created)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test the price monitor script
cd backend
python price_monitor.py
```

**Expected Output:**
- Script will attempt to fetch prices from Apple and Reebelo
- You'll see log messages about fetching prices
- `prices.json` will be created/updated with price data
- If prices drop below thresholds, notifications will be sent (if configured)

**Note:** If websites block the requests or HTML structure changed, you may see warnings. This is expected during development.

### 2. Test Flask API

In a terminal, start the Flask server:

```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

Then test the API endpoint:

```bash
# In another terminal
curl http://localhost:5000/api/prices
```

Or open in browser: `http://localhost:5000/api/prices`

**Expected Output:** JSON array of price entries (may be empty `[]` if no prices fetched yet)

### 3. Test React Frontend

In a new terminal:

```bash
cd web_ui
npm install  # If not already done
npm run dev
```

The frontend will start at `http://localhost:3000`

**What to Check:**
- Page loads without errors
- Header displays "iPhone Price Monitor"
- Price cards show for each model (may show "N/A" if no data)
- Charts display (may be empty if no historical data)

### 4. Test Full Stack Integration

1. **Terminal 1** - Start Flask API:
   ```bash
   cd backend
   python app.py
   ```

2. **Terminal 2** - Start React dev server:
   ```bash
   cd web_ui
   npm run dev
   ```

3. **Terminal 3** - Run price monitor to generate data:
   ```bash
   cd backend
   python price_monitor.py
   ```

4. Open browser to `http://localhost:3000`

   - Frontend should fetch data from Flask API
   - Price cards should update with real data
   - Charts should display price history

## Testing Specific Features

### Test Price Drop Notifications

1. Create a `.env` file in the project root with test SMTP credentials:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SMTP_TO=test@example.com
   PRICE_THRESHOLD_15=1.0  # Low threshold for testing
   ```

2. Manually edit `backend/prices.json` to add an old, higher price:
   ```json
   [
     {
       "timestamp": "2024-01-01T00:00:00",
       "model": "iPhone 15 Pro Max",
       "price": 1200.00,
       "source": "apple_refurbished"
     }
   ]
   ```

3. Run the price monitor - if new price is lower than threshold, notification should trigger

### Test API Endpoints

```bash
# Test prices endpoint
curl http://localhost:5000/api/prices

# Test root (should serve React app)
curl http://localhost:5000/
```

### Test Frontend Components

The React app includes error handling. Test error states:

1. Stop Flask API - frontend should show error message
2. Stop price monitor - API should return empty array (or last known prices)

## Troubleshooting Tests

### Backend Issues

**Problem:** `ModuleNotFoundError`
- **Solution:** Make sure virtual environment is activated and dependencies installed

**Problem:** Price scraping returns None
- **Solution:** This is normal if websites block requests or HTML changed. Check logs for details.

**Problem:** SMTP errors
- **Solution:** Verify `.env` file exists and credentials are correct. For Gmail, use App Password.

### Frontend Issues

**Problem:** Frontend can't connect to API
- **Solution:** Ensure Flask API is running on port 5000 and CORS is enabled

**Problem:** Build errors with "#" in path
- **Solution:** This is expected. Frontend will work in development mode (`npm run dev`). Production builds will work fine in GitHub Actions.

**Problem:** Charts not displaying
- **Solution:** Ensure `prices.json` has data. Check browser console for errors.

## Automated Testing (Future Enhancement)

You can add unit tests for:
- Price parsing functions
- Price comparison logic
- API endpoints
- React components

But for now, manual testing as described above is sufficient.

