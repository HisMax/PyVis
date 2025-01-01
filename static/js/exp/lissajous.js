// 利萨如图形相关的全局变量
let lissajousAnimationId = null;
let currentLissajousTime = 0;

// 更新利萨如图形
function updateLissajous() {
    const freqX = parseFloat($('#freq-x').val());
    const freqY = parseFloat($('#freq-y').val());
    const phase = parseFloat($('#phase').val()) * Math.PI / 180;
    const showAnimation = $('#show-animation').prop('checked');

    // 更新频率比和周期信息
    const gcd = calculateGCD(freqX * 10, freqY * 10) / 10;
    const ratioX = (freqX / gcd).toFixed(1);
    const ratioY = (freqY / gcd).toFixed(1);
    $('#freq-ratio').text(`${ratioY}:${ratioX}`);
    $('#period').text(`${ratioX}π`);

    // 停止现有的动画
    if (lissajousAnimationId) {
        cancelAnimationFrame(lissajousAnimationId);
    }

    // 重置时间
    currentLissajousTime = 0;

    const layout = {
        ...baseLayout,
        title: {
            text: '利萨如图形',
            font: { size: 24 }
        },
        xaxis: {
            ...baseLayout.xaxis,
            range: [-1.5, 1.5],
            title: 'x = A·sin(2πfx·t + φ)'
        },
        yaxis: {
            ...baseLayout.yaxis,
            range: [-1.5, 1.5],
            title: 'y = A·sin(2πfy·t)',
            scaleanchor: 'x',
            scaleratio: 1
        }
    };

    if (showAnimation) {
        // 计算一个完整周期所需的时间
        const periodTime = (freqX / gcd) / freqX * 2 * Math.PI;
        let isDrawing = true;
        let lastPauseTime = 0;

        function animate(timestamp) {
            if (isDrawing) {
                // 生成点
                const points = 500;  // 增加点数使曲线更平滑
                const t = Array.from({length: points}, (_, i) => 
                    (i * currentLissajousTime) / (points - 1)
                );
                const x = t.map(t => Math.sin(2 * Math.PI * freqX * t + phase));
                const y = t.map(t => Math.sin(2 * Math.PI * freqY * t));

                Plotly.newPlot('lissajous', [{
                    x: x,
                    y: y,
                    mode: 'lines',
                    line: {
                        color: '#1976d2',
                        width: 2
                    }
                }], layout, {responsive: true});

                currentLissajousTime += 0.02;
                $('#current-time').text(currentLissajousTime.toFixed(2));

                // 检查是否完成一个周期
                if (currentLissajousTime >= periodTime) {
                    isDrawing = false;
                    lastPauseTime = timestamp;
                }
            } else {
                // 暂停0.6秒后重新开始
                if (timestamp - lastPauseTime >= 600) {
                    currentLissajousTime = 0;
                    isDrawing = true;
                }
            }

            lissajousAnimationId = requestAnimationFrame(animate);
        }

        // 开始动画前先清空图形
        Plotly.newPlot('lissajous', [{
            x: [],
            y: [],
            mode: 'lines',
            line: {
                color: '#1976d2',
                width: 2
            }
        }], layout, {responsive: true});

        animate(performance.now());
    } else {
        // 静态模式 - 绘制完整的利萨如图形
        const points = 1000;  // 使用更多的点以获得更平滑的曲线
        const t = Array.from({length: points}, (_, i) => (2 * Math.PI * i) / (points - 1));
        const x = t.map(t => Math.sin(freqX * t + phase));
        const y = t.map(t => Math.sin(freqY * t));

        Plotly.newPlot('lissajous', [{
            x: x,
            y: y,
            mode: 'lines',
            line: {
                color: '#1976d2',
                width: 2
            }
        }], layout, {responsive: true});
    }
}

// 添加投影图更新函数
function updateProjection(x, y, t) {
    const traces = [
        {
            x: [0, x],
            y: [y, y],
            mode: 'lines',
            line: { color: '#1976d2', width: 1, dash: 'dot' }
        },
        {
            x: [x, x],
            y: [0, y],
            mode: 'lines',
            line: { color: '#1976d2', width: 1, dash: 'dot' }
        },
        {
            x: [x],
            y: [y],
            mode: 'markers',
            marker: {
                color: '#f44336',
                size: 8
            }
        }
    ];

    const layout = {
        ...baseLayout,
        title: {
            text: '投影视图',
            font: { size: 20 }
        },
        xaxis: {
            range: [-1.5, 1.5],
            title: 'x'
        },
        yaxis: {
            range: [-1.5, 1.5],
            title: 'y',
            scaleanchor: 'x',
            scaleratio: 1
        }
    };

    Plotly.newPlot('lissajous-projection', traces, layout, {responsive: true});
}

// 计算最大公约数的辅助函数
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

// 初始化利萨如图形的事件监听
function initLissajousEvents() {
    // 添加动画显示切换事件监听
    $('#show-animation').change(function() {
        if (!this.checked && lissajousAnimationId) {
            cancelAnimationFrame(lissajousAnimationId);
            currentLissajousTime = 0;
        }
        updateLissajous();
    });

    // 参数更新事件
    $('#freq-x, #freq-y, #phase').on('input', function() {
        currentLissajousTime = 0;
        updateLissajous();
    });
}

// 导出函数
export {
    updateLissajous,
    updateProjection,
    initLissajousEvents
}; 