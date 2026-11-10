# RetailIQ – AI-Powered Inventory Intelligence

Enterprise Inventory Monitoring, Forecasting, and Automated Replenishment Agent.

## Deployment to Vercel (100% Pre-Configured)

1. **Push to GitHub**:
   ```bash
   git init
   git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
   git add .
   git commit -m "Deploy RetailIQ to Vercel"
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your repository.
   - Vercel will automatically detect **Vite** as the framework preset.
   - Click **Deploy**!
   - Everything (Vite frontend + FastAPI serverless backend + SQLite database) will deploy together.
