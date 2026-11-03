(() => {
    const section = document.getElementById('education');
    if (!section) return;

    const educationGrid = document.getElementById('education-grid');
    const loadingState = document.getElementById('education-loading');
    const emptyState = document.getElementById('education-empty');
    const errorState = document.getElementById('education-error');
    const retryButton = document.getElementById('education-retry');
    const cardTemplate = document.getElementById('education-card-template');
    const deleteForm = document.getElementById('delete-education-form');
    const deleteModal = document.getElementById('delete-education-modal');
    const deleteName = document.getElementById('delete-education-name');
    const searchInput = document.getElementById('education-search-input');
    const searchForm = document.getElementById('education-search-form');
    const educationForm = document.getElementById('education-form');
    const formModal = document.getElementById('add-education-modal');
    const formTitle = document.getElementById('add-education-modal-title');
    const formErrors = document.getElementById('education-form-errors');
    const placeholderId = '00000000-0000-0000-0000-000000000000';
    let searchTimer;
    let activeRequest;
    let editingId = null;
    let saving = false;

    function getCookie(name) {
        const prefix = `${name}=`;
        const cookie = document.cookie.split(';').map(value => value.trim())
            .find(value => value.startsWith(prefix));
        return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : null;
    }

    function educationEndpoint(pattern, id) {
        return pattern.replace(placeholderId, id);
    }

    async function writeEducation(url, method, payload) {
        const response = await fetch(url, {
            method,
            headers: {
                Accept: 'application/json', 'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: payload === undefined ? undefined : JSON.stringify(payload),
        });
        if (response.status === 204) return null;
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            const messages = Object.values(data).flat().filter(value => typeof value === 'string');
            throw new Error(messages.join(' ') || `Permintaan gagal (HTTP ${response.status}).`);
        }
        return data;
    }

    function setEducationState(state) {
        loadingState.hidden = state !== 'loading';
        emptyState.hidden = state !== 'empty';
        errorState.hidden = state !== 'error';
        educationGrid.hidden = state !== 'data';
        educationGrid.setAttribute('aria-busy', String(state === 'loading'));
        retryButton.disabled = state === 'loading';
    }

    function prepareEducationForm(education = null) {
        if (!educationForm || saving) return;
        editingId = education ? education.id : null;
        educationForm.reset();
        formErrors.hidden = true;
        formErrors.textContent = '';
        formTitle.textContent = editingId ? 'Edit Education' : 'Tambah Education';
        educationForm.querySelector('[type="submit"]').textContent = editingId ? 'Simpan Perubahan' : 'Tambah Education';
        if (education) {
            for (const field of ['institution', 'degree', 'description', 'started_at', 'ended_at']) {
                educationForm.elements.namedItem(field).value = education[field] ?? '';
            }
        }
    }

    function buildEducationCardElement(education) {
        if (!education || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(education.id)
            || typeof education.started_at !== 'string') {
            throw new Error('Format Education tidak sesuai');
        }
        const card = cardTemplate.content.firstElementChild.cloneNode(true);
        const setText = (field, value) => {
            card.querySelector(`[data-field="${field}"]`).textContent = value;
        };
        setText('institution', education.institution);
        setText('degree', education.degree);
        setText('description', education.description);
        card.querySelector('[data-field="description"]').hidden = !education.description;
        const endYear = education.is_ongoing ? 'Present' : education.ended_at.slice(0, 4);
        setText('period', `${education.started_at.slice(0, 4)}-${endYear}`);
        setText('status', education.is_ongoing ? 'Ongoing' : 'Completed');
        setText('star-count', education.star_count);

        const editLink = card.querySelector('[data-action="edit"]');
        if (editLink) {
            editLink.href = educationEndpoint(section.dataset.editUrl, education.id);
            editLink.addEventListener('click', event => {
                if (!educationForm) return;
                event.preventDefault();
                if (saving) return;
                prepareEducationForm(education);
                formModal.showPopover();
            });
        }
        const deleteButton = card.querySelector('[data-action="delete"]');
        if (deleteButton && deleteForm && deleteName) {
            deleteButton.setAttribute('aria-label', `Hapus ${education.institution}`);
            deleteButton.addEventListener('click', () => {
                deleteName.textContent = `${education.degree} - ${education.institution}`;
                deleteForm.action = educationEndpoint(section.dataset.deleteUrl, education.id);
            });
        }
        const starButton = card.querySelector('[data-action="star"]');
        if (starButton) {
            setText('star-label', education.is_starred ? 'Unstar' : 'Star');
            starButton.classList.toggle('is-starred', education.is_starred);
            starButton.setAttribute('aria-pressed', String(education.is_starred));
            starButton.addEventListener('click', async () => {
                if (starButton.disabled) return;
                starButton.disabled = true;
                try {
                    await writeEducation(educationEndpoint(section.dataset.starUrl, education.id), 'POST');
                    await fetchEducation();
                    showToast('Berhasil', 'Star diperbarui.', 'success');
                } catch (error) {
                    showToast('Gagal memperbarui star', error.message, 'error');
                } finally {
                    starButton.disabled = false;
                }
            });
        }
        return card;
    }

    async function fetchEducation() {
        clearTimeout(searchTimer);
        if (activeRequest) activeRequest.abort();
        const controller = new AbortController();
        activeRequest = controller;
        const query = searchInput.value.trim();
        const url = new URL(section.dataset.endpoint, window.location.origin);
        if (query) url.searchParams.set('institution', query);
        setEducationState('loading');
        try {
            const response = await fetch(url, {
                headers: { Accept: 'application/json' }, signal: controller.signal,
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (controller.signal.aborted) return;
            if (!Array.isArray(data)) throw new Error('Format respons tidak sesuai');
            educationGrid.replaceChildren(...data.map(buildEducationCardElement));
            emptyState.textContent = query
                ? 'Tidak ada pendidikan yang cocok dengan pencarian.' : 'No education history yet.';
            setEducationState(data.length ? 'data' : 'empty');
        } catch (error) {
            if (controller.signal.aborted) return;
            console.error('Gagal memuat Education:', error);
            setEducationState('error');
        }
    }

    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimer);
        if (activeRequest) activeRequest.abort();
        searchTimer = setTimeout(fetchEducation, 300);
    });
    searchForm.addEventListener('submit', event => {
        event.preventDefault();
        fetchEducation();
    });
    const createButton = section.querySelector('[data-action="create"]');
    if (createButton) createButton.addEventListener('click', () => prepareEducationForm());

    if (educationForm && formModal && formErrors) {
        const submitButton = educationForm.querySelector('[type="submit"]');
        educationForm.addEventListener('submit', async event => {
            event.preventDefault();
            if (saving) return;
            saving = true;
            submitButton.disabled = true;
            submitButton.textContent = 'Menyimpan...';
            formErrors.hidden = true;
            formErrors.textContent = '';
            const currentId = editingId;
            try {
                const fields = new FormData(educationForm);
                const payload = Object.fromEntries([
                    'institution', 'degree', 'description', 'started_at', 'ended_at',
                ].map(name => [name, fields.get(name)]));
                payload.ended_at = payload.ended_at || null;
                const url = currentId ? educationEndpoint(section.dataset.detailUrl, currentId) : section.dataset.endpoint;
                await writeEducation(url, currentId ? 'PUT' : 'POST', payload);
                educationForm.reset();
                if (formModal.matches(':popover-open')) formModal.hidePopover();
                await fetchEducation();
                showToast('Berhasil', currentId ? 'Data pendidikan berhasil diperbarui.' : 'Data pendidikan berhasil ditambahkan.', 'success');
            } catch (error) {
                formErrors.textContent = error.message;
                formErrors.hidden = false;
                showToast('Gagal menyimpan pendidikan', error.message, 'error');
            } finally {
                saving = false;
                submitButton.disabled = false;
                submitButton.textContent = currentId ? 'Simpan Perubahan' : 'Tambah Education';
            }
        });
    }
    if (deleteForm && deleteModal) {
        const submitButton = deleteForm.querySelector('[type="submit"]');
        deleteForm.addEventListener('submit', async event => {
            event.preventDefault();
            if (submitButton.disabled) return;
            submitButton.disabled = true;
            try {
                await writeEducation(deleteForm.action, 'DELETE');
                if (deleteModal.matches(':popover-open')) deleteModal.hidePopover();
                await fetchEducation();
                showToast('Berhasil', 'Data pendidikan berhasil dihapus.', 'success');
            } catch (error) {
                showToast('Gagal menghapus pendidikan', error.message, 'error');
            } finally {
                submitButton.disabled = false;
            }
        });
    }
    retryButton.addEventListener('click', fetchEducation);
    fetchEducation();
})();
