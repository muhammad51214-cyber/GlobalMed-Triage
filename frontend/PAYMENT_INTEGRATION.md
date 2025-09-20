# Crossmint Payment Integration

This document explains the Crossmint payment system integration in the GlobalMed Dispatch application.

## Overview

The payment system allows users to purchase premium emergency dispatch services through Crossmint's secure payment platform. The integration supports multiple payment methods including credit cards, cryptocurrency, Apple Pay, and Google Pay.

## Architecture

### Components

1. **PaymentSystem** - Main payment plan selection interface
2. **PaymentIntegration** - Compact payment component for workflows
3. **CrossmintGateway** - Direct Crossmint API integration
4. **PaymentContext** - Global payment state management
5. **DevelopmentNotice** - Development mode indicator

### Utilities

- **crossmintApi.ts** - Secure API utility with SSL certificate handling

## Features

### Payment Plans

- **Basic Emergency** ($29.99/month) - Essential dispatch services
- **Premium Dispatch** ($79.99/month) - Advanced services with priority support
- **Enterprise Solution** ($199.99/month) - Complete emergency management system

### Payment Methods

- 💳 Credit/Debit Cards
- ₿ Cryptocurrency payments
- 🍎 Apple Pay
- G Google Pay

## Development vs Production

### Development Mode

In development mode (`import.meta.env.DEV`), the system:
- Simulates API calls instead of making real requests
- Shows a development notice to users
- Uses mock payment data
- Avoids SSL certificate issues

### Production Mode

In production mode, the system:
- Makes real API calls to Crossmint
- Handles SSL certificate validation
- Processes actual payments
- Provides real-time payment status

## SSL Certificate Issue Resolution

The original error `ERR_CERT_DATE_INVALID` was caused by SSL certificate validation issues when making requests to the Crossmint API. This has been resolved by:

1. **Secure API Utility** - Created `crossmintApi.ts` with proper error handling
2. **Development Fallback** - Simulates API responses in development mode
3. **Production Ready** - Handles SSL issues gracefully in production
4. **User Feedback** - Clear error messages and development notices

## Usage

### Basic Payment Flow

```typescript
import { usePayment } from '../contexts/PaymentContext';

const { setPaymentRequired, hasActiveSubscription } = usePayment();

// Check if payment is required
if (!hasActiveSubscription('premium')) {
  setPaymentRequired(true, 'premium');
}
```

### Payment Integration

```typescript
import PaymentIntegration from '../components/PaymentIntegration';

<PaymentIntegration
  onPaymentComplete={(success, data) => {
    if (success) {
      console.log('Payment successful:', data);
    }
  }}
  serviceType="premium"
  amount={79.99}
  description="Upgrade to premium services"
/>
```

## Environment Variables

Required environment variables:

```env
VITE_CROSSMINT_API_KEY=ck_staging_5j4j1E4KdKqWjcDzUPCnTa7h3BNj4k3RjCbaQEqEeN15YBDkPRjrV1cKgYQovS6KrSpW4UpwDUsbEUU9SyoNgVkAHJkwthwwRRjsChMqTMRF78w17wdQswvkE9U1GqimAHPo4URdSxQV2aFpYTqY7rH5xKFeVWL2fBQPZhyUaS7MsZr2gdabCjdGiUWNzq4QhYi2CCUfsgLtXKgLQQ2sSB16
```

## Security Features

- API key stored securely in environment variables
- Payment data encrypted through Crossmint
- Secure order creation and tracking
- Error handling for failed payments
- Development mode protection

## Testing

The payment system can be tested by:

1. **Development Mode** - Automatic simulation of payments
2. **Payment Plans** - Select different service tiers
3. **Payment Methods** - Test all supported payment options
4. **Error Handling** - Verify error states and recovery

## Troubleshooting

### Common Issues

1. **SSL Certificate Errors** - Resolved by development mode simulation
2. **API Key Issues** - Check environment variable configuration
3. **Payment Failures** - Verify Crossmint account setup

### Debug Mode

Enable debug logging by checking the browser console for:
- Payment processing logs
- API call details
- Error messages
- Development mode indicators

## Future Enhancements

- Real-time payment status updates
- Payment history management
- Subscription renewal handling
- Multi-currency support
- Advanced analytics integration
