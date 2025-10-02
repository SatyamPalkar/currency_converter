# Deployment Guide - Elite Currency Exchange

## Quick Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

1. **Initialize Git (if not already done)**
   ```bash
   git init
   ```

2. **Add all files**
   ```bash
   git add .
   ```

3. **Commit your changes**
   ```bash
   git commit -m "Deploy Elite Currency Exchange"
   ```

4. **Create a GitHub repository**
   - Go to https://github.com
   - Click "New repository"
   - Name it "elite-currency-exchange"
   - Don't initialize with README (we already have one)

5. **Connect and push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/elite-currency-exchange.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Click "Sign up" or "Sign in"
   - Connect your GitHub account

2. **Deploy Your App**
   - Click "New app"
   - Select your GitHub repository: `elite-currency-exchange`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **Your App is Live!**
   - Your app will be available at: `https://YOUR_USERNAME-elite-currency-exchange-app-xxxxx.streamlit.app`
   - Deployment usually takes 2-3 minutes

### Step 3: Custom Domain (Optional)

If you want a custom domain:
1. Go to your app settings in Streamlit Cloud
2. Add your custom domain
3. Update your DNS settings

## Alternative Deployment Options

### Heroku Deployment

1. **Install Heroku CLI**
2. **Create Procfile**
   ```
   web: sh setup.sh && streamlit run app.py
   ```
3. **Create setup.sh**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [general]\n\
   email = \"your-email@domain.com\"\n\
   " > ~/.streamlit/credentials.toml
   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = $PORT\n\
   " > ~/.streamlit/config.toml
   ```
4. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Railway Deployment

1. Go to https://railway.app
2. Connect your GitHub repository
3. Select Python environment
4. Deploy automatically

## Troubleshooting

### Common Issues:

1. **Import Errors**
   - Make sure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **API Errors**
   - The Frankfurter API is free and doesn't require authentication
   - Check internet connectivity

3. **Deployment Fails**
   - Check the logs in Streamlit Cloud
   - Ensure all files are committed to GitHub

### Support

- Streamlit Community: https://discuss.streamlit.io
- GitHub Issues: Create an issue in your repository
- Streamlit Docs: https://docs.streamlit.io

## Post-Deployment

### Monitor Your App
- Check app performance in Streamlit Cloud dashboard
- Monitor usage and errors
- Update as needed

### Share Your App
- Add the live URL to your README.md
- Share on social media
- Add to your portfolio

---

**Your Elite Currency Exchange is now live! 🎉**
