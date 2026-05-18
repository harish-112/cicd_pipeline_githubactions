# FastAPI CI/CD Pipeline with GitHub Actions

A fully-automated, production-ready CI/CD pipeline for deploying a FastAPI application using GitHub Actions, Azure VMs, Docker, and SonarQube for code quality analysis.

## 🎯 Project Overview

This project demonstrates a complete DevOps workflow where code changes automatically trigger:
- **Automated Testing** - Runs unit tests on every push
- **Code Quality Analysis** - SonarQube scans for bugs and code smells
- **Docker Containerization** - Builds and containerizes the app
- **Automated Deployment** - Deploys to a self-hosted Azure VM runner

No manual deployments. No manual testing. Just push code and watch it happen.

## 🏗️ Architecture

```
Your Local Machine
        ↓
    git push
        ↓
GitHub Repository
        ↓
GitHub Actions Workflow Triggered
        ↓
    ┌─────────────────────────┬─────────────────────────┐
    ↓                         ↓                         ↓
Run Tests               SonarQube Analysis        Build Docker Image
(pytest)               (Code Quality Check)      (containerize app)
    ↓                         ↓                         ↓
    └─────────────────────────┴─────────────────────────┘
                        ↓
                Deploy to Azure VM
        (Docker container starts running)
                        ↓
            FastAPI App Live at IP:5000
```

## 🛠️ Tech Stack

- **Framework**: FastAPI (async Python web framework)
- **Testing**: pytest (unit testing)
- **CI/CD**: GitHub Actions (workflow automation)
- **Code Quality**: SonarQube (bug detection, security analysis)
- **Containerization**: Docker & docker-compose
- **Infrastructure**: Azure VMs
  - **Runner VM**: Self-hosted GitHub Actions runner + app deployment
  - **SonarQube VM**: Docker container running SonarQube server

## 📋 Prerequisites

Before you get started, make sure you have:

### Local Development
- Python 3.9+
- Git
- Virtual environment (venv or conda)

### Infrastructure
- **Azure Account** with 2 VMs:
  - 1 VM for GitHub Actions self-hosted runner (Ubuntu 20.04+)
  - 1 VM for SonarQube (Ubuntu 20.04+)
- GitHub repository with Actions enabled
- Docker and Docker Compose installed on both VMs

## 🚀 Quick Start

### 1. Local Development Setup

```bash
# Clone the repository
git clone https://github.com/harish-112/cicd_pipeline_githubactions.git
cd cicd_pipeline_githubactions

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\Activate.ps1

# Or on Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests locally
pytest test_app.py -v

# Start the app locally
python app.py
```

The app will be available at `http://localhost:5000`

Interactive API docs: `http://localhost:5000/docs`

### 2. Azure VMs Setup

#### A. Runner VM (GitHub Actions Self-Hosted Runner)

```bash
# SSH into your runner VM
ssh -i your-key.pem azureuser@<runner-ip>

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install GitHub Actions Runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.x.x.tar.gz \
  -L https://github.com/actions/runner/releases/download/v2.x.x/actions-runner-linux-x64-2.x.x.tar.gz
tar xzf ./actions-runner-linux-x64-2.x.x.tar.gz

# Configure runner
./config.sh --url https://github.com/harish-112/cicd_pipeline_githubactions --token YOUR_GITHUB_TOKEN

# Run as service
sudo ./svc.sh install
sudo ./svc.sh start
```

#### B. SonarQube VM

```bash
# SSH into SonarQube VM
ssh -i your-key.pem azureuser@<sonarqube-ip>

# Install Docker (same as above)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Run SonarQube in Docker
docker run -d --name sonarqube -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://db:5432/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:latest

# Access at http://<sonarqube-ip>:9000
# Default credentials: admin/admin
```

## 📝 How the Pipeline Works

### Step 1: You Push Code
```bash
git add .
git commit -m "Add new endpoint"
git push origin main
```

### Step 2: GitHub Actions Triggers
The workflow in `.github/workflows/cicd.yml` automatically starts:

```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

### Step 3: Tests Run
```bash
# Automatically runs on self-hosted runner
pytest test_app.py -v
```

### Step 4: SonarQube Analysis
Code gets scanned for:
- ❌ Bugs
- 🔐 Security vulnerabilities
- 💧 Code duplication
- 📏 Code complexity

### Step 5: Docker Build & Deploy
If tests pass:
```bash
# Build Docker image
docker build -t fastapi-app:latest .

