{% extends "base.html" %}

{% block title %}Products - ShopNow{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-12 d-flex justify-content-between align-items-center">
        <h1>Products</h1>
        {% if current_user.is_authenticated and current_user.is_admin %}
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addProductModal">
            <i class="bi bi-plus-circle"></i> Add Product
        </button>
        {% endif %}
    </div>
</div>

<!-- Products Grid -->
{% if products %}
    <div class="row">
        {% set default_image = 'https://via.placeholder.com/800x600?text=Product+Image' %}
        {% for product in products.items %}
            {% set product_image = product.image_url if product.image_url else (url_for('static', filename='uploads/' ~ product.images[0].filename) if product.images and product.images|length > 0 else default_image) %}
            <div class="col-6 col-md-4 col-lg-3 mb-4">
                <div class="card h-100">
                    <a href="{{ url_for('products.detail', product_id=product.product_id) }}" style="text-decoration: none; display: block;">
                        <div style="height:200px; overflow:hidden; border-radius: 0.5rem 0.5rem 0 0;">
                            <img src="{{ product_image }}" class="img-fluid product-img" alt="{{ product.name }}" style="width:100%;height:100%;object-fit:cover;" onerror="this.onerror=null;this.src='{{ default_image }}';">
                        </div>
                    </a>
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <p class="card-text text-muted small">{{ product.description[:100] }}{% if product.description|length > 100 %}...{% endif %}</p>
                        <div class="mt-auto">
                            <p class="card-text">
                                <strong class="text-primary">${{ "%.2f"|format(product.price|float) }}</strong>
                                {% if product.stock > 0 %}
                                    <span class="badge bg-success ms-2">In Stock</span>
                                {% else %}
                                    <span class="badge bg-danger ms-2">Out of Stock</span>
                                {% endif %}
                            </p>
                            <a href="{{ url_for('products.detail', product_id=product.product_id) }}" class="btn btn-primary btn-sm w-100">
                                View Details
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
    <div class="d-flex justify-content-center">
        {% if products.has_prev %}
            <a class="btn btn-outline-secondary me-2" href="?page={{ products.prev_num }}">Previous</a>
        {% endif %}
        {% if products.has_next %}
            <a class="btn btn-outline-secondary" href="?page={{ products.next_num }}">Next</a>
        {% endif %}
    </div>
{% else %}
    <div class="alert alert-info">
        <h5>No products found</h5>
        <p>Try adjusting your search or filter criteria.</p>
    </div>
{% endif %}

<!-- Add Product Modal (Admin Only) -->
{% if current_user.is_authenticated and current_user.is_admin %}
<div class="modal fade" id="addProductModal" tabindex="-1" aria-labelledby="addProductModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="addProductModalLabel">Add New Product</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form id="addProductForm">
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="productName" class="form-label">Product Name <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="productName" name="name" required>
                        <div class="invalid-feedback"></div>
                    </div>
                    <div class="mb-3">
                        <label for="productPrice" class="form-label">Price <span class="text-danger">*</span></label>
                        <input type="number" class="form-control" id="productPrice" name="price" step="0.01" min="0.01" required>
                        <div class="invalid-feedback"></div>
                    </div>
                    <div class="mb-3">
                        <label for="productStock" class="form-label">Stock Status <span class="text-danger">*</span></label>
                        <select class="form-select" id="productStock" name="stock_status" required>
                            <option value="">Select status...</option>
                            <option value="in_stock">In Stock</option>
                            <option value="out_of_stock">Out of Stock</option>
                        </select>
                        <div class="invalid-feedback"></div>
                    </div>
                    <div class="mb-3" id="stockQuantityGroup" style="display: none;">
                        <label for="stockQuantity" class="form-label">Stock Quantity <span class="text-danger">*</span></label>
                        <input type="number" class="form-control" id="stockQuantity" name="stock" min="0" value="0">
                        <div class="invalid-feedback"></div>
                    </div>
                    <div class="mb-3">
                        <label for="productDescription" class="form-label">Description</label>
                        <textarea class="form-control" id="productDescription" name="description" rows="3"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="productImageUrl" class="form-label">Image URL <span class="text-danger">*</span></label>
                        <input type="url" class="form-control" id="productImageUrl" name="image_url" required>
                        <div class="invalid-feedback"></div>
                        <small class="form-text text-muted">Enter a valid image URL</small>
                    </div>
                    <div class="mb-3">
                        <label for="productCategory" class="form-label">Category <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="productCategory" name="category" required>
                        <div class="invalid-feedback"></div>
                        <small class="form-text text-muted">Enter category name (e.g., Electronics, Clothing, Books)</small>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Product</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endif %}
{% endblock %}

