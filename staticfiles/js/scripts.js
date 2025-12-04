// ===== GLOBAL VARIABLES =====
let currentSlide = 0;
let cart = JSON.parse(localStorage.getItem('pearlluxury-cart')) || [];
let isAutoSliding = true;

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    initHeroSlider();
    initScrollAnimations();
    initCart();
    updateCartBadge();
    initSearch();
});

// ===== HERO SLIDER FUNCTIONALITY =====
function initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.indicator');
    
    if (slides.length === 0) return;
    
    // Auto-rotate slides every 5 seconds
    setInterval(() => {
        if (isAutoSliding) {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }
    }, 5000);
}

function showSlide(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.indicator');
    
    // Remove active class from all slides and indicators
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));
    
    // Add active class to current slide and indicator
    if (slides[index]) {
        slides[index].classList.add('active');
    }
    if (indicators[index]) {
        indicators[index].classList.add('active');
    }
}

function goToSlide(index) {
    currentSlide = index;
    showSlide(currentSlide);
    
    // Pause auto-sliding briefly when user manually changes slide
    isAutoSliding = false;
    setTimeout(() => {
        isAutoSliding = true;
    }, 10000);
}

// ===== MOBILE MENU FUNCTIONALITY =====
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');
    
    if (mobileMenu.style.display === 'block') {
        mobileMenu.style.display = 'none';
        menuIcon.style.display = 'block';
        closeIcon.style.display = 'none';
        mobileMenu.classList.remove('open');
    } else {
        mobileMenu.style.display = 'block';
        menuIcon.style.display = 'none';
        closeIcon.style.display = 'block';
        mobileMenu.classList.add('open');
    }
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    
    if (mobileMenu && mobileMenuBtn && 
        !mobileMenu.contains(event.target) && 
        !mobileMenuBtn.contains(event.target)) {
        mobileMenu.style.display = 'none';
        const menuIcon = document.getElementById('menu-icon');
        const closeIcon = document.getElementById('close-icon');
        if (menuIcon) menuIcon.style.display = 'block';
        if (closeIcon) closeIcon.style.display = 'none';
        mobileMenu.classList.remove('open');
    }
});

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Observe all elements with animation classes
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// ===== SEARCH FUNCTIONALITY =====
function initSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', handleSearch);
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
    });
}

function handleSearch(e) {
    const query = e.target.value.toLowerCase();
    
    // Debounce search
    clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
        if (query.length > 2) {
            showSearchSuggestions(query);
        } else {
            hideSearchSuggestions();
        }
    }, 300);
}

function showSearchSuggestions(query) {
    // Mock search suggestions - in real implementation, this would call your backend
    const suggestions = [
        'Electronics',
        'Gaming Laptop',
        '4K TV',
        'Protein Powder',
        'Fish Tank',
        'Gas Cylinders'
    ].filter(item => item.toLowerCase().includes(query));

    // Create or update suggestions dropdown
    let dropdown = document.querySelector('.search-suggestions');
    if (!dropdown) {
        dropdown = document.createElement('div');
        dropdown.className = 'search-suggestions';
        dropdown.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 0.5rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            z-index: 1000;
            max-height: 200px;
            overflow-y: auto;
        `;
        document.querySelector('.search-wrapper').appendChild(dropdown);
    }

    dropdown.innerHTML = suggestions.map(suggestion => 
        `<div class="search-suggestion" style="padding: 0.75rem; cursor: pointer; border-bottom: 1px solid #f3f4f6;" 
         onclick="performSearch('${suggestion}')">${suggestion}</div>`
    ).join('');
}

function hideSearchSuggestions() {
    const dropdown = document.querySelector('.search-suggestions');
    if (dropdown) {
        dropdown.remove();
    }
}

function performSearch(query) {
    hideSearchSuggestions();
    
    // In a real implementation, you would redirect to search results or filter products
    showNotification(`Searching for: ${query}`, 'success');
    
    // Mock redirect to appropriate category
    const categoryMap = {
        'electronics': 'electronics.html',
        'laptop': 'electronics.html',
        'tv': 'electronics.html',
        'protein': 'supplements.html',
        'supplement': 'supplements.html',
        'fish': 'aquarium.html',
        'tank': 'aquarium.html',
        'gas': 'gas.html'
    };
    
    const lowerQuery = query.toLowerCase();
    for (const [key, page] of Object.entries(categoryMap)) {
        if (lowerQuery.includes(key)) {
            setTimeout(() => {
                window.location.href = page;
            }, 1000);
            return;
        }
    }
}

// ===== CART FUNCTIONALITY =====
function initCart() {
    updateCartDisplay();
    updateCartBadge();
}

function addToCart(name, price, image = '') {
    const existingItem = cart.find(item => item.name === name);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: Date.now(),
            name: name,
            price: price,
            quantity: 1,
            image: image
        });
    }
    
    localStorage.setItem('pearlluxury-cart', JSON.stringify(cart));
    updateCartBadge();
    showNotification(`${name} added to cart!`, 'success');
    
    // Add visual feedback
    const button = event.target;
    const originalText = button.textContent;
    button.textContent = 'Added!';
    button.style.background = '#10b981';
    setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '';
    }, 2000);
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    localStorage.setItem('pearlluxury-cart', JSON.stringify(cart));
    updateCartDisplay();
    updateCartBadge();
    showNotification('Item removed from cart', 'success');
}

function updateQuantity(id, newQuantity) {
    if (newQuantity <= 0) {
        removeFromCart(id);
        return;
    }
    
    const item = cart.find(item => item.id === id);
    if (item) {
        item.quantity = newQuantity;
        localStorage.setItem('pearlluxury-cart', JSON.stringify(cart));
        updateCartDisplay();
        updateCartBadge();
    }
}

function updateCartBadge() {
    const badges = document.querySelectorAll('.cart-badge');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    badges.forEach(badge => {
        badge.textContent = totalItems;
        badge.style.display = totalItems > 0 ? 'flex' : 'none';
    });
}

function updateCartDisplay() {
    const cartContainer = document.getElementById('cart-items');
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    
    if (!cartContainer) return;
    
    if (cart.length === 0) {
        cartContainer.innerHTML = `
            <div class="empty-cart" style="text-align: center; padding: 3rem; color: #6b7280;">
                <svg width="64" height="64" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="margin: 0 auto 1rem;">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m1.6 8L5 3H3m4 10v6a1 1 0 001 1h8a1 1 0 001-1v-6m-10 0V9a1 1 0 011-1h8a1 1 0 011 1v4.01"></path>
                </svg>
                <h3 style="margin-bottom: 0.5rem;">Your cart is empty</h3>
                <p>Start shopping to add items to your cart</p>
                <a href="index.html" class="btn btn-primary btn-rounded" style="margin-top: 1rem;">Continue Shopping</a>
            </div>
        `;
        return;
    }
    
    cartContainer.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-image" style="background-image: url('${item.image || 'https://via.placeholder.com/80'}')"></div>
            <div class="cart-item-details">
                <h3 class="cart-item-title">${item.name}</h3>
                <p class="cart-item-price">$${item.price}</p>
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                    <input type="number" value="${item.quantity}" class="quantity-input" 
                           onchange="updateQuantity(${item.id}, parseInt(this.value))" min="1">
                    <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                </div>
            </div>
            <button class="remove-btn" onclick="removeFromCart(${item.id})">
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
            </button>
        </div>
    `).join('');
    
    // Update totals
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const shipping = subtotal > 100 ? 0 : 10;
    const total = subtotal + shipping;
    
    if (subtotalElement) subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
    if (totalElement) totalElement.textContent = `$${total.toFixed(2)}`;
}

