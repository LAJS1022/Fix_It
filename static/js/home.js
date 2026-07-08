// Hero search: text query -> search.html?q=...
document.getElementById('hero-search-btn').addEventListener('click', () => {
    const q = document.getElementById('hero-search-input').value.trim();
    window.location.href = q ? `search.html?q=${encodeURIComponent(q)}` : 'search.html';
});

document.getElementById('hero-search-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') document.getElementById('hero-search-btn').click();
});

// "Usar mi ubicación" -> geolocate then go to search.html with lat/lng
document.getElementById('hero-location-btn').addEventListener('click', () => {
    navigator.geolocation.getCurrentPosition(
        pos => {
            window.location.href = `search.html?lat=${pos.coords.latitude}&lng=${pos.coords.longitude}`;
        },
        () => {
            window.location.href = 'search.html';
        }
    );
});

// Category scroll arrows
const categoryPills = document.getElementById('category-pills');
const scrollLeftBtn = document.getElementById('category-scroll-left');
const scrollRightBtn = document.getElementById('category-scroll-right');

if (categoryPills && scrollLeftBtn && scrollRightBtn) {
    const scrollAmount = 300;
    scrollLeftBtn.addEventListener('click', () => {
        categoryPills.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });
    scrollRightBtn.addEventListener('click', () => {
        categoryPills.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
}

// Category pills -> search.html?category=slug
document.querySelectorAll('.category-pill').forEach(btn => {
    btn.addEventListener('click', () => {
        window.location.href = `search.html?category=${encodeURIComponent(btn.dataset.slug)}`;
    });
});

// Populate "Populares cerca de ti" with top-rated nearby providers
function renderPopularCard(p) {
    return `
        <div class="bg-surface-container-lowest rounded-2xl overflow-hidden shadow-[0px_4px_20px_rgba(0,109,119,0.05)] border border-outline-variant/30 hover:-translate-y-1 transition-all duration-300 group cursor-pointer" onclick="location.href='provider.html?id=${p.id}'">
            <div class="relative h-48">
                <img alt="${p.name}" class="w-full h-full object-cover" src="${p.photo_url || 'https://placehold.co/400x300'}"/>
                <div class="absolute top-3 right-3 bg-white/90 backdrop-blur px-2 py-1 rounded-lg flex items-center gap-1 shadow-sm">
                    <span class="material-symbols-outlined text-[#FFB703] text-[18px]" style="font-variation-settings: 'FILL' 1;">star</span>
                    <span class="font-label-md text-label-md font-bold">${p.avg_rating.toFixed(1)}</span>
                </div>
            </div>
            <div class="p-5 flex flex-col h-full">
                <div class="flex items-center gap-1 mb-1">
                    <h3 class="font-headline-sm text-headline-sm text-on-surface">${p.name}</h3>
                    ${p.verified ? `<span class="material-symbols-outlined text-primary text-[18px]" style="font-variation-settings: 'FILL' 1;">verified</span>` : ''}
                </div>
                <p class="text-on-surface-variant font-label-md text-label-md mb-4 uppercase tracking-wider">${p.category || ''}</p>
                <div class="mt-auto space-y-4">
                    <div class="flex justify-between items-center text-on-surface-variant font-body-sm">
                        <span class="flex items-center gap-1">
                            <span class="material-symbols-outlined text-[16px]">distance</span>
                            ${p.distance_km} km
                        </span>
                        <span class="font-bold text-primary">$${p.price_min ?? '--'} - $${p.price_max ?? '--'} MXN/hr</span>
                    </div>
                    <button class="w-full py-3 bg-primary-container text-on-primary-container rounded-xl font-label-lg text-label-lg hover:brightness-90 transition-all active:scale-[0.98] pointer-events-none">
                        Ver perfil
                    </button>
                </div>
            </div>
        </div>
    `;
}

async function loadPopularProviders(lat, lng) {
    try {
        const params = new URLSearchParams({ lat, lng, radius: 50 });
        const res = await fetch(`${API_BASE}/search/nearby?${params}`);
        const providers = await res.json();

        if (!providers.length) {
            document.getElementById('popular-providers').innerHTML = `
                <p class="col-span-full text-on-surface-variant text-center py-8">
                    Aún no hay profesionales registrados en tu zona. ¡Sé el primero en unirte!
                </p>`;
            return;
        }

        const top = providers.sort((a, b) => b.avg_rating - a.avg_rating).slice(0, 4);
        document.getElementById('popular-providers').innerHTML = top.map(renderPopularCard).join('');
    } catch (err) {
        console.error('Could not load popular providers', err);
    }
}

navigator.geolocation.getCurrentPosition(
    pos => loadPopularProviders(pos.coords.latitude, pos.coords.longitude),
    () => loadPopularProviders(20.9674, -89.5926) // fallback: Mérida center
);