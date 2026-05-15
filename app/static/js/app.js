const html = document.documentElement;
const toggle = document.getElementById('theme-toggle');
const saved = localStorage.getItem('fb-theme');
if (saved === 'dark') html.dataset.theme = 'dark';
if (toggle) {
    toggle.addEventListener('click', function () {
        const isDark = html.dataset.theme === 'dark';
        html.dataset.theme = isDark ? 'light' : 'dark';
        localStorage.setItem('fb-theme', isDark ? 'light' : 'dark');
    });
}

function openModal(id) {
    document.getElementById(id).style.display = 'grid';
}
function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}
function closeModalOnOverlay(event, id) {
    if (event.target.id === id) closeModal(id);
}

function setupSwatches(containerId, hiddenInputId) {
    const container = document.getElementById(containerId);
    const hidden = document.getElementById(hiddenInputId);
    if (!container || !hidden) return;
    container.querySelectorAll('.fbg-swatch').forEach(sw => {
        sw.addEventListener('click', function () {
            container.querySelectorAll('.fbg-swatch').forEach(s => s.classList.remove('is-on'));
            this.classList.add('is-on');
            hidden.value = this.dataset.color;
        });
    });
}
setupSwatches('create-swatches', 'create-color');

function openCreateModal() {
    document.getElementById('create-nome').value = '';
    document.getElementById('create-tag').value = '';
    document.getElementById('create-descrizione').value = '';
    openModal('create-modal');
    setTimeout(() => document.getElementById('create-nome').focus(), 50);
}

function openCreateTagModal() {
    document.getElementById('create-nome-tag').value = '';
    const swatches = document.querySelectorAll('#create-swatches .fbg-swatch');
    swatches.forEach((s, i) => s.classList.toggle('is-on', i === 0));
    openModal('create-tag-modal');
    setTimeout(() => document.getElementById('create-nome-tag').focus(), 50);
}

function openEditModal(id, name, tag, description) {
    const form = document.getElementById('edit-form');
    form.action = '/binders/' + id + '/edit';
    document.getElementById('edit-nome').value = name;
    document.getElementById('edit-descrizione').value = description;

    const select = document.getElementById('edit-tag');
    if (select) {
        select.value = tag;
    }

    openModal('edit-modal');
}

function openDeleteModal(id, name) {
    const form = document.getElementById('delete-form');
    form.action = '/binders/' + id + '/delete';
    document.getElementById('delete-binder-name').textContent = name;
    openModal('delete-modal');
}

document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        ['create-modal', 'create-tag-modal', 'edit-modal', 'delete-modal'].forEach(id => {
            const m = document.getElementById(id);
            if (m && m.style.display !== 'none') closeModal(id);
        });
    }
});

function openUploadModal(binderId) {
    const form = document.getElementById('upload-form');
    form.action = '/binders/' + binderId + '/upload';
    document.getElementById('upload-input').value = '';
    document.getElementById('upload-pending').innerHTML = '';
    document.getElementById('upload-summary').textContent = 'No files selected';
    document.getElementById('upload-submit').disabled = true;
    openModal('upload-modal');
}

(function setupDropzone() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('upload-input');
    const pending = document.getElementById('upload-pending');
    const summary = document.getElementById('upload-summary');
    const submitBtn = document.getElementById('upload-submit');

    if (!dropzone || !fileInput) return;

    dropzone.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        updatePreview(fileInput.files);
    });

    dropzone.addEventListener('dragover', function (e) {
        e.preventDefault();
        dropzone.classList.add('is-hover');
    });

    dropzone.addEventListener('dragleave', function () {
        dropzone.classList.remove('is-hover');
    });

    dropzone.addEventListener('drop', function (e) {
        e.preventDefault();
        dropzone.classList.remove('is-hover');

        fileInput.files = e.dataTransfer.files;
        updatePreview(fileInput.files);
    });

    function updatePreview(files) {
        pending.innerHTML = '';
        if (!files || files.length === 0) {
            summary.textContent = 'No files selected';
            submitBtn.disabled = true;
            return;
        }
        Array.from(files).forEach(f => {
            const item = document.createElement('div');
            item.className = 'fbg-pending-item';
            item.innerHTML = `
                <div class="fbg-pending-glyph">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
                        <path d="M14 3v5h5M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"></path>
                    </svg>
                </div>
                <span class="fbg-pending-title">${f.name}</span>
                <span class="fbg-pending-size">${humanSize(f.size)}</span>
            `;
            pending.appendChild(item);
        });
        summary.textContent = files.length + ' file' + (files.length > 1 ? 's' : '') + ' selected';
        submitBtn.disabled = false;
    }

    function humanSize(n) {
        if (n < 1024) return n + ' B';
        if (n < 1024 * 1024) return (n / 1024).toFixed(0) + ' KB';
        return (n / 1024 / 1024).toFixed(1) + ' MB';
    }
})();

function toggleDropdown(id) {
    const dd = document.getElementById(id);
    if (!dd) return;
    closeAllDropdowns(id);
    dd.classList.toggle('is-open');
}

function closeDropdown(id) {
    const dd = document.getElementById(id);
    if (dd) dd.classList.remove('is-open');
}

function closeAllDropdowns(except) {
    document.querySelectorAll('.fbg-dropdown.is-open').forEach(dd => {
        if (dd.id !== except) dd.classList.remove('is-open');
    });
}

(function setupDropdowns() {
    const trigger = document.getElementById('plus-trigger');
    if (trigger) {
        trigger.addEventListener('click', function (e) {
            e.stopPropagation();
            toggleDropdown('plus-dropdown');
        });
    }

    document.addEventListener('click', function () {
        closeAllDropdowns();
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeAllDropdowns();
    });
})();