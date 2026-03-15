/* ==========================================================
   PyMessenger – app.js
   Handles: Auth, Chat, Heartbeat, Online Status, Read Receipts
   ========================================================== */

const API = '';   // same origin — FastAPI serves frontend

// ── Session helpers ───────────────────────────────────────────────────────────
function getSession() {
  try { return JSON.parse(sessionStorage.getItem('pymessenger_user') || 'null'); }
  catch { return null; }
}
function setSession(user) { sessionStorage.setItem('pymessenger_user', JSON.stringify(user)); }
function clearSession()   { sessionStorage.removeItem('pymessenger_user'); }
function initials(name = '') {
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) || '?';
}

async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Request failed');
  return data;
}

// ── AUTH PAGE ─────────────────────────────────────────────────────────────────
function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.form-section').forEach(s => s.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
  document.getElementById('section-' + tab).classList.add('active');
}

function showAlert(id, message, type) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = message;
  el.className = 'alert ' + type + ' show';
  setTimeout(() => el.classList.remove('show'), 4500);
}

async function handleLogin() {
  const username = document.getElementById('login-username').value.trim();
  if (!username) { showAlert('login-alert', 'Please enter your username.', 'error'); return; }
  const btn = document.getElementById('btn-login');
  btn.disabled = true; btn.textContent = 'Signing in…';
  try {
    const data = await apiFetch('/login', { method: 'POST', body: JSON.stringify({ username }) });
    setSession({ username: data.username, display_name: data.display_name });
    window.location.href = '/chat';
  } catch (err) {
    showAlert('login-alert', err.message, 'error');
  } finally {
    btn.disabled = false; btn.textContent = 'Sign In';
  }
}

async function handleRegister() {
  const username     = document.getElementById('reg-username').value.trim();
  const display_name = document.getElementById('reg-displayname').value.trim();
  if (!username || !display_name) { showAlert('register-alert', 'All fields are required.', 'error'); return; }
  const btn = document.getElementById('btn-register');
  btn.disabled = true; btn.textContent = 'Creating…';
  try {
    await apiFetch('/register', { method: 'POST', body: JSON.stringify({ username, display_name }) });
    showAlert('register-alert', ' Account created! You can now log in.', 'success');
    document.getElementById('reg-username').value = '';
    document.getElementById('reg-displayname').value = '';
    setTimeout(() => switchTab('login'), 1800);
  } catch (err) {
    showAlert('register-alert', err.message, 'error');
  } finally {
    btn.disabled = false; btn.textContent = 'Create Account';
  }
}

// ── CHAT STATE ────────────────────────────────────────────────────────────────
let currentPeer    = null;
let allUsers       = [];
let onlineUsers    = new Set();   // set of online usernames
let pollInterval   = null;
let heartbeatTimer = null;
const POLL_MS      = 3000;
const HEARTBEAT_MS = 5000;

// ── INIT ──────────────────────────────────────────────────────────────────────
function initChat() {
  const user = getSession();
  if (!user) { window.location.href = '/'; return; }

  document.getElementById('my-display-name').textContent = user.display_name;
  document.getElementById('my-avatar').textContent = initials(user.display_name);

  loadUsers();
  startHeartbeat();
  startPolling();
}

// ── HEARTBEAT — tells server we are alive ─────────────────────────────────────
function startHeartbeat() {
  const user = getSession();
  if (!user) return;
  const ping = () => apiFetch('/heartbeat', { method: 'POST', body: JSON.stringify({ username: user.username }) }).catch(() => {});
  ping();  // immediately
  heartbeatTimer = setInterval(ping, HEARTBEAT_MS);
}

// ── LOAD USERS + ONLINE STATUS ────────────────────────────────────────────────
async function loadUsers() {
  try {
    const [uData, oData] = await Promise.all([
      apiFetch('/users'),
      apiFetch('/online_users'),
    ]);
    allUsers   = uData.users;
    onlineUsers = new Set(oData.online_users);
    renderUserList(allUsers);
    updatePeerStatus();   // refresh chat header if a chat is open
  } catch (err) {
    showToast('Failed to load users.', 'error');
  }
}

function renderUserList(users) {
  const me   = getSession();
  const list = document.getElementById('user-list');
  list.innerHTML = '';

  users
    .filter(u => u.username !== me.username)
    .forEach(u => {
      const isOnline = onlineUsers.has(u.username);
      const item = document.createElement('div');
      item.className = 'user-item' + (currentPeer?.username === u.username ? ' active' : '');
      item.id = 'user-item-' + u.username;
      item.onclick = () => openConversation(u);
      item.innerHTML = `
        <div class="avatar-wrap">
          <div class="avatar">${initials(u.display_name)}</div>
          <span class="online-dot ${isOnline ? 'online' : 'offline'}" id="dot-${u.username}"></span>
        </div>
        <div>
          <div class="ui-name">${escHtml(u.display_name)}</div>
          <div class="ui-preview" id="preview-${u.username}">
            ${isOnline ? '● Online' : '● Offline'}
          </div>
        </div>
      `;
      list.appendChild(item);
    });
}

function updatePeerStatus() {
  if (!currentPeer) return;
  const isOnline = onlineUsers.has(currentPeer.username);
  const dot    = document.getElementById('peer-online-dot');
  const status = document.getElementById('peer-status');
  if (dot) {
    dot.className = 'online-dot ' + (isOnline ? 'online' : 'offline');
  }
  if (status) {
    status.textContent = isOnline ? '● Online' : '● Offline';
    status.className   = 'peer-status ' + (isOnline ? 'online' : 'offline');
  }
  // Also update sidebar dot without full re-render
  const sidebarDot = document.getElementById('dot-' + currentPeer.username);
  if (sidebarDot) sidebarDot.className = 'online-dot ' + (isOnline ? 'online' : 'offline');
}

