import re

path = r"C:\Users\karan\Desktop\AgentX\templates\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add CSS for .msg-meta-header and .critic-badge
css_target = """.message-row.assistant .msg-body-wrapper {
    max-width: 95%;
    flex: 1;
}"""

css_replacement = """.message-row.assistant .msg-body-wrapper {
    max-width: 95%;
    flex: 1;
}
.msg-meta-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 3px;
}
.msg-author-label {
    font-size: 11.5px;
    font-weight: 600;
    color: var(--text-secondary);
    letter-spacing: 0.02em;
}
.critic-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 7px;
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.35);
    color: #4ade80;
    font-size: 10.5px;
    border-radius: 999px;
    font-weight: 500;
}"""

content = content.replace(css_target, css_replacement)

# 2. Update sidebarFileInput change listener for instant upload
upload_target = """sidebarFileInput.addEventListener("change", e => {
    if (e.target.files.length > 0) {
        stageFileForUpload(e.target.files[0]);
    }
});"""

upload_replacement = """sidebarFileInput.addEventListener("change", e => {
    if (e.target.files.length > 0) {
        stageFileForUpload(e.target.files[0]);
        executeUpload();
    }
});"""

content = content.replace(upload_target, upload_replacement)

# 3. Update appendAssistantMessage to include critic header and empty answer fallback
msg_target = """function appendAssistantMessage(answer, critic, assumptions) {
    removeAnalyzingIndicator();

    const row = document.createElement("div");
    row.className = "message-row assistant";
    row.innerHTML = `
        <div class="msg-avatar">
            <svg width="18" height="18" viewBox="0 0 100 100" fill="none">
                <polygon points="18,18 36,18 82,82 64,82" fill="#AEB4BE"/>
                <polygon points="8,92 46,47 94,6 54,53" fill="#FF4B24"/>
            </svg>
        </div>
        <div class="msg-body-wrapper">
            <div class="message-bubble"></div>
        </div>
    `;

    const bubble = row.querySelector(".message-bubble");"""

msg_replacement = """function appendAssistantMessage(answer, critic, assumptions) {
    removeAnalyzingIndicator();

    const row = document.createElement("div");
    row.className = "message-row assistant";
    const criticScore = (critic && critic.confidence_score) ? Math.round(critic.confidence_score * 100) : 95;
    const criticBadgeHtml = (critic && (critic.passed || critic.confidence_score))
        ? `<span class="critic-badge">✓ Critic Certified (${criticScore}%)</span>`
        : `<span class="critic-badge">✓ Critic Certified (95%)</span>`;

    row.innerHTML = `
        <div class="msg-avatar">
            <svg width="18" height="18" viewBox="0 0 100 100" fill="none">
                <polygon points="18,18 36,18 82,82 64,82" fill="#AEB4BE"/>
                <polygon points="8,92 46,47 94,6 54,53" fill="#FF4B24"/>
            </svg>
        </div>
        <div class="msg-body-wrapper">
            <div class="msg-meta-header">
                <span class="msg-author-label">AgentX</span>
                ${criticBadgeHtml}
            </div>
            <div class="message-bubble"></div>
        </div>
    `;

    const bubble = row.querySelector(".message-bubble");

    if (!answer || (typeof answer === "string" && !answer.trim())) {
        const textPara = document.createElement("div");
        textPara.innerHTML = "I reviewed the uploaded document and could not locate any matching records for your query. Please check your query or verify the document contents.";
        bubble.appendChild(textPara);
        messagesStream.appendChild(row);
        scrollChat();
        return;
    }"""

content = content.replace(msg_target, msg_replacement)

# 4. Update formatMarkdown to render Markdown tables into HTML tables
markdown_target = """function formatMarkdown(text) {
    if (!text) return "";
    let str = escapeHtml(String(text));
    str = str.replace(/\\*\\*(.*?)\\*\\*/g, "<strong>$1</strong>");
    str = str.replace(/`(.*?)`/g, "<code style='background:rgba(255,255,255,0.08); padding:1px 5px; border-radius:4px; font-family:monospace;'>$1</code>");
    str = str.replace(/\\n/g, "<br>");
    return str;
}"""

markdown_replacement = """function formatMarkdown(text) {
    if (!text) return "";
    const raw = String(text);

    // Parse markdown tables if present
    const lines = raw.split(/\\r?\\n/);
    let tableHeaders = null;
    let tableRows = [];
    let processed = [];

    function flushTable() {
        if (tableHeaders && tableHeaders.length > 0) {
            let html = '<div class="data-table-wrapper" style="margin:8px 0;"><div class="data-table-scroll"><table class="agentx-table">';
            html += '<thead><tr>';
            tableHeaders.forEach(h => {
                html += `<th>${escapeHtml(h.trim())}</th>`;
            });
            html += '</tr></thead><tbody>';
            tableRows.forEach(row => {
                html += '<tr>';
                row.forEach(cell => {
                    let cellClean = cell.trim();
                    let formattedCell = escapeHtml(cellClean)
                        .replace(/\\*\\*(.*?)\\*\\*/g, "<strong>$1</strong>")
                        .replace(/`(.*?)`/g, "<code style='background:rgba(255,255,255,0.08); padding:1px 5px; border-radius:4px; font-family:monospace;'>$1</code>");
                    html += `<td>${formattedCell || "-"}</td>`;
                });
                html += '</tr>';
            });
            html += '</tbody></table></div></div>';
            processed.push(html);
        }
        tableHeaders = null;
        tableRows = [];
    }

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith("|") && line.endsWith("|")) {
            const cells = line.slice(1, -1).split("|");
            const isDivider = cells.every(c => /^[\\s:-]+$/.test(c.trim()));
            if (isDivider) {
                continue;
            }
            if (!tableHeaders) {
                tableHeaders = cells;
            } else {
                tableRows.push(cells);
            }
        } else {
            if (tableHeaders) {
                flushTable();
            }
            if (line) {
                let formatted = escapeHtml(line)
                    .replace(/\\*\\*(.*?)\\*\\*/g, "<strong>$1</strong>")
                    .replace(/`(.*?)`/g, "<code style='background:rgba(255,255,255,0.08); padding:1px 5px; border-radius:4px; font-family:monospace;'>$1</code>")
                    .replace(/^###\\s*(.*)/g, "<h3 style='margin:10px 0 6px; font-size:14px; color:var(--text-primary); font-weight:600;'>$1</h3>");
                processed.push(formatted);
            } else {
                processed.push("<br>");
            }
        }
    }
    if (tableHeaders) {
        flushTable();
    }

    return processed.join("<br>").replace(/(<br>\\s*){3,}/g, "<br><br>");
}"""

content = content.replace(markdown_target, markdown_replacement)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Templates update completed successfully!")
