"""
Build updated templates/index.html for AgentX.
Implements:
1. Move "Suggested Questions" next to the question box (directly above input box, horizontal scrollable chips, auto-send on click, staggered animation, hover lift).
2. Dynamic, stylish AgentX SVG logo (crossing gradient rounded strokes, stroke-dashoffset draw, idle glow pulse, hover rotate, continuous spin on analyzing).
3. Animated, dynamic page (ambient drifting floating blobs, low-contrast, page section fade/slide-up, chat slide-in, bouncing dots typing indicator, card/button hover lift/glow, animated dashed upload border, dark mode theme, prefers-reduced-motion).
4. Simplified question input box (ONLY placeholder 'Ask anything about your dataset', no disclaimers/hints/counters, arrow send icon, glowing focus).
"""

import sys
from pathlib import Path

INDEX_PATH = Path(r"C:\Users\karan\Desktop\AgentX\templates\index.html")

new_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AgentX | AI Data Analyst</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root {
    --bg-main: #090b14;
    --bg-sidebar: #0e1220;
    --panel: #13172c;
    --panel-elevated: #181d36;
    --panel-border: #232946;
    --panel-border-hover: #363e63;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-purple: #8b5cf6;
    --accent-indigo: #6366f1;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-emerald: #10b981;
    --accent-rose: #f43f5e;
    --glow-purple: rgba(139, 92, 246, 0.28);
    --glow-cyan: rgba(6, 182, 212, 0.25);
    --sidebar-width: 320px;
    --header-height: 56px;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background: radial-gradient(circle at 85% 15%, #19163b 0%, transparent 40%),
                radial-gradient(circle at 15% 85%, #0f1d38 0%, transparent 40%),
                var(--bg-main);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    min-height: 100vh;
    overflow: hidden;
    display: flex;
}

button, input, textarea, select {
    font-family: inherit;
    color: inherit;
}

button {
    cursor: pointer;
    border: none;
    background: none;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #252b45;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #3b4268;
}

.app-container {
    display: flex;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    position: relative;
}

/* ========================================================
   SUBTLE AMBIENT ANIMATED BACKGROUND (Requirement 3)
   ======================================================== */
.ambient-glow {
    position: absolute;
    border-radius: 50%;
    filter: blur(85px);
    opacity: 0.14;
    pointer-events: none;
    z-index: 0;
    will-change: transform;
}
.blob-1 {
    width: 440px;
    height: 440px;
    top: -80px;
    right: 8%;
    background: radial-gradient(circle, #8b5cf6, #6366f1);
    animation: floatBlob1 22s ease-in-out infinite alternate;
}
.blob-2 {
    width: 490px;
    height: 490px;
    bottom: -110px;
    left: 10%;
    background: radial-gradient(circle, #3b82f6, #06b6d4);
    animation: floatBlob2 26s ease-in-out infinite alternate;
}
.blob-3 {
    width: 320px;
    height: 320px;
    top: 35%;
    left: 45%;
    background: radial-gradient(circle, #8b5cf6, transparent);
    animation: floatBlob3 30s ease-in-out infinite alternate;
}

@keyframes floatBlob1 {
    0% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(-35px, 25px) scale(1.08); }
    100% { transform: translate(25px, -20px) scale(0.95); }
}
@keyframes floatBlob2 {
    0% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(40px, -35px) scale(1.06); }
    100% { transform: translate(-25px, 25px) scale(0.94); }
}
@keyframes floatBlob3 {
    0% { transform: translate(0, 0) scale(1); opacity: 0.08; }
    50% { transform: translate(-20px, -20px) scale(1.12); opacity: 0.16; }
    100% { transform: translate(20px, 15px) scale(1); opacity: 0.08; }
}

/* ========================================================
   1. LEFT SIDEBAR
   ======================================================== */
.sidebar {
    width: var(--sidebar-width);
    height: 100vh;
    background: var(--bg-sidebar);
    border-right: 1px solid var(--panel-border);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 50;
    overflow-y: auto;
    position: relative;
    animation: pageFadeSlide 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes pageFadeSlide {
    from {
        opacity: 0;
        transform: translateY(14px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.sidebar-header {
    padding: 14px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

/* --- DYNAMIC, STYLISH SVG LOGO (Requirement 2) --- */
.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    outline: none;
}
.brand-x-wrapper {
    position: relative;
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    background: rgba(19, 23, 44, 0.85);
    border: 1px solid rgba(139, 92, 246, 0.35);
    box-shadow: 0 0 14px var(--glow-purple);
    transition: all 0.35s ease;
    animation: logoGlowPulse 4s ease-in-out infinite alternate;
}
.brand:hover .brand-x-wrapper {
    border-color: rgba(6, 182, 212, 0.7);
    box-shadow: 0 0 22px rgba(6, 182, 212, 0.5), 0 0 32px var(--glow-purple);
    transform: scale(1.06);
}
.brand-x-svg {
    width: 24px;
    height: 24px;
    overflow: visible;
    transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), filter 0.4s ease;
}
/* Page load stroke draw-in */
.x-stroke {
    stroke-dasharray: 45;
    stroke-dashoffset: 45;
    animation: drawXStroke 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.x-stroke.stroke-1 {
    animation-delay: 0.1s;
}
.x-stroke.stroke-2 {
    animation-delay: 0.3s;
}
@keyframes drawXStroke {
    to {
        stroke-dashoffset: 0;
    }
}
@keyframes logoGlowPulse {
    0% {
        box-shadow: 0 0 8px rgba(99, 102, 241, 0.35);
    }
    50% {
        box-shadow: 0 0 18px rgba(139, 92, 246, 0.6), 0 0 28px rgba(139, 92, 246, 0.2);
    }
    100% {
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.45);
    }
}
/* Hover: rotate smoothly and brighten */
.brand:hover .brand-x-svg {
    transform: rotate(180deg) scale(1.1);
    filter: drop-shadow(0 0 10px #06b6d4) drop-shadow(0 0 18px #8b5cf6);
}
/* While analyzing: spins or pulses continuously */
.is-analyzing .brand-x-svg,
body.is-analyzing .brand-x-svg {
    animation: xContinuousSpin 1.4s cubic-bezier(0.4, 0, 0.2, 1) infinite !important;
}
@keyframes xContinuousSpin {
    0% {
        transform: rotate(0deg) scale(1);
        filter: drop-shadow(0 0 8px #6366f1);
    }
    50% {
        transform: rotate(180deg) scale(1.15);
        filter: drop-shadow(0 0 20px #06b6d4);
    }
    100% {
        transform: rotate(360deg) scale(1);
        filter: drop-shadow(0 0 8px #8b5cf6);
    }
}

.brand-text h1 {
    font-size: 16px;
    font-weight: 800;
    letter-spacing: -0.4px;
    color: #ffffff;
    display: flex;
    align-items: center;
}
.brand-title .x-letter {
    background: linear-gradient(135deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    display: inline-block;
    transition: transform 0.3s ease;
}
.brand:hover .brand-title .x-letter {
    transform: scale(1.15);
}
.brand-text p {
    font-size: 8.5px;
    font-weight: 600;
    color: var(--accent-cyan);
    letter-spacing: 1px;
    text-transform: uppercase;
}

.sidebar-action-bar {
    padding: 12px 14px 6px;
}
.new-chat-btn {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 9px 12px;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.18), rgba(59, 130, 246, 0.14));
    border: 1px solid rgba(139, 92, 246, 0.35);
    border-radius: 8px;
    color: #ffffff;
    font-size: 12.5px;
    font-weight: 600;
}
.new-chat-btn:hover {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(59, 130, 246, 0.25));
    border-color: var(--accent-purple);
    box-shadow: 0 0 14px var(--glow-purple);
    transform: translateY(-2px) scale(1.02);
}

/* Sidebar Section Headers */
.sidebar-section {
    padding: 10px 14px 6px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}
.sidebar-section-title {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* --- SIDEBAR: Upload Component with Animated Dashed Border (Requirement 3) --- */
.upload-dropzone {
    border: 2px dashed rgba(139, 92, 246, 0.35);
    border-radius: 10px;
    padding: 14px 12px;
    text-align: center;
    background: rgba(14, 18, 32, 0.55);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
    position: relative;
    background-size: 200% 200%;
}
.upload-dropzone:hover {
    border-color: rgba(139, 92, 246, 0.7);
    background: rgba(24, 29, 54, 0.7);
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 4px 18px rgba(139, 92, 246, 0.2);
}
.upload-dropzone.dragover, .upload-dropzone.drag-active {
    border-color: var(--accent-cyan) !important;
    background: rgba(6, 182, 212, 0.12) !important;
    box-shadow: 0 0 24px rgba(6, 182, 212, 0.45) !important;
    transform: scale(1.02);
}

.upload-icon-small {
    font-size: 20px;
    color: var(--accent-purple);
    margin-bottom: 4px;
}
.upload-dropzone-text {
    font-size: 11.5px;
    font-weight: 600;
    color: var(--text-primary);
}
.upload-dropzone-sub {
    font-size: 9.5px;
    color: var(--text-muted);
    margin-top: 2px;
}

/* Selected File Preview Card */
.file-preview-card {
    display: none;
    margin-top: 8px;
    padding: 8px 10px;
    border-radius: 8px;
    background: var(--panel);
    border: 1px solid var(--panel-border);
    transition: all 0.2s ease;
}
.file-preview-card:hover {
    transform: translateY(-1px);
    border-color: rgba(139, 92, 246, 0.4);
}
.file-preview-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11.5px;
}
.file-preview-name {
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 170px;
}
.file-preview-meta {
    font-size: 10px;
    color: var(--accent-cyan);
    font-family: 'JetBrains Mono', monospace;
}
.preview-actions {
    display: flex;
    gap: 6px;
    margin-top: 6px;
}
.btn-primary {
    flex: 1;
    padding: 5px 8px;
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
    color: #ffffff;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    box-shadow: 0 2px 6px var(--glow-purple);
}
.btn-primary:hover:not(:disabled) {
    transform: translateY(-1px) scale(1.02);
    box-shadow: 0 4px 12px var(--glow-purple);
    filter: brightness(1.12);
}
.btn-danger-outline {
    padding: 5px 8px;
    background: transparent;
    border: 1px solid rgba(244, 63, 94, 0.4);
    color: var(--accent-rose);
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
}
.btn-danger-outline:hover {
    background: rgba(244, 63, 94, 0.12);
    transform: translateY(-1px);
}

.upload-progress-wrap {
    display: none;
    margin-top: 8px;
    height: 4px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 2px;
    overflow: hidden;
}
.upload-progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--accent-indigo), var(--accent-cyan));
    transition: width 0.25s ease;
}

.upload-error-box {
    display: none;
    margin-top: 8px;
    padding: 6px 8px;
    border-radius: 6px;
    background: rgba(244, 63, 94, 0.12);
    border: 1px solid rgba(244, 63, 94, 0.3);
    color: #fecdd3;
    font-size: 11px;
    line-height: 1.35;
}

/* --- SIDEBAR: Active Dataset Profiler Info --- */
.dataset-info-box {
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 11px;
    transition: all 0.2s ease;
}
.dataset-info-box:hover {
    transform: translateY(-1px);
    border-color: rgba(139, 92, 246, 0.35);
}
.info-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    color: var(--text-secondary);
}
.info-val {
    font-weight: 600;
    color: var(--text-primary);
    font-family: 'JetBrains Mono', monospace;
}
.schema-chips-container {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    max-height: 90px;
    overflow-y: auto;
    margin-top: 4px;
    padding-top: 4px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
}
.schema-pill {
    font-size: 9.5px;
    padding: 2px 6px;
    border-radius: 4px;
    background: rgba(139, 92, 246, 0.1);
    border: 1px solid rgba(139, 92, 246, 0.2);
    color: #ddd6fe;
    font-family: 'JetBrains Mono', monospace;
}

/* --- SIDEBAR: Chat History --- */
.history-group-header {
    font-size: 9.5px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    padding: 8px 4px 2px;
}
.history-item-btn {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 8px;
    margin: 2px 0;
    border-radius: 6px;
    font-size: 11.5px;
    color: var(--text-secondary);
    text-align: left;
    border: 1px solid transparent;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease, color 0.2s ease;
}
.history-item-btn:hover {
    background: rgba(255, 255, 255, 0.04);
    color: var(--text-primary);
    transform: translateX(3px);
}
.history-item-btn.active {
    background: linear-gradient(90deg, rgba(139, 92, 246, 0.18), rgba(59, 130, 246, 0.1));
    border-color: rgba(139, 92, 246, 0.4);
    color: #ffffff;
}
.history-title-truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
    min-width: 0;
}
.history-del-btn {
    opacity: 0;
    font-size: 11px;
    color: var(--text-muted);
    padding: 2px;
    margin-left: 4px;
}
.history-item-btn:hover .history-del-btn {
    opacity: 0.7;
}
.history-del-btn:hover {
    opacity: 1 !important;
    color: var(--accent-rose);
}

.sidebar-footer {
    padding: 10px 14px;
    border-top: 1px solid var(--panel-border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(10, 13, 24, 0.85);
    margin-top: auto;
}
.user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    overflow: hidden;
}
.user-avatar-circle {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
    display: grid;
    place-items: center;
    font-size: 11px;
    flex-shrink: 0;
}
.user-name-text {
    font-size: 11.5px;
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.logout-btn-link {
    font-size: 11px;
    color: var(--text-muted);
    text-decoration: none;
}
.logout-btn-link:hover {
    color: var(--accent-rose);
}

/* ========================================================
   2. MAIN WORKSPACE (Chat, Tables, Charts, Fixed Composer)
   ======================================================== */
.main-workspace {
    flex: 1;
    height: 100vh;
    display: flex;
    flex-direction: column;
    min-width: 0;
    background: transparent;
    position: relative;
    z-index: 10;
    animation: pageFadeSlide 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Top Navigation Bar */
.topbar {
    height: var(--header-height);
    border-bottom: 1px solid var(--panel-border);
    background: rgba(9, 11, 20, 0.8);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    flex-shrink: 0;
    z-index: 30;
}
.topbar-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.mobile-toggle-btn {
    display: none;
    font-size: 18px;
    color: var(--text-secondary);
}
.session-title-text {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 400px;
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 10px;
}
.export-tool-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 7px;
    font-size: 11.5px;
    font-weight: 500;
    color: var(--text-secondary);
    text-decoration: none;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, border-color 0.2s ease;
}
.export-tool-btn:hover {
    color: var(--text-primary);
    border-color: rgba(139, 92, 246, 0.5);
    background: var(--panel-elevated);
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 4px 14px rgba(139, 92, 246, 0.25);
}

/* Chat Stream Scroll View */
.chat-scroll-area {
    flex: 1;
    overflow-y: auto;
    padding: 24px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.chat-content-width {
    width: 100%;
    max-width: 940px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* Chat Welcome Card */
.chat-welcome-box {
    text-align: center;
    padding: 36px 20px 24px;
    margin-top: 40px;
    animation: fadeIn 0.4s ease;
}
.welcome-logo-badge {
    width: 56px;
    height: 56px;
    margin: 0 auto 16px;
    border-radius: 16px;
    background: rgba(19, 23, 44, 0.9);
    border: 1px solid rgba(139, 92, 246, 0.4);
    box-shadow: 0 0 24px var(--glow-purple);
    display: grid;
    place-items: center;
}
.chat-welcome-box h2 {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
    background: linear-gradient(120deg, #ffffff, #c7d2fe);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.chat-welcome-box p {
    font-size: 13px;
    color: var(--text-secondary);
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Message Rows (Requirement 3: Slide-In) */
.message-row {
    display: flex;
    gap: 12px;
    width: 100%;
    animation: msgSlideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes msgSlideIn {
    from {
        opacity: 0;
        transform: translateY(12px) scale(0.985);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}
.message-row.user {
    justify-content: flex-end;
}
.message-row.user .msg-body-wrapper {
    align-items: flex-end;
}
.message-row.user .message-bubble {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.22), rgba(139, 92, 246, 0.28));
    border: 1px solid rgba(139, 92, 246, 0.4);
    color: #ffffff;
    border-bottom-right-radius: 4px;
}
.message-row.assistant .message-bubble {
    background: var(--panel);
    border: 1px solid var(--panel-border);
    color: var(--text-primary);
    border-bottom-left-radius: 4px;
    width: 100%;
}

.msg-avatar {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    display: grid;
    place-items: center;
    font-size: 13px;
    flex-shrink: 0;
}
.message-row.assistant .msg-avatar {
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
    color: #ffffff;
    box-shadow: 0 0 10px var(--glow-purple);
}
.message-row.user .msg-avatar {
    background: #252b45;
    color: var(--text-secondary);
    order: 2;
}

.msg-body-wrapper {
    display: flex;
    flex-direction: column;
    gap: 6px;
    max-width: 88%;
}
.message-row.assistant .msg-body-wrapper {
    max-width: 95%;
    flex: 1;
}

.message-bubble {
    padding: 12px 16px;
    border-radius: 12px;
    font-size: 13px;
    line-height: 1.55;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    overflow-x: auto;
}

/* Stated Assumptions Pill */
.assumption-banner {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 8px;
    background: rgba(6, 182, 212, 0.1);
    border: 1px solid rgba(6, 182, 212, 0.25);
    border-radius: 5px;
    font-size: 10.5px;
    color: #a5f3fc;
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
}

/* Structured Output Table */
.data-table-wrapper {
    margin-top: 10px;
    border-radius: 8px;
    border: 1px solid var(--panel-border);
    overflow: hidden;
    background: #0d101d;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
}
.data-table-header-info {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 12px;
    background: rgba(255, 255, 255, 0.02);
    border-bottom: 1px solid var(--panel-border);
    font-size: 11px;
    color: var(--text-muted);
}
.data-table-scroll {
    max-height: 380px;
    overflow: auto;
}
.agentx-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    text-align: left;
}
.agentx-table th {
    position: sticky;
    top: 0;
    background: #141930;
    color: #c7d2fe;
    font-weight: 600;
    padding: 8px 12px;
    border-bottom: 1px solid var(--panel-border);
    white-space: nowrap;
    z-index: 2;
}
.agentx-table td {
    padding: 7px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    color: var(--text-secondary);
    white-space: nowrap;
}
.agentx-table tr:hover td {
    background: rgba(139, 92, 246, 0.08);
    color: var(--text-primary);
}
.agentx-table tr:nth-child(even) td {
    background: rgba(255, 255, 255, 0.015);
}

/* Analyzing indicator typing dots (Requirement 3) */
.analyzing-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--text-secondary);
}
.typing-dots {
    display: inline-flex;
    gap: 4px;
    align-items: center;
}
.dot-flashing {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-purple);
    animation: bounceDot 1.4s infinite ease-in-out both;
}
.dot-flashing:nth-child(1) { animation-delay: -0.32s; }
.dot-flashing:nth-child(2) { animation-delay: -0.16s; }
.dot-flashing:nth-child(3) { animation-delay: 0s; }

@keyframes bounceDot {
    0%, 80%, 100% {
        transform: translateY(0);
        opacity: 0.4;
    }
    40% {
        transform: translateY(-6px);
        opacity: 1;
        background: var(--accent-cyan);
    }
}

/* ========================================================
   SUGGESTED QUESTIONS CHIPS ROW (Requirement 1)
   ======================================================== */
.suggested-chips-bar {
    width: 100%;
    margin-bottom: 8px;
    overflow: hidden;
}
.suggested-chips-container {
    display: flex;
    align-items: center;
    gap: 8px;
    overflow-x: auto;
    padding: 4px 2px 6px;
    scrollbar-width: none;
    -ms-overflow-style: none;
    -webkit-overflow-scrolling: touch;
}
.suggested-chips-container::-webkit-scrollbar {
    display: none;
}
.suggested-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(19, 23, 44, 0.85);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(139, 92, 246, 0.28);
    color: #cbd5e1;
    font-size: 11.5px;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 9999px;
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;
    opacity: 0;
    transform: translateY(8px);
    animation: chipFadeIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    animation-delay: calc(var(--chip-idx, 0) * 0.06s);
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                background 0.2s ease,
                border-color 0.2s ease,
                color 0.2s ease,
                box-shadow 0.2s ease;
    user-select: none;
}
.suggested-chip:hover {
    transform: translateY(-2px) scale(1.02);
    background: rgba(139, 92, 246, 0.2);
    border-color: rgba(139, 92, 246, 0.65);
    color: #ffffff;
    box-shadow: 0 4px 14px rgba(139, 92, 246, 0.25);
}
.suggested-chip:active {
    transform: translateY(0) scale(0.98);
}
.suggested-chip .chip-sparkle {
    font-size: 10px;
    color: var(--accent-purple);
    transition: transform 0.2s ease;
}
.suggested-chip:hover .chip-sparkle {
    transform: rotate(45deg) scale(1.2);
    color: var(--accent-cyan);
}
@keyframes chipFadeIn {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ========================================================
   SIMPLIFIED QUESTION INPUT BOX (Requirement 4)
   ======================================================== */
.composer-fixed-area {
    padding: 6px 16px 14px;
    background: linear-gradient(180deg, transparent, rgba(9, 11, 20, 0.95) 25%, var(--bg-main));
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
    z-index: 20;
}
.composer-inner-wrapper {
    width: 100%;
    max-width: 940px;
    display: flex;
    flex-direction: column;
    gap: 0;
}
.composer-input-box {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    background: var(--panel);
    border: 1px solid rgba(139, 92, 246, 0.28);
    border-radius: 16px;
    padding: 10px 14px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.composer-input-box:focus-within {
    border-color: rgba(139, 92, 246, 0.85);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.22),
                0 8px 30px rgba(0, 0, 0, 0.55),
                0 0 20px var(--glow-purple);
}
.composer-textarea {
    flex: 1;
    min-height: 24px;
    max-height: 140px;
    background: transparent;
    border: none;
    outline: none;
    resize: none;
    font-size: 13.5px;
    line-height: 1.5;
    color: var(--text-primary);
    padding: 4px 0;
}
.composer-textarea::placeholder {
    color: var(--text-muted);
    font-size: 13.5px;
}
.composer-send-btn {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
    color: #ffffff;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    box-shadow: 0 2px 10px var(--glow-purple);
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.composer-send-btn svg {
    transition: transform 0.2s ease;
}
.composer-send-btn:hover:not(:disabled) {
    transform: scale(1.06);
    filter: brightness(1.2);
    box-shadow: 0 4px 16px rgba(139, 92, 246, 0.45);
}
.composer-send-btn:hover:not(:disabled) svg {
    transform: translateY(-2px);
}
.composer-send-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
}

/* ========================================================
   RESPONSIVE DESIGN & REDUCED MOTION (Requirement 3, 5)
   ======================================================== */
@media (max-width: 900px) {
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        transform: translateX(-100%);
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.7);
    }
    .sidebar.open {
        transform: translateX(0);
    }
    .mobile-toggle-btn {
        display: block;
    }
    .suggested-chips-container {
        padding-bottom: 8px;
    }
}

@media (max-width: 600px) {
    .topbar {
        padding: 0 12px;
    }
    .session-title-text {
        max-width: 150px;
    }
    .chat-scroll-area {
        padding: 16px 10px;
    }
    .composer-fixed-area {
        padding: 4px 10px 10px;
    }
}

/* Accessibility: Respect Reduced Motion (Requirement 3) */
@media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
        animation-duration: 0.001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.001ms !important;
        scroll-behavior: auto !important;
    }
    .brand-x-svg, .brand-x-wrapper, .dot-flashing, .ambient-glow {
        animation: none !important;
    }
}
</style>
</head>
<body>

