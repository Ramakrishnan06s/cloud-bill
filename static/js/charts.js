document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            // Revenue Chart
            const revenueCtx = document.getElementById('revenueChart').getContext('2d');
            new Chart(revenueCtx, {
                type: 'line',
                data: {
                    labels: data.revenue.labels,
                    datasets: [{
                        label: 'Total Revenue (INR)',
                        data: data.revenue.values,
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.2)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { 
                            beginAtZero: true,
                            grid: { color: 'rgba(255, 255, 255, 0.05)' },
                            ticks: { color: '#94a3b8' }
                        },
                        x: { 
                            grid: { display: false },
                            ticks: { color: '#94a3b8' }
                        }
                    }
                }
            });

            // Usage Chart
            const usageCtx = document.getElementById('usageChart').getContext('2d');
            new Chart(usageCtx, {
                type: 'doughnut',
                data: {
                    labels: data.usage.labels,
                    datasets: [{
                        data: data.usage.values,
                        backgroundColor: [
                            '#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ec4899'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    cutout: '70%',
                    plugins: {
                        legend: { 
                            position: 'bottom',
                            labels: { color: '#94a3b8', padding: 20 }
                        }
                    }
                }
            });
        });
});
