// Business Idea to PRD Generator Frontend
// Handles form submission, API communication, and result display

class PRDGenerator {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.currentRequest = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkApiStatus();
        this.setupMarkdownRenderer();
    }

    // Configure marked.js for markdown rendering
    setupMarkdownRenderer() {
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                breaks: true,
                gfm: true,
                sanitize: false,
                smartLists: true,
                smartypants: true,
                highlight: function(code, lang) {
                    if (lang && hljs.getLanguage(lang)) {
                        try {
                            return hljs.highlight(code, { language: lang }).value;
                        } catch (err) {
                            console.warn('Highlight.js error:', err);
                        }
                    }
                    return hljs.highlightAuto(code).value;
                }
            });
        }
    }

    bindEvents() {
        // Form submission
        const form = document.getElementById('prd-form');
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));

        // Action buttons
        const copyBtn = document.getElementById('copy-btn');
        const downloadBtn = document.getElementById('download-btn');
        const newBtn = document.getElementById('new-btn');
        const retryBtn = document.getElementById('retry-btn');

        copyBtn?.addEventListener('click', () => this.copyToClipboard());
        downloadBtn?.addEventListener('click', () => this.downloadPRD());
        newBtn?.addEventListener('click', () => this.resetForm());
        retryBtn?.addEventListener('click', () => this.retryGeneration());

        // Auto-resize textarea
        const businessIdeaTextarea = document.getElementById('business-idea');
        businessIdeaTextarea.addEventListener('input', this.autoResizeTextarea);
    }

    autoResizeTextarea(e) {
        e.target.style.height = 'auto';
        e.target.style.height = e.target.scrollHeight + 'px';
    }

    async checkApiStatus() {
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');

        try {
            const response = await fetch(`${this.apiBaseUrl}/health`, {
                method: 'GET',
                timeout: 5000
            });

            if (response.ok) {
                statusDot.className = 'status-dot connected';
                statusText.textContent = 'API Connected - Ready to generate PRDs';
                
                // Get crew info
                try {
                    const crewResponse = await fetch(`${this.apiBaseUrl}/crew-info`);
                    if (crewResponse.ok) {
                        const crewInfo = await crewResponse.json();
                        console.log('Agent Crew Info:', crewInfo);
                    }
                } catch (err) {
                    console.warn('Could not fetch crew info:', err);
                }
            } else {
                throw new Error(`API returned status ${response.status}`);
            }
        } catch (error) {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'API Disconnected - Please start the server first';
            console.error('API connection error:', error);
        }
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        // Collect form data
        const formData = new FormData(e.target);
        const requestData = {};
        
        for (const [key, value] of formData.entries()) {
            if (value.trim()) {
                requestData[key] = value.trim();
            }
        }

        // Validate required fields
        if (!requestData.business_idea) {
            this.showError('Business idea is required');
            return;
        }

        // Start generation process
        await this.generatePRD(requestData);
    }

    async generatePRD(requestData) {
        this.showProgress();
        this.hideError();
        this.hideResults();

        const generateBtn = document.getElementById('generate-btn');
        const btnText = generateBtn.querySelector('.btn-text');
        const spinner = generateBtn.querySelector('.loading-spinner');

        // Update button state
        generateBtn.disabled = true;
        btnText.textContent = 'Generating...';
        spinner.style.display = 'block';

        try {
            // Simulate progress steps
            this.updateProgress(0, 'Initializing agent crew...');
            await this.delay(500);

            this.updateProgress(15, 'Starting market research...');
            this.activateStep('step-1');
            await this.delay(1000);

            // Make the API request
            console.log('Sending request:', requestData);
            const response = await fetch(`${this.apiBaseUrl}/generate-prd`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`API request failed (${response.status}): ${errorData}`);
            }

            // Update progress for different stages
            this.updateProgress(40, 'Market research complete. Developing business model...');
            this.completeStep('step-1');
            this.activateStep('step-2');
            await this.delay(1000);

            this.updateProgress(70, 'Business model complete. Creating PRD document...');
            this.completeStep('step-2');
            this.activateStep('step-3');
            await this.delay(1000);

            this.updateProgress(95, 'Finalizing PRD document...');
            
            const result = await response.json();
            console.log('API Response:', result);

            this.updateProgress(100, 'PRD generation complete!');
            this.completeStep('step-3');
            
            // Show results
            await this.delay(500);
            this.showResults(result);

        } catch (error) {
            console.error('Generation error:', error);
            this.showError(`Failed to generate PRD: ${error.message}`);
        } finally {
            // Reset button state
            generateBtn.disabled = false;
            btnText.textContent = 'Generate PRD';
            spinner.style.display = 'none';
            this.hideProgress();
        }
    }

    showProgress() {
        const progressSection = document.getElementById('progress-section');
        progressSection.style.display = 'block';
        progressSection.scrollIntoView({ behavior: 'smooth' });
        
        // Reset all steps
        document.querySelectorAll('.step').forEach(step => {
            step.classList.remove('active', 'completed');
        });
    }

    hideProgress() {
        const progressSection = document.getElementById('progress-section');
        progressSection.style.display = 'none';
    }

    updateProgress(percentage, text) {
        const progressFill = document.getElementById('progress-fill');
        const progressText = document.getElementById('progress-text');
        
        progressFill.style.width = `${percentage}%`;
        progressText.textContent = text;
    }

    activateStep(stepId) {
        const step = document.getElementById(stepId);
        if (step) {
            step.classList.add('active');
        }
    }

    completeStep(stepId) {
        const step = document.getElementById(stepId);
        if (step) {
            step.classList.remove('active');
            step.classList.add('completed');
        }
    }

    showResults(result) {
        const resultsSection = document.getElementById('results-section');
        const validationResults = document.getElementById('validation-results');
        const prdContent = document.getElementById('prd-content');

        // Display validation results
        if (result.validation_results) {
            const validation = result.validation_results;
            const statusClass = validation.validation_passed ? 'validation-success' : 'validation-warning';
            
            validationResults.innerHTML = `
                <div class="${statusClass}">
                    ✅ PRD Validation: ${validation.validation_passed ? 'Passed' : 'Needs Review'}
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #666;">
                    Sections found: ${validation.found_sections}/${validation.total_sections} 
                    (${validation.completeness_score.toFixed(1)}% complete)
                    ${validation.missing_sections?.length ? 
                        `<br>Missing: ${validation.missing_sections.join(', ')}` : ''}
                </div>
            `;
        }

        // Render markdown content
        if (result.prd_document) {
            this.renderMarkdown(result.prd_document, prdContent);
            this.currentPRDContent = result.prd_document;
        }

        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    renderMarkdown(markdown, container) {
        if (typeof marked !== 'undefined') {
            try {
                const html = marked.parse(markdown);
                container.innerHTML = html;
                
                // Highlight code blocks
                if (typeof hljs !== 'undefined') {
                    container.querySelectorAll('pre code').forEach((block) => {
                        hljs.highlightElement(block);
                    });
                }
            } catch (error) {
                console.error('Markdown rendering error:', error);
                // Fallback to plain text
                container.innerHTML = `<pre>${this.escapeHtml(markdown)}</pre>`;
            }
        } else {
            // Fallback if marked.js is not available
            container.innerHTML = `<pre>${this.escapeHtml(markdown)}</pre>`;
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    hideResults() {
        const resultsSection = document.getElementById('results-section');
        resultsSection.style.display = 'none';
    }

    showError(message) {
        const errorSection = document.getElementById('error-section');
        const errorMessage = document.getElementById('error-message');
        
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        errorSection.scrollIntoView({ behavior: 'smooth' });
    }

    hideError() {
        const errorSection = document.getElementById('error-section');
        errorSection.style.display = 'none';
    }

    async copyToClipboard() {
        if (!this.currentPRDContent) return;

        try {
            await navigator.clipboard.writeText(this.currentPRDContent);
            
            // Show feedback
            const copyBtn = document.getElementById('copy-btn');
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '✅ Copied!';
            copyBtn.style.background = 'rgba(40, 167, 69, 0.3)';
            
            setTimeout(() => {
                copyBtn.textContent = originalText;
                copyBtn.style.background = '';
            }, 2000);
        } catch (error) {
            console.error('Copy failed:', error);
            alert('Failed to copy to clipboard. Please select and copy manually.');
        }
    }

    downloadPRD() {
        if (!this.currentPRDContent) return;

        const blob = new Blob([this.currentPRDContent], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        
        // Generate filename with timestamp
        const timestamp = new Date().toISOString().slice(0, 10);
        a.href = url;
        a.download = `PRD_${timestamp}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    resetForm() {
        // Clear form
        document.getElementById('prd-form').reset();
        
        // Hide sections
        this.hideResults();
        this.hideError();
        this.hideProgress();
        
        // Reset current content
        this.currentPRDContent = null;
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Focus on business idea field
        setTimeout(() => {
            document.getElementById('business-idea').focus();
        }, 500);
    }

    retryGeneration() {
        this.hideError();
        const lastFormData = this.getLastFormData();
        if (lastFormData) {
            this.generatePRD(lastFormData);
        }
    }

    getLastFormData() {
        // Get current form data for retry
        const form = document.getElementById('prd-form');
        const formData = new FormData(form);
        const requestData = {};
        
        for (const [key, value] of formData.entries()) {
            if (value.trim()) {
                requestData[key] = value.trim();
            }
        }
        
        return Object.keys(requestData).length > 0 ? requestData : null;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing PRD Generator...');
    new PRDGenerator();
});

// Handle page visibility changes to reconnect if needed
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Check API status when page becomes visible again
        setTimeout(() => {
            if (window.prdGenerator) {
                window.prdGenerator.checkApiStatus();
            }
        }, 1000);
    }
});

// Export for debugging
window.PRDGenerator = PRDGenerator;