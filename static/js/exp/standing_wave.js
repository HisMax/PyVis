// 驻波实验的状态管理
const state = {
    isPlaying: true,
    currentTime: 0,
    animationId: null
};

// 驻波参数获取
function getParameters() {
    return {
        speed: parseFloat($('#wave-speed').val()),
        wavelength: parseFloat($('#wavelength').val()),
        amplitude: parseFloat($('#amplitude').val())
    };
}

// 创建波形轨迹
function createTraces(data, showComponents) {
    const traces = [];
    
    // 添加行波分量（如果选中显示）
    if (showComponents) {
        traces.push({
            x: data.x,
            y: data.forward_wave,
            name: '前行波',
            mode: 'lines',
            line: { color: '#2196f3', width: 1.5, dash: 'dot' }
        });
        traces.push({
            x: data.x,
            y: data.backward_wave,
            name: '反射波',
            mode: 'lines',
            line: { color: '#ff9800', width: 1.5, dash: 'dot' }
        });
    }

    // 添加驻波
    traces.push({
        x: data.x,
        y: data.y,
        name: '驻波',
        mode: 'lines',
        line: { color: '#1976d2', width: 3 }
    });

    // 添加波节点和波腹点
    traces.push({
        x: data.nodes,
        y: Array(data.nodes.length).fill(0),
        mode: 'markers',
        marker: {
            color: '#f44336',
            size: 10,
            symbol: 'circle'
        },
        name: '波节点',
        showlegend: false
    });

    traces.push({
        x: data.antinodes,
        y: Array(data.antinodes.length).fill(0),
        mode: 'markers',
        marker: {
            color: '#4caf50',
            size: 10,
            symbol: 'circle'
        },
        name: '波腹点',
        showlegend: false
    });

    return traces;
}

// 创建图表布局
function createLayout(showComponents) {
    return {
        ...window.baseLayout,
        title: {
            text: '驻波',
            font: { size: 24 }
        },
        showlegend: showComponents,
        legend: {
            x: 1,
            xanchor: 'right',
            y: 1
        },
        xaxis: {
            ...window.baseLayout.xaxis,
            range: [0, 1],
            title: {
                text: '位置 (x/L)',
                font: {
                    size: 12,
                    family: 'SF Mono, Consolas, monospace'
                }
            }
        },
        yaxis: {
            ...window.baseLayout.yaxis,
            range: [-2.5, 2.5],
            title: {
                text: '振幅 (A)',
                font: {
                    size: 12,
                    family: 'SF Mono, Consolas, monospace'
                }
            }
        }
    };
}

// 更新波形显示
function updatePlot(data) {
    const showComponents = $('#show-components').prop('checked');
    const traces = createTraces(data, showComponents);
    const layout = createLayout(showComponents);

    Plotly.newPlot('standing-wave', traces, layout, {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToAdd: ['drawline', 'eraseshape'],
        modeBarButtonsToRemove: ['lasso2d', 'select2d']
    });

    // 更新波节点数显示
    $('#node-count').text(data.nodes.length - 1);
    $('#antinode-count').text(data.antinodes.length);
}

// 驻波更新主函数
function updateStandingWave(CONFIG) {
    if (!state.isPlaying) return;

    const params = getParameters();
    const k = 2 * Math.PI / params.wavelength;
    const omega = k * params.speed;
    state.currentTime += CONFIG.timeStep * params.speed;

    $.get(`/api/standing_wave?t=${state.currentTime}&k=${k}&omega=${omega}&amplitude=${params.amplitude}`, function(data) {
        updatePlot(data);
        
        state.animationId = setTimeout(() => {
            requestAnimationFrame(() => updateStandingWave(CONFIG));
        }, 1000 / CONFIG.frameRate);
    });

    return state.animationId;
}

// 播放控制
function togglePlay() {
    state.isPlaying = !state.isPlaying;
    $('#play-pause').text(state.isPlaying ? '暂停' : '播放');
    if (state.isPlaying) {
        updateStandingWave(window.CONFIG);
    }
}

// 重置实验
function resetExperiment() {
    state.currentTime = 0;
    $('#wave-speed').val(1);
    if (typeof window.updateValues === 'function') {
        window.updateValues();
    }
    if (state.isPlaying) {
        updateStandingWave(window.CONFIG);
    }
}

// 停止动画
function stopAnimation() {
    if (state.animationId) {
        clearTimeout(state.animationId);
        state.animationId = null;
    }
}

// 初始化驻波实验的事件监听
function initStandingWaveEvents() {
    // 添加行波显示切换事件
    $('#show-components').change(function() {
        $('#wave-components').toggle(this.checked);
    });

    // 播放/暂停按钮事件
    $('#play-pause').click(togglePlay);

    // 重置按钮事件
    $('#reset').click(resetExperiment);
}

// 导出函数和状态
export {
    updateStandingWave,
    initStandingWaveEvents,
    stopAnimation,
    state
}; 