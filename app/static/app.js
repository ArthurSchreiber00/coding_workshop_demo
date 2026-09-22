// Kleine UI-Helfer für Toolshed.

function toggleDropdown(id) {
  var menu = document.getElementById(id);
  menu.classList.toggle("open");
}

function filterStatus(status) {
  var rows = document.querySelectorAll("#items-table tr[data-status]");
  rows.forEach(function (row) {
    row.style.display = !status || row.dataset.status === status ? "" : "none";
  });
  var labels = { "": "Alle", available: "verfügbar", on_loan: "ausgeliehen", maintenance: "Wartung" };
  document.querySelector("#status-filter .dropdown-toggle").textContent = labels[status] + " ▾";
  document.getElementById("status-menu").classList.remove("open");
}

document.addEventListener("click", function (event) {
  if (!event.target.closest(".dropdown")) {
    document.querySelectorAll(".dropdown-menu.open").forEach(function (m) { m.classList.remove("open"); });
  }
});
