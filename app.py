
<!DOCTYPE html>
<html>
<head>
  <title>Admin Dashboard</title>

  <!-- Bootstrap + Icons -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">

  <style>
    body {
      background: #f1f5f9;
      font-family: 'Segoe UI', sans-serif;
    }

    .sidebar {
      height: 100vh;
      background: linear-gradient(180deg, #111827, #1f2937);
      color: white;
      padding: 20px;
      position: fixed;
      width: 230px;
    }

    .sidebar h4 {
      margin-bottom: 30px;
      font-weight: 600;
    }

    .sidebar a {
      color: #9ca3af;
      display: block;
      margin: 12px 0;
      text-decoration: none;
      padding: 8px;
      border-radius: 8px;
      transition: 0.3s;
    }

    .sidebar a:hover {
      background: #374151;
      color: white;
    }

    .main {
      margin-left: 250px;
      padding: 25px;
    }

    .card-box {
      border-radius: 15px;
      padding: 20px;
      color: white;
      box-shadow: 0 8px 20px rgba(0,0,0,0.1);
      transition: 0.3s;
    }

    .card-box:hover {
      transform: translateY(-5px);
    }

    .table {
      background: white;
      border-radius: 12px;
      overflow: hidden;
    }

    .table th {
      font-weight: 600;
    }

    .badge {
      padding: 6px 12px;
      font-size: 12px;
      border-radius: 20px;
    }

    .btn {
      border-radius: 8px;
    }

    input, select {
      border-radius: 8px !important;
    }

    table tbody tr:hover {
      background-color: #f9fafb;
    }
  </style>
</head>

<body>

<!-- SIDEBAR -->
<div class="sidebar">
  <h4>🎟️ HelpDesk</h4>

  <a href="#" style="background:#374151; color:white;">
    <i class="bi bi-speedometer2"></i> Dashboard
  </a>

  <a href="#"><i class="bi bi-ticket"></i> Tickets</a>
  <a href="#"><i class="bi bi-people"></i> Users</a>
  <a href="{{ url_for('logout') }}"><i class="bi bi-box-arrow-right"></i> Logout</a>
</div>

<!-- MAIN CONTENT -->
<div class="main">

  <h3 class="mb-4">Dashboard</h3>

  <!-- 📊 STATS -->
  <div class="row mb-4">
    <div class="col-md-3">
      <div class="card-box" style="background:linear-gradient(135deg,#1e293b,#334155);">
        <i class="bi bi-ticket"></i>
        <h5>Total Tickets</h5>
        <h3>{{ total }}</h3>
      </div>
    </div>

    <div class="col-md-3">
      <div class="card-box" style="background:linear-gradient(135deg,#ef4444,#dc2626);">
        <i class="bi bi-exclamation-circle"></i>
        <h5>Open</h5>
        <h3>{{ open_count }}</h3>
      </div>
    </div>

    <div class="col-md-3">
      <div class="card-box" style="background:linear-gradient(135deg,#f59e0b,#d97706);">
        <i class="bi bi-hourglass-split"></i>
        <h5>In Progress</h5>
        <h3>{{ progress }}</h3>
      </div>
    </div>

    <div class="col-md-3">
      <div class="card-box" style="background:linear-gradient(135deg,#22c55e,#16a34a);">
        <i class="bi bi-check-circle"></i>
        <h5>Resolved</h5>
        <h3>{{ resolved }}</h3>
      </div>
    </div>
  </div>

  <!-- 🔍 SEARCH -->
  <form method="GET" class="row mb-3">
    <div class="col-md-6">
      <input type="text" name="search" class="form-control" placeholder="Search tickets...">
    </div>

    <div class="col-md-3">
      <select name="status" class="form-control">
        <option value="">All Status</option>
        <option value="Open">Open</option>
        <option value="In Progress">In Progress</option>
        <option value="Resolved">Resolved</option>
      </select>
    </div>

    <div class="col-md-2">
      <button class="btn btn-primary w-100">Filter</button>
    </div>
  </form>

  <!-- 📋 TABLE -->
  <table class="table table-hover shadow-sm">
    <thead class="table-light">
      <tr>
        <th>ID</th>
        <th>User</th>
        <th>Issue</th>
        <th>Priority</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
    </thead>

    <tbody>
      {% for t in tickets %}
      <tr>
        <td>#{{ t['id'] }}</td>

        <td>
          <b>{{ t['name'] }}</b><br>
          <small>{{ t['email'] }}</small>
        </td>

        <td>{{ t['issue'] }}</td>

        <td>
          <span class="badge bg-secondary">{{ t['priority'] }}</span>
        </td>

        <!-- STATUS -->
        <td>
          {% if t['status'] == 'Open' %}
            <span class="badge bg-danger">Open</span>
          {% elif t['status'] == 'In Progress' %}
            <span class="badge bg-warning text-dark">In Progress</span>
          {% else %}
            <span class="badge bg-success">Resolved</span>
          {% endif %}
        </td>

        <!-- ACTIONS -->
        <td>
          <form action="{{ url_for('update_ticket', id=t['id']) }}" method="POST" class="d-flex gap-1">
            <select name="status" class="form-select form-select-sm">
              <option>Open</option>
              <option>In Progress</option>
              <option>Resolved</option>
            </select>
            <button class="btn btn-sm btn-primary">✔</button>
          </form>

          <form action="{{ url_for('delete_ticket', id=t['id']) }}" method="POST" class="mt-1">
            <button class="btn btn-sm btn-danger w-100">Delete</button>
          </form>
        </td>

      </tr>
      {% endfor %}
    </tbody>
  </table>

</div>

</body>
</html>