<div class="app-container">

    <!-- Ambient Animated Background (Requirement 3) -->
    <div class="ambient-glow blob-1"></div>
    <div class="ambient-glow blob-2"></div>
    <div class="ambient-glow blob-3"></div>

    <!-- ========================================================
         1. LEFT SIDEBAR (Upload, Dataset Profile, History)
         ======================================================== -->
    <aside class="sidebar" id="sidebar">
        <!-- Brand Header with Dynamic SVG Logo (Requirement 2) -->
        <div class="sidebar-header">
            <a href="/" class="brand" id="brandLogo" title="AgentX | AI Data Analyst">
                <div class="brand-x-wrapper">
                    <svg class="brand-x-svg" width="34" height="34" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="agentx-grad-1" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#6366f1">
                                    <animate attributeName="stop-color" values="#6366f1;#8b5cf6;#06b6d4;#6366f1" dur="7s" repeatCount="indefinite" />
                                </stop>
                                <stop offset="50%" stop-color="#8b5cf6">
                                    <animate attributeName="stop-color" values="#8b5cf6;#06b6d4;#6366f1;#8b5cf6" dur="7s" repeatCount="indefinite" />
                                </stop>
                                <stop offset="100%" stop-color="#06b6d4">
                                    <animate attributeName="stop-color" values="#06b6d4;#6366f1;#8b5cf6;#06b6d4" dur="7s" repeatCount="indefinite" />
                                </stop>
                            </linearGradient>
                            <linearGradient id="agentx-grad-2" x1="100%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" stop-color="#06b6d4">
                                    <animate attributeName="stop-color" values="#06b6d4;#6366f1;#8b5cf6;#06b6d4" dur="7s" repeatCount="indefinite" />
                                </stop>
                                <stop offset="50%" stop-color="#8b5cf6">
                                    <animate attributeName="stop-color" values="#8b5cf6;#06b6d4;#6366f1;#8b5cf6" dur="7s" repeatCount="indefinite" />
                                </stop>
                                <stop offset="100%" stop-color="#6366f1">
                                    <animate attributeName="stop-color" values="#6366f1;#8b5cf6;#06b6d4;#6366f1" dur="7s" repeatCount="indefinite" />
                                </stop>
                            </linearGradient>
                        </defs>
                        <!-- Stroke 1: Top-Left to Bottom-Right -->
                        <path class="x-stroke stroke-1" d="M8 8 L28 28" stroke="url(#agentx-grad-1)" stroke-width="4.5" stroke-linecap="round" />
                        <!-- Stroke 2: Top-Right to Bottom-Left -->
                        <path class="x-stroke stroke-2" d="M28 8 L8 28" stroke="url(#agentx-grad-2)" stroke-width="4.5" stroke-linecap="round" />
                    </svg>
                </div>
                <div class="brand-text">
                    <h1 class="brand-title">Agent<span class="x-letter">X</span></h1>
                    <p class="brand-tagline">AI Data Analyst</p>
                </div>
            </a>
            <button class="mobile-toggle-btn" id="closeSidebarBtn" title="Close Sidebar" style="font-size:16px;">✕</button>
        </div>

        <!-- New Chat Trigger -->
        <div class="sidebar-action-bar">
            <button class="new-chat-btn" id="newChatBtn">
                <span>+</span>
                <span>New Analysis Chat</span>
            </button>
        </div>

        <!-- 1. UPLOAD COMPONENT (Section 3a) -->
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>Import Dataset</span>
                <span style="font-size:8.5px; color:var(--accent-cyan); font-family:'JetBrains Mono';">MAX 100MB</span>
            </div>

            <!-- Upload Drop Area -->
            <div class="upload-dropzone" id="dropZone">
                <div class="upload-icon-small">📁</div>
                <div class="upload-dropzone-text">Click or drag & drop</div>
                <div class="upload-dropzone-sub">CSV, TSV, XLSX, JSON, Parquet, TXT</div>
                <input type="file" id="sidebarFileInput" style="display:none;" accept=".csv,.tsv,.xlsx,.xls,.json,.jsonl,.parquet,.txt,.pdf">
            </div>

            <!-- Selected File Preview Card -->
            <div class="file-preview-card" id="filePreviewCard">
                <div class="file-preview-row">
                    <span class="file-preview-name" id="previewFileName">filename.csv</span>
                    <span class="file-preview-meta" id="previewFileMeta">0 KB</span>
                </div>
                <div class="preview-actions">
                    <button class="btn-primary" id="btnUploadSubmit">↑ Upload Now</button>
                    <button class="btn-danger-outline" id="btnUploadClear">Remove</button>
                </div>
            </div>

            <!-- Upload Progress Bar -->
            <div class="upload-progress-wrap" id="uploadProgressWrap">
                <div class="upload-progress-bar" id="uploadProgressBar"></div>
            </div>

            <!-- Upload Error Alert Box -->
            <div class="upload-error-box" id="uploadErrorBox"></div>
        </div>

        <!-- 2. DATASET PROFILE & SCHEMA (Section 3b) -->
        <div class="sidebar-section" id="datasetInfoSection" style="display:none;">
            <div class="sidebar-section-title">
                <span>Dataset Profile</span>
                <button id="btnRemoveDataset" style="color:var(--accent-rose); font-size:10px;" title="Unload dataset">Unload ✕</button>
            </div>
            <div class="dataset-info-box">
                <div class="info-row">
                    <span>File:</span>
                    <span class="info-val" id="infoFileName">-</span>
                </div>
                <div class="info-row">
                    <span>Rows:</span>
                    <span class="info-val" id="infoRowsVal">0</span>
                </div>
                <div class="info-row">
                    <span>Columns:</span>
                    <span class="info-val" id="infoColsVal">0</span>
                </div>
                <div style="font-size:9.5px; color:var(--text-muted); margin:6px 0 2px; font-weight:600;">SCHEMA FIELDS:</div>
                <div class="schema-chips-container" id="infoSchemaChips"></div>
            </div>
        </div>

        <!-- 3. CHAT HISTORY (Old Suggested Questions section removed as per Requirement 1) -->
        <div class="sidebar-section" style="flex:1; border-bottom:none;">
            <div class="sidebar-section-title">
                <span>Chat History</span>
                <button id="refreshHistoryBtn" style="color:var(--text-muted); font-size:11px;" title="Refresh">↻</button>
            </div>
            <div id="historyListContainer">
                <div style="font-size:11px; color:var(--text-muted); padding:10px; text-align:center;" id="historyLoading">Loading chats...</div>
            </div>
        </div>

        <!-- Sidebar User Footer -->
        <div class="sidebar-footer">
            <div class="user-info">
                <div class="user-avatar-circle">👤</div>
                <div class="user-name-text">{{ session.get('username', 'Account') }}</div>
            </div>
            <a href="/logout" class="logout-btn-link" title="Sign out">Logout ⎋</a>
        </div>
    </aside>

    <!-- ========================================================
         2. MAIN ANALYTICS WORKSPACE
         ======================================================== -->
    <main class="main-workspace">

        <!-- Top Navigation Bar -->
        <header class="topbar">
            <div class="topbar-left">
                <button class="mobile-toggle-btn" id="openSidebarBtn" title="Toggle Sidebar">☰</button>
                <div class="session-title-text" id="headerSessionTitle">Data Analyst Session</div>
            </div>
            <div class="topbar-right">
                <button type="button" class="export-tool-btn" id="btnCopyAnswer" title="Copy Latest Answer">
                    📋 Copy Answer
                </button>
                <button type="button" class="export-tool-btn" id="btnExportCSV" title="Export Current Table as CSV" style="display:none;">
                    📥 Export CSV
                </button>
                <a href="#" id="exportReportBtn" class="export-tool-btn" target="_blank" style="display:none;" title="Download Executive Report">
                    📄 Executive Report
                </a>
            </div>
        </header>

        <!-- Chat Stream Area -->
        <div class="chat-scroll-area" id="chatScrollArea">
            <div class="chat-content-width">

                <!-- Welcome Box -->
                <div class="chat-welcome-box" id="chatWelcomeBox">
                    <div class="welcome-logo-badge">
                        <svg width="34" height="34" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path class="x-stroke stroke-1" d="M8 8 L28 28" stroke="url(#agentx-grad-1)" stroke-width="4.5" stroke-linecap="round" />
                            <path class="x-stroke stroke-2" d="M28 8 L8 28" stroke="url(#agentx-grad-2)" stroke-width="4.5" stroke-linecap="round" />
                        </svg>
                    </div>
                    <h2>Ask Any Question On Any Dataset</h2>
                    <p>AgentX auto-detects schemas, executes sandboxed Python code, self-heals errors, and returns mathematically grounded results in proper tables & plain English.</p>
                </div>

                <!-- Messages stream container -->
                <div id="messagesStream" style="display:flex; flex-direction:column; gap:16px; width:100%;"></div>

            </div>
        </div>

        <!-- ========================================================
             FIXED BOTTOM COMPOSER (Requirements 1 & 4)
             ======================================================== -->
        <div class="composer-fixed-area">
            <div class="composer-inner-wrapper">

                <!-- 1. Suggested Questions Chips Bar directly above input (Requirement 1) -->
                <div class="suggested-chips-bar" id="suggestedChipsBar">
                    <div class="suggested-chips-container" id="suggestedChipsContainer"></div>
                </div>

                <!-- 2. Simplified Input Box (Requirement 4) -->
                <form id="queryForm">
                    <div class="composer-input-box">
                        <textarea
                            id="queryInput"
                            class="composer-textarea"
                            placeholder="Ask anything about your dataset"
                            rows="1"
                            required
                        ></textarea>
                        <button type="submit" class="composer-send-btn" id="sendBtn" title="Send Question" disabled>
                            <!-- Upward Arrow SVG Icon -->
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="12" y1="19" x2="12" y2="5"></line>
                                <polyline points="5 12 12 5 19 12"></polyline>
                            </svg>
                        </button>
                    </div>
                </form>

            </div>
        </div>

    </main>
