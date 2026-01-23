// Global state
let uploadedFile = null;
let pageCount = 0;
let priceBW = 2;
let priceColor = 10;

// DOM Elements
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const uploadSection = document.getElementById('upload-section');
const settingsSection = document.getElementById('settings-section');
const successSection = document.getElementById('success-section');
const fileInfo = document.getElementById('file-info');
const fileName = document.getElementById('file-name');
const pageCountEl = document.getElementById('page-count');
const uploadError = document.getElementById('upload-error');
const settingsForm = document.getElementById('settings-form');
const totalPriceEl = document.getElementById('total-price');
const loading = document.getElementById('loading');
const loadingText = document.getElementById('loading-text');

// File upload handling
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

async function handleFile(file) {
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showError('Please upload a PDF file');
        return;
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File size must be less than 10MB');
        return;
    }

    uploadedFile = file;
    showLoading('Uploading file...');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            pageCount = data.page_count;
            priceBW = data.price_bw;
            priceColor = data.price_color;

            fileName.textContent = data.filename;
            pageCountEl.textContent = data.page_count;
            
            fileInfo.classList.remove('hidden');
            uploadError.classList.add('hidden');
            
            // Show settings section
            hideLoading();
            uploadSection.classList.add('hidden');
            settingsSection.classList.remove('hidden');
            
            // Calculate initial price
            updatePrice();
        } else {
            hideLoading();
            showError(data.error || 'Upload failed');
        }
    } catch (error) {
        hideLoading();
        showError('Network error. Please try again.');
    }
}

function showError(message) {
    uploadError.textContent = message;
    uploadError.classList.remove('hidden');
}

// Price calculation
function updatePrice() {
    const formData = new FormData(settingsForm);
    const colorMode = formData.get('color_mode');
    const duplex = formData.get('duplex');
    const copies = parseInt(formData.get('copies') || 1);

    const pricePerPage = colorMode === 'color' ? priceColor : priceBW;
    let total = pageCount * pricePerPage * copies;

    // Apply duplex discount
    if (duplex === 'double') {
        total *= 0.8; // 20% discount
    }

    totalPriceEl.textContent = `₹${total.toFixed(2)}`;
}

// Update price on any setting change
settingsForm.addEventListener('change', updatePrice);
settingsForm.addEventListener('input', updatePrice);

// Payment handling
settingsForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(settingsForm);
    const settings = {
        color_mode: formData.get('color_mode'),
        duplex: formData.get('duplex'),
        copies: formData.get('copies'),
        orientation: formData.get('orientation'),
        pages_per_sheet: formData.get('pages_per_sheet')
    };

    showLoading('Creating payment order...');

    try {
        // Create Razorpay order
        const response = await fetch('/create-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        });

        const data = await response.json();

        if (data.success) {
            hideLoading();
            openRazorpay(data.order_id, data.amount);
        } else {
            hideLoading();
            alert(data.error || 'Failed to create payment order');
        }
    } catch (error) {
        hideLoading();
        alert('Network error. Please try again.');
    }
});

function openRazorpay(orderId, amount) {
    const options = {
        key: RAZORPAY_KEY_ID,
        amount: amount * 100, // Convert to paise
        currency: 'INR',
        name: 'PrintEase',
        description: 'Print Job Payment',
        order_id: orderId,
        handler: function(response) {
            verifyPayment(response);
        },
        prefill: {
            name: '',
            email: '',
            contact: ''
        },
        theme: {
            color: '#4CAF50'
        },
        modal: {
            ondismiss: function() {
                alert('Payment cancelled. Please try again.');
            }
        }
    };

    const rzp = new Razorpay(options);
    rzp.open();
}

async function verifyPayment(paymentData) {
    showLoading('Verifying payment and printing...');

    try {
        const response = await fetch('/verify-payment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                razorpay_order_id: paymentData.razorpay_order_id,
                razorpay_payment_id: paymentData.razorpay_payment_id,
                razorpay_signature: paymentData.razorpay_signature
            })
        });

        const data = await response.json();

        hideLoading();

        if (data.success) {
            // Show success message
            settingsSection.classList.add('hidden');
            successSection.classList.remove('hidden');
        } else {
            alert(data.error || 'Payment verification failed');
        }
    } catch (error) {
        hideLoading();
        alert('Network error. Please try again.');
    }
}

function showLoading(text = 'Processing...') {
    loadingText.textContent = text;
    loading.classList.remove('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}
