const API_BASE = "/api/v1";

let allProviders = [];

async function loadProviders(lat, lng, category = "") {
    const radius = document.getElementById('radius-range')?.value || 10;
    const params = new URLSearchParams({ lat, lng, radius });
    if (category) params.append("category", category);

    const res = await fetch(`${API_BASE}/search/nearby?${params}`);
    allProviders = await res.json();
    applyFiltersAndRender();
}

async function loadByQuery(q, category = "") {
    const params = new URLSearchParams();
    if (q) params.append("q", q);
    if (category) params.append("category", category);

    const res = await fetch(`${API_BASE}/search/?${params}`);
    allProviders = await res.json();
    applyFiltersAndRender();
}

function applyFiltersAndRender() {
    const maxPrice = parseFloat(document.getElementById('price-range').value);
    const minRating = parseFloat(document.getElementById('min-rating-range').value);
    const sortBy = document.getElementById('sort-select').value;

    let filtered = allProviders.filter(p => {
        const priceOk = p.price_max == null || p.price_max <= maxPrice;
        const ratingOk = (p.avg_rating || 0) >= minRating;
        return priceOk && ratingOk;
    });

    if (sortBy === 'rating') {
        filtered.sort((a, b) => (b.avg_rating || 0) - (a.avg_rating || 0));
    } else if (sortBy === 'price') {
        filtered.sort((a, b) => (a.price_min || 0) - (b.price_min || 0));
    } else if (sortBy === 'distance') {
        filtered.sort((a, b) => (a.distance_km ?? Infinity) - (b.distance_km ?? Infinity));
    }

    updateExpertCount(filtered.length);
    renderProviders(filtered);
}

function updateExpertCount(count) {
    const label = count === 1 ? '1 experto listo para ayudarte' : `${count} expertos listos para ayudarte`;
    document.getElementById('expert-count').textContent = count > 0 ? label : 'No hay expertos disponibles con estos filtros';
}

function renderProviders(providers) {
    const container = document.getElementById('results-container');
    if (!providers.length) {
        container.innerHTML = `<p class="col-span-full text-on-surface-variant text-center py-12">Aún no hay profesionales registrados en tu zona.</p>`;
        return;
    }
    container.innerHTML = providers.map(p => `
        <div class="bg-surface-container-lowest rounded-xl p-4 border border-outline-variant hover:shadow-[0px_4px_20px_rgba(0,109,119,0.05)] transition-all group">
            <div class="relative mb-4">
                <img alt="${p.name}" class="w-full h-48 object-cover rounded-lg" src="${p.photo_url || 'https://placehold.co/400x300'}"/>
                <div class="absolute top-2 right-2 bg-surface-container-lowest/90 backdrop-blur-sm px-2 py-1 rounded-md flex items-center gap-1 shadow-sm">
                    <span class="material-symbols-outlined text-[#FFB703] text-[18px]" style="font-variation-settings: 'FILL' 1;">star</span>
                    <span class="font-bold text-on-surface text-label-md">${p.avg_rating.toFixed(1)}</span>
                    <span class="text-on-surface-variant text-[10px]">(${p.review_count})</span>
                </div>
            </div>
            <div class="flex justify-between items-start mb-2">
                <div>
                    <div class="flex items-center gap-1">
                        <h3 class="font-headline-sm text-headline-sm text-on-surface">${p.name}</h3>
                        ${p.verified ? '<span class="material-symbols-outlined text-primary text-[18px]">verified</span>' : ''}
                    </div>
                    <span class="inline-block bg-secondary-container text-on-secondary-container px-2 py-0.5 rounded text-label-md font-medium mt-1">${p.category || ''}</span>
                </div>
            </div>
            <div class="flex flex-col gap-1 mb-4 text-on-surface-variant font-body-sm text-body-sm">
                <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-[18px]">location_on</span>
                    <span>${p.distance_km != null ? p.distance_km + ' km de distancia' : (p.service_zone || 'Zona no especificada')}</span>
                </div>
            </div>
            <div class="flex items-center justify-between pt-4 border-t border-outline-variant">
                <div class="flex flex-col">
                    <span class="text-label-sm text-on-surface-variant uppercase tracking-wider">Desde</span>
                    <span class="font-bold text-primary">$${p.price_min ?? '--'} - $${p.price_max ?? '--'} <span class="text-[10px]">MXN/hr</span></span>
                </div>
                <button class="bg-primary text-white px-4 py-2 rounded-lg font-label-lg hover:bg-primary/90 transition-colors" onclick="location.href='/provider.html?id=${p.id}'">Ver perfil</button>
            </div>
        </div>
    `).join('');
}