</div>

<!-- ========================================================
     CLIENT-SIDE LOGIC & EVENT CONTROLLER
     ======================================================== -->
<script>
let activeDatasetId = null;
let activeConversationId = null;
let selectedFileToUpload = null;
let lastTableData = null;

// DOM Elements
const sidebar = document.getElementById("sidebar");
const openSidebarBtn = document.getElementById("openSidebarBtn");
const closeSidebarBtn = document.getElementById("closeSidebarBtn");
const newChatBtn = document.getElementById("newChatBtn");

// Upload
const dropZone = document.getElementById("dropZone");
const sidebarFileInput = document.getElementById("sidebarFileInput");
const filePreviewCard = document.getElementById("filePreviewCard");
const previewFileName = document.getElementById("previewFileName");
const previewFileMeta = document.getElementById("previewFileMeta");
const btnUploadSubmit = document.getElementById("btnUploadSubmit");
const btnUploadClear = document.getElementById("btnUploadClear");
const uploadProgressWrap = document.getElementById("uploadProgressWrap");
const uploadProgressBar = document.getElementById("uploadProgressBar");
const uploadErrorBox = document.getElementById("uploadErrorBox");

// Dataset info
const datasetInfoSection = document.getElementById("datasetInfoSection");
const infoFileName = document.getElementById("infoFileName");
const infoRowsVal = document.getElementById("infoRowsVal");
const infoColsVal = document.getElementById("infoColsVal");
const infoSchemaChips = document.getElementById("infoSchemaChips");
const btnRemoveDataset = document.getElementById("btnRemoveDataset");

