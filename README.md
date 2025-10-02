# Elite Currency Exchange

A professional, high-end currency converter web application with real-time exchange rates, advanced analytics, and beautiful visualizations.

## 🌟 Features

### Core Functionality
- **Real-time Currency Conversion**: Convert between 30+ currencies with live exchange rates
- **Historical Rate Lookup**: Check exchange rates for any date since 2000
- **Interactive Charts**: Multiple chart types (Line, Area, Candlestick) with different time periods
- **Quick Calculator**: Preset amounts for instant conversions

### Professional Interface
- **Glassmorphism Design**: Modern, professional UI with glass-card effects
- **Responsive Layout**: Optimized for desktop and mobile devices
- **Clean Typography**: Professional fonts and spacing
- **Real-time Stats**: Current rates, 24h changes, weekly highs/lows

### Advanced Features
- **Conversion History**: Track your recent conversions with timestamps
- **Currency Comparison**: Compare rates against major currencies
- **Loading States**: Smooth animations and progress indicators
- **Error Handling**: Professional error messages and validation

## 🚀 Live Demo

**Deployed Application**: [Your Streamlit Cloud URL will go here]

## 📁 Project Structure

```
currency_converter/
├── app.py                 # Main Streamlit application
├── api.py                 # Frankfurter API integration
├── currency.py            # Currency formatting utilities
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version specification
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## 🛠️ Local Development

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd currency_converter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy Elite Currency Exchange"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Choose `app.py` as the main file
   - Click "Deploy"

### Alternative Deployment Options

#### Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
```

#### Railway
- Connect your GitHub repository to Railway
- Select Python environment
- Deploy automatically

## 🔧 Configuration

### Environment Variables
No environment variables required - the app uses the free Frankfurter API.

### Customization
- **Colors**: Modify the CSS in `app.py` for custom branding
- **Currencies**: Add more currency mappings in the `currency_names` dictionary
- **Features**: Extend functionality by adding new sections

## 📊 API Information

This application uses the **Frankfurter API** for exchange rate data:
- **Base URL**: https://api.frankfurter.app
- **Rate Limit**: No authentication required
- **Data Source**: European Central Bank
- **Update Frequency**: Daily (weekdays)

## 🔒 Security & Privacy

- **No Data Storage**: No user data is stored permanently
- **Session-based History**: Conversion history is only stored during the session
- **HTTPS**: All API calls are made over secure connections
- **No Authentication**: No user accounts or personal information required

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Frankfurter API** for providing free exchange rate data
- **Streamlit** for the amazing web app framework
- **Plotly** for interactive charts and visualizations

## 📞 Support

For support or questions:
- Create an issue in this repository
- Contact: [Your email or contact information]

---

**Built with ❤️ using Python and Streamlit**