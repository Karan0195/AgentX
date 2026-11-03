path = r"C:\Users\karan\Desktop\AgentX\templates\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove duplicate "Dataset Explorer" in sidebar tabs
# Currently:
#         <!-- Navigation Tabs (Dashboard, Dataset Explorer, Chat History) -->
#         <div class="sidebar-nav-tabs">
#             <button type="button" class="nav-item-btn active" id="navDashboardBtn" onclick="startNewChat()">
#                 <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
#                 <span class="nav-item-label">Dashboard</span>
#             </button>
#             <button type="button" class="nav-item-btn" id="navExplorerBtn" onclick="document.getElementById('sidebarFileInput').click()">
#                 <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
#                 <span class="nav-item-label">Dataset Explorer</span>
#             </button>
#         </div>

old_nav_tabs = """        <!-- Navigation Tabs (Dashboard, Dataset Explorer, Chat History) -->
        <div class="sidebar-nav-tabs">
            <button type="button" class="nav-item-btn active" id="navDashboardBtn" onclick="startNewChat()">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                <span class="nav-item-label">Dashboard</span>
            </button>
            <button type="button" class="nav-item-btn" id="navExplorerBtn" onclick="document.getElementById('sidebarFileInput').click()">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                <span class="nav-item-label">Dataset Explorer</span>
            </button>
        </div>"""

new_nav_tabs = """        <!-- Navigation Tab (Dashboard) -->
        <div class="sidebar-nav-tabs">
            <button type="button" class="nav-item-btn active" id="navDashboardBtn" onclick="startNewChat()">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                <span class="nav-item-label">Dashboard</span>
            </button>
        </div>"""

assert old_nav_tabs in content, "old_nav_tabs not found!"
content = content.replace(old_nav_tabs, new_nav_tabs)

# 2. Update hero greeting HTML (remove the separate "Hello," line, use single animated cycler)
old_greeting = """                    <div class="hero-greeting-small">Hello,</div>
                    <h1 class="hero-greeting-heading">Welcome back, <span class="user-first-name-dyn text-gradient-orange">{{ (session.get('full_name') or session.get('username') or 'Explorer')|title }}</span>!</h1>
                    <p class="hero-greeting-sub">What would you like to explore today?</p>"""

new_greeting = """                    <h1 class="hero-greeting-heading" id="heroGreetingHeading">
                        <span class="greeting-cycler text-gradient-orange" id="greetingCycler">Hi, <span class="user-first-name-dyn">{{ (session.get('full_name') or session.get('username') or 'Karan')|title }}</span>!</span>
                    </h1>
                    <p class="hero-greeting-sub">What would you like to explore today?</p>"""

assert old_greeting in content, "old_greeting not found!"
content = content.replace(old_greeting, new_greeting)

# 3. Add CSS for .greeting-cycler if not present
if ".greeting-cycler" not in content:
    css_anchor = ".hero-greeting-heading {"
    css_addition = """.greeting-cycler {
    display: inline-block;
    transition: opacity 0.35s ease, transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
"""
    content = content.replace(css_anchor, css_addition + css_anchor)

# 4. Update initDynamicUserGreeting() in JavaScript
old_js_greeting = """/* ---------------- DYNAMIC LOGGED-IN USER GREETING (Requirement 2) ---------------- */
function initDynamicUserGreeting() {
    fetch('/api/auth/me')
        .then(r => r.json())
        .then(data => {
            if (data && data.logged_in && data.user) {
                const rawName = data.user.full_name || data.user.username || 'Explorer';
                const firstName = rawName.trim().split(/\\s+/)[0];
                const capitalized = firstName.charAt(0).toUpperCase() + firstName.slice(1);
                
                // Update all first name and full name occurrences
                document.querySelectorAll('.user-first-name-dyn').forEach(el => {
                    el.textContent = capitalized;
                });
                document.querySelectorAll('.user-full-name-dyn').forEach(el => {
                    el.textContent = rawName;
                });
            }
        })
        .catch(err => console.log("Auth me fetch error:", err));
}"""

new_js_greeting = """/* ---------------- DYNAMIC LOGGED-IN USER GREETING & SESSION TRACKING ---------------- */
function initDynamicUserGreeting() {
    fetch('/api/auth/me')
        .then(r => r.json())
        .then(data => {
            if (data && data.logged_in && data.user) {
                const rawName = data.user.full_name || data.user.username || 'Karan';
                const firstName = rawName.trim().split(/\\s+/)[0];
                const capitalized = firstName.charAt(0).toUpperCase() + firstName.slice(1);
                
                document.querySelectorAll('.user-first-name-dyn').forEach(el => {
                    el.textContent = capitalized;
                });
                document.querySelectorAll('.user-full-name-dyn').forEach(el => {
                    el.textContent = rawName;
                });

                // Determine whether user is in first session or returning (second session onwards)
                fetch('/api/conversations')
                    .then(r => r.json())
                    .then(convData => {
                        const previousChatsCount = (convData && convData.conversations) ? convData.conversations.length : 0;
                        const userStorageKey = `agentx_user_visits_${data.user.id || data.user.username}`;
                        let visitCount = parseInt(localStorage.getItem(userStorageKey) || "0", 10);
                        
                        if (!sessionStorage.getItem("agentx_session_visit_registered")) {
                            visitCount += 1;
                            localStorage.setItem(userStorageKey, visitCount.toString());
                            sessionStorage.setItem("agentx_session_visit_registered", "true");
                        }

                        // Requirement: For new users, show "Welcome back" from second session onwards
                        const isSecondSessionOrMore = (previousChatsCount > 0) || (visitCount >= 2);

                        let greetingPhrases = [];
                        if (isSecondSessionOrMore) {
                            // Returning user: "Welcome back, Karan!", "Hello, Karan!", "Hi, Karan!"
                            greetingPhrases = [
                                `Welcome back, ${capitalized}!`,
                                `Hello, ${capitalized}!`,
                                `Hi, ${capitalized}!`
                            ];
                        } else {
                            // First session: "Hi, Karan!", "Hello, Karan!" (no "Welcome back" on first visit)
                            greetingPhrases = [
                                `Hi, ${capitalized}!`,
                                `Hello, ${capitalized}!`,
                                `Welcome to AgentX, ${capitalized}!`
                            ];
                        }

                        const cyclerEl = document.getElementById("greetingCycler");
                        if (cyclerEl) {
                            cyclerEl.textContent = greetingPhrases[0];
                        }

                        // Cycle greetings one by one smoothly
                        let phraseIndex = 0;
                        if (window._greetingTimer) clearInterval(window._greetingTimer);
                        window._greetingTimer = setInterval(() => {
                            if (!chatWelcomeBox || chatWelcomeBox.style.display === "none") return;
                            const el = document.getElementById("greetingCycler");
                            if (!el) return;
                            phraseIndex = (phraseIndex + 1) % greetingPhrases.length;
                            el.style.opacity = "0";
                            el.style.transform = "translateY(-6px)";
                            setTimeout(() => {
                                el.textContent = greetingPhrases[phraseIndex];
                                el.style.opacity = "1";
                                el.style.transform = "translateY(0)";
                            }, 350);
                        }, 4000);
                    })
                    .catch(() => {});
            }
        })
        .catch(err => console.log("Auth me fetch error:", err));
}"""

assert old_js_greeting in content, "old_js_greeting not found!"
content = content.replace(old_js_greeting, new_js_greeting)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Applied greeting updates & duplicate Dataset Explorer removal successfully!")