// Suggested Chips Bar (Requirement 1)
const suggestedChipsBar = document.getElementById("suggestedChipsBar");
const suggestedChipsContainer = document.getElementById("suggestedChipsContainer");

// History
const historyListContainer = document.getElementById("historyListContainer");
const historyLoading = document.getElementById("historyLoading");
const refreshHistoryBtn = document.getElementById("refreshHistoryBtn");

// Chat & Composer
const chatScrollArea = document.getElementById("chatScrollArea");
const chatWelcomeBox = document.getElementById("chatWelcomeBox");
const messagesStream = document.getElementById("messagesStream");
const queryForm = document.getElementById("queryForm");
const queryInput = document.getElementById("queryInput");
const sendBtn = document.getElementById("sendBtn");

// Export buttons
const btnCopyAnswer = document.getElementById("btnCopyAnswer");
const btnExportCSV = document.getElementById("btnExportCSV");
const exportReportBtn = document.getElementById("exportReportBtn");

/* ---------------- MOBILE SIDEBAR TOGGLE ---------------- */
if (openSidebarBtn) openSidebarBtn.addEventListener("click", () => sidebar.classList.add("open"));
if (closeSidebarBtn) closeSidebarBtn.addEventListener("click", () => sidebar.classList.remove("open"));

/* ---------------- TEXTAREA AUTO-RESIZE & KEYSTROKES ---------------- */
queryInput.addEventListener("input", function() {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
    sendBtn.disabled = !this.value.trim();
});

