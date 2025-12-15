# iPhone Price Monitor

A full-stack price monitoring application that tracks iPhone 15 Pro Max, 16 Pro Max, and 17 Pro Max (256GB) prices from Apple Certified Refurbished and Reebelo. The application includes a Python backend for price scraping, a Flask API, a React frontend with Material UI, and automated daily price checks via GitHub Actions.

## Architecture

- **Backend**: Python price monitoring script (`price_monitor.py`) that scrapes prices and stores them in `prices.json`
- **API**: Flask application (`app.py`) serving price data and static frontend files
- **Frontend**: React application with Material UI (Material 3) displaying price cards and historical charts
- **DevOps**: GitHub Actions workflow running daily at 8:00 AM PST to check prices and update the repository

## Features

- Daily automated price monitoring via GitHub Actions
- Price drop notifications via SMTP email and/or webhook
- Modern React frontend with Material UI styling
- Historical price charts using Chart.js
- Responsive design with dark mode support
- Configurable price drop thresholds

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Git
- GitHub account (for repository and Actions)

## Setup Instructions

### 1. Clone or Initialize Repository

If you haven't already, initialize the repository:

```bash
git init
```

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository named `PhoneDealFinder`
2. Make it public (or private if you prefer)
3. **Do not** initialize it with a README, .gitignore, or license (we already have these)

### 3. Add Remote and Push

```bash
git remote add origin https://github.com/YOUR_USERNAME/PhoneDealFinder.git
git add .
git commit -m "Initial commit: iPhone Price Monitor"
git branch -M main
git push -u origin main
```

### 4. Configure GitHub Secrets

Go to your repository on GitHub → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

**Required for Email Notifications:**
- `SMTP_HOST` - Your SMTP server (e.g., `smtp.gmail.com`)
- `SMTP_PORT` - SMTP port (e.g., `587`)
- `SMTP_USER` - Your email address
- `SMTP_PASSWORD` - Your email password or app-specific password
- `SMTP_TO` - Recipient email address

**Optional:**
- `WEBHOOK_URL` - Webhook URL for notifications (leave empty if not using)
- `PRICE_THRESHOLD_15` - Price drop threshold % for iPhone 15 Pro Max (default: 5.0)
- `PRICE_THRESHOLD_16` - Price drop threshold % for iPhone 16 Pro Max (default: 5.0)
- `PRICE_THRESHOLD_17` - Price drop threshold % for iPhone 17 Pro Max (default: 5.0)

### 5. Local Development Setup

#### Backend Setup

1. Create a virtual environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r ../requirements.txt
```

3. Create a `.env` file in the project root:

```bash
cd ..
touch .env
```

Add your environment variables to `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_TO=recipient@example.com
WEBHOOK_URL=https://your-webhook-url.com
PRICE_THRESHOLD_15=5.0
PRICE_THRESHOLD_16=5.0
PRICE_THRESHOLD_17=5.0
```

4. Test the price monitor:

```bash
cd backend
python price_monitor.py
```

This will create `prices.json` with initial price data.

#### Frontend Setup

1. Install dependencies:

```bash
cd web_ui
npm install
```

2. Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

**Note**: If you encounter build issues due to the "#" character in the path (iCloud Drive), you can:
- Build the frontend in a different location, or
- The build will work fine in GitHub Actions where the path won't have special characters

#### Run Flask API

In a separate terminal:

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

### 6. Build Frontend for Production

```bash
cd web_ui
npm run build
```

This creates a `build/` directory that Flask will serve.

## Usage

### Manual Price Check

Run the price monitor script manually:

```bash
cd backend
python price_monitor.py
```

### View Frontend

1. Start the Flask API: `cd backend && python app.py`
2. Open `http://localhost:5000` in your browser

The frontend will automatically fetch price data from `/api/prices` and display:
- Current prices for each model in cards
- Price change indicators (up/down)
- Historical price charts

### Automated Daily Checks

The GitHub Actions workflow runs daily at 8:00 AM PST (16:00 UTC). It will:
1. Check prices from all sources
2. Update `prices.json`
3. Send notifications if prices drop below thresholds
4. Commit and push updated `prices.json` to the repository

## Project Structure

```
PhoneDealFinder/
├── backend/
│   ├── price_monitor.py    # Price scraping and monitoring script
│   ├── app.py              # Flask API server
│   └── prices.json         # Price history data (generated)
├── web_ui/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── components/     # React components
│   │   │   ├── Header.jsx
│   │   │   ├── PriceCard.jsx
│   │   │   └── PriceChart.jsx
│   │   └── index.jsx
│   ├── build/              # Production build (generated)
│   └── package.json
├── .github/
│   └── workflows/
│       └── price_monitor.yml  # GitHub Actions workflow
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

## API Endpoints

- `GET /api/prices` - Returns all price history as JSON array

## Configuration

### Price Drop Thresholds

Set the percentage drop required to trigger notifications:
- Default: 5% drop
- Configure via environment variables: `PRICE_THRESHOLD_15`, `PRICE_THRESHOLD_16`, `PRICE_THRESHOLD_17`

### Notification Methods

**Email (SMTP):**
- Configure SMTP settings in environment variables
- Supports Gmail, Outlook, and other SMTP servers
- For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833)

**Webhook:**
- Optional webhook URL for custom integrations
- Receives JSON payload with price drop details

## Troubleshooting

### Build Issues with "#" in Path

If you're using iCloud Drive and encounter build errors due to the "#" character:
- The build will work correctly in GitHub Actions
- For local builds, consider cloning to a path without special characters

### Price Scraping Failures

If prices aren't being fetched:
- Check that the target websites are accessible
- Verify the HTML structure hasn't changed (selectors may need updating)
- Check network connectivity and rate limiting

### Email Notifications Not Sending

- Verify SMTP credentials in GitHub Secrets
- For Gmail, ensure you're using an App Password, not your regular password
- Check that `SMTP_TO` is set correctly

## Security Considerations

- Never commit `.env` files or credentials to the repository
- All sensitive data is stored in GitHub Secrets for Actions
- The scraper uses proper User-Agent headers and rate limiting
- No personal or financial data is collected or stored

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available for personal use.

## Notes

- The price scraping functions may need adjustment if the target websites change their HTML structure
- Apple's Certified Refurbished page uses dynamic content, so the scraper may need updates
- Reebelo listings may vary, so the lowest price is selected from available listings
- Price data is stored in `prices.json` and tracked in Git for historical analysis