function filterUsers(query) {
  const q = query.toLowerCase();
  document.querySelectorAll('.user-item').forEach(el => {
    const name = el.querySelector('.ui-name').textContent.toLowerCase();
    el.style.display = name.includes(q) ? '' : 'none';
  });
}

// ── OPEN CONVERSATION ─────────────────────────────────────────────────────────
async function openConversation(peer) {
  currentPeer = peer;

  document.getElementById('empty-state').classList.add('hidden');
  document.getElementById('conversation').classList.add('active');

  document.getElementById('peer-name').textContent       = peer.display_name;
  document.getElementById('peer-avatar').textContent     = initials(peer.display_name);

  // Highlight sidebar item
  document.querySelectorAll('.user-item').forEach(el => el.classList.remove('active'));
  const item = document.getElementById('user-item-' + peer.username);
  if (item) item.classList.add('active');

  updatePeerStatus();

  // Mark all messages from peer → me as seen
  const me = getSession();
  apiFetch('/mark_seen', {
    method: 'POST',
    body: JSON.stringify({ sender: peer.username, receiver: me.username }),
  }).catch(() => {});

  await fetchMessages();
}

// ── FETCH & RENDER MESSAGES ───────────────────────────────────────────────────
async function fetchMessages() {
  if (!currentPeer) return;
  const me = getSession();
  try {
    const data = await apiFetch(`/get_messages?user1=${me.username}&user2=${currentPeer.username}`);
    renderMessages(data.messages);
  } catch {
    showToast('Could not load messages.', 'error');
  }
}

function tickHTML(msg, me) {
  // Only show ticks on sent messages
  if (msg.from !== me.username) return '';

  const peerOnline = onlineUsers.has(msg.to);
  if (msg.seen) {
    // Double green tick ✓✓
    return `<span class="tick seen">✓✓</span>`;
  } else if (peerOnline) {
    // Double gray tick — delivered (peer is online but hasn't seen yet)
    return `<span class="tick delivered">✓✓</span>`;
  } else {
    // Single gray tick — sent, peer offline
    return `<span class="tick sent">✓</span>`;
  }
}

function renderMessages(messages) {
  const me   = getSession();
  const area = document.getElementById('messages-area');
  const wasAtBottom = area.scrollHeight - area.scrollTop - area.clientHeight < 80;

  area.innerHTML = '';
  let lastDate = '';

  messages.forEach(msg => {
    const date = (msg.timestamp || '').split(' ')[0];
    if (date && date !== lastDate) {
      lastDate = date;
      const divider = document.createElement('div');
      divider.className = 'date-divider';
      divider.textContent = formatDate(date);
      area.appendChild(divider);
    }

    const isSent = msg.from === me.username;
    const row    = document.createElement('div');
    row.className = 'bubble-row ' + (isSent ? 'sent' : 'received');
    row.innerHTML = `
      <div class="bubble">
        ${escHtml(msg.message)}
        <span class="bubble-time">
          ${formatTime(msg.timestamp)}
          ${tickHTML(msg, me)}
        </span>
      </div>
    `;
    area.appendChild(row);
  });

  // Update sidebar preview — show last msg text (not online status)
  if (messages.length > 0) {
    const last    = messages[messages.length - 1];
    const preview = document.getElementById('preview-' + currentPeer.username);
    if (preview) preview.textContent = (last.from === me.username ? 'You: ' : '') + last.message;
  }

  if (wasAtBottom || messages.length === 0) area.scrollTop = area.scrollHeight;
}

// ── SEND MESSAGE ──────────────────────────────────────────────────────────────
async function sendMessage() {
  const input = document.getElementById('msg-input');
  const text  = input.value.trim();
  if (!text || !currentPeer) return;

  const me = getSession();
  input.value = '';
  input.style.height = '';

  try {
    await apiFetch('/send_message', {
      method: 'POST',
      body: JSON.stringify({ sender: me.username, receiver: currentPeer.username, text }),
    });
    await fetchMessages();
  } catch (err) {
    showToast('Failed to send: ' + err.message, 'error');
    input.value = text;
  }
}

// ── POLLING ───────────────────────────────────────────────────────────────────
function startPolling() {
  if (pollInterval) clearInterval(pollInterval);
  pollInterval = setInterval(async () => {
    await loadUsers();       // refreshes online status + sidebar dots
    await fetchMessages();   // refreshes ticks + new messages
  }, POLL_MS);
}

// ── LOGOUT ────────────────────────────────────────────────────────────────────
function logout() {
  clearSession();
  if (pollInterval)   clearInterval(pollInterval);
  if (heartbeatTimer) clearInterval(heartbeatTimer);
  window.location.href = '/';
}

// ── UTILS ─────────────────────────────────────────────────────────────────────
function autoGrow(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function showToast(message, type = 'success') {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = message;
  t.className   = 'toast ' + type + ' show';
  setTimeout(() => t.classList.remove('show'), 3000);
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatTime(ts = '') {
  try {
    const parts = ts.split(' ');
    if (parts.length < 2) return ts;
    const [h, m] = parts[1].split(':');
    const hour   = parseInt(h, 10);
    const ampm   = hour >= 12 ? 'PM' : 'AM';
    return `${((hour % 12) || 12)}:${m} ${ampm}`;
  } catch { return ts; }
}

function formatDate(dateStr = '') {
  try {
    const today = new Date().toISOString().split('T')[0];
    const yest  = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    if (dateStr === today) return 'Today';
    if (dateStr === yest)  return 'Yesterday';
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  } catch { return dateStr; }
}