queryInput.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        if (!sendBtn.disabled) {
            queryForm.requestSubmit();
        }
    }
});

/* ---------------- FILE UPLOAD HANDLING (Section 3a) ---------------- */
dropZone.addEventListener("click", () => sidebarFileInput.click());

sidebarFileInput.addEventListener("change", e => {
    if (e.target.files.length > 0) {
        stageFileForUpload(e.target.files[0]);
    }
});

["dragenter", "dragover"].forEach(evt => {
    dropZone.addEventListener(evt, e => {
        e.preventDefault();
        dropZone.classList.add("dragover");
        dropZone.classList.add("drag-active");
    });
});
["dragleave", "drop"].forEach(evt => {
    dropZone.addEventListener(evt, e => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        dropZone.classList.remove("drag-active");
    });
});

dropZone.addEventListener("drop", e => {
    if (e.dataTransfer.files.length > 0) {
        stageFileForUpload(e.dataTransfer.files[0]);
        // Trigger upload immediately on drop as per spec
        executeUpload();
    }
});

function stageFileForUpload(file) {
    selectedFileToUpload = file;
    previewFileName.textContent = file.name;
    const sizeKB = (file.size / 1024).toFixed(1);
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    previewFileMeta.textContent = file.size > 1048576 ? `${sizeMB} MB` : `${sizeKB} KB`;
    filePreviewCard.style.display = "block";
    uploadErrorBox.style.display = "none";
}

