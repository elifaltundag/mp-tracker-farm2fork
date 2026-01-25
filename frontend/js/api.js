/**
 * API İstemci - Fetch API kullanarak backend ile iletişim
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

class APIClient {
    /**
     * Tüm örnekleri listele
     */
    static async getSamples(page = 1, pageSize = 20, filters = {}) {
        const params = new URLSearchParams({
            page: page,
            page_size: pageSize,
            ...filters
        });

        const response = await fetch(`${API_BASE_URL}/samples?${params}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    /**
     * Tekil örnek getir
     */
    static async getSample(id) {
        const response = await fetch(`${API_BASE_URL}/samples/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    /**
     * Yeni örnek oluştur
     */
    static async createSample(sampleData) {
        const response = await fetch(`${API_BASE_URL}/samples`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sampleData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Örnek oluşturulamadı');
        }

        return await response.json();
    }

    /**
     * Örnek güncelle
     */
    static async updateSample(id, sampleData) {
        const response = await fetch(`${API_BASE_URL}/samples/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sampleData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Örnek güncellenemedi');
        }

        return await response.json();
    }

    /**
     * Örnek sil
     */
    static async deleteSample(id) {
        const response = await fetch(`${API_BASE_URL}/samples/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }
}
