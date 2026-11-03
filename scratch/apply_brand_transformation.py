"""
AgentX Complete UI Branding & Design Transformation
Applies the 10th X logo design and the official color palette:
Deep Black: #08090D
Dark Charcoal: #111318
Graphite: #1B1E25
Metallic Silver: #AEB4BE
Bright Orange-Red: #FF4B24
Dark Orange: #B92D16
Soft White: #F5F6F8
"""

import sys
from pathlib import Path

BASE_DIR = Path(r"C:\Users\karan\Desktop\AgentX")
TEMPLATES_DIR = BASE_DIR / "templates"

# ========================================================
# 1. GENERATE LOGIN.HTML
# ========================================================
LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AgentX | Secure Authentication</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><polygon points='18,18 36,18 82,82 64,82' fill='%231B1E25'/><polygon points='62,18 82,18 56,48 44,48' fill='%23282D37'/><polygon points='18,82 38,82 56,60 44,60' fill='%23282D37'/><polygon points='8,92 46,47 94,6 54,53' fill='%23FF4B24'/><line x1='14' y1='86' x2='88' y2='12' stroke='%23FFF5F0' stroke-width='3'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">

<style>
:root {
    --bg-main: #08090D;
    --bg-card: #111318;
    --panel-graphite: #1B1E25;
    --border-color: #232833;
    --border-hover: #373E4D;
    --text-primary: #F5F6F8;
    --text-secondary: #AEB4BE;
    --text-muted: #727B8E;
    --accent-orange-red: #FF4B24;
    --accent-orange-dark: #B92D16;
    --accent-orange-light: #FF6B3D;
    --glow-orange: rgba(255, 75, 36, 0.32);
    --glow-orange-soft: rgba(255, 75, 36, 0.15);
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background: radial-gradient(circle at 80% 15%, #1B1E25 0%, transparent 45%),
                radial-gradient(circle at 20% 85%, #14171E 0%, transparent 40%),
                var(--bg-main);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    position: relative;
    overflow-x: hidden;
}

/* Subtle Ambient Glow Blobs */
.ambient-glow {
    position: absolute;
    border-radius: 50%;
    filter: blur(90px);
    opacity: 0.12;
    pointer-events: none;
    z-index: 1;
}
.blob-1 {
    width: 450px;
    height: 450px;
    top: -100px;
    right: 10%;
    background: radial-gradient(circle, #FF4B24, #B92D16);
    animation: floatBlob1 20s ease-in-out infinite alternate;
}
.blob-2 {
    width: 480px;
    height: 480px;
    bottom: -120px;
    left: 8%;
    background: radial-gradient(circle, #AEB4BE, transparent);
    animation: floatBlob2 25s ease-in-out infinite alternate;
}
@keyframes floatBlob1 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(-30px, 30px) scale(1.08); }
}
@keyframes floatBlob2 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(35px, -30px) scale(0.95); }
}