// --- Filter bar wiring ---

document.getElementById('sort-select').addEventListener('change', applyFiltersAndRender);

document.getElementById('price-range').addEventListener('input', (e) => {
    document.getElementById('price-range-label').textContent = `$${Number(e.target.value).toLocaleString()} MXN`;
    applyFiltersAndRender();
});

document.getElementById('min-rating-range').addEventListener('input', (e) => {
    const v = parseFloat(e.target.value);
    document.getElementById('min-rating-label').textContent = v === 0 ? 'Cualquiera' : `${v.toFixed(1)}+`;
    applyFiltersAndRender();
});

document.getElementById('radius-range').addEventListener('input', (e) => {
    document.getElementById('radius-label').textContent = `${e.target.value} km`;
});
document.getElementById('radius-range').addEventListener('change', () => {
    // radius changes the API query itself, so refetch
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category') || '';
    const lat = window.currentLat, lng = window.currentLng;
    if (lat && lng) loadProviders(lat, lng, category);
});

document.getElementById('more-filters-btn').addEventListener('click', () => {
    document.getElementById('more-filters-panel').classList.toggle('hidden');
});

// "Hoy" / "Esta semana" toggle: UI-only. There is no availability field on
// Provider in the backend yet, so this cannot filter real results until
// that data exists. It just tracks which pill is visually selected.
document.querySelectorAll('.availability-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.availability-btn').forEach(b => {
            b.classList.remove('bg-secondary-container', 'text-on-secondary-container');
            b.classList.add('border', 'border-outline-variant', 'text-on-surface-variant');
        });
        btn.classList.remove('border', 'border-outline-variant', 'text-on-surface-variant');
        btn.classList.add('bg-secondary-container', 'text-on-secondary-container');
    });
});

const CATEGORY_NAMES = {
    plomeria: 'Plomeros',
    electricidad: 'Electricistas',
    jardineria: 'Jardineros',
    limpieza: 'Limpieza',
    pintura: 'Pintores',
    mudanzas: 'Mudanzas',
    mascotas: 'Cuidado de mascotas',
    reparaciones: 'Reparaciones',
    carpinteria: 'Carpinteros',
    cerrajeria: 'Cerrajeros'
};

function updatePageHeader(category) {
    const name = CATEGORY_NAMES[category] || 'Todos los servicios';
    document.getElementById('breadcrumb-category').textContent = name;
    document.getElementById('page-title').textContent =
        category ? `${name} cerca de Mérida, Yucatán` : 'Profesionales cerca de Mérida, Yucatán';
    document.title = `Fix It - ${name} en Mérida`;
}

// --- Initial load ---

const urlParams = new URLSearchParams(window.location.search);
const q = urlParams.get('q');
const category = urlParams.get('category') || '';
const paramLat = urlParams.get('lat');
const paramLng = urlParams.get('lng');

updatePageHeader(category);

if (q) {
    loadByQuery(q, category);
} else if (paramLat && paramLng) {
    window.currentLat = paramLat;
    window.currentLng = paramLng;
    loadProviders(paramLat, paramLng, category);
} else {
    navigator.geolocation.getCurrentPosition(
        pos => {
            window.currentLat = pos.coords.latitude;
            window.currentLng = pos.coords.longitude;
            loadProviders(pos.coords.latitude, pos.coords.longitude, category);
        },
        () => {
            window.currentLat = 20.9674;
            window.currentLng = -89.5926;
            loadProviders(20.9674, -89.5926, category); // fallback: Mérida center
        }
    );
}