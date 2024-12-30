from flask import request, jsonify
import numpy as np
from . import api_bp

@api_bp.route('/api/wave_superposition')
def get_wave_superposition():
    """计算两个正弦波叠加的结果。
    
    可用于演示波的干涉现象，包括相长干涉和相消干涉。返回两个原始波形和叠加后的波形。

    请求参数:
        amp1 (float): 第一个波的振幅，默认值为1
        freq1 (float): 第一个波的频率，默认值为1
        amp2 (float): 第二个波的振幅，默认值为1
        freq2 (float): 第二个波的频率，默认值为2
        phase (float): 相位差，单位弧度，默认值为0

    返回值:
        JSON对象，包含以下字段：
        - x (list[float]): 位置坐标数组
        - wave1 (list[float]): 第一个波的振幅数组
        - wave2 (list[float]): 第二个波的振幅数组
        - superposition (list[float]): 叠加波的振幅数组
        
    示例:
        GET /api/wave_superposition?amp1=1&freq1=1&amp2=1&freq2=2&phase=0
    """
    amp1 = float(request.args.get('amp1', 1))
    freq1 = float(request.args.get('freq1', 1))
    amp2 = float(request.args.get('amp2', 1))
    freq2 = float(request.args.get('freq2', 2))
    phase = float(request.args.get('phase', 0))
    
    x = np.linspace(0, 10, 500)
    wave1 = amp1 * np.sin(2*np.pi*freq1*x)
    wave2 = amp2 * np.sin(2*np.pi*freq2*x + phase)
    superposition = wave1 + wave2
    
    return jsonify({
        'x': x.tolist(),
        'wave1': wave1.tolist(),
        'wave2': wave2.tolist(),
        'superposition': superposition.tolist()
    }) 