// Custom JavaScript for E-Commerce Platform

document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // Confirm delete actions
  const deleteForms = document.querySelectorAll('form[action*="delete"]');
  deleteForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!confirm("Are you sure you want to delete this item?")) {
        e.preventDefault();
      }
    });
  });

  // Quantity input validation
  const quantityInputs = document.querySelectorAll('input[name="quantity"]');
  quantityInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      const max = parseInt(this.getAttribute("max"));
      const min = parseInt(this.getAttribute("min"));
      const value = parseInt(this.value);

      if (value > max) {
        this.value = max;
        alert("Maximum quantity exceeded. Set to " + max);
      }
      if (value < min) {
        this.value = min;
      }
    });
  });
});
