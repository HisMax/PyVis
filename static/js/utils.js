// 通用图表配置
const baseLayout = {
    showlegend: false,
    margin: { l: 50, r: 30, t: 50, b: 50 },
    plot_bgcolor: '#fff',
    paper_bgcolor: '#fff',
    font: {
        family: 'Segoe UI',
        size: 14
    },
    xaxis: {
        showgrid: true,
        gridcolor: '#f0f0f0',
        zeroline: true,
        zerolinecolor: '#e0e0e0'
    },
    yaxis: {
        showgrid: true,
        gridcolor: '#f0f0f0',
        zeroline: true,
        zerolinecolor: '#e0e0e0'
    }
};

// 更新参数显示
function updateValues() {
    const speed = parseFloat($('#wave-speed').val());
    const wavelength = parseFloat($('#wavelength').val());
    const amplitude = parseFloat($('#amplitude').val());
    
    $('#wave-speed-value').text(speed.toFixed(2));
    $('#wavelength-value').text(wavelength.toFixed(2));
    $('#amplitude-value').text(amplitude.toFixed(2));
    
    const k = 2 * Math.PI / wavelength;
    const omega = k * speed;
    const frequency = speed / wavelength;
    const period = 1 / frequency;
    const energy = 0.5 * amplitude * amplitude * omega * omega;
    
    $('#frequency-value').text(frequency.toFixed(2));
    $('#angular-freq-value').text(omega.toFixed(2));
    $('#wave-number-value').text(k.toFixed(2));
    $('#period-value').text(period.toFixed(2));
    $('#energy-value').text(energy.toFixed(2));
}

// 计算最大公约数
function calculateGCD(a, b) {
    a = Math.abs(a);
    b = Math.abs(b);
    while (b) {
        let t = b;
        b = a % b;
        a = t;
    }
    return a;
} 