function proceedToCheckout() {
    if (cart.length === 0) {
        showNotification('Your cart is empty!', 'error');
        return;
    }
    
    // In a real implementation, this would integrate with a payment processor
    showNotification('Redirecting to checkout...', 'success');
    
    // Mock checkout process
    setTimeout(() => {
        alert(`Order total: $${cart.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2)}\n\nThank you for your order!\n\nThis is a demo - no actual payment was processed.`);
        
        // Clear cart after successful "checkout"
        cart = [];
        localStorage.setItem('pearlluxury-cart', JSON.stringify(cart));
        updateCartDisplay();
        updateCartBadge();
    }, 1500);
}

// ===== NOTIFICATION SYSTEM =====
function showNotification(message, type = 'success') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }
    
    // Create new notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Hide notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 3000);
}

// ===== SMOOTH SCROLLING =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== PRODUCT FILTERING (for category pages) =====
function filterProducts(category) {
    const products = document.querySelectorAll('.product-card');
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    // Update active filter button
    filterBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Filter products
    products.forEach(product => {
        const productCategory = product.dataset.category;
        if (category === 'all' || productCategory === category) {
            product.style.display = 'block';
            product.classList.add('animate-fadeInUp');
        } else {
            product.style.display = 'none';
        }
    });
}

// ===== PRICE RANGE FILTERING =====
function filterByPrice() {
    const minPrice = parseInt(document.getElementById('min-price').value) || 0;
    const maxPrice = parseInt(document.getElementById('max-price').value) || 10000;
    const products = document.querySelectorAll('.product-card');
    
    products.forEach(product => {
        const price = parseInt(product.dataset.price) || 0;
        if (price >= minPrice && price <= maxPrice) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}

// ===== LAZY LOADING IMAGES =====
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// ===== WISHLIST FUNCTIONALITY =====
let wishlist = JSON.parse(localStorage.getItem('pearlluxury-wishlist')) || [];

function toggleWishlist(id, name) {
    const index = wishlist.findIndex(item => item.id === id);
    
    if (index > -1) {
        wishlist.splice(index, 1);
        showNotification(`${name} removed from wishlist`, 'success');
    } else {
        wishlist.push({ id, name });
        showNotification(`${name} added to wishlist`, 'success');
    }
    
    localStorage.setItem('pearlluxury-wishlist', JSON.stringify(wishlist));
    updateWishlistButtons();
}

function updateWishlistButtons() {
    const wishlistBtns = document.querySelectorAll('.wishlist-btn');
    wishlistBtns.forEach(btn => {
        const id = btn.dataset.id;
        const isInWishlist = wishlist.some(item => item.id === id);
        btn.classList.toggle('active', isInWishlist);
    });
}

// ===== INITIALIZE ON PAGE LOAD =====
window.addEventListener('load', () => {
    initLazyLoading();
    updateWishlistButtons();
    
    // Add loading animation
    document.body.classList.add('loaded');
});

// ===== FORM VALIDATION =====
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#ef4444';
            isValid = false;
        } else {
            input.style.borderColor = '#d1d5db';
        }
    });
    
    return isValid;
}

// ===== BACK TO TOP BUTTON =====
window.addEventListener('scroll', () => {
    const backToTop = document.getElementById('back-to-top');
    if (window.pageYOffset > 300) {
        if (backToTop) backToTop.style.display = 'block';
    } else {
        if (backToTop) backToTop.style.display = 'none';
    }
});

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}