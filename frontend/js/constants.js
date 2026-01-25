/**
 * UI String'leri - i18n hazırlığı
 */

const STRINGS = {
    // Genel
    APP_TITLE: "Mikroplastik Takip Sistemi",
    LOADING: "Yükleniyor...",
    ERROR: "Hata",
    SUCCESS: "Başarılı",

    // Butonlar
    BTN_NEW_SAMPLE: "+ Yeni Örnek",
    BTN_SAVE: "Kaydet",
    BTN_CANCEL: "İptal",
    BTN_DELETE: "Sil",
    BTN_EDIT: "Düzenle",
    BTN_FILTER: "Filtrele",
    BTN_CLEAR_FILTER: "Filtreyi Temizle",
    BTN_IMPORT_EXCEL: "📥 Excel İçe Aktar",
    BTN_EXPORT_EXCEL: "📤 Excel'e Aktar",

    // Tablo başlıkları
    TH_SAMPLE_NO: "Örnek No",
    TH_DATE: "Tarih",
    TH_TYPE: "Tür",
    TH_LOCATION: "Konum",
    TH_MP_TOTAL: "MP Toplam",
    TH_ACTIONS: "İşlemler",

    // Form alanları
    LABEL_SAMPLE_NO: "Örnek Numarası",
    LABEL_DATE: "Örnekleme Tarihi",
    LABEL_SAMPLE_TYPE: "Örnek Türü",
    LABEL_LOCATION: "Yerleşim Yeri",
    LABEL_COORDINATES: "Koordinatlar",
    LABEL_LATITUDE: "Enlem",
    LABEL_LONGITUDE: "Boylam",
    LABEL_GEOLOGY: "Jeoloji",
    LABEL_IRRIGATION_TYPE: "Sulama Türü",
    LABEL_PLASTIC_MULCH: "Plastik Malç",

    // Placeholder'lar
    PH_SAMPLE_NO: "Örnek numarasını girin",
    PH_LOCATION: "Örn: Hasköy",
    PH_LATITUDE: "Örn: 38.127516",
    PH_LONGITUDE: "Örn: 27.509202",

    // Mesajlar
    MSG_NO_DATA: "Henüz veri yok",
    MSG_CONFIRM_DELETE: "Bu örneği silmek istediğinizden emin misiniz?",
    MSG_SAMPLE_CREATED: "Örnek başarıyla oluşturuldu",
    MSG_SAMPLE_UPDATED: "Örnek başarıyla güncellendi",
    MSG_SAMPLE_DELETED: "Örnek başarıyla silindi",
    MSG_ERROR_LOADING: "Veriler yüklenirken hata oluştu",
    MSG_ERROR_CREATING: "Örnek oluşturulurken hata oluştu",
    MSG_ERROR_UPDATING: "Örnek güncellenirken hata oluştu",
    MSG_ERROR_DELETING: "Örnek silinirken hata oluştu",

    // Filtreler
    FILTER_ALL: "Tümü",
    FILTER_SAMPLE_TYPE: "Örnek Türü",
    FILTER_GEOLOGY: "Jeoloji",

    // Sayfalama
    PAGE_PREVIOUS: "« Önceki",
    PAGE_NEXT: "Sonraki »",
    PAGE_INFO: "Sayfa {current} / {total}",
    TOTAL_RECORDS: "Toplam {count} kayıt"
};

// Enum değerleri (Backend ile senkronize)
const ENUMS = {
    ORNEK_TURLERI: ["Standart Örnek", "Referans Örnek"],
    SULAMA_TURLERI: ["Salma Sulama", "Damlama Sulama", "Yağmurlama Sulama", "Arık Sulama"],
    SULAMA_KAYNAKLARI: ["Nehir", "Yeraltı Suyu", "Baraj Sulaması"],
    JEOLOJI_TURLERI: [
        "Alüvyon",
        "Alüvyon yelpazesi",
        "Andezit",
        "Kireçtaşı",
        "Konglomera",
        "Mermer",
        "Metamorfik",
        "Ofiyolitik"
    ],
    ALINAN_ORNEK_TURLERI: ["Toprak", "Su", "Gübre", "Bitki"]
};
