# Security Checklist for StoryGenerator

## 🔴 CRITICAL - Immediate Actions Required

### 1. API Key Security

- [ ] **Revoke ALL exposed API keys immediately**
  - [ ] OpenAI API keys exposed in:
    - `Generators/GStoryIdeas.py`
    - `Generators/GScript.py`
    - `Generators/GRevise.py`
    - `Generators/GEnhanceScript.py`
  - [ ] ElevenLabs API key exposed in:
    - `Generators/GVoice.py`

- [ ] **Generate new API keys**
  - [ ] New OpenAI API key: https://platform.openai.com/api-keys
  - [ ] New ElevenLabs API key: https://elevenlabs.io/app/settings/api-keys

- [ ] **Remove hardcoded keys from source**
  - [ ] Update `GStoryIdeas.py` to use environment variables
  - [ ] Update `GScript.py` to use environment variables
  - [ ] Update `GRevise.py` to use environment variables
  - [ ] Update `GEnhanceScript.py` to use environment variables
  - [ ] Update `GVoice.py` to use environment variables

- [ ] **Set up environment variables**
  - [ ] Install `python-dotenv`: `pip install python-dotenv`
  - [ ] Copy `.env.example` to `.env`
  - [ ] Add new API keys to `.env`
  - [ ] Verify `.env` is in `.gitignore`
  - [ ] Test that code works with environment variables

### 2. Git History Cleanup

⚠️ **WARNING**: Removing secrets from Git history requires force-pushing and can affect collaborators

- [ ] **Option A: Use BFG Repo-Cleaner (Recommended)**
  ```bash
  # Install BFG
  # Download from: https://rtyley.github.io/bfg-repo-cleaner/
  
  # Create a fresh clone
  git clone --mirror https://github.com/Nomoos/StoryGenerator.git
  cd StoryGenerator.git
  
  # Remove the API keys (replace with actual key prefixes)
  bfg --replace-text passwords.txt
  
  # Force push
  git reflog expire --expire=now --all
  git gc --prune=now --aggressive
  git push --force
  ```

- [ ] **Option B: Use git-filter-repo**
  ```bash
  pip install git-filter-repo
  
  # Create patterns file
  echo 'sk-proj-==>' > patterns.txt
  echo 'sk_==>' >> patterns.txt
  
  # Run filter
  git filter-repo --replace-text patterns.txt
  
  # Force push
  git push --force
  ```

- [ ] **Notify all collaborators** about force push
- [ ] **Everyone needs to re-clone** the repository

### 3. Monitoring

- [ ] **Set up API usage alerts**
  - [ ] OpenAI: https://platform.openai.com/usage
  - [ ] ElevenLabs: https://elevenlabs.io/app/usage

- [ ] **Monitor for unusual activity**
  - [ ] Check API usage patterns
  - [ ] Review billing statements
  - [ ] Set up spending limits if available

- [ ] **Enable GitHub secret scanning**
  - [ ] Go to repository Settings → Security → Code security
  - [ ] Enable "Secret scanning"

## 🟡 HIGH PRIORITY - Complete Within 1 Week

### 4. Additional Security Measures

- [ ] **Implement proper secret management**
  - [ ] Document how to set up `.env` file
  - [ ] Add `.env.example` with placeholder values
  - [ ] Update README with security instructions

- [ ] **Code review**
  - [ ] Search codebase for other hardcoded secrets
    ```bash
    grep -r "sk-" .
    grep -r "api_key" .
    grep -r "password" .
    grep -r "secret" .
    ```

- [ ] **Repository settings**
  - [ ] Enable branch protection on main branch
  - [ ] Require pull request reviews
  - [ ] Enable status checks

- [ ] **Access control**
  - [ ] Review who has access to the repository
  - [ ] Remove unnecessary collaborators
  - [ ] Use principle of least privilege

### 5. Development Security

- [ ] **Install pre-commit hooks**
  ```bash
  pip install pre-commit
  pre-commit install
  ```

- [ ] **Add security scanning**
  - [ ] Install `bandit`: `pip install bandit`
  - [ ] Run security scan: `bandit -r Generators/ Models/ Tools/`
  - [ ] Fix any issues found

- [ ] **Dependency security**
  - [ ] Check for vulnerable packages: `pip-audit`
  - [ ] Update dependencies: `pip list --outdated`
  - [ ] Pin versions in `requirements.txt`

## 🟢 MEDIUM PRIORITY - Complete Within 2 Weeks

### 6. Infrastructure Security

- [ ] **Separate development and production**
  - [ ] Use different API keys for dev/prod
  - [ ] Document environment setup
  - [ ] Create separate `.env` files

- [ ] **Implement logging (without sensitive data)**
  - [ ] Log API calls (without keys)
  - [ ] Log errors and exceptions
  - [ ] Set up log rotation

- [ ] **Rate limiting and retries**
  - [ ] Implement exponential backoff
  - [ ] Add rate limiting
  - [ ] Handle API errors gracefully

### 7. Team Security

- [ ] **Security training**
  - [ ] Share security best practices with team
  - [ ] Document what NOT to commit
  - [ ] Regular security reminders

- [ ] **Code review process**
  - [ ] Always review PRs for secrets
  - [ ] Use automated tools in CI/CD
  - [ ] Implement security checklist for reviews

- [ ] **Documentation**
  - [ ] Document security procedures
  - [ ] Create incident response plan
  - [ ] Document who to contact for security issues

## 🔵 LOW PRIORITY - Nice to Have

### 8. Advanced Security

- [ ] **Secrets management service**
  - [ ] Consider AWS Secrets Manager
  - [ ] Or Azure Key Vault
  - [ ] Or HashiCorp Vault

- [ ] **CI/CD security**
  - [ ] Add secret scanning to CI
  - [ ] Add dependency scanning
  - [ ] Add SAST (Static Application Security Testing)

- [ ] **Security audits**
  - [ ] Regular security reviews
  - [ ] Penetration testing
  - [ ] Third-party security audit

## Verification Steps

After completing the critical items, verify:

1. **No secrets in code**
   ```bash
   # Should return no results
   grep -r "sk-proj" Generators/
   grep -r "sk_" Generators/
   ```

2. **Environment variables working**
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   assert os.getenv('OPENAI_API_KEY'), "OpenAI key not found"
   assert os.getenv('ELEVENLABS_API_KEY'), "ElevenLabs key not found"
   ```

3. **Git history clean** (after cleanup)
   ```bash
   git log --all --full-history --source --all -- '*api_key*'
   # Should return no results
   ```

4. **No unauthorized API usage**
   - Check OpenAI dashboard
   - Check ElevenLabs dashboard
   - Verify charges are expected

## Emergency Response

If you suspect the keys have been compromised:

1. **Immediate**: Revoke keys (takes ~5 minutes)
2. **Within 1 hour**: Generate new keys and update `.env`
3. **Within 24 hours**: Review API usage logs
4. **Within 48 hours**: Complete git history cleanup
5. **Within 1 week**: Implement all critical security measures

## Resources

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Git Secret Removal Guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## Contact

For security concerns, contact: [Add security contact email]

---

**Last Updated**: January 2025  
**Review Frequency**: Monthly or after any security incident
