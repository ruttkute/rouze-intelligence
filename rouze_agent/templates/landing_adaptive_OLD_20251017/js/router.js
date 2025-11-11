// Path Selection and Dynamic Content Loading

function selectPath(pathType) {
    // Hide quiz if open
    document.getElementById('quiz').classList.add('hidden');
    
    // Scroll to dynamic content area
    const contentArea = document.getElementById('dynamic-content');
    contentArea.classList.remove('hidden');
    contentArea.scrollIntoView({ behavior: 'smooth' });
    
    // Load appropriate module
    loadPathModule(pathType);
}

async function loadPathModule(pathType) {
    const contentArea = document.getElementById('dynamic-content');
    
    // Show loading state
    contentArea.innerHTML = '<div class="loading">Loading your path...</div>';
    
    try {
        // Fetch module content
        const response = await fetch(`modules/path-${pathType}.html`);
        const html = await response.text();
        
        // Inject content with fade-in
        setTimeout(() => {
            contentArea.innerHTML = html;
            contentArea.classList.add('fade-in');
        }, 300);
        
    } catch (error) {
        console.error('Failed to load module:', error);
        contentArea.innerHTML = `
            <div class="error-state">
                <h3>Something went wrong</h3>
                <p>Please <a href="mailto:hello@rouze.com">contact us directly</a></p>
            </div>
        `;
    }
}

// Department Deep Dive
function exploreDepartment(deptName) {
    const modal = document.getElementById('department-modal');
    loadDepartmentDetail(deptName, modal);
    modal.classList.remove('hidden');
}

async function loadDepartmentDetail(deptName, modal) {
    try {
        const response = await fetch(`modules/dept-${deptName}.html`);
        const html = await response.text();
        modal.querySelector('.modal-content').innerHTML = html;
    } catch (error) {
        console.error('Failed to load department:', error);
    }
}