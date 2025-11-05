# GitHub Actions Workflows

This directory contains automated CI/CD workflows for the Agile TaskIQ project.

## Workflows

### 1. CI/CD Pipeline (`ci.yml`)

**Triggers**: Push to main/master/develop, Pull Requests

**Jobs**:
- **Backend Tests**: Runs pytest with coverage reporting
- **Frontend Tests**: Runs React tests with coverage
- **Linting**: Code quality checks (flake8, black, isort)
- **Security Quick Check**: Fast security scan (Bandit, Safety)
- **Build Test**: Validates Docker builds
- **Integration Tests**: End-to-end testing with docker-compose
- **Status Check**: Overall pipeline status

**Artifacts**:
- Backend coverage reports (HTML)
- Frontend coverage reports
- Test results

### 2. Security Scan (`security.yml`)

**Triggers**: 
- Push to main/master/develop
- Pull Requests
- Weekly schedule (Mondays at 9 AM UTC)
- Manual trigger

**Jobs**:
- **Security Scan**: 
  - Bandit (Python security linter)
  - Safety (dependency vulnerability check)
  - pip-audit (Python package vulnerabilities)
  - TruffleHog (secret detection)
- **Dependency Review**: Reviews dependency changes in PRs
- **CodeQL Analysis**: Advanced code analysis for Python and JavaScript
- **Docker Security**: Trivy scanner for container vulnerabilities
- **Security Gate**: Final security check

**Artifacts**:
- Bandit security report (JSON)
- Safety security report (JSON)
- pip-audit security report (JSON)
- Trivy scan results (SARIF)

## Usage

### Viewing Workflow Results

1. Navigate to the **Actions** tab in GitHub
2. Select a workflow run
3. View job results and logs
4. Download artifacts for detailed reports

### Manual Trigger

To manually trigger the security scan:

1. Go to **Actions** tab
2. Select **Security Scan** workflow
3. Click **Run workflow**
4. Select branch and click **Run workflow**

### Status Badges

Add to your README.md:

```markdown
![CI/CD](https://github.com/YOUR_ORG/YOUR_REPO/workflows/CI/CD%20Pipeline/badge.svg)
![Security](https://github.com/YOUR_ORG/YOUR_REPO/workflows/Security%20Scan/badge.svg)
```

## Security Reports

### Accessing Reports

After each security scan:

1. Go to workflow run
2. Scroll to **Artifacts** section
3. Download security reports:
   - `bandit-security-report`
   - `safety-security-report`
   - `pip-audit-security-report`

### Interpreting Results

**Bandit Severity Levels**:
- LOW: Minor issues, informational
- MEDIUM: Potential security issues
- HIGH: Serious security issues that should be addressed

**Safety/pip-audit**:
- Lists known CVEs in dependencies
- Provides severity ratings and remediation advice

### Addressing Security Issues

1. Review security report artifacts
2. Prioritize by severity (HIGH → MEDIUM → LOW)
3. Update vulnerable dependencies:
   ```bash
   pip install --upgrade <package>
   ```
4. Fix code issues identified by Bandit
5. Re-run security scan to verify fixes

## Coverage Reports

### Backend Coverage

- **Threshold**: 80% minimum
- **Location**: `backend/htmlcov/index.html` (in artifacts)
- **Upload**: Automatically uploaded to Codecov (if configured)

### Frontend Coverage

- **Location**: `frontend/coverage/` (in artifacts)
- **Format**: HTML and LCOV

## Troubleshooting

### Workflow Fails on Dependencies

**Issue**: `pip install` or `npm ci` fails

**Solution**:
- Check `requirements.txt` and `package.json` are valid
- Ensure all dependencies are available
- Check for version conflicts

### Tests Fail in CI but Pass Locally

**Issue**: Tests pass on local machine but fail in GitHub Actions

**Solution**:
- Check environment variables
- Verify database setup
- Check file paths (case sensitivity on Linux)
- Review CI logs for specific errors

### Security Scan Reports False Positives

**Issue**: Bandit reports issues that are not actual vulnerabilities

**Solution**:
- Add `# nosec` comment to suppress specific warnings
- Update `.banditrc` configuration file
- Document why the issue is not a concern

### Docker Build Fails

**Issue**: Docker image build fails in CI

**Solution**:
- Test build locally: `docker build -t test .`
- Check Dockerfile syntax
- Verify all files are committed
- Check `.dockerignore` isn't excluding needed files

## Configuration

### Environment Variables

Set in GitHub repository settings → Secrets and variables → Actions:

- `CODECOV_TOKEN`: For coverage upload (optional)
- `DOCKER_USERNAME`: For Docker Hub push (if deploying)
- `DOCKER_PASSWORD`: For Docker Hub push (if deploying)

### Branch Protection Rules

Recommended settings:

1. Go to Settings → Branches
2. Add rule for `main` branch:
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - Select required checks:
     - Backend Tests
     - Frontend Tests
     - Security Quick Check
     - Integration Tests
   - ✅ Require pull request reviews
   - ✅ Dismiss stale reviews

## Performance

### Typical Run Times

- **CI/CD Pipeline**: 5-10 minutes
- **Security Scan**: 8-15 minutes
- **CodeQL Analysis**: 10-20 minutes

### Optimization Tips

1. Use caching for dependencies
2. Run jobs in parallel where possible
3. Use `continue-on-error` for non-critical checks
4. Limit integration test scope

## Maintenance

### Weekly Tasks

- Review security scan results
- Update dependencies with vulnerabilities
- Check coverage trends

### Monthly Tasks

- Review and update workflow configurations
- Update GitHub Actions versions
- Review and clean up old artifacts

## Support

For issues with workflows:

1. Check workflow logs in GitHub Actions
2. Review this documentation
3. Contact DevOps team or Member 4 (Integration & Testing)

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Safety Documentation](https://pyup.io/safety/)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)

---

**Last Updated**: November 5, 2025  
**Maintained By**: Member 4 (Integration & Testing)