.auth-wrapper {
    width: 100%;
    max-width: 460px;
    position: relative;
    z-index: 10;
    animation: authFadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes authFadeIn {
    from {
        opacity: 0;
        transform: translateY(16px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.auth-card {
    background: linear-gradient(165deg, rgba(17, 19, 24, 0.95), rgba(11, 13, 17, 0.98));
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 38px 34px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.75), 0 0 40px rgba(255, 75, 36, 0.08);
    backdrop-filter: blur(16px);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.auth-card:hover {
    border-color: rgba(255, 75, 36, 0.35);
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), 0 0 45px var(--glow-orange-soft);
}

.brand-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-bottom: 28px;
}

/* 10th Logo Badge */
.brand-icon-wrapper {
    width: 64px;
    height: 64px;
    display: grid;
    place-items: center;
    border-radius: 16px;
    background: linear-gradient(145deg, #1B1E25, #111318);
    border: 1px solid rgba(255, 75, 36, 0.35);
    box-shadow: 0 0 24px var(--glow-orange);
    margin-bottom: 14px;
    position: relative;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}

.brand-icon-wrapper:hover {
    transform: scale(1.08) rotate(5deg);
    border-color: var(--accent-orange-red);
    box-shadow: 0 0 35px var(--glow-orange);
}

.brand-title {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.brand-title .x-accent {
    color: var(--accent-orange-red);
    text-shadow: 0 0 16px rgba(255, 75, 36, 0.6);
}

.brand-subtitle {
    font-size: 11.5px;
    color: var(--text-secondary);
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 600;
}

.auth-tabs {
    display: flex;
    background: #0B0C10;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 4px;
    margin-bottom: 24px;
    gap: 4px;
}

.tab-btn {
    flex: 1;
    padding: 9px;
    background: transparent;
    border: none;
    border-radius: 8px;
    color: var(--text-secondary);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.tab-btn:hover {
    color: var(--text-primary);
}

.tab-btn.active {
    background: linear-gradient(135deg, rgba(255, 75, 36, 0.22), rgba(185, 45, 22, 0.18));
    border: 1px solid rgba(255, 75, 36, 0.45);
    color: #ffffff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
}

.form-group {
    margin-bottom: 18px;
}

.form-label {
    display: block;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 7px;
}

.input-container {
    position: relative;
    display: flex;
    align-items: center;
}

.form-input {
    width: 100%;
    padding: 12px 16px;
    background: var(--panel-graphite);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 13.5px;
    transition: all 0.2s ease;
}

.form-input:focus {
    outline: none;
    border-color: var(--accent-orange-red);
    box-shadow: 0 0 0 3px rgba(255, 75, 36, 0.2);
    background: #14171E;
}

.form-input.has-icon {
    padding-right: 44px;
}

.toggle-password {
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 15px;
    padding: 4px;
    display: flex;
    align-items: center;
    transition: color 0.2s;
}

.toggle-password:hover {
    color: var(--text-primary);
}

.auth-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 22px;
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    color: var(--text-secondary);
}

.checkbox-label input {
    accent-color: var(--accent-orange-red);
    cursor: pointer;
}

.submit-btn {
    width: 100%;
    padding: 13px;
    border: none;
    border-radius: 11px;
    background: linear-gradient(135deg, var(--accent-orange-red), var(--accent-orange-dark));
    color: white;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 4px 18px rgba(255, 75, 36, 0.4);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
}

.submit-btn:hover {
    box-shadow: 0 6px 26px rgba(255, 75, 36, 0.65);
    transform: translateY(-2px) scale(1.01);
    filter: brightness(1.1);
}

.submit-btn:active {
    transform: translateY(0);
}

.submit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.alert-box {
    display: none;
    padding: 12px 14px;
    border-radius: 10px;
    font-size: 12px;
    margin-bottom: 18px;
    line-height: 1.4;
    animation: fadeIn 0.3s ease;
}

.alert-danger {
    background: rgba(185, 45, 22, 0.18);
    border: 1px solid rgba(255, 75, 36, 0.45);
    color: #FFA278;
}

.alert-success {
    background: rgba(174, 180, 190, 0.12);
    border: 1px solid rgba(174, 180, 190, 0.35);
    color: #F5F6F8;
}

.spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
}

.auth-footer {
    text-align: center;
    margin-top: 24px;
    color: var(--text-muted);
    font-size: 11px;
}

.privacy-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin-top: 18px;
    color: var(--text-secondary);
    font-size: 11px;
}
</style>
</head>
<body>

<div class="ambient-glow blob-1"></div>
<div class="ambient-glow blob-2"></div>

<div class="auth-wrapper">
    <div class="auth-card">
        <!-- Brand Section with 10th Logo -->
        <div class="brand-section">
            <div class="brand-icon-wrapper" title="AgentX Identity">
                <svg width="44" height="44" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="login-metal-1" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#3A404E" />
                            <stop offset="50%" stop-color="#1B1E25" />
                            <stop offset="100%" stop-color="#0E1014" />
                        </linearGradient>
                        <linearGradient id="login-metal-2" x1="100%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#282D37" />
                            <stop offset="100%" stop-color="#08090D" />
                        </linearGradient>
                        <linearGradient id="login-slash" x1="0%" y1="100%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#B92D16" />
                            <stop offset="30%" stop-color="#FF4B24" />
                            <stop offset="70%" stop-color="#FF6B3D" />
                            <stop offset="100%" stop-color="#FFA278" />
                        </linearGradient>
                        <linearGradient id="login-highlight" x1="0%" y1="100%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#FF4B24" />
                            <stop offset="50%" stop-color="#FFFFFF" />
                            <stop offset="100%" stop-color="#FF6B3D" />
                        </linearGradient>
                        <filter id="login-glow" x="-30%" y="-30%" width="160%" height="160%">
                            <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
                            <feMerge>
                                <feMergeNode in="blur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>

                    <!-- Metallic X Arms -->
                    <polygon points="62,18 82,18 56,48 44,48" fill="url(#login-metal-1)" />
                    <polygon points="18,82 38,82 56,60 44,60" fill="url(#login-metal-2)" />
                    <polygon points="18,18 36,18 82,82 64,82" fill="url(#login-metal-1)" />
                    <polygon points="27,18 82,82 76,82 21,18" fill="url(#login-metal-2)" opacity="0.85" />
                    <!-- Silver bevel edges -->
                    <polygon points="18,18 36,18 34,20 20,20" fill="#AEB4BE" opacity="0.8" />
                    <polygon points="64,82 82,82 80,80 66,80" fill="#AEB4BE" opacity="0.8" />

                    <!-- 10th Logo Sharp Red-Orange Slash -->
                    <polygon points="8,92 46,47 94,6 54,53" fill="url(#login-slash)" filter="url(#login-glow)" />
                    <polygon points="12,88 48,49 90,10 52,51" fill="#FF4B24" />
                    <line x1="14" y1="86" x2="88" y2="12" stroke="url(#login-highlight)" stroke-width="2" stroke-linecap="round" />
                    <polygon points="94,6 88,14 86,10" fill="#FFF5F0" />
                    <polygon points="8,92 16,86 12,84" fill="#FF4B24" />
                </svg>
            </div>
            <h1 class="brand-title">Agent<span class="x-accent">X</span></h1>
            <p class="brand-subtitle">Autonomous AI Intelligence Engine</p>
        </div>

        <div class="auth-tabs">
            <button class="tab-btn active" id="tabSignIn" onclick="switchTab('signin')">Sign In</button>
            <button class="tab-btn" id="tabSignUp" onclick="switchTab('signup')">Create Account</button>
        </div>

        <!-- Alert Notification Box -->
        <div class="alert-box" id="alertBox"></div>

        <!-- SIGN IN FORM -->
        <form id="signInForm" onsubmit="handleSignIn(event)">
            <div class="form-group">
                <label class="form-label" for="loginIdentifier">Username or Email</label>
                <div class="input-container">
                    <input type="text" id="loginIdentifier" class="form-input" placeholder="e.g. admin or your@email.com" required autocomplete="username">
                </div>
            </div>

            <div class="form-group">
                <label class="form-label" for="loginPassword">Password</label>
                <div class="input-container">
                    <input type="password" id="loginPassword" class="form-input has-icon" placeholder="Enter your password" required autocomplete="current-password">
                    <button type="button" class="toggle-password" onclick="togglePasswordVisibility('loginPassword', this)">👁</button>
                </div>
            </div>

            <div class="auth-options">
                <label class="checkbox-label">
                    <input type="checkbox" id="rememberMe">
                    <span>Remember my session</span>
                </label>
            </div>

            <button type="submit" class="submit-btn" id="btnSubmitLogin">
                <span id="btnTextLogin">Sign In to AgentX</span>
            </button>
        </form>

        <!-- SIGN UP FORM -->
        <form id="signUpForm" style="display:none;" onsubmit="handleSignUp(event)">
            <div class="form-group">
                <label class="form-label" for="signupUsername">Username</label>
                <div class="input-container">
                    <input type="text" id="signupUsername" class="form-input" placeholder="Choose a username (3-30 chars)" required autocomplete="username">
                </div>
            </div>

            <div class="form-group">
                <label class="form-label" for="signupEmail">Email Address</label>
                <div class="input-container">
                    <input type="email" id="signupEmail" class="form-input" placeholder="your.name@company.com" required autocomplete="email">
                </div>
            </div>

            <div class="form-group">
                <label class="form-label" for="signupPassword">Password</label>
                <div class="input-container">
                    <input type="password" id="signupPassword" class="form-input has-icon" placeholder="Min. 6 characters" required autocomplete="new-password">
                    <button type="button" class="toggle-password" onclick="togglePasswordVisibility('signupPassword', this)">👁</button>
                </div>
            </div>

            <div class="form-group">
                <label class="form-label" for="signupConfirmPassword">Confirm Password</label>
                <div class="input-container">
                    <input type="password" id="signupConfirmPassword" class="form-input has-icon" placeholder="Re-enter your password" required autocomplete="new-password">
                    <button type="button" class="toggle-password" onclick="togglePasswordVisibility('signupConfirmPassword', this)">👁</button>
                </div>
            </div>

            <button type="submit" class="submit-btn" id="btnSubmitSignup">
                <span id="btnTextSignup">Create AgentX Account</span>
            </button>
        </form>

        <div class="privacy-badge">
            <span>🛡</span>
            <span>Zero Data Leakage • Sandboxed Code Execution</span>
        </div>
    </div>

    <div class="auth-footer">
        © 2026 AgentX Autonomous AI Systems. All rights reserved.
    </div>
</div>

<script>
function switchTab(tab) {
    const tabSignIn = document.getElementById('tabSignIn');
    const tabSignUp = document.getElementById('tabSignUp');
    const signInForm = document.getElementById('signInForm');
    const signUpForm = document.getElementById('signUpForm');
    const alertBox = document.getElementById('alertBox');
    alertBox.style.display = 'none';

    if (tab === 'signin') {
        tabSignIn.classList.add('active');
        tabSignUp.classList.remove('active');
        signInForm.style.display = 'block';
        signUpForm.style.display = 'none';
        document.getElementById('loginIdentifier').focus();
    } else {
        tabSignUp.classList.add('active');
        tabSignIn.classList.remove('active');
        signUpForm.style.display = 'block';
        signInForm.style.display = 'none';
        document.getElementById('signupUsername').focus();
    }
}

function togglePasswordVisibility(fieldId, btn) {
    const field = document.getElementById(fieldId);
    if (field.type === 'password') {
        field.type = 'text';
        btn.style.opacity = '1';
    } else {
        field.type = 'password';
        btn.style.opacity = '0.7';
    }
}

function showAlert(message, type = 'danger') {
    const box = document.getElementById('alertBox');
    box.className = `alert-box alert-${type}`;
    box.textContent = message;
    box.style.display = 'block';
}

async function handleSignIn(e) {
    e.preventDefault();
    const btn = document.getElementById('btnSubmitLogin');
    const btnText = document.getElementById('btnTextLogin');
    const identifier = document.getElementById('loginIdentifier').value.trim();
    const password = document.getElementById('loginPassword').value;
    const remember = document.getElementById('rememberMe').checked;

    btn.disabled = true;
    btnText.innerHTML = '<span class="spinner"></span> Authenticating...';

    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ identifier, password, remember })
        });
        const data = await res.json();
        if (res.ok && data.success) {
            showAlert('Login successful! Initializing autonomous workspace...', 'success');
            setTimeout(() => {
                window.location.href = data.redirect || '/';
            }, 500);
        } else {
            showAlert(data.error || 'Authentication failed. Please verify credentials.');
        }
    } catch (err) {
        showAlert('Network or server error during sign in.');
    } finally {
        btn.disabled = false;
        btnText.textContent = 'Sign In to AgentX';
    }
}

async function handleSignUp(e) {
    e.preventDefault();
    const btn = document.getElementById('btnSubmitSignup');
    const btnText = document.getElementById('btnTextSignup');
    const username = document.getElementById('signupUsername').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirmPassword').value;

    if (password !== confirm) {
        showAlert('Passwords do not match.');
        return;
    }

    btn.disabled = true;
    btnText.innerHTML = '<span class="spinner"></span> Creating account...';

    try {
        const res = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        const data = await res.json();
        if (res.ok && data.success) {
            showAlert('Account created successfully! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = data.redirect || '/';
            }, 600);
        } else {
            showAlert(data.error || 'Account creation failed.');
        }
    } catch (err) {
        showAlert('Network or server error during sign up.');
    } finally {
        btn.disabled = false;
        btnText.textContent = 'Create AgentX Account';
    }
}
</script>
</body>
</html>
"""

with open(TEMPLATES_DIR / "login.html", "w", encoding="utf-8") as f:
    f.write(LOGIN_HTML)

print("Generated dark metallic & orange-red login.html with 10th logo!")
