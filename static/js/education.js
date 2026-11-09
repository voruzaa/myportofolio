(() => {
    const section = document.getElementById('education');
    if (!section) return;

    const educationGrid = document.getElementById('education-grid');
    const loadingState = document.getElementById('education-loading');
    const emptyState = document.getElementById('education-empty');
    const errorState = document.getElementById('education-error');
    const retryButton = document.getElementById('education-retry');
    const cardTemplate = document.getElementById('education-card-template');
    const deleteModal = document.getElementById('delete-education-modal');
    const deleteForm = document.getElementById('delete-education-form');
    const deleteName = document.getElementById('delete-education-name');
    const searchInput = document.getElementById('education-search-input');
    const searchForm = document.getElementById('education-search-form');
    const addForm = document.getElementById('education-form');
    const addModal = document.getElementById('add-education-modal');
    const formErrors = document.getElementById('education-form-errors');
    const editModal = document.getElementById('edit-education-modal');
    const editForm = document.getElementById('education-edit-form');
    const editErrors = document.getElementById('education-edit-errors');
    const placeholderId = '00000000-0000-0000-0000-000000000000';
    const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    let searchTimer;
    let activeRequest;

    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'));
        return match ? decodeURIComponent(match[2]) : null;
    }

    function escapeHtml(value) {
        return String(value ?? '').replace(/[&<>"']/g, (char) => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;',
        }[char]));
    }

    function detailUrl(id) {
        return section.dataset.apiDetailUrl.replace(placeholderId, encodeURIComponent(id));
    }

    function starUrl(id) {
        return section.dataset.apiStarUrl.replace(placeholderId, encodeURIComponent(id));
    }

    function extractErrorMessage(data, fallback) {
        if (!data) return fallback;
        if (typeof data.message === 'string' && data.message) return data.message;
        if (data.detail) return data.detail;
        if (data.errors && typeof data.errors === 'object') {
            const messages = Object.values(data.errors)
                .flatMap((errors) => errors.map((error) => error.message));
            if (messages.length) return messages.join(' ');
        }
        const fieldMessages = Object.entries(data)
            .filter(([key]) => key !== 'message' && key !== 'detail')
            .flatMap(([, errors]) => Array.isArray(errors) ? errors : [String(errors)]);
        return fieldMessages.join(' ') || fallback;
    }

    function setEducationState(state) {
        loadingState.hidden = state !== 'loading';
        emptyState.hidden = state !== 'empty';
        errorState.hidden = state !== 'error';
        educationGrid.hidden = state !== 'data';
        educationGrid.setAttribute('aria-busy', String(state === 'loading'));
        retryButton.disabled = state === 'loading';
    }

    function buildEducationCardElement(item) {
        if (!item || typeof item.id !== 'string' || !UUID_PATTERN.test(item.id)
            || typeof item.started_at !== 'string') {
            throw new Error('Format Education tidak sesuai');
        }

        const card = cardTemplate.content.firstElementChild.cloneNode(true);
        const setText = (field, value) => {
            card.querySelector(`[data-field="${field}"]`).textContent = value;
        };

        setText('institution', item.institution);
        setText('degree', item.degree);
        setText('description', item.description);
        card.querySelector('[data-field="description"]').hidden = !item.description;
        const endYear = item.is_ongoing ? 'Present' : item.ended_at.slice(0, 4);
        setText('period', `${item.started_at.slice(0, 4)}-${endYear}`);
        setText('status', item.is_ongoing ? 'Ongoing' : 'Completed');
        setText('star-count', item.star_count);

        const editButton = card.querySelector('[data-action="edit"]');
        if (editButton) {
            editButton.setAttribute('aria-label', `Edit ${escapeHtml(item.institution)}`);
            editButton.addEventListener('click', () => openEditModal(item));
        }

        const deleteButton = card.querySelector('[data-action="delete"]');
        if (deleteButton && deleteModal && deleteForm && deleteName) {
            deleteButton.setAttribute('aria-label', `Hapus ${escapeHtml(item.institution)}`);
            deleteButton.addEventListener('click', () => {
                deleteName.textContent = `${item.degree} - ${item.institution}`;
                deleteForm.dataset.educationId = item.id;
            });
        }

        const starButton = card.querySelector('[data-action="star"]');
        if (starButton) {
            setText('star-label', item.is_starred ? 'Unstar' : 'Star');
            starButton.classList.toggle('is-starred', item.is_starred);
            starButton.setAttribute('aria-pressed', String(item.is_starred));
            starButton.addEventListener('click', async () => {
                starButton.disabled = true;
                try {
                    const response = await fetch(starUrl(item.id), {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                            Accept: 'application/json',
                        },
                    });
                    if (response.status === 403) throw new Error('Anda tidak diizinkan memberi star.');
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    const updated = await response.json();
                    setText('star-count', updated.star_count);
                    setText('star-label', updated.is_starred ? 'Unstar' : 'Star');
                    starButton.classList.toggle('is-starred', updated.is_starred);
                    starButton.setAttribute('aria-pressed', String(updated.is_starred));
                } catch (error) {
                    showToast('Gagal memberi star', error.message, 'error');
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
        const url = new URL(section.dataset.apiListUrl, window.location.origin);
        if (query) url.searchParams.set('institution', query);
        setEducationState('loading');
        try {
            const response = await fetch(url, {
                headers: { Accept: 'application/json' },
                signal: controller.signal,
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            if (controller.signal.aborted) return;
            if (!Array.isArray(data)) throw new Error('Format respons tidak sesuai');

            educationGrid.replaceChildren(...data.map(buildEducationCardElement));
            emptyState.textContent = query
                ? 'Tidak ada pendidikan yang cocok dengan pencarian.'
                : 'No education history yet.';
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
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        fetchEducation();
    });

    if (addForm && addModal && formErrors) {
        const submitButton = addForm.querySelector('[type="submit"]');
        addForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            if (submitButton.disabled) return;
            submitButton.disabled = true;
            submitButton.textContent = 'Menyimpan...';
            formErrors.hidden = true;
            formErrors.textContent = '';
            try {
                const response = await fetch(section.dataset.apiListUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                        Accept: 'application/json',
                    },
                    body: JSON.stringify(Object.fromEntries(new FormData(addForm).entries())),
                });
                const data = await response.json().catch(() => null);
                if (response.status === 403) throw new Error(extractErrorMessage(data, 'Anda tidak diizinkan menambahkan pendidikan.'));
                if (response.status === 400) throw new Error(extractErrorMessage(data, 'Data yang dikirim tidak valid.'));
                if (!response.ok) throw new Error(`HTTP ${response.status}`);

                addForm.reset();
                if (addModal.matches(':popover-open')) addModal.hidePopover();
                searchInput.value = '';
                await fetchEducation();
                showToast('Berhasil', 'Data pendidikan berhasil ditambahkan.', 'success');
            } catch (error) {
                const message = error instanceof TypeError
                    ? 'Tidak dapat menyimpan data. Silakan coba lagi.' : error.message;
                formErrors.textContent = message;
                formErrors.hidden = false;
                showToast('Gagal menambahkan pendidikan', message, 'error');
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = 'Tambah Education';
            }
        });
    }

    if (editModal && editForm && editErrors) {
        const editSubmitButton = editForm.querySelector('[type="submit"]');

        function openEditModal(item) {
            editForm.dataset.educationId = item.id;
            editForm.elements.institution.value = item.institution;
            editForm.elements.degree.value = item.degree;
            editForm.elements.description.value = item.description;
            editForm.elements.started_at.value = item.started_at;
            editForm.elements.ended_at.value = item.ended_at || '';
            editErrors.hidden = true;
            editErrors.textContent = '';
            editModal.showPopover();
        }

        editForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            if (editSubmitButton.disabled) return;
            editSubmitButton.disabled = true;
            editSubmitButton.textContent = 'Menyimpan...';
            editErrors.hidden = true;
            editErrors.textContent = '';
            try {
                const response = await fetch(detailUrl(editForm.dataset.educationId), {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                        Accept: 'application/json',
                    },
                    body: JSON.stringify(Object.fromEntries(new FormData(editForm).entries())),
                });
                const data = await response.json().catch(() => null);
                if (response.status === 403) throw new Error(extractErrorMessage(data, 'Anda tidak diizinkan mengubah pendidikan.'));
                if (response.status === 400) throw new Error(extractErrorMessage(data, 'Data yang dikirim tidak valid.'));
                if (!response.ok) throw new Error(`HTTP ${response.status}`);

                if (editModal.matches(':popover-open')) editModal.hidePopover();
                await fetchEducation();
                showToast('Berhasil', 'Data pendidikan berhasil diperbarui.', 'success');
            } catch (error) {
                const message = error instanceof TypeError
                    ? 'Tidak dapat menyimpan data. Silakan coba lagi.' : error.message;
                editErrors.textContent = message;
                editErrors.hidden = false;
                showToast('Gagal memperbarui pendidikan', message, 'error');
            } finally {
                editSubmitButton.disabled = false;
                editSubmitButton.textContent = 'Simpan Perubahan';
            }
        });
    }

    if (deleteModal && deleteForm && deleteName) {
        deleteForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const submitButton = deleteForm.querySelector('[type="submit"]');
            const educationId = deleteForm.dataset.educationId;
            if (!educationId || (submitButton && submitButton.disabled)) return;
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Menghapus...';
            }
            try {
                const response = await fetch(detailUrl(educationId), {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        Accept: 'application/json',
                    },
                });
                if (response.status === 403) {
                    const data = await response.json().catch(() => null);
                    throw new Error(extractErrorMessage(data, 'Anda tidak diizinkan menghapus pendidikan.'));
                }
                if (!response.ok && response.status !== 204) throw new Error(`HTTP ${response.status}`);

                if (deleteModal.matches(':popover-open')) deleteModal.hidePopover();
                await fetchEducation();
                showToast('Berhasil', 'Data pendidikan berhasil dihapus.', 'success');
            } catch (error) {
                showToast('Gagal menghapus pendidikan', error.message, 'error');
            } finally {
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Ya, Hapus';
                }
            }
        });
    }

    retryButton.addEventListener('click', fetchEducation);
    fetchEducation();
})();
