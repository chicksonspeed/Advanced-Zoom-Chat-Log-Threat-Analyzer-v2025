
# Advanced Zoom Chat Log Threat Analyzer v2025

**Enterprise Edition - Real-time Threat Detection & Analysis Platform**

A sophisticated application for analyzing Zoom chat logs to detect threats, harassment, and suspicious behavior patterns. Originally built as a desktop GUI application, now evolved into a modern web-based platform with enhanced features, real-time analysis, dynamic threat scoring, and comprehensive reporting capabilities.

![Version](https://img.shields.io/badge/version-v2025.08.26-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Flask](https://img.shields.io/badge/flask-2.3+-orange)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 🚀 Evolution & Features

### 🔄 **Application Evolution**
- **Original Version**: Desktop GUI built with Tkinter and PyInstaller
- **Current Version**: Modern web-based interface with Flask and Socket.IO
- **Enhanced Features**: Real-time updates, responsive design, improved UX
- **Better Performance**: Optimized for large datasets and faster processing

### 🔍 **Advanced Threat Detection**
- **Real-time Analysis**: Process chat logs instantly with live threat detection
- **Dynamic Scoring System**: 1-10 severity scale with color-coded threat levels
- **Smart Spam Detection**: Context-aware spam scoring based on user threat history
- **Behavioral Analysis**: Track user patterns, frequency, and escalation
- **Configurable Rules**: Customizable threat detection patterns and weights

### 🌐 **Modern Web Interface (Current)**
- **Responsive Design**: Beautiful dark-mode UI with modern aesthetics
- **Real-time Updates**: Live threat detection with Socket.IO integration
- **Interactive Dashboard**: Comprehensive analytics with multiple tabs
- **Drag & Drop Upload**: Intuitive file upload with progress tracking
- **Batch Processing**: Process entire folders of chat logs efficiently
- **Cross-platform**: Works on any device with a modern web browser

### 🖥️ **Original Desktop GUI (Legacy)**
- **Native Application**: Standalone executable for macOS
- **Tkinter Interface**: Traditional desktop application layout
- **File-based Processing**: Direct file system integration
- **Local Processing**: No network dependencies
- **Simple Interface**: Basic upload and analysis functionality

### 📊 **Comprehensive Dashboard**
- **Real-time Metrics**: Live threat counts, user analysis, and risk scoring
- **Interactive Tabs**: Threats, Users, Timeline, Analytics, Meetings, Reports
- **Individual Meeting View**: Browse specific chat logs with full context
- **Visual Analytics**: Charts and graphs for threat distribution and trends

### 🔒 **Security & Privacy**
- **AES-256 Encryption**: All message content encrypted at rest
- **Local Processing**: No data leaves your system
- **Secure Storage**: SQLite database with encrypted content
- **Backup System**: Automatic file backups with integrity checks
- **Auto-cleanup**: Automatic deletion of low-threat data after 7 days

### 📈 **Enterprise Reporting**
- **Law Enforcement Package**: Complete evidence export with hashes
- **Executive Summary**: High-level threat analysis and recommendations
- **PDF/Excel Export**: Professional reports for documentation
- **Templated Harassment Reports**: Pre-filled forms for official complaints

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- macOS (tested on macOS 14.6.0)
- 4GB+ RAM recommended for large datasets
- Modern web browser (Chrome, Firefox, Safari, Edge) - for web version

### Quick Start - Web Version (Current)
```bash
# Clone or navigate to the application directory
cd "/Users/hampusnilsson/zoom scripts/ZoomChatThreatAnalyzer_App_v2025"

# Create and activate virtual environment
python3 -m venv venv_secure_analyzer
source venv_secure_analyzer/bin/activate

# Install core dependencies
pip install -r requirements_improved.txt

# Install web dependencies
pip install flask flask-socketio

# Run the web application
python advanced_web_analyzer.py
```

### Legacy Desktop Version (Original)
```bash
# For the original Tkinter-based GUI
python improved_app_gui.py

# Or build standalone executable
python build_standalone.py
```

### Alternative Installation Script
```bash
# Use the provided installation script
chmod +x install_improved.sh
./install_improved.sh
```

### Manual Dependencies Installation
```bash
# Core dependencies
pip install cryptography>=41.0.0
pip install typing-extensions>=4.0.0

# Web framework (for current version)
pip install flask>=2.3.0
pip install flask-socketio>=5.3.0

# GUI framework (for legacy version)
pip install tkinter

# Optional: PDF export
pip install weasyprint>=60.0
```

## 🎯 Usage

### Starting the Web Application (Current)
```bash
# Navigate to the app directory
cd "/Users/hampusnilsson/zoom scripts/ZoomChatThreatAnalyzer_App_v2025"

# Activate virtual environment
source venv_secure_analyzer/bin/activate

# Launch the web application
python advanced_web_analyzer.py
```

The web application will start on **http://localhost:8081**

### Starting the Desktop Application (Legacy)
```bash
# For the original GUI version
python improved_app_gui.py

# Or run the standalone executable
./ZoomChatThreatAnalyzer.app
```

### Quick Start Guide - Web Version

#### 1. **Upload Files**
- **Drag & Drop**: Simply drag .txt chat log files into the upload area
- **Select Files**: Click "Select Files" to choose individual chat logs
- **Select Folder**: Click "Select Folder" to process entire directories
- **Process Folder**: Use "Process Folder" to analyze files in a specific path

#### 2. **View Results**
- **Threats Tab**: Real-time threat detection with severity indicators
- **Users Tab**: User behavior analysis and risk profiling
- **Meetings Tab**: Browse individual chat logs with full context
- **Analytics Tab**: Data visualization and trend analysis

#### 3. **Generate Reports**
- **PDF Report**: Professional documentation
- **Excel Report**: Data analysis and filtering
- **Evidence Package**: Law enforcement export
- **Executive Summary**: High-level analysis

### Quick Start Guide - Desktop Version (Legacy)

#### 1. **File Upload**
- Use the file browser to select .txt chat log files
- Click "Upload Files" to process individual files
- Use "Process Folder" for batch processing

#### 2. **View Analysis**
- Check the threat list for detected issues
- Review user statistics and patterns
- Export reports as needed

## 🔄 Version Comparison

### **Web Version (Current) - Advantages**
- ✅ **Modern UI**: Beautiful dark-mode interface with responsive design
- ✅ **Real-time Updates**: Live threat detection with Socket.IO
- ✅ **Cross-platform**: Works on any device with a web browser
- ✅ **Better UX**: Drag & drop, progress indicators, interactive tabs
- ✅ **Scalable**: Handles large datasets more efficiently
- ✅ **Easy Updates**: No need to rebuild executables
- ✅ **Mobile Friendly**: Responsive design works on phones/tablets

### **Desktop Version (Legacy) - Advantages**
- ✅ **Standalone**: No network dependencies
- ✅ **Native Performance**: Direct system integration
- ✅ **Offline Only**: Completely self-contained
- ✅ **Simple Deployment**: Single executable file
- ✅ **System Integration**: Native file dialogs and notifications

### **Shared Features (Both Versions)**
- ✅ **Same Core Engine**: Identical threat detection algorithms
- ✅ **Same Security**: AES-256 encryption and secure storage
- ✅ **Same Analysis**: Dynamic scoring and behavioral tracking
- ✅ **Same Reports**: PDF, Excel, and law enforcement exports
- ✅ **Same Configuration**: Shared config.json and rules

## Understanding the Interface

### Web Version Interface

#### 📊 Dashboard Overview
- **Analysis Overview**: Total files processed and messages analyzed
- **Threat Detection**: Number of threats detected and high-severity alerts
- **User Analysis**: Unique users and risk users identified
- **Time Analysis**: Days covered and peak activity periods

#### 🚨 Threat Severity Scale (1-10)
- **1-2: Low** (Light Green) - Minor concerns
- **3-4: Low-Medium** (Dark Green) - Moderate concerns
- **5-6: Medium** (Yellow) - Significant concerns
- **7-8: Medium-High** (Orange) - Serious threats
- **9-10: High** (Red) - Critical threats

#### 🔄 Dynamic Spam Detection
- **Clean users** (0 threats): Spam scores 3/10
- **Low-threat users** (1-5 threats): Spam scores 4/10
- **Medium-threat users** (6-10 threats): Spam scores 5/10
- **High-threat users** (10+ threats): Spam scores 7-10/10

### Desktop Version Interface (Legacy)

#### 📋 Basic Layout
- **File Upload Section**: Simple file browser and upload buttons
- **Analysis Results**: Basic list of detected threats
- **Statistics Panel**: Simple metrics display
- **Export Options**: Basic report generation buttons

## Navigation Tabs (Web Version)

#### 🚨 Threats Tab
- Real-time threat detection with severity indicators
- Color-coded threat levels (1-10 scale)
- SPAM indicators for repeated messages
- Scrollable threat list (1200px height)
- Live updates as new threats are detected

#### 👥 Users Tab
- User behavior analysis and risk profiling
- Message frequency and threat patterns
- User threat history and escalation tracking
- Risk user identification and scoring

#### 📅 Timeline Tab
- Temporal analysis of threats
- Activity patterns and peak threat periods
- Chronological threat progression
- Time-based threat clustering

#### 📊 Analytics Tab
- Data visualization and charts
- Threat category distribution
- Risk metrics and trend analysis
- Performance statistics

#### 📋 Meetings Tab
- Individual chat log browsing
- Complete meeting context with all messages
- Meeting-specific threat analysis
- Export individual meeting reports
- Back navigation to main dashboard

#### 📄 Reports Tab
- Generate comprehensive reports
- Law enforcement evidence packages
- Executive summaries and PDF exports
- Custom report templates

## ⚙️ Configuration

### Core Settings (`config.json`)
```json
{
  "watch_dir": "/Users/hampusnilsson/zoom scripts/ZoomChatThreatAnalyzer_App_v2025/ChatLogs",
  "db_path": "/Users/hampusnilsson/zoom scripts/ZoomChatThreatAnalyzer_App_v2025/secure_chat.db",
  "report_dir": "/Users/hampusnilsson/zoom scripts/ZoomChatThreatAnalyzer_App_v2025/output",
  "backup_dir": "/Users/hampusnilsson/zoom scripts/ZoomChatThreatAnalyzer_App_v2025/backups",
  "min_severity_for_alert": 60,
  "auto_delete_days": 7,
  "sophisticated_rules": true,
  "user_behavior_tracking": true
}
```

### Threat Detection Rules
Customize threat detection patterns in `config.json`:
```json
{
  "name": "Rule_Name",
  "pattern": "regex_pattern",
  "weight": 40,
  "category": "threat_category"
}
```

### Current Default Rules
- **Threaten_Call_Boss**: Boss-related threats (weight: 40)
- **Doxxing_Leak**: Personal information sharing (weight: 45)
- **Harassment_Insult**: Verbal abuse and insults (weight: 25)
- **Meth_Mention**: Drug-related content (weight: 10)
- **Coercion_Blackmail**: Blackmail attempts (weight: 35)
- **Self_Harm_Risk**: Suicide threats (weight: 60)
- **Aggressive_Demand**: Demanding behavior (weight: 20)

## 🔧 Technical Architecture

### Core Components (Both Versions)
- **`improved_analyzer_core.py`**: Core analysis engine with encryption
- **`config.json`**: Configuration and threat detection rules
- **`secure_chat.db`**: SQLite database with encrypted content

### Web Version Components
- **`advanced_web_analyzer.py`**: Main Flask web application with Socket.IO
- **HTML5/CSS3**: Modern responsive interface
- **JavaScript**: Interactive dashboard functionality

### Desktop Version Components (Legacy)
- **`improved_app_gui.py`**: Main Tkinter GUI application
- **`build_standalone.py`**: PyInstaller build script
- **Tkinter**: Native GUI framework

### Web Technologies (Current)
- **Flask**: Python web framework
- **Flask-SocketIO**: Real-time communication
- **HTML5/CSS3**: Modern responsive interface
- **JavaScript**: Interactive dashboard functionality
- **SQLite**: Local database storage

### Desktop Technologies (Legacy)
- **Tkinter**: Python GUI framework
- **PyInstaller**: Executable packaging
- **SQLite**: Local database storage

### Data Flow (Both Versions)
1. **File Upload** → File selection or drag & drop
2. **Encryption** → AES-256 encryption of message content
3. **Analysis** → Threat detection with dynamic scoring
4. **Storage** → Encrypted storage in SQLite database
5. **Display** → Dashboard with analysis results
6. **Export** → Professional reports and evidence packages

### Security Features (Both Versions)
- **AES-256 Encryption**: All sensitive data encrypted
- **SHA-256 Integrity**: File integrity verification
- **Local Processing**: No external data transmission
- **Secure Backups**: Encrypted backup system
- **Auto-cleanup**: Automatic deletion of low-threat data

## 📈 Performance

### Scalability (Both Versions)
- **Large Datasets**: Handles 1000+ chat logs efficiently
- **Real-time Processing**: Instant analysis and updates
- **Memory Efficient**: Optimized for large message volumes
- **Database Optimization**: Indexed queries for fast retrieval

### System Requirements
- **Minimum**: 2GB RAM, 1GB storage
- **Recommended**: 4GB RAM, 5GB storage
- **Large Datasets**: 8GB RAM, 20GB storage

### Web Performance (Current)
- **Real-time Updates**: Socket.IO for live data streaming
- **Responsive Design**: Works on desktop and mobile devices
- **Fast Loading**: Optimized for quick dashboard access
- **Efficient Rendering**: Smooth scrolling and interactions

### Desktop Performance (Legacy)
- **Native Speed**: Direct system integration
- **Offline Processing**: No network overhead
- **System Resources**: Direct access to hardware
- **File System**: Native file operations

## 🚨 Threat Detection Capabilities

### Pattern Recognition (Both Versions)
- **Threats & Harassment**: Verbal abuse, intimidation, blackmail
- **Doxxing Attempts**: Personal information sharing
- **Self-Harm Risk**: Suicide threats and dangerous behavior
- **Spam & Repetition**: Automated or repeated messages
- **Behavioral Patterns**: Escalating language and frequency

### Dynamic Scoring (Both Versions)
- **Context-Aware**: Considers user history and patterns
- **Escalation Detection**: Identifies increasing threat levels
- **Frequency Analysis**: Tracks message patterns and timing
- **Similarity Matching**: Detects repeated or similar threats

### Advanced Features (Both Versions)
- **User Behavior Tracking**: Monitor individual user patterns
- **Threat History**: Track user-specific threat escalation
- **Message Deduplication**: SHA-256 based duplicate detection
- **Automatic Cleanup**: Remove low-threat data after 7 days

## 📊 Reporting Features

### Law Enforcement Package (Both Versions)
- **Complete Evidence Export**: All relevant data with integrity hashes
- **Templated Reports**: Pre-filled harassment complaint forms
- **Source Documentation**: Original files with backup copies
- **Chain of Custody**: Cryptographic integrity verification

### Executive Summary (Both Versions)
- **High-Level Analysis**: Key metrics and trends
- **Risk Assessment**: Overall threat level evaluation
- **Recommendations**: Action items and next steps
- **Visual Charts**: Threat distribution and patterns

### Export Formats (Both Versions)
- **PDF Reports**: Professional documentation
- **Excel Reports**: Data analysis and filtering
- **CSV Export**: Raw data for external analysis
- **JSON Export**: Structured data for integration

## 🔍 Troubleshooting

### Common Issues - Web Version

#### Application Won't Start
```bash
# Check Python version
python3 --version

# Verify virtual environment
source venv_secure_analyzer/bin/activate

# Reinstall dependencies
pip install -r requirements_improved.txt
pip install flask flask-socketio
```

#### Port Already in Use
```bash
# Kill existing processes
pkill -f "python advanced_web_analyzer.py"

# Or change port in advanced_web_analyzer.py
# app.run(host='0.0.0.0', port=8082, debug=True)
```

#### Web Interface Issues
```bash
# Clear browser cache
# Try different browser
# Check firewall settings
# Verify localhost:8081 is accessible
```

### Common Issues - Desktop Version (Legacy)

#### GUI Won't Display
```bash
# Check Tkinter installation
python3 -c "import tkinter; print('Tkinter available')"

# Reinstall Tkinter
pip install tkinter
```

#### Executable Won't Run
```bash
# Rebuild executable
python build_standalone.py

# Check file permissions
chmod +x ZoomChatThreatAnalyzer.app
```

### Database Issues (Both Versions)
```bash
# Remove corrupted database
rm secure_chat.db

# Restart application (new database will be created)
python advanced_web_analyzer.py  # or python improved_app_gui.py
```

### Performance Optimization
- **Large Files**: Process in smaller batches
- **Memory Issues**: Increase system RAM or reduce batch size
- **Slow Processing**: Check disk space and database size
- **Web Performance**: Use modern browser, clear cache

## 🔒 Privacy & Compliance

### Data Protection (Both Versions)
- **Local Processing**: All analysis performed locally
- **No Cloud Storage**: Data never leaves your system
- **Encrypted Storage**: All sensitive data encrypted at rest
- **Secure Deletion**: Automatic cleanup of low-threat data

### Compliance Features (Both Versions)
- **Audit Trail**: Complete processing history
- **Evidence Integrity**: Cryptographic verification
- **Export Controls**: Configurable data retention
- **Access Logs**: User activity tracking

### Security Best Practices (Both Versions)
- **Regular Updates**: Keep dependencies updated
- **Access Control**: Limit application access
- **Backup Strategy**: Regular encrypted backups
- **Monitoring**: Track system performance and usage

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>

# Install development dependencies
pip install -r requirements_improved.txt
pip install flask flask-socketio
pip install pytest black flake8

# Run tests
pytest

# Code formatting
black *.py
```

### Code Structure
- **Web Interface**: Flask-based responsive UI
- **Desktop Interface**: Tkinter-based native GUI
- **Analysis Engine**: Modular threat detection system
- **Database Layer**: SQLite with encryption wrapper
- **Reporting System**: Template-based report generation

### Development Guidelines
- **Code Style**: Follow PEP 8 standards
- **Testing**: Write unit tests for new features
- **Documentation**: Update README for changes
- **Security**: Review encryption and access controls

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Documentation
- **User Guide**: This README
- **API Reference**: Inline code documentation
- **Configuration**: `config.json` examples
- **Troubleshooting**: Common issues and solutions

### Getting Help
- **Issues**: Check troubleshooting section
- **Configuration**: Review `config.json` examples
- **Performance**: Monitor system resources
- **Security**: Verify encryption and access controls

### System Information
- **Version**: v2025.08.26
- **Python**: 3.9+
- **Flask**: 2.3+ (web version)
- **Tkinter**: Built-in (desktop version)
- **Database**: SQLite with encryption
- **Platform**: macOS (tested on 14.6.0)

## 🎨 UI/UX Features

### Modern Design (Web Version)
- **Dark Mode**: Professional dark theme
- **Responsive Layout**: Works on all screen sizes
- **Interactive Elements**: Hover effects and animations
- **Clean Typography**: Readable and professional fonts

### User Experience (Web Version)
- **Intuitive Navigation**: Clear tab structure
- **Real-time Feedback**: Live updates and progress indicators
- **Drag & Drop**: Easy file upload
- **Batch Processing**: Efficient bulk operations

### Visual Elements (Web Version)
- **Color-coded Threats**: Severity-based color system
- **Progress Indicators**: Upload and processing status
- **Interactive Charts**: Data visualization
- **Professional Icons**: Clear visual hierarchy

### Legacy Interface (Desktop Version)
- **Native Look**: Traditional desktop application appearance
- **Simple Layout**: Basic file upload and results display
- **System Integration**: Native file dialogs and notifications
- **Offline Operation**: No network dependencies

## 🔄 Migration Guide

### From Desktop to Web Version
1. **Install Web Dependencies**: `pip install flask flask-socketio`
2. **Run Web Application**: `python advanced_web_analyzer.py`
3. **Access via Browser**: Navigate to http://localhost:8081
4. **Same Data**: Database and configuration files are shared

### From Web to Desktop Version
1. **Install Tkinter**: Usually included with Python
2. **Run Desktop App**: `python improved_app_gui.py`
3. **Same Data**: Database and configuration files are shared

---

**Advanced Zoom Chat Log Threat Analyzer v2025** - Enterprise-grade threat detection and analysis for Zoom chat logs.

*Built with security, privacy, and usability in mind. Available as both modern web interface and traditional desktop application.*

**Web Application**: http://localhost:8081  
**Desktop Application**: `python improved_app_gui.py`
