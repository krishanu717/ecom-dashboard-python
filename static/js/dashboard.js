const brutalColors = [
    '#ff6b6b', '#4ecdc4', '#ffe66d', '#1a535c', '#ff9f1c',
    '#ffde59', '#70d6ff', '#ff9770', '#ffd670', '#e9ff70'
];

function getChartOptions() {
    const isDark = document.body.classList.contains('dark-mode');
    const color = isDark ? '#fff' : '#000';
    const gridColor = isDark ? '#444' : '#000';

    return {
        elements: {
            line: { borderWidth: 3, borderColor: color },
            point: { borderWidth: 2, borderColor: color, radius: 4, hoverRadius: 6 },
            bar: { borderWidth: 3, borderColor: color },
            arc: { borderWidth: 3, borderColor: color }
        },
        plugins: {
            legend: { labels: { font: { family: "'Space Grotesk', sans-serif", weight: 'bold' }, color: color } }
        },
        scales: {
            x: { grid: { color: gridColor, tickLength: 8, drawBorder: true }, ticks: { color: color, font: { family: "'Space Grotesk', sans-serif", weight: 'bold' } } },
            y: { grid: { color: gridColor, tickLength: 8, drawBorder: true }, ticks: { color: color, font: { family: "'Space Grotesk', sans-serif", weight: 'bold' } } }
        }
    };
}

function getPieOptions() {
    const isDark = document.body.classList.contains('dark-mode');
    const color = isDark ? '#fff' : '#000';

    return {
        elements: { arc: { borderWidth: 3, borderColor: color } },
        plugins: { legend: { labels: { font: { family: "'Space Grotesk', sans-serif", weight: 'bold' }, color: color } } }
    };
}

let currentRange = "all";
let charts = {};

document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
    }

    initializeDashboard();

    document.getElementById('btnLast30Days').addEventListener('click', () => updateFilter('30d', 'btnLast30Days'));
    document.getElementById('btnLast6Months').addEventListener('click', () => updateFilter('6m', 'btnLast6Months'));
    document.getElementById('btnAllTime').addEventListener('click', () => updateFilter('all', 'btnAllTime'));

    document.getElementById('darkModeToggle').addEventListener('click', toggleDarkMode);
});

function toggleDarkMode() {
    if (document.body.classList.contains("dark-mode")) {
        document.body.classList.remove("dark-mode");
        localStorage.setItem("darkMode", "disabled");
    } else {
        document.body.classList.add("dark-mode");
        localStorage.setItem("darkMode", "enabled");
    }
    initializeDashboard();
}

function updateFilter(range, btnId) {
    currentRange = range;
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active-filter'));
    document.getElementById(btnId).classList.add('active-filter');
    initializeDashboard();
}

function destroyCharts() {
    Object.values(charts).forEach(chart => {
        if (chart) chart.destroy();
    });
}

async function initializeDashboard() {
    destroyCharts();
    await Promise.all([
        loadKPI(),
        loadRevenueGrowth(),
        loadMonthlySalesChart(),
        loadTopProductsChart(),
        loadCategoryChart(),
        loadCitiesChart(),
        loadStatesChart()
    ]);
}

async function loadKPI() {
    try {
        const response = await fetch(`/api/kpi?range=${currentRange}`);
        const data = await response.json();

        const formatter = new Intl.NumberFormat('en-US', {
            style: 'currency', currency: 'USD', maximumFractionDigits: 0
        });

        document.getElementById('revenueCard').innerText = formatter.format(data.total_revenue || 0);
        document.getElementById('ordersCard').innerText = (data.total_orders || 0).toLocaleString();
        document.getElementById('productsCard').innerText = (data.total_products || 0).toLocaleString();
        document.getElementById('citiesCard').innerText = (data.total_cities || 0).toLocaleString();
    } catch (error) {
        console.error("API Error: loadKPI", error);
    }
}

