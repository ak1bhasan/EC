<nav class="navbar navbar-expand-lg navbar-light mb-4">
  <div class="container">
    <a class="navbar-brand" href="{{ url_for('main.home') }}">
      <i class="bi bi-shop"></i> ShopNow
    </a>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('products.index') }}"
            >Products</a
          >
        </li>
      </ul>
      <ul class="navbar-nav">
        {% if current_user.is_authenticated %} {% if not current_user.is_admin
        %}
        <!-- Customer-only navigation items -->
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('cart.view_cart') }}">
            <i class="bi bi-cart"></i> Cart {% if current_user.carts and
            current_user.carts[0].items %}
            <span
              class="badge"
              style="
                background: rgba(239, 68, 68, 0.3);
                color: #dc2626;
                border: 1px solid rgba(239, 68, 68, 0.4);
              "
              >{{ current_user.carts[0].items|length }}</span
            >
            {% endif %}
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('orders.history') }}">Orders</a>
        </li>
        {% endif %} {% if current_user.is_admin %}
        <li class="nav-item dropdown">
          <a
            class="nav-link dropdown-toggle"
            href="#"
            id="adminDropdown"
            role="button"
            data-bs-toggle="dropdown"
          >
            Admin
          </a>
          <ul class="dropdown-menu">
            <li>
              <a class="dropdown-item" href="{{ url_for('admin.dashboard') }}"
                >Dashboard</a
              >
            </li>
            <li>
              <a class="dropdown-item" href="{{ url_for('admin.products') }}"
                >Products</a
              >
            </li>
            <li>
              <a class="dropdown-item" href="{{ url_for('admin.orders') }}"
                >Orders</a
              >
            </li>
          </ul>
        </li>
        {% endif %}
        <li class="nav-item dropdown">
          <a
            class="nav-link dropdown-toggle"
            href="#"
            id="userDropdown"
            role="button"
            data-bs-toggle="dropdown"
          >
            <i class="bi bi-person-circle"></i> {{ current_user.name }}
          </a>
          <ul class="dropdown-menu" data-bs-auto-close="true">
            {% if not current_user.is_admin %}
            <li>
              <a class="dropdown-item" href="{{ url_for('auth.profile') }}"
                >Profile</a
              >
            </li>
            <li><hr class="dropdown-divider" /></li>
            {% endif %}
            <li>
              <form
                method="POST"
                action="{{ url_for('auth.logout') }}"
                id="logout-form"
                style="margin: 0; padding: 0"
              >
                <button
                  type="submit"
                  class="dropdown-item border-0 bg-transparent w-100 text-start"
                  id="logout-btn"
                  style="
                    cursor: pointer;
                    padding: 0.625rem 1rem;
                    pointer-events: auto;
                  "
                >
                  <i class="bi bi-box-arrow-right"></i> Logout
                </button>
              </form>
            </li>
          </ul>
        </li>
        {% else %}
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('auth.login') }}">Login</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('auth.register') }}">Register</a>
        </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
<script>
  // Logout button handler - ensure it works properly
  document.addEventListener("DOMContentLoaded", function () {
    const logoutBtn = document.getElementById("logout-btn");
    const logoutForm = document.getElementById("logout-form");

    if (logoutBtn && logoutForm) {
      // Remove any existing handlers
      logoutBtn.onclick = null;

      // Add click handler with proper event handling
      logoutBtn.addEventListener(
        "click",
        function (e) {
          e.preventDefault();
          e.stopPropagation();
          e.stopImmediatePropagation();
          console.log("Logout button clicked");
          logoutForm.submit();
          return false;
        },
        true
      ); // Use capture phase

      // Also handle form submit directly
      logoutForm.addEventListener(
        "submit",
        function (e) {
          e.stopPropagation();
          console.log("Logout form submitting");
        },
        true
      );
    }
  });
</script>
