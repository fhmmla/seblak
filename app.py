import os
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

# URL Backend FastAPI
BASE_API_URL = "https://seblak-api.onrender.com"


def get_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def safe_json(resp):
    """Parse JSON response safely — returns dict even if body is empty or non-JSON."""
    try:
        return resp.json()
    except Exception:
        return {"detail": resp.text or f"Server returned status {resp.status_code} with empty response."}


# ─── AUTH ROUTES ──────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# ─── API PROXY: AUTH ──────────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    try:
        resp = requests.post(
            f"{BASE_API_URL}/login",
            data={"username": data.get("username"), "password": data.get("password")},
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": f"Koneksi ke server gagal: {str(e)}"}), 503


# ─── DASHBOARD MAHASISWA ──────────────────────────────────────────────────────

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/mahasiswa/add", methods=["GET"])
def add_mahasiswa():
    return render_template("add_mahasiswa.html")

@app.route("/mahasiswa/edit/<nim>", methods=["GET"])
def edit_mahasiswa(nim):
    return render_template("edit_mahasiswa.html", nim=nim)


# ─── API PROXY: MAHASISWA ─────────────────────────────────────────────────────

@app.route("/api/mahasiswa", methods=["GET"])
def api_get_mahasiswa():
    token = request.headers.get("X-Token")
    kelas = request.args.get("kelas", "")
    params = {}
    if kelas:
        params["kelas"] = kelas
    try:
        resp = requests.get(
            f"{BASE_API_URL}/mahasiswa",
            params=params,
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/mahasiswa/kelas", methods=["GET"])
def api_get_kelas():
    """Ambil daftar kelas unik dari data mahasiswa — dipakai dropdown di frontend."""
    token = request.headers.get("X-Token")
    try:
        resp = requests.get(
            f"{BASE_API_URL}/mahasiswa/kelas",
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/mahasiswa", methods=["POST"])
def api_create_mahasiswa():
    token = request.headers.get("X-Token")
    payload = request.get_json()
    try:
        resp = requests.post(
            f"{BASE_API_URL}/mahasiswa",
            json=payload,
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/mahasiswa/<nim>", methods=["PUT"])
def api_update_mahasiswa(nim):
    token = request.headers.get("X-Token")
    payload = request.get_json()
    try:
        resp = requests.put(
            f"{BASE_API_URL}/mahasiswa/{nim}",
            json=payload,
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/mahasiswa/<nim>", methods=["DELETE"])
def api_delete_mahasiswa(nim):
    token = request.headers.get("X-Token")
    try:
        resp = requests.delete(
            f"{BASE_API_URL}/mahasiswa/{nim}",
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


# ─── API PROXY: SEARCH & SORT ─────────────────────────────────────────────────

@app.route("/api/mahasiswa/search", methods=["GET"])
def api_search_mahasiswa():
    token = request.headers.get("X-Token")
    nim = request.args.get("nim", "")
    method = request.args.get("method", "linear")
    try:
        resp = requests.get(
            f"{BASE_API_URL}/mahasiswa/search",
            params={"nim": nim, "method": method},
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/mahasiswa/sequential-search", methods=["GET"])
def api_seq_search_mahasiswa():
    token = request.headers.get("X-Token")
    keyword = request.args.get("keyword", "")
    try:
        resp = requests.get(
            f"{BASE_API_URL}/mahasiswa/sequential-search",
            params={"keyword": keyword},
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/mahasiswa/sort", methods=["GET"])
def api_sort_mahasiswa():
    token = request.headers.get("X-Token")
    method = request.args.get("method", "insertion")
    key = request.args.get("key", "nim")
    try:
        resp = requests.get(
            f"{BASE_API_URL}/mahasiswa/sort",
            params={"method": method, "key": key},
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


# ─── PENILAIAN PAGE ───────────────────────────────────────────────────────────

@app.route("/penilaian", methods=["GET"])
def penilaian():
    return render_template("penilaian.html")


@app.route("/api/penilaian/top", methods=["GET"])
def api_get_top_mahasiswa():
    token = request.headers.get("X-Token")
    limit = request.args.get("limit", 10)
    try:
        resp = requests.get(
            f"{BASE_API_URL}/penilaian/top",
            params={"limit": limit},
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


# ─── API PROXY: PERTEMUAN ─────────────────────────────────────────────────────

@app.route("/api/pertemuan", methods=["GET"])
def api_get_pertemuan():
    token = request.headers.get("X-Token")
    kelas = request.args.get("kelas", "")
    params = {}
    if kelas:
        params["kelas"] = kelas
    try:
        resp = requests.get(
            f"{BASE_API_URL}/pertemuan",
            params=params,
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/pertemuan", methods=["POST"])
def api_create_pertemuan():
    token = request.headers.get("X-Token")
    payload = request.get_json()
    try:
        resp = requests.post(
            f"{BASE_API_URL}/pertemuan",
            json=payload,
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/pertemuan/<int:pertemuan_id>/tutup", methods=["PUT"])
def api_tutup_pertemuan(pertemuan_id):
    token = request.headers.get("X-Token")
    try:
        resp = requests.put(
            f"{BASE_API_URL}/pertemuan/{pertemuan_id}/tutup",
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/pertemuan/<int:pertemuan_id>/nilai", methods=["GET"])
def api_get_nilai(pertemuan_id):
    token = request.headers.get("X-Token")
    try:
        resp = requests.get(
            f"{BASE_API_URL}/pertemuan/{pertemuan_id}/nilai",
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/pertemuan/<int:pertemuan_id>/nilai", methods=["POST"])
def api_submit_nilai(pertemuan_id):
    token = request.headers.get("X-Token")
    payload = request.get_json()
    try:
        resp = requests.post(
            f"{BASE_API_URL}/pertemuan/{pertemuan_id}/nilai",
            json=payload,
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


# ─── USERS PAGE ───────────────────────────────────────────────────────────────

@app.route("/users", methods=["GET"])
def users_page():
    return render_template("users.html")


# ─── API PROXY: USERS (Dosen only) ────────────────────────────────────────────

@app.route("/api/users", methods=["GET"])
def api_get_users():
    token = request.headers.get("X-Token")
    try:
        resp = requests.get(
            f"{BASE_API_URL}/users",
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/users", methods=["POST"])
def api_create_user():
    token = request.headers.get("X-Token")
    payload = request.get_json()
    try:
        resp = requests.post(
            f"{BASE_API_URL}/users",
            json=payload,
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/users/<username>", methods=["DELETE"])
def api_delete_user(username):
    token = request.headers.get("X-Token")
    try:
        resp = requests.delete(
            f"{BASE_API_URL}/users/{username}",
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503


@app.route("/api/export-backup", methods=["GET"])
def api_export_backup():
    token = request.headers.get("X-Token")
    try:
        resp = requests.get(
            f"{BASE_API_URL}/export-backup",
            headers=get_auth_headers(token),
            timeout=15,
        )
        return jsonify(safe_json(resp)), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"detail": str(e)}), 503

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)
