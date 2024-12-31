// 全局状态管理
const experimentState = {
    current: 'lissajous',
    animations: {
        lissajous: null,
        standingWave: null,
        waveSuperposition: null
    },
    playState: {
        lissajous: true,
        standingWave: true,
        waveSuperposition: true
    }
};

// 停止所有动画
function stopAllAnimations() {
    Object.values(experimentState.animations).forEach(id => {
        if (id) {
            cancelAnimationFrame(id);
        }
    });
}

// 切换实验
function switchExperiment(targetExperiment) {
    // 停止当前动画
    stopAllAnimations();
    
    // 隐藏所有实验内容
    $('.experiment-content').addClass('d-none');
    
    // 显示目标实验
    $(`#${targetExperiment}-experiment`).removeClass('d-none');
    
    // 更新当前实验
    experimentState.current = targetExperiment;
    
    // 更新侧边栏选中状态
    $('.list-group-item').removeClass('active');
    $(`.list-group-item[data-experiment="${targetExperiment}"]`).addClass('active');
    
    // 触发实验切换事件
    $(document).trigger('experimentChanged', [targetExperiment]);
    
    // 强制重新计算布局并重绘图表
    setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
        if (targetExperiment === 'standing-wave') {
            initStandingWave();
        } else if (targetExperiment === 'wave-superposition') {
            initWaveSuperposition();
        }
    }, 100);
}

// 事件监听
$(document).ready(function() {
    // 实验切换
    $('.list-group-item').click(function(e) {
        e.preventDefault();
        const targetExperiment = $(this).data('experiment');
        switchExperiment(targetExperiment);
    });
    
    // 窗口大小改变时重绘图表
    let resizeTimeout;
    $(window).resize(function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            const plotDiv = document.getElementById(`${experimentState.current}`);
            if (plotDiv) {
                Plotly.Plots.resize(plotDiv);
            }
        }, 250);
    });
    
    // 初始化当前实验
    switchExperiment(experimentState.current);
}); 