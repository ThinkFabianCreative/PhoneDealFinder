import React from 'react';
import { Card, CardContent, Typography, Box, Chip, Link, Button, CardMedia } from '@mui/material';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import RemoveIcon from '@mui/icons-material/Remove';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

const PriceCard = ({ model, currentPrice, previousPrice, source, url, imageUrl }) => {
  const getPriceChange = () => {
    if (!previousPrice || !currentPrice) return null;
    const change = currentPrice - previousPrice;
    const percentChange = ((change / previousPrice) * 100).toFixed(1);
    return { change, percentChange };
  };

  const priceChange = getPriceChange();
  const isDrop = priceChange && priceChange.change < 0;
  const isRise = priceChange && priceChange.change > 0;

  return (
    <Card 
      sx={{ 
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 4
        }
      }}
      elevation={2}
    >
      {imageUrl && (
        <CardMedia
          component="img"
          image={imageUrl}
          alt={model}
          sx={{
            height: 200,
            objectFit: 'contain',
            backgroundColor: '#fafafa',
            p: 2
          }}
          onError={(e) => {
            e.target.style.display = 'none';
          }}
        />
      )}
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography variant="h6" component="h2" gutterBottom>
          {model}
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Chip 
            label={source === 'apple_refurbished' ? 'Apple Refurbished' : 'Reebelo'} 
            size="small" 
            color={source === 'apple_refurbished' ? 'primary' : 'secondary'}
            sx={{ mb: 1 }}
          />
        </Box>
        <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', mb: 1 }}>
          ${currentPrice ? currentPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : 'N/A'}
        </Typography>
        {priceChange && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 2 }}>
            {isDrop && <TrendingDownIcon color="success" />}
            {isRise && <TrendingUpIcon color="error" />}
            {!isDrop && !isRise && <RemoveIcon color="disabled" />}
            <Typography 
              variant="body2" 
              color={isDrop ? 'success.main' : isRise ? 'error.main' : 'text.secondary'}
            >
              {isDrop ? '-' : '+'}${Math.abs(priceChange.change).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} 
              ({isDrop ? '' : '+'}{priceChange.percentChange}%)
            </Typography>
          </Box>
        )}
        {url && (
          <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid', borderColor: 'divider' }}>
            <Button
              component={Link}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              variant="outlined"
              size="small"
              fullWidth
              endIcon={<OpenInNewIcon />}
            >
              View Listing
            </Button>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default PriceCard;