async function loadRevenueGrowth() {
    try {
        const response = await fetch(`/api/revenue-growth?range=${currentRange}`);
        const data = await response.json();
        const growthVal = data.growth_percent || 0;
        const growthEl = document.getElementById('revenueGrowth');

        if (growthVal > 0) {
            growthEl.innerText = `Growth: +${growthVal}%`;
            growthEl.style.color = 'green';
        } else if (growthVal < 0) {
            growthEl.innerText = `Growth: ${growthVal}%`;
            growthEl.style.color = 'red';
        } else {
            growthEl.innerText = `Growth: 0%`;
            growthEl.style.color = 'gray';
        }
    } catch (error) {
        console.error("API Error: loadRevenueGrowth", error);
    }
}

async function loadMonthlySalesChart() {
    try {
        const response = await fetch(`/api/monthly-sales?range=${currentRange}`);
        const data = await response.json();

        const ctx = document.getElementById('monthlySalesChart').getContext('2d');
        const borderColor = document.body.classList.contains('dark-mode') ? '#fff' : '#000';
        charts.monthlySales = new Chart(ctx, {
            type: 'line',
            data: { labels: data.labels, datasets: [{ label: 'Revenue', data: data.data, backgroundColor: '#ff6b6b', borderColor: borderColor, fill: false, tension: 0.3 }] },
            options: getChartOptions()
        });
    } catch (error) { console.error("API Error: loadMonthlySalesChart", error); }
}

async function loadTopProductsChart() {
    try {
        const response = await fetch(`/api/top-products?range=${currentRange}`);
        const data = await response.json();

        const ctx = document.getElementById('topProductsChart').getContext('2d');
        const borderColor = document.body.classList.contains('dark-mode') ? '#fff' : '#000';
        charts.topProducts = new Chart(ctx, {
            type: 'bar',
            data: { labels: data.labels, datasets: [{ label: 'Quantity Sold', data: data.data, backgroundColor: '#4ecdc4', borderColor: borderColor, borderWidth: 3 }] },
            options: getChartOptions()
        });
    } catch (error) { console.error("API Error: loadTopProductsChart", error); }
}

async function loadCategoryChart() {
    try {
        const response = await fetch(`/api/category-sales?range=${currentRange}`);
        const data = await response.json();

        const ctx = document.getElementById('categorySalesChart').getContext('2d');
        const borderColor = document.body.classList.contains('dark-mode') ? '#fff' : '#000';
        charts.categorySales = new Chart(ctx, {
            type: 'pie',
            data: { labels: data.labels, datasets: [{ data: data.data, backgroundColor: brutalColors, borderColor: borderColor, borderWidth: 3 }] },
            options: getPieOptions()
        });
    } catch (error) { console.error("API Error: loadCategoryChart", error); }
}

async function loadCitiesChart() {
    try {
        const response = await fetch(`/api/top-cities?range=${currentRange}`);
        const data = await response.json();

        const ctx = document.getElementById('topCitiesChart').getContext('2d');
        const borderColor = document.body.classList.contains('dark-mode') ? '#fff' : '#000';
        charts.topCities = new Chart(ctx, {
            type: 'bar',
            data: { labels: data.labels, datasets: [{ label: 'Revenue', data: data.data, backgroundColor: '#ff9f1c', borderColor: borderColor, borderWidth: 3 }] },
            options: getChartOptions()
        });
    } catch (error) { console.error("API Error: loadCitiesChart", error); }
}

async function loadStatesChart() {
    try {
        const response = await fetch(`/api/top-states?range=${currentRange}`);
        const data = await response.json();

        const ctx = document.getElementById('topStatesChart').getContext('2d');
        const borderColor = document.body.classList.contains('dark-mode') ? '#fff' : '#000';
        charts.topStates = new Chart(ctx, {
            type: 'bar',
            data: { labels: data.labels, datasets: [{ label: 'Revenue', data: data.data, backgroundColor: '#70d6ff', borderColor: borderColor, borderWidth: 3 }] },
            options: getChartOptions()
        });
    } catch (error) { console.error("API Error: loadStatesChart", error); }
}