{% block extra_js %}
{% if current_user.is_authenticated and current_user.is_admin %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const addProductForm = document.getElementById('addProductForm');
    const stockStatusSelect = document.getElementById('productStock');
    const stockQuantityGroup = document.getElementById('stockQuantityGroup');
    const stockQuantityInput = document.getElementById('stockQuantity');
    
    // Show/hide stock quantity input based on stock status
    stockStatusSelect.addEventListener('change', function() {
        if (this.value === 'in_stock') {
            stockQuantityGroup.style.display = 'block';
            stockQuantityInput.setAttribute('required', 'required');
        } else {
            stockQuantityGroup.style.display = 'none';
            stockQuantityInput.removeAttribute('required');
            stockQuantityInput.value = 0;
        }
    });
    
    // Handle form submission
    addProductForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset validation
        const formInputs = addProductForm.querySelectorAll('.form-control, .form-select');
        formInputs.forEach(input => {
            input.classList.remove('is-invalid');
            const feedback = input.nextElementSibling;
            if (feedback && feedback.classList.contains('invalid-feedback')) {
                feedback.textContent = '';
            }
        });
        
        // Get form data
        const formData = new FormData(addProductForm);
        const data = {
            name: formData.get('name'),
            price: parseFloat(formData.get('price')),
            stock_status: formData.get('stock_status'),
            stock: formData.get('stock_status') === 'in_stock' ? parseInt(formData.get('stock') || 0) : 0,
            description: formData.get('description') || '',
            image_url: formData.get('image_url'),
            category: formData.get('category')
        };
        
        // Validate
        let isValid = true;
        if (!data.name || data.name.trim() === '') {
            showError('productName', 'Product name is required');
            isValid = false;
        }
        if (!data.price || data.price <= 0) {
            showError('productPrice', 'Price must be greater than 0');
            isValid = false;
        }
        if (!data.stock_status) {
            showError('productStock', 'Stock status is required');
            isValid = false;
        }
        if (data.stock_status === 'in_stock' && (!data.stock || data.stock < 0)) {
            showError('stockQuantity', 'Stock quantity must be 0 or greater');
            isValid = false;
        }
        if (!data.image_url || data.image_url.trim() === '') {
            showError('productImageUrl', 'Image URL is required');
            isValid = false;
        }
        if (!data.category || data.category.trim() === '') {
            showError('productCategory', 'Category is required');
            isValid = false;
        }
        
        if (!isValid) {
            return;
        }
        
        // Disable submit button
        const submitBtn = addProductForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Adding...';
        
        try {
            // Get CSRF token from meta tag or cookie
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || 
                             getCookie('csrf_token') || 
                             '{{ csrf_token() }}';
            
            const response = await fetch('{{ url_for("products.add") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('addProductModal'));
                modal.hide();
                
                // Reset form
                addProductForm.reset();
                stockQuantityGroup.style.display = 'none';
                
                // Show success message
                showFlashMessage('Product added successfully!', 'success');
                
                // Reload page after a short delay
                setTimeout(() => {
                    window.location.reload();
                }, 500);
            } else {
                // Show error messages
                if (result.errors) {
                    // Map backend field names to frontend field IDs
                    const fieldMap = {
                        'name': 'productName',
                        'price': 'productPrice',
                        'stock_status': 'productStock',
                        'stock': 'stockQuantity',
                        'image_url': 'productImageUrl',
                        'category': 'productCategory'
                    };
                    Object.keys(result.errors).forEach(field => {
                        const fieldId = fieldMap[field] || field;
                        showError(fieldId, result.errors[field]);
                    });
                } else {
                    showFlashMessage(result.message || 'Error adding product', 'danger');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            showFlashMessage('An error occurred while adding the product', 'danger');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Add Product';
        }
    });
    
    function showError(fieldId, message) {
        const field = document.getElementById(fieldId);
        field.classList.add('is-invalid');
        const feedback = field.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = message;
        }
    }
    
    function showFlashMessage(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const main = document.querySelector('main');
        main.insertBefore(alertDiv, main.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
    
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
});
</script>
{% endif %}
{% endblock %}

