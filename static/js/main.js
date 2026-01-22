// PrintEase - Main JavaScript (UPI Flow)

document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const pageCount = document.getElementById('page-count');
    const uploadError = document.getElementById('upload-error');
    const uploadSection = document.getElementById('upload-section');
    const settingsSection = document.getElementById('settings-section');
    const settingsForm = document.getElementById('settings-form');
    const totalPrice = document.getElementById('total-price');
    const loading = document.getElementById('loading');

    let uploadedPageCount = 0;
    let priceBW = 2;
    let priceColor = 10;

    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Handle file upload
    function handleFile(file) {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showError('Only PDF files are allowed');
            return;
        }

        showLoading();
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.success) {
                uploadedPageCount = data.page_count;
                priceBW = data.price_bw;
                priceColor = data.price_color;
                
                fileName.textContent = data.filename;
                pageCount.textContent = data.page_count;
                fileInfo.classList.remove('hidden');
                uploadError.classList.add('hidden');
                
                // Show settings section
                setTimeout(() => {
                    settingsSection.classList.remove('hidden');
                    updatePrice();
                }, 300);
            } else {
                showError(data.error);
            }
        })
        .catch(error => {
            hideLoading();
            showError('Upload failed. Please try again.');
        });
    }

    // Update price calculation
    function updatePrice() {
        const colorMode = document.querySelector('input[name="color_mode"]:checked').value;
        const duplex = document.querySelector('input[name="duplex"]:checked').value;
        const copies = parseInt(document.getElementById('copies').value) || 1;

        let pricePerPage = colorMode === 'color' ? priceColor : priceBW;
        let total = uploadedPageCount * pricePerPage * copies;
        
        if (duplex === 'double') {
            total = total * 0.8; // 20% discount
        }

        totalPrice.textContent = '₹' + Math.round(total);
    }

    // Listen for settings changes
    settingsForm.addEventListener('change', updatePrice);
    document.getElementById('copies').addEventListener('input', updatePrice);

    // Form submit - create job
    settingsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            color_mode: document.querySelector('input[name="color_mode"]:checked').value,
            duplex: document.querySelector('input[name="duplex"]:checked').value,
            copies: document.getElementById('copies').value,
            orientation: document.querySelector('input[name="orientation"]:checked').value,
            pages_per_sheet: document.getElementById('pages_per_sheet').value
        };

        showLoading();

        fetch('/create-job', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.success) {
                // Redirect to payment page
                window.location.href = '/payment/' + data.job_id;
            } else {
                showError(data.error);
            }
        })
        .catch(error => {
            hideLoading();
            showError('Failed to create job. Please try again.');
        });
    });

    // Show error
    function showError(message) {
        uploadError.textContent = message;
        uploadError.classList.remove('hidden');
    }

    // Loading
    function showLoading() {
        loading.classList.remove('hidden');
    }

    function hideLoading() {
        loading.classList.add('hidden');
    }
});