btnUploadClear.addEventListener("click", () => {
    selectedFileToUpload = null;
    sidebarFileInput.value = "";
    filePreviewCard.style.display = "none";
    uploadErrorBox.style.display = "none";
});

btnUploadSubmit.addEventListener("click", executeUpload);

async function executeUpload() {
    if (!selectedFileToUpload) return;

    btnUploadSubmit.disabled = true;
    btnUploadSubmit.textContent = "Uploading...";
    uploadProgressWrap.style.display = "block";
    uploadProgressBar.style.width = "40%";
    uploadErrorBox.style.display = "none";

    const formData = new FormData();
    formData.append("file", selectedFileToUpload);

    try {
        uploadProgressBar.style.width = "70%";
        const res = await fetch("/api/upload", {
            method: "POST",
            body: formData
        });

        if (res.status === 401) {
            window.location.href = "/login";
            return;
        }

        const data = await res.json();
        uploadProgressBar.style.width = "100%";

        if (!res.ok) {
            throw new Error(data.error || "Upload failed.");
        }

        activeDatasetId = data.dataset_id;
        filePreviewCard.style.display = "none";
        sidebarFileInput.value = "";
        selectedFileToUpload = null;

        // Populate Sidebar Dataset Info
        renderDatasetInfo(data);

        // Enable Ask
        sendBtn.disabled = !queryInput.value.trim();

    } catch (err) {
        uploadErrorBox.textContent = err.message;
        uploadErrorBox.style.display = "block";
    } finally {
        btnUploadSubmit.disabled = false;
        btnUploadSubmit.textContent = "↑ Upload Now";
        setTimeout(() => { uploadProgressWrap.style.display = "none"; uploadProgressBar.style.width = "0%"; }, 600);
    }
}

function renderDatasetInfo(data) {
    datasetInfoSection.style.display = "block";
    infoFileName.textContent = data.filename || "Uploaded File";
    infoRowsVal.textContent = Number(data.rows ?? 0).toLocaleString();
    infoColsVal.textContent = Number(data.columns ?? 0).toLocaleString();

    // Render schema column chips
    infoSchemaChips.replaceChildren();
    if (Array.isArray(data.column_names)) {
        data.column_names.forEach(col => {
            const pill = document.createElement("span");
            pill.className = "schema-pill";
            pill.textContent = col;
            infoSchemaChips.appendChild(pill);
        });
    }

    // Render dynamic suggested chips directly above input box (Requirement 1)
    renderSuggestedChips(data);

    // Report download button
    if (exportReportBtn) {
        exportReportBtn.style.display = "inline-flex";
        exportReportBtn.href = `/api/report/download?dataset_id=${activeDatasetId}`;
    }
}

