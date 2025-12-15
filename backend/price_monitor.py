#!/usr/bin/env python3
"""
iPhone Price Monitor
Fetches current prices for iPhone 15/16/17 Pro Max (256GB) from various sources
and stores them in prices.json. Sends notifications when prices drop.
"""

import json
import os
import time
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, List
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
PRICES_FILE = os.path.join(os.path.dirname(__file__), 'prices.json')
RATE_LIMIT_DELAY = 2.5  # seconds between requests
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Model configurations
MODELS = {
    'iPhone 15 Pro Max': {
        'source': 'apple_refurbished',
        'url': 'https://www.apple.com/shop/product/refurbished/iphone/iphone-15-pro-max',
        'storage': '256GB',
        'image_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/refurb-iphone-15-pro-max-naturaltitanium-256gb?wid=200&hei=200&fmt=jpeg&qlt=90&.v=1694026287138'
    },
    'iPhone 16 Pro Max': {
        'source': 'reebelo',
        'url': 'https://www.reebelo.com/search?q=iphone+16+pro+max+256gb',
        'storage': '256GB',
        'image_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-max-naturaltitanium-select?wid=200&hei=200&fmt=jpeg&qlt=90&.v=1726616109456'
    },
    'iPhone 17 Pro Max': {
        'source': 'reebelo',
        'url': 'https://www.reebelo.com/search?q=iphone+17+pro+max+256gb',
        'storage': '256GB',
        'image_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-max-naturaltitanium-select?wid=200&hei=200&fmt=jpeg&qlt=90&.v=1726616109456'  # Placeholder - update when iPhone 17 is released
    }
}