# Deploy to runner VM
docker run -d -p 5000:5000 fastapi-app:latest
```

### Step 6: App Goes Live
Your FastAPI app is now running at: `http://<runner-vm-ip>:5000`

## 📂 Project Structure

```
cicd_pipeline_githubactions/
├── app.py                      # FastAPI application
├── test_app.py                 # Unit tests
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # (Optional) Multi-container setup
├── .gitignore                  # Git ignore rules
├── .github/
│   └── workflows/
│       └── cicd.yml           # GitHub Actions workflow
└── README.md                   # This file
```

## 🧪 Testing

Run tests locally:
```bash
pytest test_app.py -v
```

Run specific test:
```bash
pytest test_app.py::test_home -v
```

With coverage:
```bash
pytest test_app.py --cov=app
```

## 🐳 Docker

Build image locally:
```bash
docker build -t fastapi-app:latest .
```

Run container:
```bash
docker run -p 5000:5000 fastapi-app:latest
```

## 🔐 Environment Variables

Create a `.env` file (not committed to repo):
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
SONARQUBE_TOKEN=your-sonarqube-token
```

**Note:** Add `.env` to `.gitignore` to keep secrets safe!

## 📊 Monitoring & Debugging

### GitHub Actions
- View workflow runs: GitHub repo → Actions tab
- Check logs if deployment fails
- Re-run jobs directly from GitHub UI

### SonarQube Dashboard
- Navigate to: `http://<sonarqube-ip>:9000`
- View code quality metrics
- Check security hotspots
- Track issues over time

### App Logs on Runner VM
```bash
docker logs <container-id>
```

## 🛑 Troubleshooting

**Pipeline not triggering?**
- Check GitHub Actions are enabled in repo settings
- Verify runner is online: `Settings → Actions → Runners`
- Check branch protection rules don't block deployment

**Tests failing?**
```bash
# Run locally first
pytest test_app.py -v

# Check logs on runner VM
ssh user@runner-ip
docker logs <container-id>
```

**SonarQube not scanning?**
- Verify SonarQube server is running: `docker ps`
- Check sonar project token in GitHub Actions secrets
- Ensure runner VM can reach SonarQube VM (network security groups)

**App not accessible?**
- Check Docker container is running: `docker ps`
- Verify firewall allows port 5000
- Check app logs: `docker logs <container-id>`

## 🔄 Workflow Tips

### Making Changes
```bash
# Create feature branch (best practice)
git checkout -b feature/add-endpoint

# Make changes, test locally
pytest test_app.py -v

# Commit and push
git add .
git commit -m "Add users endpoint"
git push origin feature/add-endpoint

# Open Pull Request on GitHub
# (Create PR button appears after push)
```

### Code Review Before Merge
- GitHub Actions runs tests automatically on PR
- SonarQube provides quality report
- Team reviews and approves
- Merge to main branch
- Deployment happens automatically

## 📈 Performance & Scalability

Currently deployed on single Azure VM. To scale:

- **Horizontal Scaling**: Multiple Docker containers + load balancer
- **Auto-scaling**: Azure App Service or Kubernetes
- **Database**: Add PostgreSQL for data persistence
- **Caching**: Redis for session/cache management

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open Pull Request

GitHub Actions will automatically test your changes!

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [SonarQube Documentation](https://docs.sonarqube.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Azure VMs Documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/)

## ⚙️ Advanced Configuration

### Custom SonarQube Rules
Edit `sonar-project.properties`:
```properties
sonar.projectKey=fastapi-app
sonar.sources=.
sonar.exclusions=venv/**,tests/**
sonar.python.coverage.reportPaths=coverage.xml
```

### Multi-Environment Deployment
Configure different environments in GitHub Actions:
```yaml
strategy:
  matrix:
    environment: [dev, staging, production]
```

### Slack Notifications
Add workflow notifications to Slack:
```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
```

## 📧 Support & Issues

Found a bug? Have a question?
- Open an issue on GitHub
- Include error logs and steps to reproduce
- Tag with appropriate labels (bug, enhancement, question)

## 📄 License

This project is open source. Feel free to use for learning and projects.

---

**Happy Deploying! 🚀**

*Built with ❤️ using FastAPI, Docker, and GitHub Actions*