/* ---------------- DYNAMIC SUGGESTED CHIPS (Requirement 1) ---------------- */
function renderSuggestedChips(data) {
    if (!suggestedChipsBar || !suggestedChipsContainer) return;

    let questions = [];
    if (data && Array.isArray(data.suggested_questions) && data.suggested_questions.length > 0) {
        questions = data.suggested_questions;
    } else if (data && data.profile && Array.isArray(data.profile.suggested_questions) && data.profile.suggested_questions.length > 0) {
        questions = data.profile.suggested_questions;
    } else if (data && Array.isArray(data.column_names) && data.column_names.length > 0) {
        const cols = data.column_names;
        const numCols = cols.filter(c => /salary|amount|price|revenue|cost|rating|score|balance|profit|age|attendance|cgpa|value/i.test(c));
        const catCols = cols.filter(c => /dept|department|category|region|branch|city|status|gender|brand|diagnosis/i.test(c));

        if (numCols.length > 0 && catCols.length > 0) {
            questions.push(`Average ${numCols[0]} by ${catCols[0]}`);
        }
        if (numCols.length > 0) {
            questions.push(`Top 5 records by ${numCols[0]}`);
            questions.push(`Highest ${numCols[0]}`);
        }
        if (catCols.length > 0) {
            questions.push(`Breakdown by ${catCols[0]}`);
        }
        questions.push("Total records in this dataset");
        questions.push("Summary of missing values");
    } else {
        // Generic starter suggestions before upload
        questions = [
            "Total records count",
            "Summary statistics overview",
            "Highest values ranking",
            "Category breakdown analysis"
        ];
    }

    // Limit to 3-5 chips (scrollable sideways on mobile)
    const displayChips = questions.slice(0, 5);
    suggestedChipsContainer.replaceChildren();

    if (displayChips.length > 0) {
        displayChips.forEach((q, idx) => {
            const chip = document.createElement("button");
            chip.type = "button";
            chip.className = "suggested-chip";
            chip.style.setProperty("--chip-idx", idx);
            chip.innerHTML = `<span class="chip-sparkle">✧</span><span>${escapeHtml(q)}</span>`;
            chip.onclick = () => {
                queryInput.value = q;
                queryInput.dispatchEvent(new Event("input"));
                queryInput.focus();
                // Send immediately on click as per Requirement 1
                if (!sendBtn.disabled) {
                    queryForm.requestSubmit();
                }
            };
            suggestedChipsContainer.appendChild(chip);
        });
        suggestedChipsBar.style.display = "block";
    } else {
        suggestedChipsBar.style.display = "none";
    }
}

btnRemoveDataset.addEventListener("click", () => {
    if (confirm("Remove active dataset from this session?")) {
        activeDatasetId = null;
        datasetInfoSection.style.display = "none";
        renderSuggestedChips(null);
        if (exportReportBtn) exportReportBtn.style.display = "none";
    }
});

/* ---------------- CSV & EXCEL EXPORT (Section 3d) ---------------- */
btnExportCSV.addEventListener("click", () => {
    if (!lastTableData || !lastTableData.columns || !lastTableData.rows) {
        alert("No table data available to export.");
        return;
    }
    const cols = lastTableData.columns;
    const rows = lastTableData.rows;

    let csvContent = cols.map(c => `"${String(c).replace(/"/g, '""')}"`).join(",") + "\n";
    rows.forEach(r => {
        csvContent += r.map(v => `"${String(v !== null && v !== undefined ? v : '').replace(/"/g, '""')}"`).join(",") + "\n";
    });

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `agentx_export_${Date.now()}.csv`;
    link.click();
    URL.revokeObjectURL(url);
});

btnCopyAnswer.addEventListener("click", () => {
    const bubbles = document.querySelectorAll(".message-row.assistant .message-bubble");
    if (bubbles.length === 0) return;
    const lastBubble = bubbles[bubbles.length - 1];
    navigator.clipboard.writeText(lastBubble.innerText).then(() => {
        btnCopyAnswer.textContent = "✓ Copied!";
        setTimeout(() => { btnCopyAnswer.textContent = "📋 Copy Answer"; }, 1500);
    });
});

/* ========================================================
   CHAT STREAM RENDERING & SUBMISSION
   ======================================================== */
queryForm.addEventListener("submit", async e => {
    e.preventDefault();

    const question = queryInput.value.trim();
    if (!question) return;

    if (!activeDatasetId) {
        alert("Please upload a dataset or file first.");
        return;
    }

    queryInput.value = "";
    queryInput.style.height = "auto";
    sendBtn.disabled = true;

    appendUserMessage(question);
    appendAnalyzingIndicator();

    try {
        const res = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                dataset_id: activeDatasetId,
                question: question,
                conversation_id: activeConversationId
            })
        });

        if (res.status === 401) {
            window.location.href = "/login";
            return;
        }

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Question evaluation failed");

        if (data.conversation_id) {
            activeConversationId = data.conversation_id;
            loadConversations(activeConversationId);
        }

        appendAssistantMessage(data.answer, data.critic, data.stated_assumptions);

    } catch (err) {
        removeAnalyzingIndicator();
        appendAssistantMessage("I encountered an issue processing that query: " + err.message, null, null);
    } finally {
        queryInput.focus();
    }
});

function appendUserMessage(text) {
    if (chatWelcomeBox) chatWelcomeBox.style.display = "none";

    const row = document.createElement("div");
    row.className = "message-row user";
    row.innerHTML = `
        <div class="msg-avatar">👤</div>
        <div class="msg-body-wrapper">
            <div class="message-bubble">${escapeHtml(text)}</div>
        </div>
    `;
    messagesStream.appendChild(row);
    scrollChat();
}

/* Typing Indicator (Requirement 2 & 3: Logo spin + bouncing dots) */
function appendAnalyzingIndicator() {
    document.body.classList.add("is-analyzing");

    const row = document.createElement("div");
    row.className = "message-row assistant";
    row.id = "analyzingIndicatorRow";
    row.innerHTML = `
        <div class="msg-avatar">✧</div>
        <div class="msg-body-wrapper">
            <div class="message-bubble">
                <div class="analyzing-indicator">
                    <span class="typing-dots">
                        <span class="dot-flashing"></span>
                        <span class="dot-flashing"></span>
                        <span class="dot-flashing"></span>
                    </span>
                    <span>Analyzing dataset & compiling sandboxed code...</span>
                </div>
            </div>
        </div>
    `;
    messagesStream.appendChild(row);
    scrollChat();
}

function removeAnalyzingIndicator() {
    document.body.classList.remove("is-analyzing");
    const el = document.getElementById("analyzingIndicatorRow");
    if (el) el.remove();
}

