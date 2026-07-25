document.addEventListener("DOMContentLoaded", () => {
    const styleForm = document.getElementById("style-form");
    const imageInput = document.getElementById("image-input");
    const dropzone = document.getElementById("dropzone");
    const dropzonePrompt = document.getElementById("dropzone-prompt");
    const previewWrapper = document.getElementById("preview-wrapper");
    const imagePreview = document.getElementById("image-preview");
    const removeImgBtn = document.getElementById("remove-img-btn");
    const submitBtn = document.getElementById("submit-btn");
    const loadingOverlay = document.getElementById("loading-overlay");
    const loadingStep = document.getElementById("loading-step");
    const progressBar = document.getElementById("progress-bar");
    const resultsSection = document.getElementById("results-section");
    const resultsContainer = document.getElementById("results-container");
    const genderCards = document.querySelectorAll(".gender-card");

    let selectedFile = null;

    // Gender Selection Radio styling toggle
    genderCards.forEach(card => {
        card.addEventListener("click", () => {
            genderCards.forEach(c => c.classList.remove("active"));
            card.classList.add("active");
            const radio = card.querySelector(".gender-radio");
            if (radio) radio.checked = true;
        });
    });

    // Drag and Drop Events
    ["dragenter", "dragover"].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add("dragover");
        }, false);
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove("dragover");
        }, false);
    });

    dropzone.addEventListener("drop", (e) => {
        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            handleFileSelected(files[0]);
        }
    });

    imageInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelected(e.target.files[0]);
        }
    });

    removeImgBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        clearSelectedFile();
    });

    function handleFileSelected(file) {
        const allowedTypes = ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp"];
        if (!allowedTypes.includes(file.type.toLowerCase())) {
            showToast("Invalid file type. Please upload a PNG, JPG, JPEG, GIF, or WEBP image.", "error");
            return;
        }

        const maxSizeMB = 10;
        if (file.size > maxSizeMB * 1024 * 1024) {
            showToast(`File size exceeds maximum allowed limit of ${maxSizeMB}MB.`, "error");
            return;
        }

        selectedFile = file;

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            dropzonePrompt.classList.add("hidden");
            previewWrapper.classList.remove("hidden");
            submitBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    function clearSelectedFile() {
        selectedFile = null;
        imageInput.value = "";
        imagePreview.src = "";
        previewWrapper.classList.add("hidden");
        dropzonePrompt.classList.remove("hidden");
        submitBtn.disabled = true;
    }

    // Form Submit
    styleForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (!selectedFile) {
            showToast("Please select a facial photo first.", "error");
            return;
        }

        const genderVal = document.querySelector('input[name="gender"]:checked').value;
        const formData = new FormData();
        formData.append("image", selectedFile);
        formData.append("gender", genderVal);

        // Show loading modal with step progress simulation
        showLoadingState();

        try {
            updateLoadingStep("Detecting facial ROI & skin tone RGB stats...", 35);

            const response = await fetch("/analyze", {
                method: "POST",
                body: formData
            });

            updateLoadingStep("Consulting Groq LLaMA 3.3 70B AI styling model...", 75);

            const data = await response.json();

            if (!response.ok || !data.success) {
                hideLoadingState();
                showToast(data.error || "Failed to analyze image. Please try another photo.", "error");
                return;
            }

            updateLoadingStep("Building curated shopping links & styling report...", 100);

            setTimeout(() => {
                hideLoadingState();
                renderResults(data);
            }, 500);

        } catch (err) {
            hideLoadingState();
            showToast("Network error. Please check your connection and try again.", "error");
        }
    });

    function showLoadingState() {
        loadingOverlay.classList.remove("hidden");
        progressBar.style.width = "10%";
        loadingStep.textContent = "Uploading image...";
    }

    function updateLoadingStep(message, percent) {
        loadingStep.textContent = message;
        progressBar.style.width = `${percent}%`;
    }

    function hideLoadingState() {
        loadingOverlay.classList.add("hidden");
    }

    function renderResults(data) {
        try {
            const gender = data.gender || "Female";
            const analysis = data.analysis || {};
            const recommendation = data.recommendation || {};
            const shopping_links = data.shopping_links || [];

            const median_rgb = analysis.median_rgb || [180, 140, 120];
            const hex_color = analysis.hex_color || "#b48c78";
            const skin_tone = analysis.skin_tone || "Medium";
            const confidence = analysis.confidence !== undefined ? analysis.confidence : 0.85;
            const luminance = analysis.luminance !== undefined ? analysis.luminance : 150.0;

            const palette = recommendation.palette || {};
            const outfits = recommendation.outfits || {};
            const hairstyle = recommendation.hairstyle || {};
            const accessories = recommendation.accessories || [];

            const html = `
                <div class="results-wrapper">
                    <div class="results-header">
                        <span class="badge-success"><i class="fa-solid fa-circle-check"></i> Analysis Complete</span>
                        <h2 class="results-title">Personalized <span class="gradient-text">Style Profile</span></h2>
                        <p class="results-subtitle">Tailored for <strong>${gender}</strong> complexion</p>
                    </div>

                    <!-- Analysis Summary Card -->
                    <div class="card skin-tone-card">
                        <div class="skin-tone-summary">
                            <div class="color-swatch-wrapper">
                                <div class="color-swatch" style="background-color: ${hex_color};"></div>
                                <span class="swatch-hex">${hex_color}</span>
                            </div>
                            <div class="skin-tone-info">
                                <span class="meta-label">Detected Skin Tone Category</span>
                                <h3 class="skin-tone-name">${skin_tone}</h3>
                                <p class="confidence-badge">
                                    <i class="fa-solid fa-shield-halved"></i> Confidence: ${Math.round(confidence * 100)}%
                                </p>
                                <div class="rgb-stats">
                                    <span class="rgb-pill">R: ${median_rgb[0]}</span>
                                    <span class="rgb-pill">G: ${median_rgb[1]}</span>
                                    <span class="rgb-pill">B: ${median_rgb[2]}</span>
                                    <span class="rgb-pill">Luma Y: ${luminance}</span>
                                </div>
                            </div>
                        </div>
                    </div>


                <!-- Stylist Rationale Card -->
                <div class="card rationale-card">
                    <h3><i class="fa-solid fa-lightbulb icon-accent"></i> Stylist Rationale</h3>
                    <p class="rationale-text">${recommendation.rationale || ""}</p>
                </div>

                <!-- Color Palette Card -->
                <div class="card palette-card">
                    <h3><i class="fa-solid fa-swatchbook icon-accent"></i> Recommended Color Palette</h3>
                    <div class="palette-grid">
                        <div class="palette-group">
                            <span class="palette-title">Primary Colors</span>
                            <div class="chips-list">
                                ${(palette.primary || []).map(c => `<span class="chip chip-primary">${c}</span>`).join("")}
                            </div>
                        </div>
                        <div class="palette-group">
                            <span class="palette-title">Secondary Colors</span>
                            <div class="chips-list">
                                ${(palette.secondary || []).map(c => `<span class="chip chip-secondary">${c}</span>`).join("")}
                            </div>
                        </div>
                        <div class="palette-group">
                            <span class="palette-title">Accent Colors</span>
                            <div class="chips-list">
                                ${(palette.accent || []).map(c => `<span class="chip chip-accent">${c}</span>`).join("")}
                            </div>
                        </div>
                        <div class="palette-group">
                            <span class="palette-title">Colors to Avoid</span>
                            <div class="chips-list">
                                ${(palette.avoid || []).map(c => `<span class="chip chip-avoid">${c}</span>`).join("")}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Outfits Grid -->
                <div class="outfits-section">
                    <h3 class="section-title"><i class="fa-solid fa-shirt icon-accent"></i> Outfit Combinations by Code</h3>
                    <div class="outfits-grid">
                        <div class="outfit-card">
                            <div class="outfit-icon"><i class="fa-solid fa-user-tie"></i></div>
                            <h4>Formal</h4>
                            <ul>
                                ${(outfits.formal || []).map(item => `<li><i class="fa-solid fa-angle-right"></i> ${item}</li>`).join("")}
                            </ul>
                        </div>
                        <div class="outfit-card">
                            <div class="outfit-icon"><i class="fa-solid fa-briefcase"></i></div>
                            <h4>Business</h4>
                            <ul>
                                ${(outfits.business || []).map(item => `<li><i class="fa-solid fa-angle-right"></i> ${item}</li>`).join("")}
                            </ul>
                        </div>
                        <div class="outfit-card">
                            <div class="outfit-icon"><i class="fa-solid fa-glasses"></i></div>
                            <h4>Casual</h4>
                            <ul>
                                ${(outfits.casual || []).map(item => `<li><i class="fa-solid fa-angle-right"></i> ${item}</li>`).join("")}
                            </ul>
                        </div>
                        <div class="outfit-card">
                            <div class="outfit-icon"><i class="fa-solid fa-champagne-glasses"></i></div>
                            <h4>Party / Evening</h4>
                            <ul>
                                ${(outfits.party || []).map(item => `<li><i class="fa-solid fa-angle-right"></i> ${item}</li>`).join("")}
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Hair & Accessories Grid -->
                <div class="grid-2col">
                    <div class="card hair-card">
                        <h3><i class="fa-solid fa-scissors icon-accent"></i> Hairstyle & Maintenance</h3>
                        <h4>Recommendations</h4>
                        <div class="chips-list margin-bottom">
                            ${(hairstyle.recommendations || []).map(s => `<span class="chip chip-secondary">${s}</span>`).join("")}
                        </div>
                        <h4>Maintenance Routine</h4>
                        <ul>
                            ${(hairstyle.maintenance || []).map(tip => `<li><i class="fa-solid fa-check icon-success"></i> ${tip}</li>`).join("")}
                        </ul>
                    </div>

                    <div class="card accessories-card">
                        <h3><i class="fa-solid fa-gem icon-accent"></i> Recommended Accessories</h3>
                        <div class="chips-list">
                            ${(accessories || []).map(a => `<span class="chip chip-accent">${a}</span>`).join("")}
                        </div>
                    </div>
                </div>

                <!-- Shopping Links Section -->
                <div class="card shopping-card">
                    <h3><i class="fa-solid fa-cart-shopping icon-accent"></i> Curated Retailer Search Links</h3>
                    <p class="shopping-intro">Click any item query below to shop live matching products on verified platforms:</p>
                    <div class="shopping-grid">
                        ${(shopping_links || []).map(link => `
                            <div class="shopping-item-card">
                                <div class="shopping-item-header">
                                    <span class="retailer-badge badge-${link.retailer_key}">${link.retailer}</span>
                                </div>
                                <h4 class="shopping-item-title">${link.title}</h4>
                                <a href="${link.url}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">
                                    Shop on ${link.retailer} <i class="fa-solid fa-arrow-up-right-from-square"></i>
                                </a>
                            </div>
                        `).join("")}
                    </div>
                </div>

                <div class="results-actions text-center">
                    <button class="btn btn-secondary btn-lg" onclick="window.scrollTo({top: document.getElementById('upload-section').offsetTop - 80, behavior: 'smooth'})">
                        <i class="fa-solid fa-rotate-left"></i> Analyze Another Photo
                    </button>
                </div>
            </div>
        `;

            resultsContainer.innerHTML = html;
            resultsSection.classList.remove("hidden");

            window.scrollTo({
                top: resultsSection.offsetTop - 30,
                behavior: "smooth"
            });
        } catch (err) {
            console.error("Rendering error:", err);
            showToast("An error occurred while displaying results. Please refresh.", "error");
        }
    }


    function showToast(message, type = "info") {
        const toastContainer = document.getElementById("toast-container");
        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fa-solid ${type === 'error' ? 'fa-circle-exclamation' : 'fa-circle-info'}"></i>
            <span>${message}</span>
        `;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = "0";
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }
});
