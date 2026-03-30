/**
 * Ana uygulama mantığı
 */

class App {
    constructor() {
        this.currentPage = 1;
        this.pageSize = 20;
        this.filters = {};
        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.loadSamples();
    }

    setupEventListeners() {
        // Yeni örnek butonu
        document.getElementById('btnNewSample').addEventListener('click', () => {
            this.showSampleForm();
        });

        // Form kaydet butonu
        document.getElementById('btnSaveSample').addEventListener('click', () => {
            this.saveSample();
        });

        // Form iptal butonu
        document.getElementById('btnCancelForm').addEventListener('click', () => {
            this.hideSampleForm();
        });

        // Filtrele butonu
        document.getElementById('btnFilter').addEventListener('click', () => {
            this.applyFilters();
        });

        // Filtreyi temizle
        document.getElementById('btnClearFilter').addEventListener('click', () => {
            this.clearFilters();
        });
    }

    async loadSamples() {
        try {
            this.showLoading(true);
            const data = await APIClient.getSamples(this.currentPage, this.pageSize, this.filters);
            this.renderSamplesTable(data);
            this.renderPagination(data);
        } catch (error) {
            this.showError(STRINGS.MSG_ERROR_LOADING + ': ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    renderSamplesTable(data) {
        const tbody = document.getElementById('samplesTableBody');

        if (data.data.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center">${STRINGS.MSG_NO_DATA}</td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = data.data.map(sample => `
            <tr>
                <td>${sample.ornek_no}</td>
                <td>${this.formatDate(sample.ornekleme_tarihi)}</td>
                <td>${sample.ornek_turu}</td>
                <td>${sample.konum.yerlesim_yeri}</td>
                <td>${sample.mp_analiz?.sayi?.toplam || '-'}</td>
                <td>
                    <button class="btn-sm btn-edit" onclick="app.editSample('${sample.id}')">
                        ✏️
                    </button>
                    <button class="btn-sm btn-delete" onclick="app.deleteSample('${sample.id}')">
                        🗑️
                    </button>
                </td>
            </tr>
        `).join('');

        // Toplam kayıt sayısını göster
        document.getElementById('totalRecords').textContent =
            STRINGS.TOTAL_RECORDS.replace('{count}', data.total);
    }

    renderPagination(data) {
        const pagination = document.getElementById('pagination');

        pagination.innerHTML = `
            <button
                class="btn-page"
                ${data.page === 1 ? 'disabled' : ''}
                onclick="app.changePage(${data.page - 1})">
                ${STRINGS.PAGE_PREVIOUS}
            </button>
            <span class="page-info">
                ${STRINGS.PAGE_INFO
                    .replace('{current}', data.page)
                    .replace('{total}', data.total_pages)}
            </span>
            <button
                class="btn-page"
                ${data.page === data.total_pages ? 'disabled' : ''}
                onclick="app.changePage(${data.page + 1})">
                ${STRINGS.PAGE_NEXT}
            </button>
        `;
    }

    async changePage(page) {
        this.currentPage = page;
        await this.loadSamples();
    }

    showSampleForm(sampleId = null) {
        document.getElementById('sampleFormModal').style.display = 'flex';

        if (sampleId) {
            // Düzenleme modu - veriyi yükle
            this.loadSampleForEdit(sampleId);
        } else {
            // Yeni kayıt - formu temizle
            document.getElementById('sampleForm').reset();
            document.getElementById('formTitle').textContent = STRINGS.BTN_NEW_SAMPLE;
            document.getElementById('sampleId').value = '';
        }
    }

    hideSampleForm() {
        document.getElementById('sampleFormModal').style.display = 'none';
        document.getElementById('sampleForm').reset();
    }

    async loadSampleForEdit(sampleId) {
        try {
            const sample = await APIClient.getSample(sampleId);
            document.getElementById('formTitle').textContent = STRINGS.BTN_EDIT;
            document.getElementById('sampleId').value = sample.id;

            // Form alanlarını doldur
            document.getElementById('ornek_no').value = sample.ornek_no;
            document.getElementById('ornekleme_tarihi').value = sample.ornekleme_tarihi || '';
            document.getElementById('ornek_turu').value = sample.ornek_turu;
            document.getElementById('yerlesim_yeri').value = sample.konum.yerlesim_yeri;
            document.getElementById('ozel_aciklama').value = sample.konum.ozel_aciklama || '';
            document.getElementById('enlem').value = sample.konum.koordinatlar?.enlem || '';
            document.getElementById('boylam').value = sample.konum.koordinatlar?.boylam || '';
            document.getElementById('jeoloji').value = sample.konum.jeoloji || '';
            document.getElementById('yukseklik_m').value = sample.konum.yukseklik_m || '';
            document.getElementById('egim_yuzde').value = sample.konum.egim_yuzde || '';
            document.getElementById('planlama_ornek_no').value = sample.ornek?.planlama_ornek_no || '';
            document.getElementById('ornek_tur_detay').value = sample.ornek?.planlanan_detay || '';
            document.getElementById('alinan_ornek_turu').value = sample.ornek?.tur || '';
            document.getElementById('ornek_ozelligi').value = sample.ornek?.ozellik || '';
            document.getElementById('sulama_turu').value = sample.tarim?.sulama_turu || '';
            document.getElementById('plastik_malc').checked = sample.tarim?.plastik_malc || false;
        } catch (error) {
            this.showError(STRINGS.MSG_ERROR_LOADING + ': ' + error.message);
        }
    }

    async saveSample() {
        const form = document.getElementById('sampleForm');
        const formData = new FormData(form);
        const sampleId = document.getElementById('sampleId').value;

        // Form verilerini JSON'a çevir
        const sampleData = {
            ornek_no: formData.get('ornek_no'),
            ornekleme_tarihi: formData.get('ornekleme_tarihi') || null,
            ornek_turu: formData.get('ornek_turu'),
            konum: {
                yerlesim_yeri: formData.get('yerlesim_yeri'),
                ozel_aciklama: formData.get('ozel_aciklama') || null,
                koordinatlar: formData.get('enlem') && formData.get('boylam') ? {
                    enlem: parseFloat(formData.get('enlem')),
                    boylam: parseFloat(formData.get('boylam'))
                } : null,
                jeoloji: formData.get('jeoloji') || null,
                yukseklik_m: formData.get('yukseklik_m') ? parseFloat(formData.get('yukseklik_m')) : null,
                egim_yuzde: formData.get('egim_yuzde') ? parseFloat(formData.get('egim_yuzde')) : null
            },
            ornek: {
                planlama_ornek_no: formData.get('planlama_ornek_no') || null,
                planlanan_detay: formData.get('ornek_tur_detay') || null,
                tur: formData.get('alinan_ornek_turu') || null,
                ozellik: formData.get('ornek_ozelligi') || null
            },
            tarim: {
                sulama_turu: formData.get('sulama_turu') || null,
                plastik_malc: formData.get('plastik_malc') === 'on'
            }
        };

        try {
            if (sampleId) {
                // Güncelleme
                await APIClient.updateSample(sampleId, sampleData);
                this.showSuccess(STRINGS.MSG_SAMPLE_UPDATED);
            } else {
                // Yeni kayıt
                await APIClient.createSample(sampleData);
                this.showSuccess(STRINGS.MSG_SAMPLE_CREATED);
            }

            this.hideSampleForm();
            await this.loadSamples();
        } catch (error) {
            this.showError((sampleId ? STRINGS.MSG_ERROR_UPDATING : STRINGS.MSG_ERROR_CREATING) + ': ' + error.message);
        }
    }

    async editSample(sampleId) {
        this.showSampleForm(sampleId);
    }

    async deleteSample(sampleId) {
        if (!confirm(STRINGS.MSG_CONFIRM_DELETE)) {
            return;
        }

        try {
            await APIClient.deleteSample(sampleId);
            this.showSuccess(STRINGS.MSG_SAMPLE_DELETED);
            await this.loadSamples();
        } catch (error) {
            this.showError(STRINGS.MSG_ERROR_DELETING + ': ' + error.message);
        }
    }

    applyFilters() {
        const ornekTuru = document.getElementById('filterOrnekTuru').value;
        const jeoloji = document.getElementById('filterJeoloji').value;

        this.filters = {};
        if (ornekTuru) this.filters.ornek_turu = ornekTuru;
        if (jeoloji) this.filters.jeoloji = jeoloji;

        this.currentPage = 1;
        this.loadSamples();
    }

    clearFilters() {
        document.getElementById('filterOrnekTuru').value = '';
        document.getElementById('filterJeoloji').value = '';
        this.filters = {};
        this.currentPage = 1;
        this.loadSamples();
    }

    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
    }

    showError(message) {
        alert(`❌ ${STRINGS.ERROR}: ${message}`);
    }

    showSuccess(message) {
        alert(`✅ ${message}`);
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('tr-TR');
    }
}

// Uygulama başlat
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new App();
});