function appendAssistantMessage(answer, critic, assumptions) {
    removeAnalyzingIndicator();

    const row = document.createElement("div");
    row.className = "message-row assistant";
    row.innerHTML = `
        <div class="msg-avatar">✧</div>
        <div class="msg-body-wrapper">
            <div class="message-bubble"></div>
        </div>
    `;

    const bubble = row.querySelector(".message-bubble");

    // 1. Render stated assumptions if present
    if (assumptions && Array.isArray(assumptions) && assumptions.length > 0) {
        assumptions.forEach(ass => {
            const banner = document.createElement("div");
            banner.className = "assumption-banner";
            banner.textContent = `ℹ ${ass}`;
            bubble.appendChild(banner);
        });
    }

    // 2. Render structured table or plain text
    if (answer && typeof answer === "object" && answer.type === "table") {
        lastTableData = answer;
        btnExportCSV.style.display = "inline-flex";

        const textPara = document.createElement("div");
        textPara.style.marginBottom = "8px";
        textPara.innerHTML = formatMarkdown(answer.message || `Found ${answer.total_records} matching records:`);
        bubble.appendChild(textPara);

        const tableWrap = document.createElement("div");
        tableWrap.className = "data-table-wrapper";

        const headInfo = document.createElement("div");
        headInfo.className = "data-table-header-info";
        headInfo.innerHTML = `<span>Showing ${answer.displayed_records || (answer.rows ? answer.rows.length : 0)} of ${answer.total_records} records</span><span>Structured Table</span>`;
        tableWrap.appendChild(headInfo);

        const scrollWrap = document.createElement("div");
        scrollWrap.className = "data-table-scroll";
        const table = document.createElement("table");
        table.className = "agentx-table";

        // Table Head
        const thead = document.createElement("thead");
        const headerTr = document.createElement("tr");
        (answer.columns || []).forEach(c => {
            const th = document.createElement("th");
            th.textContent = c;
            headerTr.appendChild(th);
        });
        thead.appendChild(headerTr);
        table.appendChild(thead);

        // Table Body
        const tbody = document.createElement("tbody");
        (answer.rows || []).forEach(r => {
            const tr = document.createElement("tr");
            r.forEach(v => {
                const td = document.createElement("td");
                td.textContent = (v !== null && v !== undefined && v !== "") ? v : "-";
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        scrollWrap.appendChild(table);
        tableWrap.appendChild(scrollWrap);
        bubble.appendChild(tableWrap);

    } else if (answer && typeof answer === "object" && answer.type === "chart") {
        const textPara = document.createElement("div");
        textPara.innerHTML = formatMarkdown(answer.message || "Generated visualization:");
        bubble.appendChild(textPara);
        if (answer.chart_url) {
            const img = document.createElement("img");
            img.src = answer.chart_url;
            img.style.maxWidth = "100%";
            img.style.borderRadius = "8px";
            img.style.marginTop = "8px";
            bubble.appendChild(img);
        }
    } else {
        const textPara = document.createElement("div");
        const txt = typeof answer === "string" ? answer : JSON.stringify(answer, null, 2);
        textPara.innerHTML = formatMarkdown(txt);
        bubble.appendChild(textPara);
    }

    messagesStream.appendChild(row);
    scrollChat();
}

function scrollChat() {
    chatScrollArea.scrollTop = chatScrollArea.scrollHeight;
}

/* ========================================================
   PERSISTENT CHAT HISTORY
   ======================================================== */
async function loadConversations(highlightId = null) {
    try {
        const res = await fetch("/api/conversations");
        if (res.status === 401) return;
        const data = await res.json();

        historyListContainer.replaceChildren();

        if (!data.conversations || data.conversations.length === 0) {
            historyListContainer.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:10px; text-align:center;">No previous chats</div>';
            return;
        }

        data.conversations.forEach(c => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "history-item-btn" + (c.id === highlightId ? " active" : "");

            const titleSpan = document.createElement("span");
            titleSpan.className = "history-title-truncate";
            titleSpan.textContent = c.title || "Untitled Session";
            btn.appendChild(titleSpan);

            const delBtn = document.createElement("span");
            delBtn.className = "history-del-btn";
            delBtn.textContent = "✕";
            delBtn.title = "Delete conversation";
            delBtn.onclick = async (e) => {
                e.stopPropagation();
                if (confirm(`Delete conversation "${c.title}"?`)) {
                    await fetch(`/api/conversations/${c.id}`, { method: "DELETE" });
                    if (activeConversationId === c.id) {
                        startNewChat();
                    } else {
                        loadConversations(activeConversationId);
                    }
                }
            };
            btn.appendChild(delBtn);

            btn.onclick = () => selectConversation(c.id);
            historyListContainer.appendChild(btn);
        });

    } catch (e) {
        historyListContainer.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:10px; text-align:center;">Could not load history</div>';
    }
}

async function selectConversation(convId) {
    try {
        const res = await fetch(`/api/conversations/${convId}`);
        if (!res.ok) return;
        const data = await res.json();

        activeConversationId = data.id;
        activeDatasetId = data.dataset_id || activeDatasetId;

        document.querySelectorAll(".history-item-btn").forEach(b => b.classList.remove("active"));
        loadConversations(activeConversationId);

        // Update topbar title
        document.getElementById("headerSessionTitle").textContent = data.title || "Data Analyst Session";

        // Clear and rebuild chat
        messagesStream.replaceChildren();
        if (chatWelcomeBox) chatWelcomeBox.style.display = "none";

        if (Array.isArray(data.messages)) {
            data.messages.forEach(m => {
                if (m.role === "user") {
                    appendUserMessage(m.content);
                } else if (m.role === "assistant") {
                    let ansPayload = m.content;
                    try {
                        const parsed = JSON.parse(m.content);
                        if (parsed && typeof parsed === "object") ansPayload = parsed;
                    } catch (e) {}
                    appendAssistantMessage(ansPayload, null, null);
                }
            });
        }

        if (sidebar.classList.contains("open")) sidebar.classList.remove("open");

    } catch (e) {
        console.error("Failed to load conversation:", e);
    }
}

newChatBtn.addEventListener("click", startNewChat);

function startNewChat() {
    activeConversationId = null;
    messagesStream.replaceChildren();
    if (chatWelcomeBox) chatWelcomeBox.style.display = "block";
    document.getElementById("headerSessionTitle").textContent = "New Analysis Session";
    document.querySelectorAll(".history-item-btn").forEach(b => b.classList.remove("active"));
    btnExportCSV.style.display = "none";
    queryInput.value = "";
    queryInput.style.height = "auto";
    sendBtn.disabled = true;
    queryInput.focus();
    if (sidebar.classList.contains("open")) sidebar.classList.remove("open");
}

if (refreshHistoryBtn) {
    refreshHistoryBtn.addEventListener("click", () => loadConversations(activeConversationId));
}

/* Markdown Formatter Helper */
function formatMarkdown(text) {
    if (!text) return "";
    let str = escapeHtml(String(text));
    // Bold
    str = str.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    // Code ticks
    str = str.replace(/`(.*?)`/g, "<code style='background:rgba(255,255,255,0.08); padding:1px 5px; border-radius:4px; font-family:monospace;'>$1</code>");
    // Newlines
    str = str.replace(/\n/g, "<br>");
    return str;
}

function escapeHtml(text) {
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Initial page bootstrap
window.addEventListener("DOMContentLoaded", () => {
    loadConversations();
    renderSuggestedChips(null);
});
</script>
</body>
</html>
"""

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Successfully generated clean updated {INDEX_PATH}")