def load_prices() -> List[Dict]:
    """Load existing price data from JSON file."""
    if os.path.exists(PRICES_FILE):
        try:
            with open(PRICES_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error loading prices.json: {e}. Starting with empty list.")
            return []
    return []


def save_prices(prices: List[Dict]) -> None:
    """Save price data to JSON file."""
    try:
        with open(PRICES_FILE, 'w') as f:
            json.dump(prices, f, indent=2)
        logger.info(f"Saved {len(prices)} price entries to {PRICES_FILE}")
    except IOError as e:
        logger.error(f"Error saving prices.json: {e}")


def fetch_apple_refurbished_price(url: str) -> Optional[float]:
    """
    Fetch price from Apple Certified Refurbished store.
    Note: Apple's site uses dynamic content, so this may need adjustment
    based on actual page structure.
    """
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Apple's refurbished page structure may vary
        # Look for price elements - common selectors
        price_selectors = [
            'span[class*="price"]',
            'div[class*="price"]',
            '[data-autom="price"]',
            '.as-price-currentprice'
        ]
        
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Extract numeric value
                price_str = ''.join(filter(str.isdigit, price_text.replace(',', '')))
                if price_str:
                    return float(price_str) / 100 if len(price_str) > 2 else float(price_str)
        
        logger.warning(f"Could not find price on Apple Refurbished page")
        return None
        
    except requests.RequestException as e:
        logger.error(f"Error fetching Apple Refurbished price: {e}")
        return None
    except (ValueError, AttributeError) as e:
        logger.error(f"Error parsing Apple Refurbished price: {e}")
        return None


def fetch_reebelo_price(url: str) -> Optional[float]:
    """
    Fetch price from Reebelo listings.
    Returns the lowest price found for the specified model.
    """
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Reebelo price selectors - adjust based on actual page structure
        price_selectors = [
            '[class*="price"]',
            '[data-price]',
            '.product-price',
            '.price-value'
        ]
        
        prices_found = []
        for selector in price_selectors:
            price_elems = soup.select(selector)
            for elem in price_elems:
                price_text = elem.get_text(strip=True)
                # Extract numeric value (handle currency symbols)
                price_str = ''.join(filter(lambda x: x.isdigit() or x == '.', price_text.replace(',', '')))
                try:
                    price = float(price_str)
                    if 100 < price < 5000:  # Reasonable price range
                        prices_found.append(price)
                except ValueError:
                    continue
        
        if prices_found:
            return min(prices_found)  # Return lowest price
        
        logger.warning(f"Could not find price on Reebelo page")
        return None
        
    except requests.RequestException as e:
        logger.error(f"Error fetching Reebelo price: {e}")
        return None
    except (ValueError, AttributeError) as e:
        logger.error(f"Error parsing Reebelo price: {e}")
        return None


def fetch_price(model: str) -> Optional[float]:
    """Fetch price for a specific model from its configured source."""
    config = MODELS.get(model)
    if not config:
        logger.error(f"Unknown model: {model}")
        return None
    
    logger.info(f"Fetching price for {model} from {config['source']}...")
    time.sleep(RATE_LIMIT_DELAY)  # Rate limiting
    
    if config['source'] == 'apple_refurbished':
        return fetch_apple_refurbished_price(config['url'])
    elif config['source'] == 'reebelo':
        return fetch_reebelo_price(config['url'])
    else:
        logger.error(f"Unknown source: {config['source']}")
        return None


def get_latest_price(prices: List[Dict], model: str) -> Optional[float]:
    """Get the most recent price for a model."""
    model_prices = [p for p in prices if p.get('model') == model]
    if not model_prices:
        return None
    # Sort by timestamp and get latest
    model_prices.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return model_prices[0].get('price')


def check_price_drop(new_price: float, old_price: float, threshold_percent: float = 5.0) -> bool:
    """Check if price dropped by threshold percentage."""
    if old_price is None:
        return False
    drop_percent = ((old_price - new_price) / old_price) * 100
    return drop_percent >= threshold_percent


def send_email_notification(model: str, old_price: float, new_price: float) -> bool:
    """Send email notification via SMTP."""
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    smtp_to = os.getenv('SMTP_TO')
    
    if not all([smtp_host, smtp_user, smtp_password, smtp_to]):
        logger.warning("SMTP credentials not configured. Skipping email notification.")
        return False
    
    try:
        drop_percent = ((old_price - new_price) / old_price) * 100
        savings = old_price - new_price
        
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = smtp_to
        msg['Subject'] = f'Price Drop Alert: {model}'
        
        body = f"""
        Price Drop Alert!
        
        Model: {model}
        Previous Price: ${old_price:,.2f}
        New Price: ${new_price:,.2f}
        Savings: ${savings:,.2f} ({drop_percent:.1f}% drop)
        
        Check it out now!
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        logger.info(f"Email notification sent for {model}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email notification: {e}")
        return False


def send_webhook_notification(model: str, old_price: float, new_price: float) -> bool:
    """Send webhook notification."""
    webhook_url = os.getenv('WEBHOOK_URL')
    
    if not webhook_url:
        logger.debug("Webhook URL not configured. Skipping webhook notification.")
        return False
    
    try:
        drop_percent = ((old_price - new_price) / old_price) * 100
        savings = old_price - new_price
        
        payload = {
            'model': model,
            'old_price': old_price,
            'new_price': new_price,
            'savings': savings,
            'drop_percent': drop_percent,
            'timestamp': datetime.now().isoformat()
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Webhook notification sent for {model}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending webhook notification: {e}")
        return False


def get_threshold(model: str) -> float:
    """Get price drop threshold for a model from environment variables."""
    threshold_key = f'PRICE_THRESHOLD_{model.split()[1]}'  # Extract model number
    return float(os.getenv(threshold_key, '5.0'))


def main():
    """Main monitoring function."""
    logger.info("Starting price monitoring...")
    
    # Load existing prices
    prices = load_prices()
    
    # Fetch prices for each model
    timestamp = datetime.now().isoformat()
    new_entries = []
    
    for model in MODELS.keys():
        price = fetch_price(model)
        
        if price is None:
            logger.warning(f"Could not fetch price for {model}. Skipping.")
            continue
        
        # Create new entry
        entry = {
            'timestamp': timestamp,
            'model': model,
            'price': price,
            'source': MODELS[model]['source'],
            'url': MODELS[model]['url'],
            'image_url': MODELS[model].get('image_url', '')
        }
        new_entries.append(entry)
        prices.append(entry)
        
        logger.info(f"{model}: ${price:,.2f}")
        
        # Check for price drops
        old_price = get_latest_price(prices[:-1], model)  # Exclude the entry we just added
        if old_price:
            threshold = get_threshold(model)
            if check_price_drop(price, old_price, threshold):
                logger.info(f"Price drop detected for {model}: ${old_price:,.2f} -> ${price:,.2f}")
                send_email_notification(model, old_price, price)
                send_webhook_notification(model, old_price, price)
    
    # Save updated prices
    save_prices(prices)
    
    logger.info("Price monitoring completed.")


if __name__ == '__main__':
    main()

