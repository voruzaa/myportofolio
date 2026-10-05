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
    const deleteName = document.getElementById('delete-education-name');
    const searchInput = document.getElementById('education-search-input');
    const searchForm = document.getElementById('education-search-form');
    const addForm = document.getElementById('education-form');
    const addModal = document.getElementById('add-education-modal');
    const formErrors = document.getElementById('education-form-errors');
    const placeholderId = '00000000-0000-0000-0000-000000000000';
    let searchTimer;
    let activeRequest;

    function setEducationState(state) {
        loadingState.hidden = state !== 'loading';
        emptyState.hidden = state !== 'empty';
        errorState.hidden = state !== 'error';
        educationGrid.hidden = state !== 'data';
        educationGrid.setAttribute('aria-busy', String(state === 'loading'));
        retryButton.disabled = state === 'loading';
    }

    function buildEducationCardElement(item) {
        if (!item || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(item.pk)
            || !item.fields || typeof item.fields.started_at !== 'string') {
            throw new Error('Format Education tidak sesuai');
        }

        const education = item.fields;
        const card = cardTemplate.content.firstElementChild.cloneNode(true);
        const setText = (field, value) => {
            card.querySelector(`[data-field="${field}"]`).textContent = value;
        };

        // Treat server text as text, so user input cannot become executable HTML.
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
            editLink.href = section.dataset.editUrl.replace(placeholderId, item.pk);
        }

        const deleteButton = card.querySelector('[data-action="delete"]');
        if (deleteButton && deleteForm && deleteName) {
            deleteButton.setAttribute('aria-label', `Hapus ${education.institution}`);
            deleteButton.addEventListener('click', () => {
                deleteName.textContent = `${education.degree} - ${education.institution}`;
                deleteForm.action = section.dataset.deleteUrl.replace(placeholderId, item.pk);
            });
        }

        const starForm = card.querySelector('[data-action="star"]');
        if (starForm) {
            starForm.action = section.dataset.starUrl.replace(placeholderId, item.pk);
            setText('star-label', education.is_starred ? 'Unstar' : 'Star');
            const starButton = starForm.querySelector('button');
            starButton.classList.toggle('is-starred', education.is_starred);
            starButton.setAttribute('aria-pressed', String(education.is_starred));
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
                const response = await fetch(addForm.action, {
                    method: 'POST',
                    headers: { Accept: 'application/json' },
                    body: new FormData(addForm),
                });
                const data = await response.json();
                if (!response.ok) {
                    const messages = Object.values(data.errors || {})
                        .flatMap((errors) => errors.map((error) => error.message));
                    throw new Error(messages.join(' ') || data.message || 'Gagal menambahkan pendidikan.');
                }

                addForm.reset();
                if (addModal.matches(':popover-open')) addModal.hidePopover();
                searchInput.value = '';
                await fetchEducation();
                showToast('Berhasil', data.message, 'success');
            } catch (error) {
                const message = error instanceof SyntaxError || error instanceof TypeError
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

    retryButton.addEventListener('click', fetchEducation);
    fetchEducation();
})();
