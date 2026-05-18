# FastAPI CI/CD Pipeline with GitHub Actions

A fully-automated, production-ready CI/CD pipeline for deploying a FastAPI application using GitHub Actions, Azure VMs, Docker, and SonarQube for code quality analysis.

## Project Overview

This project demonstrates a complete DevOps workflow where code changes automatically trigger:
- **Automated Testing** - Runs unit tests on every push
- **Code Quality Analysis** - SonarQube scans for bugs and code smells
- **Docker Containerization** - Builds and containerizes the app
- **Automated Deployment** - Deploys to a self-hosted Azure VM runner

I developed a simple application using FastAPI with the main objective of building an automated CI/CD pipeline that gets triggered whenever changes are pushed from the local repository to the remote GitHub repository.

For the CI/CD execution, I used a self-hosted runner configured inside an Microsoft Virtual Machine to achieve better control, reliability, and performance compared to shared runners. I used MobaXterm for SSH access into the virtual machines to perform installations, configurations, and deployment-related activities.

The setup consists of two separate virtual machines:

One VM is dedicated to running the GitHub Actions self-hosted runner.
Another VM is used for setting up SonarQube using a Docker container for code quality analysis and security checks.

I also configured inbound security rules carefully to allow only the required network traffic to the virtual machines, improving the overall security of the environment.

For deployment, I chose a simpler Docker-based approach since the application is intended for smaller traffic and learning purposes. The Docker container is deployed inside the runner virtual machine itself, with port mapping configured as 5000:5000 to expose the FastAPI application.

Using the public IP address of the runner VM, the application can be accessed externally. However, I restricted unnecessary traffic through firewall and network security configurations to improve security and limit unwanted access.

The CI/CD pipeline includes:

Automated build and dependency installation
Security scanning using Trivy and Gitleaks
Unit testing
SonarQube quality analysis
Docker image build and push
Automated container deployment

In my next project, I plan to work with Kubernetes to improve scalability, self-healing, container reliability, and orchestration capabilities. I also plan to use Microsoft AKS (Azure Kubernetes Service) for easier cloud-native container management and deployment automation.

