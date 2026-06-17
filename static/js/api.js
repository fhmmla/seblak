/**
 * api.js — Central API handler for SEBLAK Frontend
 * Handles JWT token management and all fetch requests via Flask proxy.
 */

const TOKEN_KEY = "seblak_token";
const USERNAME_KEY = "seblak_username";

// ─── Token Helpers ────────────────────────────────────────────────────────────

export function saveToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USERNAME_KEY);
}

export function saveUsername(username) {
  localStorage.setItem(USERNAME_KEY, username);
}

export function getUsername() {
  return localStorage.getItem(USERNAME_KEY) || "Pengguna";
}

export function isLoggedIn() {
  return !!getToken();
}

// Background ping to keep Render server awake (every 14 minutes)
if (isLoggedIn()) {
  setInterval(() => {
    fetch("/api/ping").catch(e => console.log("Background ping failed:", e));
  }, 14 * 60 * 1000); // 14 minutes
}

// ─── Core Fetch Wrapper ───────────────────────────────────────────────────────

/**
 * Makes an authenticated request through Flask proxy.
 * @param {string} endpoint - e.g. "/api/mahasiswa"
 * @param {object} options  - fetch options (method, body, etc.)
 * @returns {Promise<{ok: boolean, status: number, data: any}>}
 */
async function apiFetch(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { "X-Token": token } : {}),
    ...(options.headers || {}),
  };

  const config = {
    method: options.method || "GET",
    headers,
    ...(options.body ? { body: JSON.stringify(options.body) } : {}),
  };

  try {
    const response = await fetch(endpoint, config);
    let data;
    try {
      data = await response.json();
    } catch {
      data = { detail: "Respon server tidak valid." };
    }

    // Token expired / unauthorized
    if (response.status === 401) {
      clearToken();
      window.location.href = "/login";
      return { ok: false, status: 401, data };
    }

    return { ok: response.ok, status: response.status, data };
  } catch (error) {
    console.error("Network error:", error);
    return {
      ok: false,
      status: 0,
      data: { detail: "Gagal terhubung ke server. Periksa koneksi internet." },
    };
  }
}

// ─── Auth ─────────────────────────────────────────────────────────────────────

export async function loginApi(username, password) {
  const response = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  let data;
  try {
    data = await response.json();
  } catch {
    data = { detail: "Respon tidak valid." };
  }
  return { ok: response.ok, status: response.status, data };
}

// ─── Mahasiswa ────────────────────────────────────────────────────────────────

export const getMahasiswa = (kelas = null) =>
  apiFetch(kelas ? `/api/mahasiswa?kelas=${encodeURIComponent(kelas)}` : "/api/mahasiswa");

export const getDaftarKelas = () =>
  apiFetch("/api/mahasiswa/kelas");

export const createMahasiswa = (payload) =>
  apiFetch("/api/mahasiswa", { method: "POST", body: payload });

export const updateMahasiswa = (nim, payload) =>
  apiFetch(`/api/mahasiswa/${nim}`, { method: "PUT", body: payload });

export const deleteMahasiswa = (nim) =>
  apiFetch(`/api/mahasiswa/${nim}`, { method: "DELETE" });

// ─── Search & Sort ────────────────────────────────────────────────────────────

export const getTopMahasiswa = (limit = 10) =>
  apiFetch(`/api/penilaian/top?limit=${limit}`);

export const searchByNim = (nim, method = "linear") =>
  apiFetch(`/api/mahasiswa/search?nim=${encodeURIComponent(nim)}&method=${method}`);

export const sequentialSearch = (keyword) =>
  apiFetch(`/api/mahasiswa/sequential-search?keyword=${encodeURIComponent(keyword)}`);

export const sortMahasiswa = (method = "insertion", key = "nim") =>
  apiFetch(`/api/mahasiswa/sort?method=${method}&key=${key}`);

// ─── Pertemuan ────────────────────────────────────────────────────────────────

export const getPertemuan = (kelas = null) =>
  apiFetch(kelas ? `/api/pertemuan?kelas=${encodeURIComponent(kelas)}` : "/api/pertemuan");

export const createPertemuan = (topik, kelas) =>
  apiFetch("/api/pertemuan", { method: "POST", body: { topik, kelas } });

export const tutupPertemuan = (id) =>
  apiFetch(`/api/pertemuan/${id}/tutup`, { method: "PUT" });

export const getNilai = (pertemuanId) =>
  apiFetch(`/api/pertemuan/${pertemuanId}/nilai`);

export const submitNilai = (pertemuanId, nim, ceklis) =>
  apiFetch(`/api/pertemuan/${pertemuanId}/nilai`, {
    method: "POST",
    body: { nim, ceklis },
  });

// ─── User Management (Dosen only) ────────────────────────────────────────────

export const getUsers = () => apiFetch("/api/users");

export const createUser = (payload) =>
  apiFetch("/api/users", { method: "POST", body: payload });

export const deleteUser = (username) =>
  apiFetch(`/api/users/${username}`, { method: "DELETE" });

export const exportBackup = () => apiFetch("/api/export-backup");

// ─── Toast Notification ───────────────────────────────────────────────────────

/**
 * Shows a dismissible toast notification.
 * @param {string} message
 * @param {"success"|"error"|"info"|"warning"} type
 * @param {number} duration - ms before auto-dismiss
 */
export function showToast(message, type = "info", duration = 3500) {
  const colorMap = {
    success:
      "bg-emerald-500 text-white border-emerald-600",
    error:
      "bg-rose-500 text-white border-rose-600",
    warning:
      "bg-amber-400 text-gray-900 border-amber-500",
    info:
      "bg-indigo-500 text-white border-indigo-600",
  };

  const iconMap = {
    success: `<svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`,
    error: `<svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`,
    warning: `<svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg>`,
    info: `<svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`,
  };

  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className =
      "fixed top-5 right-5 z-[9999] flex flex-col gap-3 pointer-events-none";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `flex items-start gap-3 px-4 py-3 rounded-xl border shadow-xl text-sm font-medium pointer-events-auto transform translate-x-32 opacity-0 transition-all duration-300 max-w-xs ${colorMap[type] || colorMap.info}`;
  toast.innerHTML = `
    ${iconMap[type] || iconMap.info}
    <span class="flex-1 leading-snug">${message}</span>
    <button onclick="this.parentElement.remove()" class="opacity-70 hover:opacity-100 transition-opacity shrink-0 text-lg leading-none">&times;</button>
  `;

  container.appendChild(toast);

  // Animate in
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      toast.classList.remove("translate-x-32", "opacity-0");
    });
  });

  // Auto-dismiss
  setTimeout(() => {
    toast.classList.add("translate-x-32", "opacity-0");
    setTimeout(() => toast.remove(), 300);
  }, duration);
}
